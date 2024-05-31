from typing import BinaryIO, cast, Optional, List
from flexidata.utils.constants import FileReaderSource, FileType
from flexidata.reader.handlers import FileHandler
from flexidata.text_processing.text_block import TextBlock
from flexidata.parser.docx import DocxParser
from flexidata.text_processing.convert_file import FileConversion
from flexidata.utils.constants import FileType
from flexidata.utils.decorators import validate_file_type_method
import os


class DocParser(FileHandler):
    """Initialize the DocParser with file handling and parsing options.

    Args:
        file_path (Optional[str]): Local path to the file, if the source is local.
        file_url (Optional[str]): URL of the file, if the source is a web URL.
        source (FileReaderSource): Type of file source.
        extract_table (bool): Flag to determine if tables should be extracted.
        extract_image (bool): Flag to determine if images should be extracted.
        output_folder (Optional[str]): Directory path where output files are saved.
        bucket_name (Optional[str]): S3 bucket name if source is S3.
        file_key (Optional[str]): S3 file key if source is S3.
    """

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

    @validate_file_type_method([FileType.DOC])
    def parse(self, extract_image: bool = False) -> List[TextBlock]:
        """Parse the Doc file to extract text and possibly tables.

        Returns:
            List[TextBlock]: A list of TextBlock objects containing the extracted data.
        """
        if extract_image:
            self.extract_image = extract_image
        temp_directory = self._create_temp_directory()
        FileConversion.convet_doc_to_docx(self.file_path, temp_directory.name)
        _, filename_no_path = os.path.split(os.path.abspath(self.file_path))
        base_filename, _ = os.path.splitext(filename_no_path)
        target_file_path = os.path.join(temp_directory.name, f"{base_filename}.docx")
        parser = DocxParser(
            file_path=target_file_path,
            source=self.source,
            extract_table=self.extract_table,
            extract_image=self.extract_image,
            bucket_name=self.bucket_name,
            file_key=self.file_key,
        )
        elements = parser.parse()
        self._delete_temp_directory(temp_directory)
        return elements
