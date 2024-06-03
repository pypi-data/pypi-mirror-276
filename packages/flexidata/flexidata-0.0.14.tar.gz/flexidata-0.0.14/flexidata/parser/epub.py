from flexidata.reader.handlers import FileHandler
from typing import Optional, List
from flexidata.text_processing.text_block import TextBlock
from flexidata.utils.constants import FileReaderSource
from flexidata.text_processing.convert_file import FileConversion
from flexidata.parser.html import HtmlParser
from flexidata.utils.decorators import validate_file_type_method
from flexidata.utils.constants import FileType


class EpubParser(FileHandler):
    """
    A parser for handling ePub files by converting them to HTML and then extracting textual content.

    Attributes:
        file_path (Optional[str]): Local or network path to the ePub file.
        file_url (Optional[str]): URL of the ePub file if sourced from a remote location.
        source (FileReaderSource): Enum indicating the source of the file (local, URL, etc.).
        extract_table (bool): Whether to extract tables from the converted HTML.
        extract_image (bool): Whether to extract images during the parsing process.
        output_folder (Optional[str]): Directory path where any output should be stored.
        bucket_name (Optional[str]): Name of the S3 bucket if used.
        file_key (Optional[str]): Object key within the S3 bucket if used.
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

    @validate_file_type_method([FileType.EPUB])
    def parse(self) -> List[TextBlock]:
        """
        Converts an ePub file to HTML format and parses it to extract text blocks.

        Returns:
            List[TextBlock]: A list of text blocks extracted from the ePub file after conversion to HTML.
        """
        # Convert ePub file to HTML, handling different source types
        if self.source == FileReaderSource.LOCAL:
            html_text = FileConversion.convert_file(
                self.file_path, source_format="epub", target_format="html"
            )
        else:
            file_content = self.get_file_content()
            temp_file_name = self.create_temp_file(file_content)
            html_text = FileConversion.convert_file(
                temp_file_name, source_format="epub", target_format="html"
            )
            self._delete_temp_file(temp_file_name)

        # Temporarily save the HTML content to a file for parsing
        html_file = self._create_temp_file_with_content(html_text, "html")
        parser = HtmlParser(
            file_path=html_file.name,
            source=FileReaderSource.LOCAL,
            extract_table=self.extract_table,
            extract_image=self.extract_image,
        )
        # Parse the HTML to extract text blocks
        text_blocks = parser.parse()
        self._delete_temp_file(html_file.name)
        return text_blocks
