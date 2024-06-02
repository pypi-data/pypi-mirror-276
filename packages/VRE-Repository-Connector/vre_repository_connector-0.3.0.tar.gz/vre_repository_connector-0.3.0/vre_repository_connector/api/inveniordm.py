# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""Wrapper for InvenioRDM instances."""

import getpass
import os.path
import pathlib
import re
import tempfile
import urllib.parse
from typing import Iterable, Optional, Tuple

from inveniordm_py.client import InvenioAPI as InvenioRESTClient
from inveniordm_py.files.metadata import FilesListMetadata, OutgoingStream
from inveniordm_py.records.metadata import DraftMetadata
from inveniordm_py.records.resources import Draft

from ..utils import doi_regex, url_regex
from .base import BaseWrapper

recid_regex = re.compile(r"^.*(/api)?/records/(.*)$")
recid_file_re = re.compile(r"(/api)?/records/([^/]+)(/files/([^/]+)(/content)?)?")


class InvenioRDM(BaseWrapper):
    """Utility class for connecting to an InvenioRDM instance."""

    def __init__(self, url: str, api_token: str = None):
        """InvenioRDM constructor."""
        if match := url_regex.match(url):
            scheme, host = match.group(2) or "https", match.group(3)
            url = f"{scheme}://{host}"
            parts = urllib.parse.urlparse(url)

            # Ensure the path in the URL starts with "/api",
            # as the InvenioAPI client can only fetch JSON
            if not parts.path.endswith("/api") and "/api/" not in parts.path:
                parts = parts._replace(path="/api")

            self.url = urllib.parse.urlunparse(parts)
            self.client = InvenioRESTClient(base_url=self.url, access_token=api_token)

        else:
            raise ValueError(f"Invalid InvenioRDM URL: {url}")

    def ask_credentials(self):
        """Ask the user interactively for credentials."""
        print(f"(InvenioRDM) Enter your API token for '{self.url}'")
        token = getpass.getpass("API Token: ")
        return {"api_token": token}

    def authenticate(self, api_token, token=None):
        """Authenticate with an API token."""
        self.client._access_token = api_token or token
        self.client.session.headers["Authorization"] = f"Bearer {api_token}"

    def clear_auth(self):
        """Clear the API token."""
        self.client._access_token = None
        self.client.session.headers.pop("Authorization", None)

    def list_files(self, recid: str) -> Iterable[str]:
        """List all files for the record."""
        url = f"{self.client._base_url}/records/{recid}/files"
        response = self.client.session.get(url)
        return [f["key"] for f in response.json()["entries"]]

    def url_to_parts(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the recid and filename from the URL."""
        recid, filename = None, None

        try:
            path = urllib.parse.urlparse(url).path
            match = recid_file_re.match(path)
            recid, filename = match.group(2), match.group(4)
        except AttributeError:
            # e.g. if the URL doesn't match the pattern
            pass

        return (recid, filename)

    def _normalize_pid(self, record_pid: str) -> str:
        """Normalize the given record PID.

        If the input is either a DOI or a URL pointing to the record's landing page
        (or API endpoint), the persistent identifier will be extracted from the string.
        Otherwise, the input will be assumed to be a persistent identifier already,
        and returned as is.
        """

        if m := doi_regex.match(record_pid):
            # the last part of the DOI
            return m.group(4)

        elif record_pid.startswith(self.url) and (m := recid_regex.match(record_pid)):
            # the part in the URL after "/records/"
            return m.group(2)

        return record_pid

    def _resolve_draft(self, record_pid: str) -> Draft:
        """Returns a draft object, given a record PID."""
        record = self.client.records(self._normalize_pid(record_pid))
        return record.draft

    def create(self, metadata: dict) -> str:
        """Creates the record with the given metadata."""
        draft = self.client.records.create(data=DraftMetadata(**metadata))
        return draft.data["id"]

    def update(self, record_pid: str, metadata: dict) -> bool:
        """Updates the draft metadata."""
        draft = self._resolve_draft(record_pid)

        try:
            draft.get()
            draft.update(data=DraftMetadata(**metadata))
            return True

        except Exception as e:
            print(f"Draft update failed: {e}")
            return False

    def upload(
        self,
        file_path: str,
        record_pid: Optional[str] = None,
        file_name: Optional[str] = None,
    ) -> Optional[str]:
        """Uploads a file to the specified draft.

        If no draft is specified, a new one will be created.
        Returns the recid of the draft and name of the uploaded file.
        """
        file_name = file_name or os.path.basename(file_path)
        if not record_pid:
            record_pid = self.create({"metadata": {"title": file_name}})

        draft = self._resolve_draft(record_pid)

        try:
            draft.get()
            file_meta = FilesListMetadata([{"key": file_name}])
            file = draft.files.create(file_meta)

            stream = open(file_path, "rb")
            for f in draft.files:
                f.set_contents(OutgoingStream(data=stream))
                f.commit()

            return (record_pid, file.data["entries"][0]["key"])

        except Exception as e:
            print(f"File upload failed: {e}")

    def remove(self, record_pid: str, file_name: str) -> bool:
        """Removes given file from the specified draft."""
        draft = self._resolve_draft(record_pid)

        try:
            draft.get()
            draft.files(file_name).delete()
            return True

        except Exception as e:
            print(f"File removal failed: {e}")
            return False

    def download(self, record_pid: str, file_name: str) -> Optional[str]:
        """Downloads given file from the specified (published) record.

        Returns the path to the downloaded file.
        """
        record = self.client.records(self._normalize_pid(record_pid))

        try:
            record.get()
            response = record.files(file_name).download()

            with tempfile.NamedTemporaryFile(delete=False) as downloaded_file:

                for chunk in response.iter_content(chunk_size=256):
                    downloaded_file.write(chunk)

            file_path = pathlib.Path(downloaded_file.name)
            return str(file_path)

        except Exception as e:
            print(f"File download failed: {e}")

    def publish(self, record_pid: str) -> Optional[str]:
        """Publishes draft given draft."""
        draft = self._resolve_draft(record_pid)

        try:
            record = draft.publish()
            return record.data["id"]

        except Exception as e:
            print(f"Draft publish failed: {e}")
