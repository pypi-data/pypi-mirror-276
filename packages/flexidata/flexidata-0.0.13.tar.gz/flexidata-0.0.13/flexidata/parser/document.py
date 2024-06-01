from typing import Type, Optional
import os
from flexidata.utils.constants import FileReaderSource, ParserMethod, FileType
from flexidata.parser.pdf import PDFParser
from flexidata.parser.docx import DocxParser
from flexidata.parser.doc import DocParser
from flexidata.parser.html import HtmlParser
from flexidata.parser.image import ImageParser
from flexidata.parser.epub import EpubParser
from flexidata.parser.md import MDParser
from flexidata.parser.rtf import RtfParser
from flexidata.parser.rst import RstParser
from flexidata.reader.handlers import FileHandler
from flexidata.parser.odt import OdtParser
from flexidata.parser.org import OrgParser

class DocumentParser(FileHandler):
    """
    A factory class that determines and utilizes specific parsers based on the file type.
    """

    def __init__(
        self,
        file_path: Optional[str] = None,
        file_url: Optional[str] = None,
        file_type: Optional[str] = None,
        source: FileReaderSource = FileReaderSource.LOCAL,
        method: ParserMethod = ParserMethod.AUTO,
        extract_table: bool = False,
        extract_image: bool = False,
        bucket_name: Optional[str] = None,
        file_key: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source, file_path, file_url, bucket_name, file_key, file_type=file_type)
        self.method = method
        self.extract_table = extract_table
        self.extract_image = extract_image
        
    
    def get_parser(self) -> Type:
        """
        Determines the appropriate parser based on the file type and returns an instance of that parser.

        Returns:
            An instance of the appropriate parser class for the file type.
        """
        if self.file_type in FileType.PDF:
            return PDFParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                method=self.method,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif self.file_type in FileType.DOCX:
            return DocxParser(file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key)
        elif self.file_type in FileType.DOC:
            return DocParser(file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key)
        elif self.file_type in FileType.HTML:
            return HtmlParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif FileType.is_image(self.file_type):
            return ImageParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                method=self.method,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif self.file_type in FileType.EPUB:
            return EpubParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif self.file_type in FileType.MD:
            return MDParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif self.file_type in FileType.RTF:
            return RtfParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif self.file_type in FileType.RST:
            return RstParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif self.file_type in FileType.ODT:
            return OdtParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        elif self.file_type in FileType.ORG:
            return OrgParser(
                file_path=self.file_path,
                file_url=self.file_url,
                source=self.source,
                extract_table=self.extract_table,
                extract_image=self.extract_image,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def parse(self):
        """
        Parses the document using the appropriate parser based on the file type.

        Returns:
            The output from the specific parser's parse method.
        """
        parser = self.get_parser()
        return parser.parse()
    
    
