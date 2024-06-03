import re
from flexidata.utils.constants import Patterns
from flexidata.utils.text import (
    no_of_sentence,
    tokenize_sentences,
    tokenize_words,
)
from flexidata.utils.decorators import ensure_nltk_package
from nltk import pos_tag
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from flexidata.Logger import Logger
from urllib.parse import urlparse

logger = Logger()


class TextType:
    """
    Provides classification of text into predefined categories based on specific characteristics.

    This class is designed to classify texts as titles, list items, or other types based on
    patterns and functions that check for specific attributes in the text. It utilizes regular
    expressions to determine if text ends with punctuation or is numeric, supporting text
    analysis and processing tasks.

    Attributes:
        TITLE (str): Represents a text identified as a title.
        LIST_ITEM (str): Represents a text identified as a list item.
        UNKNOWN (str): Default type when text does not match any specific category.

    Methods:
        find_text_type(text): Determines the type of the given text by checking against
                              predefined criteria for list items and titles. Returns 'Unknown'
                              if the text does not meet any specific criteria.
        ends_with_punctuation(text): Checks if the text ends with a punctuation mark.
                                     Returns True if it does, False otherwise.

    Example usage:
        >>> TextType.find_text_type("Chapter 1: Introduction")
        'Title'
        >>> TextType.ends_with_punctuation("Hello, world!")
        True
        >>> TextType.numeric_text("1234")
        True
    """

    EMAILL_TYPE = "Email"
    TITLE = "Title"
    LIST_ITEM = "ListItem"
    NERATIVE_TEXT = "NerativeText"
    UNKNOWN = "Unknown"
    WEB_SITE = "website"
    QUOTE = "quote"
    CAPTION = "caption"
    TABLE_OF_CONTENT = "table_of_content"
    TABLES = "tables"
    CODE_SNIPPET = "code_snippet"

    @staticmethod
    def find_text_type(text):
        """
        Determines the type of the given text by evaluating it against predefined criteria for list items and titles.

        This method classifies text as a list item, title, or unknown based on specific checks performed by
        helper functions (`is_list_item` and `is_title`). It sequentially tests each condition and returns
        the corresponding text type upon the first match.

        Parameters:
        - text (str): The text whose type is to be determined.

        Returns:
        - str: The determined type of the text. It can be 'ListItem' if the text qualifies as a list item,
            'Title' if it qualifies as a title, or 'Unknown' if it does not meet any specific criteria.

        Examples:
        >>> TextType.find_text_type("1. Introduction")
        'ListItem'
        >>> TextType.find_text_type("Introduction to Python")
        'Title'
        >>> TextType.find_text_type("This text does not fit any known category.")
        'Unknown'

        The method uses the following logic:
        - First, it checks if the text is a list item using `is_list_item`. If true, it returns 'ListItem'.
        - If the first check fails, it checks if the text is a title using `is_title`. If true, it returns 'Title'.
        - If all checks fail, it returns 'Unknown'.
        """
        if TextType.is_email(text):
            return TextType.EMAILL_TYPE
        elif TextType.is_list_item(text):
            return TextType.LIST_ITEM
        elif TextType.is_website(text):
            return TextType.WEB_SITE
        elif TextType.is_narrative_text(text):
            return TextType.NERATIVE_TEXT
        elif TextType.is_title(text):
            return TextType.TITLE
        else:
            return TextType.UNKNOWN

    @staticmethod
    def ends_with_punctuation(text: str) -> bool:
        """
        Determines if the provided string ends with a punctuation mark.

        This function evaluates the string against a predefined regular expression that identifies if a string
        ends with any character that is not a word character or whitespace. This includes typical punctuation marks
        like periods, commas, question marks, and exclamations, among others. This is useful for parsing and processing
        text where punctuation may signal the end of a sentence or other syntactic units.

        Args:
            text (str): The text to evaluate.

        Returns:
            bool: True if the text ends with a punctuation character, False otherwise.

        The regular expression specifically checks the end of the string for any non-word, non-space character,
        ensuring that text segmentation or similar processes can accurately identify sentence or phrase boundaries.
        """
        ends_in_punct_pattern = re.compile(Patterns.END_WITH_PUNCTUATION)
        return bool(ends_in_punct_pattern.search(text))

    @staticmethod
    def numeric_text(text: str) -> bool:
        """
        Determines if the provided string contains numeric patterns.

        This function evaluates the string against a predefined regular expression that identifies numeric
        patterns within text. The pattern is designed to match numbers that may include:
        - Optional leading signs (+, -, ~)
        - Comma-separated thousands
        - Optional decimal parts

        This is particularly useful for recognizing formatted numbers in data extraction and processing tasks,
        such as financial data, measurements, or when parsing structured text.

        Args:
            text (str): The text to evaluate for numeric content.

        Returns:
            bool: True if the text matches the numeric pattern, False otherwise.

        The regex captures a wide range of numeric formats to ensure comprehensive detection and is particularly
        useful in processing and validating user input or data fields in text.
        """
        numeric_text_pattern = re.compile(Patterns.NUMERIC_REGEX)
        return bool(numeric_text_pattern.search(text))

    @staticmethod
    def is_title(text, title_max_word_length=12, sentence_min_word_length=5):
        """
        Determines whether the provided text can be classified as a title based on several criteria.

        This function assesses the given text to decide if it fits the characteristics commonly
        associated with titles. It evaluates conditions such as text length, numeric content,
        punctuation, and word count to make this determination.

        Parameters:
        - text (str): The text to evaluate.
        - title_max_word_length (int): Optional. The maximum number of words a title can
        have to still be considered a title. Defaults to 12.

        Returns:
        - bool: True if the text is likely a title, otherwise False.

        Examples:
        >>> is_title("Chapter 1: An Introduction")
        False
        >>> is_title("Introduction to Programming")
        True
        >>> is_title("12345")
        False
        >>> is_title("This is an excessively long sentence that should not be considered a title")
        False

        Logic:
        - Returns False if the text is empty.
        - Returns False if the text is numeric.
        - Returns False if the text is determined to be numeric using the TextType.numeric_text.
        - Returns False if the text ends with a punctuation mark, which is checked using
        TextType.ends_with_punctuation.
        - Returns False if the text ends with a comma.
        - Returns False if the text contains more words than `title_max_word_length`.

        If none of the above conditions are met, the text is likely a title, and True is returned.
        """
        if len(text) == 0:
            return False
        if text.isnumeric() or TextType.numeric_text(text):
            return False
        if TextType.ends_with_punctuation(text):
            return False

        try:
            if detect(text) != "en":
                return False
        except LangDetectException as e:
            return False

        if text.endswith(","):
            return False
        if len(text.split(" ")) > title_max_word_length:
            return False
        if no_of_sentence(text, sentence_min_word_length) > 1:
            return False

        return True

    @staticmethod
    def is_list_item(text: str) -> bool:
        """
        Determines if the provided string matches the pattern of a list item.

        This function evaluates the string against a predefined regular expression that captures common
        patterns seen in list items, such as bullet points or numbering. This is useful for parsing and
        classifying segments of text that are part of lists in structured documents.

        Args:
            text (str): The text to evaluate as a potential list item.

        Returns:
            bool: True if the text matches the list item pattern, False otherwise.

        The regular expression should be designed to recognize various formats of list items, including those
        with bullets, numbers, and other common list markers.
        """
        return bool(Patterns.LIST_ITEM_REGEX.match(text))

    @staticmethod
    @ensure_nltk_package("taggers", "averaged_perceptron_tagger")
    def narrative_features(text: str, check_pronouns: bool = False, check_temporal: bool = False) -> bool:
        """
        Analyzes the given text to determine the presence of narrative features.

        This function performs a linguistic analysis on the text to identify narrative qualities based on verbs,
        and optionally, first-person pronouns and temporal expressions. It processes the text by tokenizing into sentences
        and words, part-of-speech tagging, and then counting relevant word forms and expressions.

        Args:
            text (str): The text to analyze.
            check_pronouns (bool): A flag to indicate whether to count first-person pronouns as a feature of narrative text.
            check_temporal (bool): A flag to indicate whether to count temporal words as a feature of narrative text.

        Returns:
            bool: True if the text meets the conditions set for being considered narrative, otherwise False.

        The analysis includes counting verbs as a base requirement for narrative text and, if specified,
        checks for the presence of first-person pronouns and temporal words to affirm the narrative style.
        """
        sentences = tokenize_sentences(text.lower())
        verb_count = 0
        first_person_pronouns_count = 0
        temporal_words_count = 0
        first_person_pronouns = {"i", "we", "us", "our", "ours", "myself", "ourselves"}
        temporal_words = {
            "then",
            "after",
            "before",
            "finally",
            "previously",
            "formerly",
        }

        for sentence in sentences:
            tokens = tokenize_words(sentence)
            tagged_tokens = pos_tag(tokens)

            for word, tag in tagged_tokens:
                if tag.startswith("VB"):  # Any form of verb
                    verb_count += 1
                if check_pronouns:
                    first_person_pronouns_count += sum(
                        1
                        for word, _ in tagged_tokens
                        if word.lower() in first_person_pronouns
                    )

                if check_temporal:
                    temporal_words_count += sum(
                        1 for word, _ in tagged_tokens if word.lower() in temporal_words
                    )

        is_narrative = verb_count > 0
        if check_pronouns:
            is_narrative = is_narrative and first_person_pronouns_count > 0
        if check_temporal:
            is_narrative = is_narrative and temporal_words_count > 0

        return is_narrative

    @staticmethod
    def is_narrative_text(text: str) -> bool:
        """
        Determines if the provided text can be classified as narrative text.

        This function evaluates several conditions:
        - Checks if the text is empty.
        - Checks if the text is numeric or identified as numeric by a custom function.
        - Uses language detection to ensure the text is in English.
        - Ensures the text has at least two sentences and exhibits features typical of narrative text.

        Args:
            text (str): The text to evaluate.

        Returns:
            bool: True if the text meets the criteria for narrative text, False otherwise.
        """

        # Check if the text is empty
        if len(text) == 0:
            return False

        # Check if the text is purely numeric or classified as numeric
        if text.isnumeric() or TextType.numeric_text(text):
            return False

        # Language detection to confirm the text is in English
        try:
            if detect(text) != "en":
                return False
        except LangDetectException:
            return False

        # Verify the text has narrative features and sufficient sentence count
        if no_of_sentence(text, 3) < 2 and (not TextType.narrative_features(text)):
            return False

        return True

    @staticmethod
    def is_website(text: str) -> bool:
        """
        Determines if the provided string is a well-formed URL indicative of a website.

        This function checks:
        - If the text is empty.
        - If the text can be successfully parsed as a URL with both a scheme (e.g., http, https) and a network location (netloc).

        Args:
            text (str): The text to evaluate as a potential URL.

        Returns:
            bool: True if the text is a valid URL, False otherwise.

        The function uses the `urlparse` method from the `urllib.parse` module and verifies 
        if the resulting object contains both a scheme and a netloc, which are essential 
        components of a valid URL.
        """
        if len(text) == 0:
            return False

        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @staticmethod
    def is_email(text: str) -> bool:
        """
        Determines if the provided string is a valid email address.

        This function performs a simple validation check using a regular expression for email addresses.
        It first checks if the text is non-empty, then applies the regular expression defined in Patterns.EMAIL_REGEX
        to ascertain if the text matches the format of a typical email address.

        Args:
            text (str): The text to evaluate as a potential email address.

        Returns:
            bool: True if the text matches the email pattern, False otherwise or if the text is empty.

        The regular expression should conform to the general structure of email addresses, typically
        allowing characters that are common in local parts of the email, followed by an '@' symbol,
        and then a domain part which includes domain labels separated by dots.
        """
        if len(text) == 0:
            return False
        return bool(re.search(Patterns.EMAIL_REGEX, text))

    @staticmethod
    def get_text_type_by_docx_style(style: str):
        """
        Maps a DOCX style name to a predefined text type.

        This function uses a dictionary to map common Word document style names (like "Heading 1", "List Bullet", etc.)
        to specific text types defined in a TextType enumeration. This mapping helps classify text blocks in a DOCX
        document based on their style, which can be crucial for parsing and processing document content semantically.

        Args:
            style (str): The style name as defined in the DOCX document's style definitions.

        Returns:
            A member of the TextType enum corresponding to the given style, or None if the style is not recognized
            or if no style is provided.

        The function will return None both when an unrecognized style is passed and when the input is None or an empty string,
        ensuring that the caller can handle these cases appropriately. The mapping covers various headings, lists,
        quotes, and special formats like table of contents entries, aiming to accommodate a broad range of document layouts.
        """
        style_textblock_mapping = {
            "Caption": TextType.CAPTION,
            "Heading 1": TextType.TITLE,
            "Heading 2": TextType.TITLE,
            "Heading 3": TextType.TITLE,
            "Heading 4": TextType.TITLE,
            "Heading 5": TextType.TITLE,
            "Heading 6": TextType.TITLE,
            "Heading 7": TextType.TITLE,
            "Heading 8": TextType.TITLE,
            "Heading 9": TextType.TITLE,
            "Intense Quote": TextType.QUOTE,
            "List": TextType.LIST_ITEM,
            "List 2": TextType.LIST_ITEM,
            "List 3": TextType.LIST_ITEM,
            "List Bullet": TextType.LIST_ITEM,
            "List Bullet 2": TextType.LIST_ITEM,
            "List Bullet 3": TextType.LIST_ITEM,
            "List Continue": TextType.LIST_ITEM,
            "List Continue 2": TextType.LIST_ITEM,
            "List Continue 3": TextType.LIST_ITEM,
            "List Number": TextType.LIST_ITEM,
            "List Number 2": TextType.LIST_ITEM,
            "List Number 3": TextType.LIST_ITEM,
            "List Paragraph": TextType.LIST_ITEM,
            "Macro Text": TextType.UNKNOWN,
            "No Spacing": TextType.UNKNOWN,
            "Quote": TextType.QUOTE,
            "Subtitle": TextType.TITLE,
            "TOCHeading": TextType.TITLE,
            "Title": TextType.TITLE,
            "toc 1": TextType.TABLE_OF_CONTENT,
            "toc 2": TextType.TABLE_OF_CONTENT,
        }

        if style:
            return style_textblock_mapping.get(style, None)
        else:
            return None
