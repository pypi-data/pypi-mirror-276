from nltk.tokenize import sent_tokenize, word_tokenize
from flexidata.utils.decorators import ensure_nltk_package
from typing import List

@ensure_nltk_package('tokenizers', 'punkt')
def tokenize_sentences(text: str) -> List[str]:
    """
    Tokenizes the given text into sentences.
    
    Parameters:
    text (str): The text to tokenize into sentences.
    
    Returns:
    list: A list of sentences extracted from the text.
    
    Example:
    >>> sample_text = "Hello world. This is an example sentence. Short here."
    >>> tokenize_sentences(sample_text)
    ['Hello world. ', 'This is an example sentence.', 'Short here.']
    """
    return sent_tokenize(text)

@ensure_nltk_package('tokenizers','punkt')
def tokenize_words(text: str) -> List[str]:
    """
    Tokenizes the input text into words using NLTK's word_tokenize.
    
    Parameters:
    text (str): The text to be tokenized into words.
    
    Returns:
    list: A list of words and punctuation from the text.
    
    Example:
    >>> sample_text = "Hello, world! This is an example."
    >>> tokenize_words(sample_text)
    ['Hello', ',', 'world', '!', 'This', 'is', 'an', 'example', '.']
    """
    return word_tokenize(text)

def no_of_sentence(text: str, min_word_length: int) -> int:
    count = 0
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        words = [word for word in tokenize_words(sentence) if word != "."]
        if len(words) < min_word_length:
            continue
        count = count + 1
    return count

