from functools import wraps
import nltk
from typing import Callable, Any, List

def validate_file_type_method(supported_extensions: List[str]) -> Callable:
    """
    Decorator to validate the file type of a class method based on the class's 'file_type' attribute.

    This decorator checks if the file type specified in the class attribute 'file_type' is among the
    supported extensions provided. It ensures that the method can only be executed if the file type
    is supported, thereby enforcing file type constraints at runtime.

    Args:
        supported_extensions (List[str]): A list of supported file extensions (e.g., ['.pdf', '.docx']).

    Returns:
        Callable: A decorator that, when applied to a class method, checks the file type before execution.

    Raises:
        ValueError: If the 'file_type' is not in the list of supported extensions.
        AttributeError: If the class does not have a 'file_type' attribute.

    Usage:
        To use this decorator, apply it to class methods that depend on specific file types:
        @validate_file_type_method(['.pdf', '.txt'])
        def process_document(self):
            ...
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # Check for 'file_type' attribute in the instance
            if hasattr(self, 'file_type'):
                # Validate the file type
                if self.file_type.lower() not in supported_extensions:
                    raise ValueError(f"Unsupported file type: {self.file_type}. Supported types are: {supported_extensions}")
            else:
                # Raise an error if 'file_type' attribute is missing
                raise AttributeError("The class must have a 'file_type' attribute.")
            # Execute the method if validation passes
            return method(self, *args, **kwargs)
        return wrapper
    return decorator

def is_debug_enabled(method):
        """
        Decorator to check if debugging is enabled before executing a method.
        This is useful for controlling the execution of debugging-specific methods.
        
        Args:
            method (callable): The method to be wrapped by the decorator.
        
        Returns:
            callable: A wrapper function that checks the debug state before method execution.
        """
        def wrapper(self, *args, **kwargs):
            if not self.debug:
                return False  # If debugging is not enabled, do nothing
            return method(self, *args, **kwargs)  # Otherwise, execute the method
        return wrapper

def ensure_nltk_package(package_category: str, package_name: str) -> Callable:
    """
    Decorator to ensure that a specific NLTK package is installed before executing a function.

    This decorator checks if the specified NLTK package is available. If the package is not available,
    it attempts to download it. This is particularly useful for functions that rely on specific NLTK
    datasets or tokenizers that may not be installed by default with the NLTK library.

    Args:
        package_category (str): The category of the NLTK package (e.g., 'taggers', 'corpora').
        package_name (str): The specific NLTK package to check and download if necessary.

    Returns:
        Callable: A decorator that wraps the original function to ensure the availability of the NLTK package.

    Usage:
        To use this decorator, annotate the function that requires an NLTK package with:
        @ensure_nltk_package('corpora', 'wordnet')
        def some_function_using_wordnet():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                # Attempt to find the package
                nltk.find(f"{package_category}/{package_name}")
            except LookupError:
                # If the package is not found, download it
                print(f"{package_name} not found, downloading now...")
                nltk.download(package_name)
            # Execute the function after ensuring the package is available
            return func(*args, **kwargs)
        return wrapper
    return decorator