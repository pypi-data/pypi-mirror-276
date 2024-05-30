from flexidata.reader.handlers import FileHandler
from typing import Optional, List, Dict, Any
from flexidata.utils.constants import FileReaderSource, ParserMethod
from flexidata.parser.pdf import PDFParser
from flexidata.utils.decorators import validate_file_type_method
from flexidata.utils.constants import FileType


class ImageParser(FileHandler):
    """
    Parser for handling image-based document processing, utilizing different parsing methods.

    Attributes:
        file_path (Optional[str]): The local path or URL to the image file.
        file_url (Optional[str]): The URL of the image file.
        source (FileReaderSource): The source type of the file, e.g., local, URL, or cloud storage.
        method (ParserMethod): The parsing method to be used (e.g., MODEL, OCR).
        extract_table (bool): Flag to determine whether to extract tables from the image.
        extract_image (bool): Flag to determine whether to further process or extract images.
        output_folder (Optional[str]): Folder path to store any output.
        bucket_name (Optional[str]): S3 bucket name, if using AWS S3 for storage.
        file_key (Optional[str]): The specific key for the file in the S3 bucket.
        kwargs (dict): Additional keyword arguments for extended configurations.

    Methods:
        parse(extract_image: bool) -> List[List[Dict[str, Any]]]:
            Parses the document based on the specified method and extraction flags.
    """

    def __init__(
        self,
        file_path: Optional[str] = None,
        file_url: Optional[str] = None,
        source: FileReaderSource = FileReaderSource.LOCAL,
        method: ParserMethod = ParserMethod.AUTO,
        extract_table: bool = False,
        extract_image: bool = False,
        bucket_name: Optional[str] = None,
        file_key: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source, file_path, file_url, bucket_name, file_key)
        self.method = method
        self.starting_page_number = 1
        self.extract_table = extract_table
        self.extract_image = extract_image
        self.text_extractable = False

    @validate_file_type_method(FileType.get_image_types())
    def parse(self, extract_image: bool = False) -> List[List[Dict[str, Any]]]:
        """
        Executes the parsing of the document using the selected method, adjusting for image-specific processing.

        Args:
            extract_image (bool): Flag indicating whether images should be extracted during parsing.

        Returns:
            List[List[Dict[str, Any]]]: A nested list containing dictionaries of extracted data blocks,
                                         each with associated metadata.
        """
        elements = []
        parser = PDFParser(
            file_path=self.file_path,
            file_url=self.file_url,
            source=self.source,
            method=self.method,
            extract_image=self.extract_image,
            extract_table=self.extract_table,
            bucket_name=self.bucket_name,
            file_key=self.file_key,
        )
        # Choose parsing method based on the parser method attribute.
        if self.method == ParserMethod.MODEL:
            elements = parser.parse_by_model(is_image=True)
        elif self.method == ParserMethod.OCR:
            elements = parser.parse_by_ocr(is_image=True)

        del parser  # Explicitly delete the parser instance to free up resources.
        return elements
