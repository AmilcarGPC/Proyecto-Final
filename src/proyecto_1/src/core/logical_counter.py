class LogicalLineCounter:
    """
    Main class to process and count logical lines
    
    Methods:
    - count_logical_lines(content: str) -> int
      Processes file content and returns logical LOC count
    
    - _process_class_definition(line: str) -> bool
    - _process_function_definition(line: str) -> bool
    - _process_control_structures(line: str) -> bool
    - _process_match_case(lines: list[str], index: int) -> tuple[bool, int]
    - _process_comprehension(line: str) -> bool
    - _process_generator(line: str) -> bool
    - _process_ternary(line: str) -> bool
    
    Private attributes:
    - _logical_count: int
    - _current_indent: int
    - _match_case_count: int
    """