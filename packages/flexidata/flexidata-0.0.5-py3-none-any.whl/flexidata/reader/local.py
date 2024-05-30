from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader

# Initialize the logger
logger = Logger()

class LocalFileReader(FileReader):
    """
    A class that extends FileReader to implement reading files from a local filesystem.

    Attributes:
        file_path (str): The path to the file on the local filesystem to be read.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the LocalFileReader with the path to the file on the local filesystem.

        Args:
            file_path (str): The path to the file that will be read.
        """
        self.file_path = file_path

    def read_file(self) -> BinaryIO:
        """
        Reads a file from the local filesystem at the specified file_path and returns its content as a BinaryIO.

        Returns:
            BinaryIO: A stream containing the content of the file.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
            PermissionError: If there is insufficient permission to read the file.
            Exception: If an unexpected error occurs during the file reading process.
        """
        try:
            with open(self.file_path, 'rb') as file:
                return BytesIO(file.read())  # Return file content as a byte stream
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"The file at {self.file_path} was not found.") from None
        except PermissionError:
            logger.error(f"Permission denied for file: {self.file_path}")
            raise PermissionError(f"Access denied for the file at {self.file_path}.") from None
        except Exception as e:
            logger.error(f"An error occurred while reading the file: {e}")
            raise Exception(f"An unexpected error occurred while reading the file: {e}") from e
