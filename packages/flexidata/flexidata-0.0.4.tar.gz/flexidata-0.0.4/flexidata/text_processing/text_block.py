from typing import Dict, List, Any
from flexidata.text_processing.classification import TextType

class TextBlockMetadata:
    """
    A class to hold metadata about a text block extracted from various sources.

    This class stores comprehensive metadata associated with a text block, which can include details such as
    file path, language, file type, page number, bounding box, extraction source, and additional properties
    that are dynamically set.

    Attributes:
        file_path (str): Path to the file from which the text block was extracted.
        languages (List[str]): List of languages identified in the text block.
        filetype (str): Type of the file (e.g., PDF, DOCX).
        page_number (int): Page number in the file where the text block is located.
        bbox (List[float], optional): Bounding box coordinates of the text block on the page.
        extraction_source (str): Source from which the text was extracted.
        **kwargs: Additional attributes that may be dynamically added to the instance.

    Methods:
        __str__: Returns a dictionary-like string representation of the object.
        to_dict: Converts the object's attributes to a dictionary.
    """
    def __init__(self, file_path: str, languages: List[str], filetype: str, page_number: int, extraction_source: str, bbox: List[float]=None, **kwargs):
        self.file_path = file_path
        self.languages = languages
        self.filetype = filetype
        self.page_number = page_number
        self.bbox = bbox
        self.extraction_source = extraction_source
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        """
        Provides a dictionary-like string representation of the metadata.

        Returns:
            str: A string representation of the metadata dictionary.
        """
        metadata_dict = self.to_dict()
        return str(metadata_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the metadata attributes of the instance into a dictionary.

        This method dynamically collects all instance attributes that are not private
        (do not start with '_') and are not callable (methods), facilitating easy conversion
        to formats suitable for serialization or display.

        Returns:
            Dict[str, Any]: A dictionary containing all metadata attributes of the instance.
        """
        # Dynamically gather all attributes of the instance
        return {attr: getattr(self, attr) for attr in dir(self) if not attr.startswith('_') and not callable(getattr(self, attr))}

class TextBlock:
    """
    A class to represent a text block with associated metadata and type classification.

    This class encapsulates a block of text along with its metadata and an optional classification type,
    which might be dynamically determined during initialization if not provided.

    Attributes:
        text (str): The actual text content of the block.
        metadata (TextBlockMetadata): Metadata associated with the text block.
        type (str, optional): The type of the text, which can be manually specified or determined based on the text content.

    Methods:
        __str__: Returns a dictionary-like string representation of the TextBlock.
        from_dict: Class method to create an instance from a dictionary.
        to_dict: Converts the instance into a dictionary, including its metadata.
    """
    def __init__(self, text: str, metadata: TextBlockMetadata, type:str =None):
        """
        Initializes a new instance of TextBlock.

        Args:
            text (str): Text content of the block.
            metadata (TextBlockMetadata): Metadata associated with the text.
            type (str, optional): Optional type of the text. If not provided, it will be determined using TextType.find_text_type.
        """
        self.text = text
        self.metadata = metadata
        if type is None:
            self.type = TextType.find_text_type(text)  # Determine the text type upon initialization
        else:
            self.type = type

    @classmethod
    def from_dict(cls, data: Dict) -> 'TextBlock':
        """
        Creates an instance of TextBlock from a dictionary.

        Args:
            data (Dict): A dictionary containing keys 'Text', 'metadata', and optionally 'Type'.

        Returns:
            TextBlock: An instance of TextBlock initialized with the provided data.
        """
        metadata = TextBlockMetadata(**data['metadata'])
        return cls(text=data["Text"], metadata=metadata)
    
    def to_dict(self) -> Dict:
        """
        Converts the text block and its attributes to a dictionary.

        This includes converting the nested metadata object to a dictionary using its to_dict method.

        Returns:
            Dict: A dictionary representation of the text block, including type, text, and metadata.
        """
        return {
            "Type": self.type,
            "Text": self.text,
            "metadata": self.metadata.to_dict()  # This calls the to_dict method of the metadata object
        }
    
    def __str__(self) -> str:
        """
        Provides a dictionary-like string representation of the TextBlock.

        Returns:
            str: A string representation of the text block as a dictionary.
        """
        text_block_dict = self.to_dict()
        return str(text_block_dict)