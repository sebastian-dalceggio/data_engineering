"""Classes that has data for different types of files.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class File:
    """Metadata of a file.

    Attributes:
        file_name (str): name of the file
        directory Optional(str): directory where the file is saved. Defaults to None.
    """

    file_name: str
    directory: Optional[str] = None

    @property
    def path(self) -> str:
        """Path where the file is saved.

        Returns:
            str: path
        """
        if self.directory:
            return f"{self.directory}/{self.file_name}"
        return self.file_name


@dataclass
class CloudFile(File):
    """Metadata of a file.

    Attributes:
        file_name (str): name of the file
        directory Optional(str): directory where the file is saved. Defaults to None.
        bucket (str): bucket name where it is saved
    """

    bucket: str


@dataclass
class GCPStorageFile(CloudFile):
    """Metadata of a GPC Storage file.

    Attributes:
        file_name (str): name of the file
        directory Optional(str): directory where the file is saved. Defaults to None.
        bucket (str): bucket name where it is saved
    """

    @property
    def path(self) -> str:
        if self.directory:
            return f"gs://{self.bucket}/{self.directory}/{self.file_name}"
        return f"gs://{self.bucket}/{self.file_name}"
