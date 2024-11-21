"""
Module name: file_reader.py
Route: src/core/file_reader.py
Description: Handles reading and validation of Python source files
Project: LOC Counter System
Author: Amílcar Pérez
Organization: Equipo 3
License: MIT
Date Created: 16-11-2024
Last Update: 17-11-2024

Dependencies:
    - pathlib
    - typing
    - utils.validators.is_valid_python_file

Usage:
    reader = PythonFileReader("script.py")
    lines, error = reader.read_lines()
"""

from pathlib import Path
from typing import Union, Optional

from utils.validators import is_valid_python_file
from utils.file_utils import read_text_file

class PythonFileReader:
    """
    Handles reading and validation of Python source files.

    Reads and validates Python source files, providing methods for validation
    and line-by-line reading with proper error handling.

    Attributes:
        file_path (Path): Path to the Python file to read
        _content (Optional[list[str]]): Cached content of the file

    Methods:
        validate() -> tuple[bool, str]: Validates if file is a valid Python file
        read_lines() -> tuple[list[str], Optional[str]]: Reads all lines from file
        content() -> list[str]: Returns cached file content or reads it

    Example:
        >>> reader = PythonFileReader("example.py")
        >>> lines, error = reader.read_lines()
        >>> print(len(lines))
        42
    """
    
    def __init__(self, file_path: Union[str, Path]):
        """
        Initialize a new Python file reader.

        Args:
            file_path (Union[str, Path]): Path to the Python file to read

        Example:
            >>> reader = PythonFileReader("script.py")
        """
        self.file_path = Path(file_path)
        self._content: Optional[list[str]] = None
        
    def validate(self) -> tuple[bool, str]:
        """
        Validates if the file is a valid Python file.

        Returns:
            tuple[bool, str]: Tuple containing validation results
                - bool: True if file is valid, False otherwise
                - str: Empty if valid, error description if invalid

        Example:
            >>> reader = PythonFileReader("script.py")
            >>> is_valid, error = reader.validate()
            >>> print(is_valid)
            True
        """
        return is_valid_python_file(self.file_path)
    
    def read_lines(self) -> tuple[list[str], Optional[str]]:
        """
        Reads all lines from the Python file.

        Returns:
            tuple[list[str], Optional[str]]: Tuple containing read results
                - list[str]: List of strings representing file lines
                - Optional[str]: None if successful, error message if failed

        Example:
            >>> reader = PythonFileReader("script.py")
            >>> lines, error = reader.read_lines()
            >>> print(lines[0])
            "def main():"
        """
        is_valid, error = self.validate()
        if not is_valid:
            return [], error
        
        self._content, error = read_text_file(self.file_path)
        return self._content, error
    
    def clear_cache(self) -> None:
        """
        Clear cached content to free memory.
        
        Example:
            >>> reader = PythonFileReader("script.py")
            >>> _ = reader.content  # Load content
            >>> reader.clear_cache()  # Free memory
        """
        self._content = None
    
    @property
    def content(self) -> list[str]:
        """
        Returns cached file content or reads it if not yet read.
        Call clear_cache() to free memory when done.

        Returns:
            list[str]: Copy of file lines

        Raises:
            RuntimeError: If there was an error reading the file
        """
        if self._content is None:
            self._content, error = self.read_lines()
            if error:
                raise RuntimeError(f"Error reading file: {error}")
        return self._content.copy()