import re
import unicodedata
from typing import List, Dict, Any

class TextPreprocessor:
    def __init__(self):
        # Initialization if needed, can be used to set up configurations
        pass

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize Unicode characters in the text using NFC form.
        
        Args:
            text (str): Input text string to be normalized.
        
        Returns:
            str: Text normalized to NFC form.
        """
        return unicodedata.normalize('NFC', text)

    @staticmethod
    def replace_unicode_quotes(text: str) -> str:
        """
        Replace various Unicode quotes and fix common encoding errors with ASCII quotes and correct characters.

        Args:
            text (str): Input text string where quotes and encoding errors will be normalized.

        Returns:
            str: Text with Unicode quotes and encoding errors replaced by correct ASCII quotes and characters.
        """
        corrections = {
            "\x91": "‘", "\x92": "’", "\x93": "“", "\x94": "”", 
            "&apos;": "'", "â\x80\x99": "'", "â\x80“": "—", "â\x80”": "–", 
            "â\x80˜": "‘", "â\x80¦": "…", "â\x80™": "’", "â\x80œ": "“", 
            "â\x80?": "”", "â\x80ť": "”", "â\x80ś": "“", "â\x80¨": "—", 
            "â\x80ł": "″", "â\x80Ž": "", "â\x80‚": "", "â\x80‰": "", 
            "â\x80‹": "", "â\x80": "", "â\x80s'": ""
        }
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        return text


    @staticmethod
    def to_lower_case(text: str) -> str:
        """
        Convert all characters in the text to lower case.
        
        Args:
            text (str): Input text string to be converted to lower case.
        
        Returns:
            str: Lowercased text.
        """
        return text.lower()

    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """
        Remove extra whitespaces from the text, replacing multiple spaces with a single space and trimming leading/trailing spaces.
        
        Args:
            text (str): Input text string from which to remove extra whitespace.
        
        Returns:
            str: Text cleaned of extra whitespace.
        """
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        return text.strip()  # Trim spaces at the beginning and end

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """
        Remove punctuation from the text.
        
        Args:
            text (str): Input text string from which to remove punctuation.
        
        Returns:
            str: Text without punctuation.
        """
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    @staticmethod
    def remove_urls(text: str) -> str:
        return re.sub(r'http[s]?://\S+', '', text)

    @staticmethod
    def remove_emails(text: str) -> str:
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    @staticmethod
    def remove_hashtags_mentions(text: str) -> str:
        text = re.sub(r'@\w+', '', text)  # Remove mentions
        return re.sub(r'#\w+', '', text)  # Remove hashtags
    
    @staticmethod
    def clean_non_ascii_chars(text: str) -> str:
        """
        Removes non-ASCII characters from the text using encoding and decoding.

        Args:
            text (str): Input text string from which to remove non-ASCII characters.

        Returns:
            str: The cleaned text with only ASCII characters.
        """
        # Encode the text to ASCII and ignore errors (i.e., non-ASCII characters)
        encoded_text = text.encode("ascii", "ignore")
        # Decode back to UTF-8 (or ASCII, since only ASCII characters are left)
        return encoded_text.decode()
    

    @staticmethod
    def apply(text: str, func):
        """
        Applies a user-defined function to the text.

        Args:
            text (str): The input text to process.
            func (callable): A function that takes a string and returns a modified string.

        Returns:
            str: The text after applying the user-defined function.

        Raises:
            Exception: If the function does not handle the text properly.
        """
        try:
            # Apply the user-defined function to the text
            return func(text)
        except Exception as e:
            raise Exception(f"An error occurred while applying the function: {str(e)}")



