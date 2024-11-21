"""
Module name: file_utils.py
Route: src/utils/file_utils.py
Description: Utilities for file operations
Project: LOC Counter System
Author: Amílcar Pérez
Organization: Equipo 3
License: MIT
Date Created: 17-11-2024
Last Update: 17-11-2024

Dependencies:
    - pathlib
    - typing

Usage:
    from utils.file_utils import read_text_file
    content, error = read_text_file("C:/example.txt")
"""

from pathlib import Path
from typing import Union, List, Optional, Tuple
import re

def read_text_file(
    file_path: Union[str, Path], 
    encoding: str = 'utf-8'
) -> Tuple[List[str], Optional[str]]:
    """
    Reads content from a text file.

    Args:
        file_path (Union[str, Path]): Path to the file to read
        encoding (str): File encoding to use. Defaults to UTF-8

    Returns:
        Tuple[List[str], Optional[str]]: Tuple containing:
            - List[str]: Lines read from file
            - Optional[str]: Error message if failed, None if successful

    Example:
        >>> lines, error = read_text_file("example.txt")
        >>> if error:
        ...     print(f"Error: {error}")
        ... else:
        ...     print(f"Read {len(lines)} lines")
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.readlines(), None
    except UnicodeDecodeError:
        return [], f"File encoding error - expected {encoding}"
    except Exception as e:
        return [], f"Error reading file: {str(e)}"

def format_long_lines(lines: List[str]) -> None:
    """
    Format Python file lines exceeding 80 characters while maintaining coding standards.
    
    Args:
        file_path: Path to Python file to format
    """
    def get_indent(line: str) -> str:
        return re.match(r'^\s*', line).group()

    def format_function_call(line: str, indent: str) -> List[str]:
        # Extract function name and arguments
        match = re.match(r'(.*?\()(.*)\)', line.strip())
        if not match:
            return [line]
        
        func_name, args = match.groups()
        if not args:
            return [line]
            
        # Split arguments and format
        args_list = [arg.strip() for arg in args.split(',')]
        formatted = [f"{indent}{func_name.strip()}("]
        
        # Add arguments with proper indentation
        args_indent = ' ' * (len(func_name) + 1)
        for i, arg in enumerate(args_list):
            if i < len(args_list) - 1:
                formatted.append(f"{indent}{args_indent}{arg},")
            else:
                formatted.append(f"{indent}{args_indent}{arg})")
        
        return formatted

    def format_expression(line: str, indent: str) -> List[str]:
        # Handle assignments with long expressions
        parts = line.split('=', 1)
        if len(parts) != 2:
            return [line]
            
        var_name = parts[0].strip()
        expression = parts[1].strip()
        
        # Split on operators
        operators = ['+', '-', '*', '/', '&', '|']
        for op in operators:
            if op in expression:
                terms = [t.strip() for t in expression.split(op)]
                formatted = [f"{indent}{var_name} = {terms[0]}"]
                expr_indent = ' ' * (len(var_name) + 3)
                
                for term in terms[1:]:
                    formatted.append(f"{indent}{expr_indent}{op} {term}")
                return formatted
                
        return [line]

    # Process lines
    formatted_lines = []
    for line in lines:
        if len(line.rstrip()) <= 80:
            formatted_lines.append(line)
            continue
            
        indent = get_indent(line)
        stripped = line.strip()
        
        # Handle different cases
        if '(' in stripped and ')' in stripped:
            formatted_lines.extend(format_function_call(line, indent))
        elif '=' in stripped:
            formatted_lines.extend(format_expression(line, indent))
        else:
            formatted_lines.append(line)

    return formatted_lines