from typing import BinaryIO, cast, Optional, List
from flexidata.utils.constants import FileReaderSource, FileType
from flexidata.reader.handlers import FileHandler
import docx
from flexidata.text_processing.text_block import TextBlockMetadata, TextBlock
from flexidata.text_processing.classification import TextType
from docx import table
from tabulate import tabulate
from flexidata.utils.constants import FileType
from flexidata.utils.decorators import validate_file_type_method

class DocxParser(FileHandler):
    """Initialize the DocxParser with file handling and parsing options.

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

    @validate_file_type_method([FileType.DOCX])
    def parse(self, extract_image: bool = False) -> List[TextBlock]:
        """Parse the DOCX file to extract text and possibly tables.

        Returns:
            List[TextBlock]: A list of TextBlock objects containing the extracted data.
        """
        document = docx.Document(cast(BinaryIO, self.get_file_content()))
        page_number = 1
        text_blocks = []
        table_index = 0
        for element in document.element.body:
            print(element.tag)
            if element.tag.endswith("tbl") and self.extract_table:
                table = document.tables[table_index]
                html_table = self.convert_table_to_text(table, as_html=True)
                text_table = self.convert_table_to_text(table, as_html=False)
                table_index = table_index + 1
                metadata = TextBlockMetadata(
                        file_path=self.get_file_path_by_source(),
                        languages=["eng"],
                        filetype=FileType.DOCX,
                        page_number=page_number,
                        extraction_source="docx",
                    )
                text_block = TextBlock(text_table, metadata, TextType.TABLES)
                text_blocks.append(text_block)
            if element.tag.endswith("p"):
                paragraph = docx.text.paragraph.Paragraph(element, document)
                if len(paragraph.text.strip()):
                    metadata = TextBlockMetadata(
                        file_path=self.get_file_path_by_source(),
                        languages=["eng"],
                        filetype=FileType.DOCX,
                        page_number=page_number,
                        extraction_source="docx",
                    )
                    text_type = TextType.get_text_type_by_docx_style(paragraph.style.name if paragraph.style else None)
                    text_block = TextBlock(paragraph.text, metadata, text_type)
                    text_blocks.append(text_block)

            if page_number is not None and self._check_page_break(element):
                page_number += 1

        return text_blocks

    def _check_page_break(self, element) -> bool:
        """Check if the given element represents a page break in the document.

        Args:
            element: The element to check.

        Returns:
            bool: True if the element is a page break, False otherwise.
        """
        page_break_indicators = [["w:br", 'type="page"'], ["lastRenderedPageBreak"]]
        if hasattr(element, "xml"):
            for indicators in page_break_indicators:
                if all(indicator in element.xml for indicator in indicators):
                    return True
        return False
    
    def convert_table_to_text(self, table: table.Table, as_html: bool = True) -> str:
        """Converts a DOCX table to a formatted string, either as HTML or plain text.

        Args:
            table (table.Table): The DOCX table to convert.
            as_html (bool): Flag to determine if the output should be in HTML format.

        Returns:
            str: The table converted to the specified format (HTML or plain text).
        """
        fmt = "html" if as_html else "plain"
        rows = list(table.rows)
        headers = [cell.text for cell in rows[0].cells]
        data = [[cell.text for cell in row.cells] for row in rows[1:]]
        return tabulate(data, headers=headers, tablefmt=fmt)
