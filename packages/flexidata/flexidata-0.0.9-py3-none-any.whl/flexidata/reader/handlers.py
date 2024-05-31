from typing import BinaryIO
from flexidata.utils.constants import FileReaderSource, ParserMethod
from flexidata.reader.factory import get_file_reader
import os
from io import BytesIO
import tempfile
from urllib.parse import urlparse, unquote
from flexidata.utils.constants import FileType

class FileHandler:
    """
    Initializes a FileHandler object with details about the file source.

    Args:
        source (str): The source type of the file, e.g., 'local', 'web_url', or 's3'.
        file_path (str, optional): The file path if the source is local. Defaults to None.
        file_url (str, optional): The URL of the file if the source is a web URL. Defaults to None.
        bucket_name (str, optional): The name of the S3 bucket if the source is S3. Defaults to None.
        file_key (str, optional): The key of the file within the S3 bucket if the source is S3. Defaults to None.
    """

    def __init__(self, source, file_path=None, file_url=None, bucket_name=None, file_key=None, file_type=None):
        self.source = source
        self.file_path = file_path
        self.file_url = file_url
        self.bucket_name = bucket_name
        self.file_key = file_key
        if source not in [FileReaderSource.LOCAL, FileReaderSource.WEB_URL, FileReaderSource.S3]:
            raise ValueError(f"Unsupported source type: {source}")

        if source == FileReaderSource.LOCAL and not file_path:
            raise ValueError("File path must be provided for local files.")
        if source == FileReaderSource.WEB_URL and not file_url:
            raise ValueError("File URL must be provided for web URL sources.")
        if source == FileReaderSource.S3 and not (bucket_name and file_key):
            raise ValueError("Bucket name and file key must be provided for S3 sources.")
        if file_type is None:
            self.file_type = self._get_file_extension()
        else:
            self.file_type = file_type

    def get_file_content(self) -> BinaryIO:
        """
        Get the content of the file based on the specified source.

        Returns:
            BinaryIO: The file content as a binary stream.
        """
        # No need to generate new file content if source is local or web URL
        if self.source == FileReaderSource.LOCAL:
            reader = get_file_reader(source_type=self.source, file_path=self.file_path)
        elif self.source == FileReaderSource.WEB_URL:
            reader = get_file_reader(source_type=self.source, url=self.file_url)
        elif self.source == FileReaderSource.S3:
            reader = get_file_reader(
                source_type=self.source,
                bucket_name=self.bucket_name,
                file_key=self.file_key,
            )
        else:
            raise ValueError(f"Unsupported source type: {self.source}")
        return reader.read_file()
    
    def get_file_path_by_source(self):
        """
        Get the file path based on the specified source type.

        Returns:
            str: The file path based on the source type.
        """
        if self.source == FileReaderSource.LOCAL:
            return self.file_path
        elif self.source == FileReaderSource.WEB_URL:
            return self.file_url
        elif self.source == FileReaderSource.S3:
            return self.file_key
        else:
            raise ValueError(f"Unsupported source type: {self.source}")
        
    def create_temp_file(self, file_content: BinaryIO) -> str:
        """
        Creates a temporary file from a BinaryIO stream.

        Args:
            file_content (BinaryIO): The BinaryIO stream containing the file data.

        Returns:
            str: The file path to the temporary file.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file_content.read())  # Write the BinaryIO content to a temp file
            return tmp.name
    

    def _delete_temp_file(self, temp_file_path: str):
        """
        Deletes a temporary file specified by the file path.

        Args:
            temp_file_path (str): The file path of the temporary file to be deleted.
        """
        try:
            os.remove(temp_file_path)  # Attempt to remove the temporary file
            print(f"Temporary file {temp_file_path} has been deleted successfully.")
        except OSError as e:
            print(f"Error: {temp_file_path} : {e.strerror}")  # Handle errors encountered during file deletion

    def _create_temp_file_with_content(self, content: str, file_type: str) -> str:
        """
        Creates a temporary file with the given content and file type.

        Args:
            content (str): The content to write to the temporary file.
            file_type (str): The file type/extension of the file (e.g., 'html', 'txt', 'json').

        Returns:
            str: The path to the temporary file.

        Raises:
            ValueError: If the file type is not supported.
        """
        # Define a mapping of file types to file extensions
        file_extensions = {
            'html': '.html',
            'txt': '.txt',
            'json': '.json',
            'xml': '.xml',
            'odt': '.odt',
        }

        # Check if the file type is supported
        if file_type not in file_extensions:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Get the file extension
        extension = file_extensions[file_type]

        # Create a temporary file with the appropriate extension
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension, mode='w', encoding='utf-8')

        try:
            # Write the content to the temporary file
            temp_file.write(content)
            temp_file.close()  # Ensure all data is written and file is closed
            return temp_file
        except Exception as e:
            # If an error occurs, ensure the file is removed
            os.unlink(temp_file.name)
            raise RuntimeError(f"Failed to create temporary file: {e}") from e
        
    def byte_io_to_String(self, file_content: BytesIO) -> str:
        """
        Converts the contents of a BytesIO object into a string.

        This method resets the read position of the BytesIO object to the beginning,
        reads the bytes, and decodes them into a string using UTF-8 encoding. This is 
        commonly used to convert binary data from files into a readable and processable 
        string format.

        Args:
            file_content (BytesIO): The BytesIO object containing the file's binary content.

        Returns:
            str: The decoded string content of the binary data.
        """
        file_content.seek(0)  # Reset the read position of the BytesIO object to the start
        string_content = file_content.read().decode('utf-8')  # Decode the byte content to a string
        return string_content

    
    def _get_extension_from_local_path(self, local_path: str) -> str:
        """
        Extracts the file extension from a local file path and retrieves its MIME type.

        This method splits the file path to extract the extension, removes any leading periods,
        converts the extension to lowercase, and then uses this extension to look up the
        corresponding MIME type from a predefined list or dictionary of file types.

        Args:
            local_path (str): The path of the file on the local file system from which to extract the extension.

        Returns:
            str: The MIME type corresponding to the extracted file extension.
        """
        extension = (os.path.splitext(local_path)[1].lstrip('.')).lower()  # Extract and process the file extension
        return FileType.get_mime_type(extension)  # Retrieve the MIME type based on the file extension
    
    def _get_extension_from_s3_key(self, s3_key: str) -> str:
        """
        Extracts the file extension from an S3 object key and retrieves its MIME type.

        This method takes the S3 object key, which often represents the file name and path
        in the S3 bucket, splits it to extract the extension part, cleans it by removing any leading periods,
        converts it to lowercase, and then uses this extension to look up the corresponding MIME type
        from a predefined list or dictionary of file types.

        Args:
            s3_key (str): The S3 object key from which to extract the file extension.

        Returns:
            str: The MIME type corresponding to the extracted file extension.
        """
        extension = (os.path.splitext(s3_key)[1].lstrip('.')).lower()  # Extract and process the file extension
        return FileType.get_mime_type(extension)  # Retrieve the MIME type based on the file extension
    

    def _get_extension_from_google_drive(file_id: str) -> str:
        pass


    
    def _get_file_extension(self) -> str:
        """
        Determines the file extension based on the source of the file.

        Depending on the file source specified (e.g., web URL, local storage, S3, or Google Drive),
        this method delegates to the appropriate helper function to extract the file extension.
        
        Returns:
            str: The file extension of the specified file.
        
        Raises:
            ValueError: If the file source is not supported, indicating the need for a valid source specification.
        """
        if self.source == "web_url":
            return self._get_file_extension_from_url(self.file_url)
        elif self.source == "local":
            return self._get_extension_from_local_path(self.file_path)
        elif self.source == "s3":
            return self._get_extension_from_s3_key(self.file_key)
        elif self.source == "google_drive":
            return self._get_extension_from_google_drive(self.file_key)
        else:
            raise ValueError(f"Unsupported source type: {self.source}")


    
    def _get_file_extension_from_url(url: str) -> str:
        """
        Extracts the file extension from a URL, handling URLs that may include query parameters or fragments.

        Args:
            url (str): The URL from which to extract the file extension.

        Returns:
            str: The file extension extracted from the URL, or an empty string if no extension could be identified.
        """
        # Parse the URL to remove any query parameters or fragments
        parsed_url = urlparse(url)
        # Unquote to decode any URL-encoded parts of the path (e.g., %20 for space)
        path = unquote(parsed_url.path)
        extension = os.path.splitext(path)[1][1:]  # Remove the dot and extract the extension
        if extension:
            return FileType.get_mime_type(extension)
        else:
            return FileType.HTML  # Default to HTML if no extension is present
    
    def _create_temp_directory(self) -> str:
        """
        Creates a temporary directory and returns the path to the directory.

        Returns:
            str: The path to the temporary directory.
        """
        return tempfile.TemporaryDirectory()
    
    def _delete_temp_directory(self, temp_dir: tempfile.TemporaryDirectory):
        """
        Deletes a temporary directory and its contents.

        Args:
            temp_dir (str): The path to the temporary directory to delete.
        """
        try:
            temp_dir.cleanup()  # Cleanup the temporary directory
            print(f"Temporary directory {temp_dir} has been deleted successfully.")
        except OSError as e:
            print(f"Error: {temp_dir} : {e.strerror}")
        