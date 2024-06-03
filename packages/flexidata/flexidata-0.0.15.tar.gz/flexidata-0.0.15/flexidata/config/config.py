import os
from dotenv import load_dotenv

class Config:
    """
    Central configuration management class that loads and retrieves environment variables.
    """

    def __init__(self):
        """
        Initialize and load environment variables from a .env file if present.
        """
        load_dotenv()  # This loads variables from a .env file into the environment

    @staticmethod
    def get(key, default=None):
        """
        Retrieve environment variables or return a default value if not found.

        Args:
            key (str): The environment variable key to look for.
            default (Any, optional): The default value to return if the variable isn't found.

        Returns:
            Any: The value of the environment variable or the default value.
        """
        return os.getenv(key, default)

# Example of setting and getting environment variables
# Set the variables in your .env file or export them to your environment before running the app.
