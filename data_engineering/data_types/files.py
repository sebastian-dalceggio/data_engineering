"""Classes that has data for different types of files.
"""
from dataclasses import dataclass


@dataclass
class File:
    """Metadata of a file.

    Attributes:
        file_name (str): name of the file
        directory (str): directory where the file is saved. It has to end in '/'
    """

    file_name: str
    directory: str

    @property
    def path(self) -> str:
        """Path where the file is saved.

        Returns:
            str: path
        """
        return f"{self.directory}{self.file_name}"


@dataclass
class CloudFile(File):
    """Metadata of a file.

    Attributes:
        file_name (str): name of the file
        directory (str): directory where the file is saved. It has to end in '/'
        bucket (str): bucket name where it is saved
    """

    bucket: str


@dataclass
class GCPStorageFile(CloudFile):
    """Metadata of a GPC Storage file.

    Attributes:
        file_name (str): name of the file
        directory (str): directory where the file is saved. It has to end in '/'
        bucket (str): bucket name where it is saved
    """

    @property
    def path(self) -> str:
        return f"gs://{self.bucket}/{self.directory}{self.file_name}"
