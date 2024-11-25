"""
Module name: validators.py
Route: src/utils/validators.py
Description: Validates Python files and their contents
Project: LOC Counter System
Author: Amílcar Pérez
Organization: Equipo 3
License: MIT
Date Created: 16-11-2024
Last Update: 17-11-2024

Dependencies:
    - os
    - pathlib
    - typing

Usage:
    from utils.validators import is_valid_python_file
    is_valid, error = is_valid_python_file("script.py")
"""

from pathlib import Path
from typing import Union

def is_valid_python_file(file_path: Union[str, Path]) -> tuple[bool, str]:
    """
    Validates if a file path corresponds to a valid Python file.

    Args:
        file_path (Union[str, Path]): Path to the file to validate

    Returns:
        tuple[bool, str]: Tuple containing (is_valid, error_message)
            is_valid: True if file is valid Python file, False otherwise
            error_message: Empty string if valid, error description if invalid

    Raises:
        PermissionError: If file exists but cannot be accessed
        Exception: For other file system related errors

    Example:
        >>> is_valid, error = is_valid_python_file("script.py")
        >>> print(is_valid, error)
        True, ""
    """
    path = Path(file_path)
    
    if not path.exists():
        return False, f"File not found: {file_path}"
    
    if not path.is_file():
        return False, f"Path is not a file: {file_path}"
        
    if path.suffix.lower() != '.py':
        return False, f"File must have .py extension: {file_path}"
    
    try:
        path.open('r').close()
        return True, ""
    except PermissionError:
        return False, f"Permission denied reading file: {file_path}"
    except Exception as e:
        return False, f"Error accessing file: {str(e)}"