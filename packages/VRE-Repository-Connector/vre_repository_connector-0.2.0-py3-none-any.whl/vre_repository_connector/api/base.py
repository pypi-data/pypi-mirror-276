# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

import abc
from typing import Dict, Iterable, Optional, Tuple


class BaseWrapper(abc.ABC):
    """The common denominator of operations that need to be supported."""

    @abc.abstractmethod
    def ask_credentials(cls) -> Dict[str, str]:
        """Ask the user interactively for credentials.

        The returned dictionary can be used as keyword arguments for ``authenticate``.
        """
        return {}

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
    ) -> Tuple[Optional[int | str], Optional[int | str]]:
        """Upload the local file under ``file_path`` to the repository.

        If the ``container_id`` is specified, then the file will be uploaded to this
        container.
        Otherwise, a new container will be created.

        A tuple with the container ID and file name/ID will be returned.

        :param file_path:    The local path of the file to upload.
        :param container_id: The ID of the container to which to add the uploaded file.
        :param name:         Override for the name of the file after upload.
        """
        return None

    @abc.abstractmethod
    def download(self, container_id: str | int, name: str | int) -> Optional[str]:
        """Download the file with the specified name from the referenced container.

        :param container_id: The ID of the container from which to download the file.
        :param name:         The name of the file to download.
        """
        return None

    @abc.abstractmethod
    def list_files(self, container_id: str | int) -> Iterable[str]:
        """List all the file names attached to the container.

        :param container_id: The container to list the files for.
        """
        return []

    @abc.abstractmethod
    def url_to_parts(self, url: str) -> Tuple[Optional[str | int], Optional[str | int]]:
        """Parse the container and file from the URL.

        :param url: The URL from which to parse the container ID and file name.
        """
        return (None, None)

    def authenticate_interactive(self):
        """Shorthand for ``ask_credentials()`` into ``authenticate()``."""
        self.authenticate(**self.ask_credentials())
