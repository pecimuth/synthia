import os

from core.model.data_source import DataSource
from core.model.project import Project
from core.service.data_source import DataSourceConstants


def is_file_allowed(file_name: str) -> bool:
    _, ext = os.path.splitext(file_name)
    return ext in [DataSourceConstants.EXT_CSV, DataSourceConstants.EXT_JSON] or\
        ext in DataSourceConstants.EXT_SQLITE


def file_extension_to_mime_type(extension: str) -> str:
    if extension == DataSourceConstants.EXT_CSV:
        return DataSourceConstants.MIME_TYPE_CSV
    elif extension == DataSourceConstants.EXT_JSON:
        return DataSourceConstants.MIME_TYPE_JSON
    elif extension in DataSourceConstants.EXT_SQLITE:
        return DataSourceConstants.MIME_TYPE_SQLITE
    raise Exception('unsupported file extension')


class FileDataSourceFactory:
    def __init__(self, proj: Project, file_name: str, storage_root: str):
        self._proj = proj
        self._storage_root = storage_root
        self._file_name = file_name
        self._directory = os.path.join(self._storage_root, str(self._proj.id))
        self._file_path = os.path.join(self._directory, self._file_name)

    @property
    def file_path(self) -> str:
        return self._file_path

    def _file_exists(self) -> bool:
        return os.path.exists(self._file_path)

    def _make_sure_directory_exists(self):
        if not os.path.exists(self._directory):
            os.mkdir(self._directory)

    def create_data_source(self) -> DataSource:
        if self._file_exists():
            raise Exception('file already exists')
        self._make_sure_directory_exists()
        _, ext = os.path.splitext(self._file_name)
        data_source = DataSource(
            file_name=self._file_name,
            mime_type=file_extension_to_mime_type(ext),
            project=self._proj
        )
        if ext == DataSourceConstants.EXT_SQLITE:
            data_source.driver = DataSourceConstants.DRIVER_SQLITE
            data_source.db = self._file_path
        return data_source
