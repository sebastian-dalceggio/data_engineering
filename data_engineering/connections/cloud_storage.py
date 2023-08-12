"""Classes to connect to a Cloud Data Storage.

This module provides the necesary classes to connect to cloud storage.
"""

from typing import List
from google.cloud.storage import Client as GCPClient # type: ignore[import]
from data_engineering.data_types.files import File, GCPStorageFile


class GCPStorage:
    """Connects to a GCP Storage system.

    It can be used to upload and download data from GCP Storage from different
    buckets.

    Attributes:
        buckets_name (List[str]): list of the names of the buckets
    """

    def __init__(self, buckets_name: List[str]) -> None:
        """Defines a connection to GCP Storage.

        Args:
            buckets_name (List[str]): list of the names of the buckets
        """
        self.buckets_name = buckets_name
        self._client = GCPClient()
        self._buckets = {
            bucket_name: self._client.get_bucket(bucket_name)
            for bucket_name in self.buckets_name
        }

    def upload_file(self, local_file: File, cloud_file: GCPStorageFile) -> None:
        """Uploads a file to GCP Storage.

        The origin and target information is in local_file and cloud_file objects.

        Args:
            local_file (File): where the file is read
            cloud_file (GCPStorageFile): where the file is uploaded
        """
        bucket = self._buckets[cloud_file.bucket]
        blob = bucket.blob(cloud_file.directory + cloud_file.file_name)
        blob.upload_from_filename(local_file.directory + local_file.file_name)

    def download_file(self, local_file: File, cloud_file: GCPStorageFile) -> None:
        """Downloads a file to GCP Storage.

        The origin and target information is in local_file and cloud_file objects.

        Args:
            local_file (File): where the file is read
            cloud_file (GCPStorageFile): where the file is uploaded
        """
        bucket = self._buckets[cloud_file.bucket]
        blob = bucket.blob(cloud_file.directory + cloud_file.file_name)
        blob.download_to_filename(local_file.directory + local_file.file_name)
