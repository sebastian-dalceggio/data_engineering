"""Classes to upload and download data to an URL.
"""
from typing import Optional
from urlpath import URL
from pathlib import Path

def download_file_from_url(url: URL, file: Path, timeout: Optional[int] = 30) -> None:
    """Download a file to the local system.

    Args:
        url (URL): where the file is downloaded
        file (Path): path to the file
        timeout (Optional[int], optional): tim out. Defaults to 30.
    """
    response = url.get(timeout=timeout)
    with open(file, "wb") as opened_file:
        opened_file.write(response.content)


def upload_file_to_url(url: URL, file: Path, timeout: Optional[int] = 30) -> None:
    """Uploads a file from the local system.

    Args:
        url (URL): where the file is uploaded
        file (Path): path to the file
        timeout (Optional[int], optional): time out. Defaults to 30.
    """
    with open(file, "rb") as opened_file:
        url.post(url, files={"file": opened_file}, timeout=timeout)
