import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader

# Initialize the logger
logger = Logger()

class S3FileReader(FileReader):
    """
    A class that extends FileReader to implement reading files from AWS S3.

    Attributes:
        bucket_name (str): The name of the S3 bucket from which to read the file.
        file_key (str): The key (path) of the file within the S3 bucket.
    """

    def __init__(self, bucket_name: str, file_key: str) -> None:
        """
        Initializes the S3FileReader with the AWS S3 bucket name and file key.

        Args:
            bucket_name (str): The name of the S3 bucket.
            file_key (str): The key of the file in the S3 bucket.
        """
        self.bucket_name = bucket_name
        self.file_key = file_key

    def read_file(self) -> BinaryIO:
        """
        Reads a file from AWS S3 using the specified bucket name and file key, and returns its content as a BinaryIO.

        Returns:
            BinaryIO: A stream containing the content of the file from S3.

        Raises:
            NoCredentialsError: If AWS credentials are not provided.
            PartialCredentialsError: If incomplete AWS credentials are provided.
            ClientError: If an S3 client error occurs.
            Exception: If an unexpected error occurs during the file reading process.
        """
        try:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=self.bucket_name, Key=self.file_key)
            return BytesIO(response['Body'].read())  # Return file content as a byte stream
        except NoCredentialsError:
            logger.error("AWS credentials not available")
            raise NoCredentialsError("AWS credentials not available. Please provide valid credentials.")
        except PartialCredentialsError:
            logger.error("Incomplete AWS credentials")
            raise PartialCredentialsError("Incomplete AWS credentials provided. Please check your credentials.")
        except ClientError as e:
            logger.error(f"Client error in AWS S3 access: {e}")
            raise ClientError(f"Client error occurred with AWS S3: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred while reading from S3: {e}") from e
