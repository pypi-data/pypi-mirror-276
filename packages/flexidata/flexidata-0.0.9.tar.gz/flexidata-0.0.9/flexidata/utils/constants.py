import re

UNICODE_BULLETS = [
    "\u0095",
    "\u2022",
    "\u2023",
    "\u2043",
    "\u3164",
    "\u204C",
    "\u204D",
    "\u2219",
    "\u25CB",
    "\u25CF",
    "\u25D8",
    "\u25E6",
    "\u2619",
    "\u2765",
    "\u2767",
    "\u29BE",
    "\u29BF",
    "\u002D",
    "",
    "*",
    "\x95",
    "·",
]


class HtmlTags:
    TAGS_TO_IGNORE = [
        "script",
        "style",
        "noscript",
        "head",
        "header",
        "footer",
        "nav",
        "audio",
        "video",
        "iframe",
        "object",
        "embed",
        "param",
        "source",
        "track",
        "canvas",
        "map",
        "area",
        "svg",
        "math",
        "meta",
        "link",
    ]
    PARAGRAPH_TAGS = ["p", "span", "pre"]
    CODE_TAGS = ["code", "kbd", "samp", "var"]
    TEXT_TAGS = ["b", "strong", "i", "em", "u", "s", "strike", "del", "ins"]
    LIST_ITEM_TAGS = ["li", "dt", "dd"]
    LIST_TAGS = ["ul", "ol", "dl"]
    TABLE_TAGS = ["table"]
    HEADINGS_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
    FOOTNOTES = ["sup"]
    CAPTIONS = ["caption"]
    PAGE_HEADERS = ["header"]
    PAGE_FOOTERS = ["footer"]
    SECTION_TAGS = ["section", "div", "article", "aside"]
    FORMS = ["form"]


class ElementType:
    PARAGRAPH = "Paragraph"
    IMAGE = "Image"
    PARAGRAPH_IN_IMAGE = "ParagraphInImage"
    FIGURE = "Figure"
    PICTURE = "Picture"
    TABLE = "Table"
    PARAGRAPH_IN_TABLE = "ParagraphInTable"
    LIST = "List"
    FORM = "Form"
    PARAGRAPH_IN_FORM = "ParagraphInForm"
    CHECK_BOX_CHECKED = "CheckBoxChecked"
    CHECK_BOX_UNCHECKED = "CheckBoxUnchecked"
    RADIO_BUTTON_CHECKED = "RadioButtonChecked"
    RADIO_BUTTON_UNCHECKED = "RadioButtonUnchecked"
    LIST_ITEM = "List-item"
    FORMULA = "Formula"
    CAPTION = "Caption"
    PAGE_HEADER = "Page-header"
    SECTION_HEADER = "Section-header"
    PAGE_FOOTER = "Page-footer"
    FOOTNOTE = "Footnote"
    TITLE = "Title"
    TEXT = "Text"
    UNCATEGORIZED_TEXT = "UncategorizedText"
    PAGE_BREAK = "PageBreak"
    CODE_SNIPPET = "CodeSnippet"
    PAGE_NUMBER = "PageNumber"
    OTHER = "Other"


class ParserMethod:
    AUTO = "auto"
    FAST = "fast"
    OCR = "ocr"
    MODEL = "model"


class FileType:
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    DOC = "application/msword"
    HTML = "text/html"
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    BMP = "image/bmp"
    TIFF = "image/tiff"
    TXT = "text/plain"
    JSON = "application/json"
    XML = "application/xml"
    EPUB = "application/epub+zip"
    RTF = "application/rtf"
    MD = "text/markdown"
    RST = "text/x-rst"
    ODT = "application/vnd.oasis.opendocument.text"
    ORG = "text/org"

    @staticmethod
    def get_image_types() -> bool:
        """
        Returns a set of supported image types.

        Returns:
            Set[str]: A set of supported image types.
        """
        return [FileType.JPEG, FileType.PNG, FileType.GIF, FileType.BMP, FileType.TIFF]

    @staticmethod
    def is_image(mime_type: str) -> bool:
        """
        Check if the MIME type is one of the supported image types.

        Args:
            mime_type (str): MIME type to check.

        Returns:
            bool: True if it's an image type, False otherwise.
        """
        image_types = {
            FileType.JPEG,
            FileType.PNG,
            FileType.GIF,
            FileType.BMP,
            FileType.TIFF,
        }
        return mime_type in image_types

    @staticmethod
    def get_mime_type(extension: str) -> str:
        """
        Returns the MIME type based on the file extension provided.

        Args:
            extension (str): The file extension (e.g., 'pdf', 'docx', 'html').

        Returns:
            str: The corresponding MIME type if known, or 'application/octet-stream' as default.
        """
        extension_to_mime = {
            "pdf": FileType.PDF,
            "docx": FileType.DOCX,
            "html": FileType.HTML,
            "jpg": FileType.JPEG,
            "jpeg": FileType.JPEG,
            "png": FileType.PNG,
            "txt": FileType.TXT,
            "json": FileType.JSON,
            "xml": FileType.XML,
            "epub": FileType.EPUB,
            "rtf": FileType.RTF,
            "md": FileType.MD,
            "rst": FileType.RST,
            "odt": FileType.ODT,
            "org": FileType.ORG,
            "doc": FileType.DOC,
        }
        return extension_to_mime.get(extension.lower(), "application/octet-stream")


class FileReaderSource:
    WEB_URL = "web_url"
    LOCAL = "local"
    S3 = "s3"
    GOOGLE_DRIVE = "google_drive"


class EXTRACTIONSOURCE:
    PDF_MINER = "pdfminer.six"


class OCREngine:
    TESSERACT = "tesseract"
    PADDLE = "paddle"
    GOOGLE_VISION = "google_vision"


class Patterns:
    WHITESPACE_NEWLINE_PATTERN = r"\s*\n\s*"
    END_WITH_PUNCTUATION = r"[^\w\s]\Z"
    LIST_ITEM_REGEX = re.compile(
        r"^([" + "".join(UNICODE_BULLETS) + r"]|\d+\)|\d+\.\s|\d+\])\s"
    )
    NUMERIC_REGEX = r"^[-+~]?(\d{1,3}(,\d{3})*|\d+)(\.\d+)?$"
    EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    DOCX_IMAGE_PATTERN = re.compile("rId\d+")
