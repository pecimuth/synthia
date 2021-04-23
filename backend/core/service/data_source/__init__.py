class DataSourceConstants:
    """Common constants including file extensions, mime types
    and driver names.
    """
    EXT_CSV = 'csv'
    EXT_JSON = 'json'
    EXT_SQLITE = ['db', 'sql', 'sqlite', 'sqlite3']

    MIME_TYPE_CSV = 'text/csv'
    MIME_TYPE_JSON = 'application/json'
    MIME_TYPE_SQLITE = 'application/vnd.sqlite3'

    DRIVER_SQLITE = 'sqlite'
    DRIVER_POSTGRES = 'postgresql'

    CLIENT_SERVER_DB_DRIVERS = [DRIVER_POSTGRES]
    """Driver names of supported client/server databases."""
