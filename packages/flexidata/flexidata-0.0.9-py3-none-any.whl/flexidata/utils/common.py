import importlib.util
from typing import NoReturn

def check_package_installed(package_name: str) -> NoReturn:
    """
    Checks if a specified package is installed and raises an ImportError if not.

    This function utilizes Python's importlib utility to find the specification of a package by its name.
    If the package cannot be found, it indicates that the package is not installed, prompting an ImportError
    with a message instructing to install the package. This can be useful in scenarios where specific
    packages are crucial for the operation of a script or application, allowing for graceful failure and
    clear guidance on how to resolve dependencies.

    Args:
        package_name (str): The name of the package to check for installation.

    Raises:
        ImportError: If the package is not found, indicating it is not installed.

    Note:
        This function always raises an exception if the package is not installed and returns None otherwise.
        It does not have a return value and the return type is annotated as NoReturn to reflect this behavior.
    """
    package_spec = importlib.util.find_spec(package_name)
    if package_spec is None:
        raise ImportError(f"{package_name} is required but not installed. Please install it using pip.")
