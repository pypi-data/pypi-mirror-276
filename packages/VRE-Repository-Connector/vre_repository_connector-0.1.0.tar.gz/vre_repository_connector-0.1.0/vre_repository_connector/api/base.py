# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

import abc
from typing import Optional, Tuple


class BaseWrapper(abc.ABC):
    """The common denominator of operations that need to be supported."""

    @abc.abstractmethod
    def authenticate(self, token_or_username, password=None):
        """Set the credentials for future API calls.

        Provides the API wrapper with a set of credentials to be used for future
        API calls.
        This method accepts two different shapes of credentials: Either just an API
        token, or a pair of username + password.

        :param token_or_username: An API token or the username.
        :param password:          The password to be used along with the username.
        """

    @abc.abstractmethod
    def clear_auth(self):
        """Clear the credentials."""

    @abc.abstractmethod
    def upload(
        self, file_path: str, container_id: Optional[str | int], name: Optional[str]
    ) -> Optional[int | str]:
        """Upload the local file under ``file_path`` to the repository.

        If the ``container_id`` is specified, then the file will be uploaded to this
        container.
        Otherwise, a new container will be created.

        :param file_path:    The local path of the file to upload.
        :param container_id: The ID of the container to which to add the uploaded file.
        :param name:         Override for the name of the file after upload.
        """

    @abc.abstractmethod
    def download(self, container_id: str | int, name: str | int) -> Optional[str]:
        """Download the file with the specified name from the referenced container.

        :param container_id: The ID of the container from which to download the file.
        :param name:         The name of the file to download.
        """

    def url_to_parts(self, url: str) -> Tuple[Optional[str | int], Optional[str | int]]:
        """Parse the container and file from the URL.

        :param url: The URL from which to parse the container ID and file name.
        """
