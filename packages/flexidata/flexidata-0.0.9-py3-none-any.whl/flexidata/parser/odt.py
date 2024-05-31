from flexidata.reader.handlers import FileHandler
from typing import Optional, List
from flexidata.text_processing.text_block import TextBlock
from flexidata.utils.constants import FileReaderSource
from flexidata.parser.docx import DocxParser
from flexidata.text_processing.convert_file import FileConversion
from flexidata.utils.decorators import validate_file_type_method
from flexidata.utils.constants import FileType
import os

class OdtParser(FileHandler):
    
    def __init__(
        self,
        file_path: Optional[str] = None,
        file_url: Optional[str] = None,
        source: FileReaderSource = FileReaderSource.LOCAL,
        extract_table: bool = False,
        extract_image: bool = False,
        bucket_name: Optional[str] = None,
        file_key: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(source, file_path, file_url, bucket_name, file_key)
        self.extract_table = extract_table
        self.extract_image = extract_image
        self.text_extractable = False

    @validate_file_type_method([FileType.ODT])
    def parse(self) -> List[TextBlock]:
        target_dir = self._create_temp_directory()
        file_name = os.path.basename(self.get_file_path_by_source())
        base_name, _ = os.path.splitext(file_name)
        target_docx_path = os.path.join(target_dir, f"{base_name}.docx")
        if self.source == FileReaderSource.LOCAL:
            docx_path = FileConversion.convert_file(
                self.file_path, source_format="odt", target_format="docx", outputfile=target_docx_path
            )
            parser = DocxParser(file_path=self.file_path,
                file_url=target_docx_path,
                source=FileReaderSource.LOCAL,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key)
            self._delete_temp_directory(target_dir)
        else:
            file_content = self.get_file_content()
            temp_file_name = self._create_temp_file_with_content(file_content, 'odt')
            docx_path = FileConversion.convert_file(
                temp_file_name.name, source_format="odt", target_format="docx", outputfile=target_docx_path
            )
            parser = DocxParser(file_path=self.file_path,
                file_url=temp_file_name.name,
                source=FileReaderSource.LOCAL,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key)
            self._delete_temp_file(temp_file_name.name)
        text_blocks = parser.parse()
        return text_blocks
