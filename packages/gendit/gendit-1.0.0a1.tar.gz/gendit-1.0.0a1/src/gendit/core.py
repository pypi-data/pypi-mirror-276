class Format:
    CSV = 'CSV'
    JSON = 'JSON'
    JSONL = 'JSONL'
    YAML = 'YAML'
    PARQUET = 'PARQUET'
    AUTO = 'AUTO'

def detect_format(file: str) -> str | None:
    """
    Detects the format to use from the file name.

    >>> detect_format('output.csv') # CSV
    >>> detect_format('output.json') # JSON
    """
    if file.endswith('.csv'):
        return Format.CSV

    if file.endswith('.json'):
        return Format.JSON

    return None
