from flexidata.utils.constants import FileReaderSource
from flexidata.reader.local import LocalFileReader
from flexidata.reader.s3 import S3FileReader
from flexidata.reader.google_drive import GoogleDriveFileReader
from flexidata.reader.web import WebFileReader
from typing import Any, Union

def get_file_reader(source_type: FileReaderSource, **kwargs: Any) -> Union[LocalFileReader, S3FileReader, GoogleDriveFileReader, WebFileReader]:
    """
    Factory function to get the appropriate file reader based on the source type.

    Args:
    source_type (FileReaderSource): The source type of the file reader.
    **kwargs (dict): Keyword arguments to pass to the file reader constructors.

    Returns:
    Union[LocalFileReader, S3FileReader, GoogleDriveFileReader, WebFileReader]: An instance of the appropriate file reader.

    Raises:
    ValueError: If the source type is not supported.
    """
    try:
        if source_type == FileReaderSource.LOCAL:
            return LocalFileReader(**kwargs)
        elif source_type == FileReaderSource.S3:
            return S3FileReader(**kwargs)
        elif source_type == FileReaderSource.GOOGLE_DRIVE:
            return GoogleDriveFileReader(**kwargs)
        elif source_type == FileReaderSource.WEB_URL:
            return WebFileReader(**kwargs)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    except Exception as e:
        raise RuntimeError(f"Failed to create file reader for {source_type}: {e}") from e
