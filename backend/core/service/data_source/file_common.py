import os
import random
import string

from core.model.data_source import DataSource
from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.exception import SomeError


def file_extension(file_name: str) -> str:
    split = os.path.splitext(file_name)
    return split[1][1:].strip().lower()


def strip_file_extensions(file_name: str) -> str:
    return file_name.split('.')[0]


def is_file_allowed(file_name: str) -> bool:
    ext = file_extension(file_name)
    return ext in [DataSourceConstants.EXT_CSV, DataSourceConstants.EXT_JSON] or\
        ext in DataSourceConstants.EXT_SQLITE


def file_extension_to_mime_type(extension: str) -> str:
    if extension == DataSourceConstants.EXT_CSV:
        return DataSourceConstants.MIME_TYPE_CSV
    elif extension == DataSourceConstants.EXT_JSON:
        return DataSourceConstants.MIME_TYPE_JSON
    elif extension in DataSourceConstants.EXT_SQLITE:
        return DataSourceConstants.MIME_TYPE_SQLITE
    raise SomeError('unsupported file extension')


class FileDataSourceFactory:
    def __init__(self, proj: Project, file_name: str, storage_root: str):
        self._proj = proj
        self._storage_root = storage_root
        self._file_name = file_name
        self._directory = os.path.join(self._storage_root, str(self._proj.id))
        random_file_name = self._with_random_prefix(self._file_name)
        self._file_path = os.path.join(self._directory, random_file_name)

    @property
    def file_path(self) -> str:
        return self._file_path

    @classmethod
    def _with_random_prefix(cls,
                            file_name: str,
                            size: int = 10,
                            letters: str = string.ascii_letters) -> str:
        prefix = ''.join(random.choice(letters) for _ in range(size))
        return '{}_{}'.format(prefix, file_name)

    def _file_exists(self) -> bool:
        return os.path.exists(self._file_path)

    def _make_sure_directory_exists(self):
        if not os.path.exists(self._directory):
            os.mkdir(self._directory)

    def create_data_source(self) -> DataSource:
        if self._file_exists():
            raise SomeError('file already exists')
        self._make_sure_directory_exists()
        ext = file_extension(self._file_name)
        data_source = DataSource(
            file_name=self._file_name,
            file_path=self._file_path,
            mime_type=file_extension_to_mime_type(ext),
            project=self._proj
        )
        if ext == DataSourceConstants.EXT_SQLITE:
            data_source.driver = DataSourceConstants.DRIVER_SQLITE
            data_source.db = self._file_path
        return data_source
