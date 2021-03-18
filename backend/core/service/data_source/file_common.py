import os
import random
import string

from core.model.data_source import DataSource
from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.exception import SomeError, FileNotAllowedError


def file_extension(file_name: str) -> str:
    """Return the text after the FIRST dot in a file name."""
    split = os.path.splitext(file_name)
    return split[-1][1:].strip().lower()


def strip_file_extensions(file_name: str) -> str:
    """Return the text before the FIRST dot in a file name."""
    return file_name.split('.')[0]


def is_file_allowed(file_name: str) -> bool:
    """Returns whether the file has only one file extension
    and it is one of the implemented file types."""
    ext = file_extension(file_name)
    return ext in [DataSourceConstants.EXT_CSV, DataSourceConstants.EXT_JSON] or\
        ext in DataSourceConstants.EXT_SQLITE


def file_extension_to_mime_type(extension: str) -> str:
    """Convert a supported file extension to its mime type."""
    if extension == DataSourceConstants.EXT_CSV:
        return DataSourceConstants.MIME_TYPE_CSV
    elif extension == DataSourceConstants.EXT_JSON:
        return DataSourceConstants.MIME_TYPE_JSON
    elif extension in DataSourceConstants.EXT_SQLITE:
        return DataSourceConstants.MIME_TYPE_SQLITE
    raise SomeError('unsupported file extension')


class FileDataSourceFactory:
    """Manage the creation of a data source backed by a file.

    The class instance receives a file name and general storage directory.
    In order to avoid clashes, the class creates a directory named by the project ID.
    The file name also receives a random prefix, so that it is possible
    to import several files with the same name.
    """

    def __init__(self, proj: Project, file_name: str, storage_root: str):
        if not is_file_allowed(file_name):
            raise FileNotAllowedError()
        self._proj = proj
        self._storage_root = storage_root
        self._file_name = file_name
        self._directory = os.path.join(self._storage_root, str(self._proj.id))
        random_file_name = self._with_random_prefix(self._file_name)
        self._file_path = os.path.join(self._directory, random_file_name)

    @property
    def file_path(self) -> str:
        """Full path where the file should be stored after a data source is created."""
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
        """Make sure that the target directory exists and no file
        with the same name exists. Create and return a data source.
        """
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
        if ext in DataSourceConstants.EXT_SQLITE:
            data_source.driver = DataSourceConstants.DRIVER_SQLITE
            data_source.db = self._file_path
        return data_source
