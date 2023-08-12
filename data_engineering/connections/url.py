"""Classes to upload and download data to an URL.
"""
from typing import Optional
import requests
from data_engineering.data_types.files import File


def download_file_from_url(url: str, file: File, timeout: Optional[int] = 30) -> None:
    """Download a file to the local system.

    Args:
        url (str): where the file is downloaded
        file (File): file data
        timeout (Optional[int], optional): tim out. Defaults to 30.
    """
    response = requests.get(url, timeout=timeout)
    with open(file.path, "wb") as opened_file:
        opened_file.write(response.content)


def upload_file_to_url(url: str, file: File, timeout: Optional[int] = 30) -> None:
    """Uploads a file from the local system.

    Args:
        url (str): where the file is uploaded
        file (File): file data
        timeout (Optional[int], optional): time out. Defaults to 30.
    """
    with open(file.path, "rb") as opened_file:
        requests.post(url, files={"file": opened_file}, timeout=timeout)
