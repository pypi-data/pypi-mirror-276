from flexidata.reader.handlers import FileHandler
from flexidata.utils.constants import FileReaderSource, HtmlTags, FileType
from flexidata.text_processing.text_block import TextBlockMetadata, TextBlock
from flexidata.text_processing.classification import TextType
from flexidata.preprocessor.base import TextPreprocessor
from lxml.etree import _Element
from typing import Optional, BinaryIO, cast, List, Tuple
from lxml import etree
from tabulate import tabulate
from flexidata.utils.decorators import validate_file_type_method
from flexidata.utils.constants import FileType

class HtmlParser(FileHandler):
    """
    Parser class for extracting text and structural data from HTML documents.

    Attributes:
        file_path (Optional[str]): The local path to the file.
        file_url (Optional[str]): The URL from where the file can be accessed.
        source (FileReaderSource): The source type of the file.
        extract_table (bool): Flag to extract table data.
        extract_image (bool): Flag to extract images.
        output_folder (Optional[str]): Directory to store output.
        bucket_name (Optional[str]): S3 bucket name if using S3 storage.
        file_key (Optional[str]): S3 file key if using S3 storage.
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

    @validate_file_type_method([FileType.HTML])
    def parse(self, extract_image: bool = False) -> List[TextBlock]:
        """
        Parses the HTML document and extracts text blocks based on specified tags and conditions.

        Args:
            extract_image (bool): If True, image extraction is performed in addition to text extraction.

        Returns:
            List[TextBlock]: A list of TextBlock objects containing metadata and extracted text.
        """
        content = cast(BinaryIO, self.get_file_content())
        parser = etree.HTMLParser()
        document_root = etree.parse(content, parser)
        document_root = document_root.xpath("//body")[0]
        self.clean_elements(document_root)
        page_elements = []
        for element_itr in document_root.iter():
            if element_itr.attrib.get("processed") == "true":
                continue
            if element_itr.tag in HtmlTags.HEADINGS_TAGS:
                text, text_type = self.get_cleaned_text(element_itr)
                self.mark_processed_with_xpath(element_itr)
                if text:
                    metadata = TextBlockMetadata(
                        file_path=self.get_file_path_by_source(),
                        languages=["en"],
                        filetype=FileType.HTML,
                        page_number=1,
                        extraction_source="lxml",
                    )
                    text_block = TextBlock(
                        text=text, metadata=metadata, type=TextType.TITLE
                    )
                    page_elements.append(text_block)
            elif element_itr.tag in HtmlTags.LIST_TAGS:
                items = self.process_list_elements(element_itr)
                list_as_text = "\n".join(items)
                list_as_html = self.get_cleaned_html(element_itr)
                self.mark_processed_with_xpath(element_itr)
                if list_as_text:
                    metadata = TextBlockMetadata(
                        text_as_html=list_as_html,
                        file_path=self.get_file_path_by_source(),
                        languages=["en"],
                        filetype=FileType.HTML,
                        page_number=1,
                        extraction_source="lxml",
                    )
                    text_block = TextBlock(
                        text=list_as_text, metadata=metadata, type=TextType.LIST_ITEM
                    )
                    page_elements.append(text_block)
            elif element_itr.tag in HtmlTags.TABLE_TAGS:
                headers, table_data = self.process_table_elements(element_itr)
                table_data_as_text = self.convert_table_to_text(
                    table_data=table_data, headers=headers
                )
                table_data_as_html = self.get_cleaned_html(element_itr, ['rowspan', 'colspan'])
                metadata = TextBlockMetadata(
                    text_as_html=table_data_as_html,
                    file_path=self.get_file_path_by_source(),
                    languages=["en"],
                    filetype=FileType.HTML,
                    page_number=1,
                    extraction_source="lxml",
                )
                text_block = TextBlock(
                    text=table_data_as_text, metadata=metadata, type=TextType.TABLES
                )
                self.mark_processed_with_xpath(element_itr)
                page_elements.append(text_block)
            elif element_itr.tag in HtmlTags.CODE_TAGS:
                text, text_type = self.get_cleaned_text(element_itr)
                self.mark_processed_with_xpath(element_itr)
                if text:
                    metadata = TextBlockMetadata(
                        file_path=self.get_file_path_by_source(),
                        languages=["en"],
                        filetype=FileType.HTML,
                        page_number=1,
                        extraction_source="lxml",
                    )
                    text_block = TextBlock(
                        text=text, metadata=metadata, type=TextType.CODE_SNIPPET
                    )
                    page_elements.append(text_block)
            elif element_itr.tag in HtmlTags.PARAGRAPH_TAGS:
                text, text_type = self.get_cleaned_text(element_itr)
                self.mark_processed_with_xpath(element_itr)
                if text:
                    if text_type is None:
                        text_type = TextType.find_text_type(text)
                    metadata = TextBlockMetadata(
                        file_path=self.get_file_path_by_source(),
                        languages=["en"],
                        filetype=FileType.HTML,
                        page_number=1,
                        extraction_source="lxml",
                    )
                    text_block = TextBlock(text=text, metadata=metadata, type=text_type)
                    page_elements.append(text_block)
        return page_elements

    def clean_elements(self, document_root: _Element) -> None:
        """
        Removes specified tags from the document root to clean up the HTML.

        Args:
            document_root (_Element): The root element of the HTML document.
        """
        etree.strip_elements(document_root, *HtmlTags.TAGS_TO_IGNORE, with_tail=False)

    def process_list_elements(self, list_element: _Element, items: Optional[List[str]] = None) -> List[str]:
        """
        Recursively processes HTML list elements and extracts cleaned text.

        This function traverses all descendants of a given list element and
        collects text, handling nested list structures by recursion. It marks
        each processed element to avoid reprocessing.

        Args:
            list_element (_Element): The root element of the list to process.
            items (Optional[List[str]]): Accumulator for collected list items' texts,
                                         initialized to None and created on first call.

        Returns:
            List[str]: A list of strings extracted and cleaned from the list elements.
        """
        if items is None:
            items = [] # Initialize the list if it's the first call

        for child in list_element.iterdescendants():
            if child.attrib.get("processed") == "true":
                continue # Skip already processed elements
            if child.tag in HtmlTags.LIST_TAGS:
                return self.process_list_elements(child, items) # Recursively process nested lists
            else:
                cleaned_text, text_type = self.get_cleaned_text(child)
                if cleaned_text:
                    items.append(cleaned_text) # Only add non-empty cleaned text
                self.mark_processed_with_xpath(child) # Mark the element as processed
        return items

    def process_table_elements(self, table_element: _Element) -> Tuple[List[str], List[List[str]]]:
        """
        Processes an HTML table element to extract headers and table data.

        This function identifies headers from the <thead> or the first <tr> of the table,
        then extracts rows and columns data from the <tbody> or subsequent <tr> elements.
        It supports tables with complex structures including nested headers.

        Args:
            table_element (_Element): The table element to process, expected to be an lxml Element.

        Returns:
            Tuple[List[str], List[List[str]]]: A tuple containing a list of headers and a list of data rows.
            Each row is represented as a list of strings corresponding to the column values.
        """
        table_data = (
            []
        )  # This will store a list of rows, where each row is a list of cell texts
        headers = []  # List to store headers from the <th> elements

        # First handle headers if present
        header_elements = table_element.xpath(".//thead/tr/th")
        if header_elements:
            for header in header_elements:
                headers.append(" ".join(header.xpath(".//text()")).strip())

        # If no explicit <thead>, try to find <th> elements in the first <tr>
        if not headers:
            first_row_headers = table_element.xpath(".//tr[1]/th")
            if first_row_headers:
                for header in first_row_headers:
                    headers.append(" ".join(header.xpath(".//text()")).strip())
                # Skip the first row in subsequent processing if it was treated as a header
                rows = table_element.xpath(".//tr[position()>1]")
            else:
                rows = table_element.xpath(".//tr")
        else:
            rows = table_element.xpath(".//tbody/tr | .//tr[not(ancestor::thead)]")

        # Process each row for data cells
        for row in rows:
            row_data = []
            cells = row.xpath(".//td")
            for cell in cells:
                text = " ".join(
                    cell.xpath(".//text()")
                )  # Joins all text within the cell
                row_data.append(text.strip())
            table_data.append(row_data)
        return headers, table_data

    def convert_table_to_text(self, table_data, headers, as_html=False):
        fmt = "html" if as_html else "plain"
        headers = [cell for cell in headers]
        data = [[cell for cell in row] for row in table_data[1:]]
        return tabulate(data, headers=headers, tablefmt=fmt)

    def mark_processed_with_xpath(self, element: _Element) -> None:
        """
        Marks an HTML element and all its descendants as processed by setting a custom attribute.

        This function is used to avoid re-processing elements in HTML parsing tasks. It sets a 'processed' attribute to 'true' 
        for the specified element and all its descendants, indicating that these elements have been handled and should not be 
        processed again.

        Args:
            element (_Element): The element to mark as processed, along with all its descendants.
        """

        # Set the 'processed' attribute to 'true' for the table element itself
        element.set("processed", "true")

        # Use XPath to select all descendants of the table element
        descendants = element.xpath(
            ".//*"
        )  # Selects all descendants of any depth
        for descendant in descendants:
            descendant.set("processed", "true")

    def get_cleaned_html(self, element_tree: _Element, attributes_to_keep: Optional[List[str]] = None) -> str:
        """
        Retrieves and cleans the HTML from an element, removing all attributes except those specified to be kept.

        This function iterates over each element within the given element tree, clearing attributes that are not explicitly marked to be retained. This is useful for simplifying HTML content or preparing it for environments where minimal attributes are desired.

        Args:
            element_tree (_Element): The root element from which to extract and clean the HTML.
            attributes_to_keep (Optional[List[str]]): A list of attribute names that should not be removed during cleaning.

        Returns:
            str: The cleaned HTML as a string, with only the specified attributes kept.
        """

        # Iterate over all elements
        for element in element_tree.iter():
            # List all attributes of the element
            for attribute in list(element.attrib):
                # Remove each attribute except specific ones you want to keep
                if attributes_to_keep is None:
                    del element.attrib[attribute]
                elif (
                    attribute not in attributes_to_keep
                ):  # Preserving 'href' for hyperlinks as an example
                    del element.attrib[attribute]

        # Return the cleaned HTML as a string without attributes except those preserved
        cleaned_html = etree.tostring(element_tree, encoding="utf-8").decode("utf-8")
        return TextPreprocessor.remove_extra_whitespace(cleaned_html)

    def get_cleaned_text(self, element: _Element) -> Optional[str]:
        """
        Extracts and cleans the text from an HTML element, removing excess whitespace.

        This function retrieves the combined text of an element and its descendants,
        then applies cleaning operations such as trimming and removing extra spaces.

        Args:
            element (_Element): The element from which text is to be extracted.

        Returns:
            Optional[str]: The cleaned text from the element, or None if the element contains no text.
        """
        text = ""
        text_type = None
        if element is not None and self.check_element_has_code(element):
            text = self.get_code_snippet(element)
            text_type = TextType.CODE_SNIPPET
        elif element is not None and element.text:
            text = ' '.join(element.xpath('.//text()')).strip()  # Concatenate all text nodes and strip whitespace
        return TextPreprocessor.remove_extra_whitespace(text), text_type

    def check_element_has_code(self, element: _Element) -> Optional[str]:
        """
        Check if the element contains code snippet.

        Args:
            element (_Element): The element to check.

        Returns:
            Optional[str]: The code snippet from the element, or None if the element contains no code.
        """
        # Check if the paragraph contains a <pre><code> block
        code_block = element.find('.//pre/code')
        if code_block is None:
            code_block = element.find('.//code')

        if code_block is not None:
            return True
        return False
    
    def get_code_snippet(self, element: _Element) -> Optional[str]:
        """
        Extracts and cleans the code snippet from an HTML element.

        This function retrieves the code snippet from the <pre><code> block.

        Args:
            element (_Element): The element from which code snippet is to be extracted.

        Returns:
            Optional[str]: The code snippet from the element, or None if the element contains no code snippet.
        """
        code_block = element.find('.//pre/code')
        if code_block is None:
            code_block = element.find('.//code')

        if code_block is not None:
            code = ' '.join(code_block.xpath('.//text()')).strip()
            return TextPreprocessor.remove_extra_whitespace(code)
        return None