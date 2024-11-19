class MetricsStorage:
    """
    Manages JSON persistence of metrics
    
    Methods:
    - save_metrics(metrics: FileMetrics) -> None
    - load_metrics(file_name: str) -> Optional[FileMetrics]
    - update_metrics(metrics: FileMetrics) -> None
    - get_all_metrics() -> list[FileMetrics]
    
    Private:
    - _ensure_storage_file() -> None
    - _read_json() -> dict
    - _write_json(data: dict) -> None
    """