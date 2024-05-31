from abc import ABC, abstractmethod
from typing import BinaryIO
import io
from flexidata.Logger import Logger
from flexidata.utils.constants import FileReaderSource

# Initializing the logger
logger = Logger()

class FileReader(ABC):
    """
    Abstract base class for file readers. 
    Classes that inherit from this must implement the read_file method 
    which is intended to open and read the content of a file, returning 
    a BinaryIO object containing the file's content.
    
    Attributes:
    source_type (FileReaderSource): The type of the source from which the file will be read.
    """

    def __init__(self, source_type: FileReaderSource):
        """
        Initialize the FileReader with a specific source type.
        
        Args:
        source_type (FileReaderSource): The source type of the file reader.
        """
        self.source_type = source_type

    @abstractmethod
    def read_file(self) -> BinaryIO:
        """
        Abstract method to read a file and return its content as a BinaryIO object.
        
        Returns:
        BinaryIO: A binary I/O stream of the file content.
        
        Raises:
        NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError("Subclasses must implement the read_file method.")

    
