from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError
from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader

# Initialize the logger
logger = Logger()

class GoogleDriveFileReader(FileReader):
    """
    A class that extends FileReader to implement reading files from Google Drive.

    Attributes:
        file_id (str): The Google Drive file identifier for the file to be read.
    """

    def __init__(self, file_id: str):
        """
        Initializes the GoogleDriveFileReader with the Google Drive file ID.

        Args:
            file_id (str): The unique identifier of the file to read from Google Drive.
        """
        self.file_id = file_id

    def read_file(self) -> BinaryIO:
        """
        Reads a file from Google Drive identified by the file_id and returns its content as a BinaryIO.

        Returns:
            BinaryIO: A stream containing the content of the file.

        Raises:
            ApiRequestError: If there is an issue with the Google Drive API request.
            Exception: If an unexpected error occurs during the file reading process.
        """
        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()  # Authenticate the user
            drive = GoogleDrive(gauth)
            file = drive.CreateFile({'id': self.file_id})  # Create a file object
            file.FetchContent()  # Fetch the content of the file
            return BytesIO(file.content)  # Return file content as a byte stream
        except ApiRequestError as e:
            logger.error(f"API request error from Google Drive: {e}")
            raise RuntimeError(f"Failed to fetch file content due to API request error: {e}") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred while accessing Google Drive: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}") from e

