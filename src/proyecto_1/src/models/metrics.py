class FileMetrics:
    """Data class to store file metrics
    
    Attributes:
    - file_name: str
    - physical_loc: int
    - logical_loc: int
    - analysis_date: datetime
    
    Methods:
    - to_dict() -> dict
      Converts metrics to JSON-compatible dictionary
    
    - from_dict(data: dict) -> FileMetrics
      Creates instance from dictionary
    
    Properties:
    - is_valid: bool
      Checks if metrics are within valid ranges
"""