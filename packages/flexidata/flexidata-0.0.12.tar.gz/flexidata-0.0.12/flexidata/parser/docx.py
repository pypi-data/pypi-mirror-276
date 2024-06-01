from typing import BinaryIO, cast, Optional, List, Any
from flexidata.utils.constants import FileReaderSource, FileType
from flexidata.reader.handlers import FileHandler
import docx
from flexidata.text_processing.text_block import TextBlockMetadata, TextBlock
from flexidata.text_processing.classification import TextType
from flexidata.ocr.agent import OCRAgentFactory
from docx import table
from tabulate import tabulate
from flexidata.utils.constants import FileType, Patterns
from flexidata.utils.decorators import validate_file_type_method
import re
from os.path import basename
import numpy as np
from PIL import Image
import io
from docx.text.paragraph import Paragraph
from docx.table import Table


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
        use_explicit_spans (bool) : Flag to determine if the output should be in same table structure.,
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
        use_explicit_spans: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(source, file_path, file_url, bucket_name, file_key)
        self.extract_table = extract_table
        self.extract_image = extract_image
        self.use_explicit_spans = use_explicit_spans
        self.text_extractable = False

    @validate_file_type_method([FileType.DOCX])
    def parse(self, extract_image: bool = False) -> List[TextBlock]:
        """Parse the DOCX file to extract text and possibly tables.

        Returns:
            List[TextBlock]: A list of TextBlock objects containing the extracted data.
        """
        if extract_image:
            self.extract_image = extract_image
        document = docx.Document(cast(BinaryIO, self.get_file_content()))
        page_number = 1
        text_blocks = []
        table_index = 0
        for section in document.sections:
            for item in section.iter_inner_content():
                if isinstance(item, Paragraph):
                    if self.extract_image:
                        image_texts = self._process_image(item, document)
                        text_blocks.extend(image_texts)
                    if len(item.text.strip()):
                        metadata = TextBlockMetadata(
                            file_path=self.get_file_path_by_source(),
                            languages=["eng"],
                            filetype=FileType.DOCX,
                            page_number=page_number,
                            extraction_source="docx",
                        )
                        text_type = TextType.get_text_type_by_docx_style(
                            item.style.name if item.style else None
                        )
                        text_block = TextBlock(item.text, metadata, text_type)
                        text_blocks.append(text_block)
                elif isinstance(item, Table):
                    if self.use_explicit_spans:
                        html_table = self.convert_table_to_text_with_span(
                            item, as_html=True
                        )
                        text_table = self.convert_table_to_text_with_span(
                            item, as_html=False
                        )
                    else:
                        html_table = self.convert_table_to_text(item, as_html=True)
                        text_table = self.convert_table_to_text(item, as_html=False)
                    table_index = table_index + 1
                    metadata = TextBlockMetadata(
                        text_as_html=html_table,
                        file_path=self.get_file_path_by_source(),
                        languages=["eng"],
                        filetype=FileType.DOCX,
                        page_number=page_number,
                        extraction_source="docx",
                    )
                    text_block = TextBlock(text_table, metadata, TextType.TABLES)
                    text_blocks.append(text_block)
                    self._process_inner_table(item, page_number, text_blocks, document)

                if page_number is not None and self._check_page_break(item):
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

    def convert_table_to_text_with_span(
        self, table: table.Table, as_html: bool = True
    ) -> str:
        """
        Convert a table from a Word document into text representation with handling for spanned rows and columns.

        Parameters:
        - table (table.Table): The table object to be converted.
        - as_html (bool, optional): Flag to determine the output format. True for HTML, False for plain text. Default is True.

        Returns:
        - str: The table represented as HTML or plain text, depending on the 'as_html' flag.
        """
        # Extract the underlying XML structure of the table
        table_xml = table._tbl
        rows = table_xml.xpath("./w:tr")
        rows_data = []
        for row in rows:
            cells_data = []
            cells = row.xpath("./w:tc")
            for cell in cells:
                # Check for column span and handle it
                cell_span_count = (
                    int(cell.tcPr.gridSpan.val) if cell.tcPr.gridSpan is not None else 0
                )
                cells_data.extend(
                    cell.xpath(".//text()")
                )  # Extract text content from the cell

                # Handle row span by checking vMerge property
                if cell.tcPr.vMerge is not None and cell.tcPr.vMerge.val != "restart":
                    self.add_empty_value(cells_data, 1)

                # Handle column span by adding empty values as needed
                elif cell_span_count:
                    no_of_empty_value = cell_span_count - 1
                    self.add_empty_value(cells_data, no_of_empty_value)

            rows_data.append(
                cells_data
            )  # Append the processed data of the current row to the rows_data list

        # Decide the output format based on the as_html flag
        if as_html:
            return self.generate_html_table_with_span(
                rows_data
            )  # Convert to HTML using a custom method
        else:
            return tabulate(
                rows_data, tablefmt="plain"
            )  # Convert to plain text using tabulate library

    def add_empty_value(self, cells_data: List[str], count: int) -> None:
        """
        Append empty strings to the cells data to account for spanned columns or rows.

        Parameters:
        - cells_data (List[str]): List containing the data of cells in a row.
        - count (int): Number of empty strings to add.
        """
        cells_data.extend(
            [""] * count
        )  # Append 'count' number of empty strings to the cells data

    def generate_html_table_with_span(self, table_data: List[List[str]]) -> str:
        """
        Generate an HTML table representation with appropriate rowspan and colspan attributes.

        Parameters:
        - rows_data (List[List[str]]): List of lists, where each sublist represents row data.

        Returns:
        - str: HTML string representing the table.
        """

        max_cols = max(len(row) for row in table_data)
        fill_matrix = [[False] * max_cols for _ in table_data]
        html = '<table border="1">\n'
        for row_index, row in enumerate(table_data):
            html += "    <tr>\n"
            col_index = 0
            while col_index < len(row):
                if fill_matrix[row_index][col_index]:
                    # Skip this cell as it's filled by a rowspan or colspan from a previous cell
                    col_index += 1
                    continue

                cell = row[col_index]
                if cell is None:
                    col_index += 1
                    continue

                # Calculate colspan
                colspan = 1
                while (
                    col_index + colspan < len(row) and row[col_index + colspan] is None
                ):
                    colspan += 1

                # Calculate rowspan
                rowspan = 1
                while (
                    row_index + rowspan < len(table_data)
                    and len(table_data[row_index + rowspan]) > col_index
                    and table_data[row_index + rowspan][col_index] is None
                ):
                    rowspan += 1

                # Set fill matrix for spans
                for i in range(rowspan):
                    for j in range(colspan):
                        if i > 0 or j > 0:  # Avoid overwriting the current cell
                            fill_matrix[row_index + i][col_index + j] = True

                # Write the cell to HTML
                html += f"        <td{' colspan=' + str(colspan) if colspan > 1 else ''}{' rowspan=' + str(rowspan) if rowspan > 1 else ''}>{cell}</td>\n"
                col_index += colspan
            html += "    </tr>\n"
        html += "</table>"
        return html

    def _process_inner_table(
        self, table: Any, page_number: int, text_blocks: List[TextBlock], document
    ) -> None:
        """
        Recursively processes each table found within a table cell, converting it into text and HTML,
        and appending the resulting TextBlock to a list.

        This method iterates over each cell of a given table. If a cell contains another table ('inner table'),
        it processes both the HTML and plain text representations of the inner table. It also creates metadata
        and a text block for the inner table, which are then appended to a list of text blocks. This method
        is called recursively for each inner table found.

        Args:
            table (Any): The table object to be processed, which can contain nested tables.
            page_number (int): The page number where the table is located, used in metadata.
            text_blocks (List[TextBlock]): A list to which the new TextBlock instances are appended.

        Example:
            >>> _process_inner_table(table_instance, 5, text_blocks_list)
            None  # The list text_blocks_list will be modified in-place.
        """
        for row in table.rows:
            for cell in row.cells:
                for item in cell.iter_inner_content():
                    if type(item).__name__ == "Table":
                        inner_table = item
                        if self.use_explicit_spans:
                            html_inner_table = self.convert_table_to_text_with_span(
                                inner_table, as_html=True
                            )
                            text_inner_table = self.convert_table_to_text_with_span(
                                inner_table, as_html=False
                            )
                        else:
                            html_inner_table = self.convert_table_to_text(
                                table, as_html=True
                            )
                            text_inner_table = self.convert_table_to_text(
                                inner_table, as_html=False
                            )
                        metadata = TextBlockMetadata(
                            is_inner_table=True,
                            text_as_html=html_inner_table,
                            file_path=self.get_file_path_by_source(),
                            languages=["eng"],
                            filetype=FileType.DOCX,
                            page_number=page_number,
                            extraction_source="docx",
                        )
                        text_block = TextBlock(
                            text_inner_table, metadata, TextType.TABLES
                        )
                        text_blocks.append(text_block)
                        self._process_inner_table(
                            item, page_number, text_blocks, document
                        )
                    else:
                        if self.extract_image:
                            image_texts = self._process_image(item, document)
                            text_blocks.extend(image_texts)

    def _process_image(self, paragraph: Any, document: Any) -> List[TextBlock]:
        """
        Extracts and processes image data embedded in a document paragraph, performing OCR on images.

        This method iterates over each run in the paragraph, searching for runs that contain references to images
        (denoted by empty text and specific content IDs). It retrieves the image data from the document's related parts,
        checks if the content type is an image (excluding specific types like 'image/x-wmf'), and uses OCR to convert
        these images to text. Each piece of extracted text is stored as a TextBlock.

        Args:
            paragraph (Any): The paragraph object containing potential image data.
            document (Any): The document object containing the paragraph and associated media data.

        Returns:
            List[TextBlock]: A list of TextBlock objects created from images found within the paragraph.

        Note:
            This function can potentially raise a KeyError if an image reference cannot be found within the document's parts.
            This function uses a predefined regex pattern, Patterns.DOCX_IMAGE_PATTERN, to locate image references in the XML.
        """
        image_texts = []
        for run in paragraph.runs:
            if run.text == "":
                try:
                    contentID = Patterns.DOCX_IMAGE_PATTERN.search(
                        run.element.xml
                    ).group(0)
                    contentType = document.part.related_parts[contentID].content_type
                except KeyError as e:
                    print(e)
                    continue
                except:
                    continue
                if not contentType.startswith("image"):
                    continue
                imgName = basename(document.part.related_parts[contentID].partname)
                imgData = document.part.related_parts[contentID].blob
                if contentType != "image/x-wmf":
                    image = np.array(Image.open(io.BytesIO(imgData)))
                    ocr_factory = OCRAgentFactory()
                    ocr_agent = ocr_factory.get_ocr_agent()
                    elements = ocr_agent.image_to_text(
                        np.array(image),
                        lang="eng",
                        page_number=1,
                        file_path=self.get_file_path_by_source(),
                        filetype=FileType.DOCX,
                    )
                    image_texts.extend(elements)
        return image_texts
