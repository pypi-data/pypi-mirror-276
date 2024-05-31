import pypandoc
from typing import Any, List
import logging
import subprocess


class FileConversion:
    """
    A class to handle file and text conversions between different formats using pypandoc.
    """

    def __init__(self) -> None:
        """
        Initializes the FileConversion class.
        Currently, the initializer does not perform any actions.
        """
        pass

    @staticmethod
    def convet_doc_to_docx(file_name: str, output_file: str) -> str:
        """
        convert .doc file to .docx using soffice
        """
        command = [
            "soffice",
            "--headless",
            "--convert-to",
            "docx",
            "--outdir",
            output_file,
            file_name,
        ]
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output, error = process.communicate()
        except FileNotFoundError:
            raise FileNotFoundError(
                """soffice command was not found. Please install libreoffice
    on your system and try again.

    - Install instructions: https://www.libreoffice.org/get-help/install-howto/
    - Mac: https://formulae.brew.sh/cask/libreoffice
    - Debian: https://wiki.debian.org/LibreOffice""",
            )

    @staticmethod
    def convert_file(
        file_name: str,
        source_format: str,
        target_format: str,
        outputfile: str = None,
        extra_args: List = None,
    ) -> str:
        """
        Converts a file from one format to another using pypandoc.

        Args:
            file_name (str): The path to the file to convert.
            source_format (str): The current format of the file.
            target_format (str): The desired format to convert the file to.

        Returns:
            str: The converted file content as a string.

        Raises:
            FileNotFoundError: If the file does not exist at the path specified.
            RuntimeError: If there is an issue during the conversion process.
        """
        try:
            if outputfile:
                return pypandoc.convert_file(
                    file_name,
                    target_format,
                    format=source_format,
                    outputfile=outputfile,
                    extra_args=extra_args,
                )
            else:
                return pypandoc.convert_file(
                    file_name,
                    target_format,
                    format=source_format,
                )
        except FileNotFoundError as err:
            msg = (
                "Error converting the file to text. Ensure you have the pandoc "
                "package installed on your system. Install instructions are available at "
                "https://pandoc.org/installing.html. The original exception text was:\n"
                f"{err}"
            )
            raise FileNotFoundError(msg)

    @staticmethod
    def convert_text(
        text: str,
        source_format: str,
        target_format: str,
        outputfile: str = None,
        extra_args: List = None,
    ) -> str:
        """
        Converts a text string from one format to another using pypandoc.

        Args:
            text (str): The text content to convert.
            source_format (str): The current format of the text.
            target_format (str): The desired format to convert the text to.

        Returns:
            str: The converted text as a string.

        Raises:
            ValueError: If the text is empty or null.
            RuntimeError: If there is an issue during the conversion process.
        """
        if not text:
            raise ValueError("Input text cannot be empty.")
        try:
            if outputfile:
                return pypandoc.convert_text(
                    text, target_format, format=source_format, outputfile=outputfile
                )
            else:
                return pypandoc.convert_text(
                    text, target_format, format=source_format, extra_args=extra_args
                )
        except FileNotFoundError as err:
            msg = (
                "Error converting the file to text. Ensure you have the pandoc "
                "package installed on your system. Install instructions are available at "
                "https://pandoc.org/installing.html. The original exception text was:\n"
                f"{err}"
            )
            raise FileNotFoundError(msg)
