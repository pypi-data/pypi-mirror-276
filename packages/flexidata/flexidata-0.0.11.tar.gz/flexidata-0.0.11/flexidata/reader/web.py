import requests
from requests.exceptions import HTTPError, RequestException
from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader

# Initialize the logger
logger = Logger()

class WebFileReader(FileReader):
    """
    A class that extends FileReader to implement reading files from a web URL.

    Attributes:
        url (str): The URL from which to read the file.
    """

    def __init__(self, url: str) -> None:
        """
        Initializes the WebFileReader with the URL of the web resource.

        Args:
            url (str): The URL of the file to be read.
        """
        self.url = url

    def read_file(self) -> BinaryIO:
        """
        Reads a file from a specified URL and returns its content as a BinaryIO.

        Returns:
            BinaryIO: A stream containing the content of the file fetched from the URL.

        Raises:
            HTTPError: If an HTTP error occurs during the request.
            RequestException: If an error occurs during the request.
            Exception: If an unexpected error occurs during the file fetching process.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred
            return BytesIO(response.content)  # Return file content as a byte stream
        except HTTPError as e:
            logger.error(f"HTTP error occurred while requesting {self.url}: {e}")
            raise HTTPError(f"HTTP error occurred while accessing {self.url}: {e}") from e
        except RequestException as e:
            logger.error(f"Error occurred while requesting {self.url}: {e}")
            raise RequestException(f"Request error occurred while accessing {self.url}: {e}") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred while accessing {self.url}: {e}")
            raise Exception(f"An unexpected error occurred while accessing {self.url}: {e}") from e
