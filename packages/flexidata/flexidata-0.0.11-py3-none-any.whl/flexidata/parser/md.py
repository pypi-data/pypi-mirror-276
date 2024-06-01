from flexidata.reader.handlers import FileHandler
from typing import Optional, List
from flexidata.text_processing.text_block import TextBlock
from flexidata.utils.constants import FileReaderSource
from flexidata.parser.html import HtmlParser
from markdown import markdown
from flexidata.utils.decorators import validate_file_type_method
from flexidata.utils.constants import FileType


class MDParser(FileHandler):
    """
    A parser for handling md files by converting them to HTML and then extracting textual content.

    Attributes:
        file_path (Optional[str]): Local or network path to the md file.
        file_url (Optional[str]): URL of the md file if sourced from a remote location.
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

    @validate_file_type_method([FileType.MD])
    def parse(self) -> List[TextBlock]:
        """
        Converts an md file to HTML format and parses it to extract text blocks.

        Returns:
            List[TextBlock]: A list of text blocks extracted from the md file after conversion to HTML.
        """
        # Convert md file to HTML, handling different source types
        file_content = self.get_file_content()
        string_content = self.byte_io_to_String(file_content)
        html_text = markdown(
            string_content,
            extensions=[
                "markdown.extensions.tables",
                "markdown.extensions.def_list",
                "markdown.extensions.fenced_code",
            ],
        )
        print(html_text)
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
