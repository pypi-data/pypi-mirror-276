# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""Helpers for interacting automatically with InvenioRDM and DBRepo."""

import pathlib
from typing import Optional, Union
from urllib.parse import urlparse, urlunparse

import pandas as pd
import requests

from .dbrepo import DBRepo
from .inveniordm import InvenioRDM


class AutoAPI:
    """Utility class which decides on which system to connect."""

    def __init__(self, url: str, auth_token_or_credentials: str = None):
        """Auto API constructor."""
        self.url = url
        self.auth_token_or_credentials = auth_token_or_credentials
        self.known_instances = {
            "dbrepo1.ec.tuwien.ac.at": "DBRepo",
            "test.dbrepo.tuwien.ac.at": "DBRepo",
            "researchdata.tuwien.ac.at": "InvenioRDM",
            "researchdata.tuwien.at": "InvenioRDM",
            "test.researchdata.tuwien.at": "InvenioRDM",
            "s168.dl.hpc.tuwien.ac.at": "InvenioRDM",
        }

    def _inject_api_route(self, url: str) -> str:
        """Injects '/api' after the host if not included."""
        parsed_url = urlparse(url)
        new_path = (
            f"/api{parsed_url.path}"
            if not parsed_url.path.startswith("/api")
            else parsed_url.path
        )

        return urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                new_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment,
            )
        )

    def _resolve_service(self, host: str) -> Optional[str]:
        """Resolves service based on known URLs."""
        return self.known_instances.get(host)

    def _follow_redirects(self, url: str):
        """Follows HTTP redirects and returns the final URL."""
        try:
            response = requests.head(url, allow_redirects=True)
            return response.url

        except requests.RequestException as e:
            raise ValueError(f"Error following redirect {e}")

    def check_or_set_api_token(self) -> None:
        """Checks if api token is set and requests it if not."""
        if self.auth_token_or_credentials is None:
            self.auth_token_or_credentials = input(
                "Input your access token for InvenioRDM: "
            )

    def suggest_repository(self, url) -> Union[DBRepo, InvenioRDM, None]:
        """Returns the suggested repository system according to the URL provided."""
        host = urlparse(url).netloc

        if host == "doi.org":
            return self.suggest_repository(self._follow_redirects(url))

        elif self._resolve_service(host) == "DBRepo":
            dbrepo = DBRepo(url)

            username = input("Username for DBRepo: ")
            password = input("Password for DBRepo: ")
            dbrepo.authenticate(username, password)

            return dbrepo

        elif self._resolve_service(host) == "InvenioRDM":

            self.check_or_set_api_token()
            return InvenioRDM(
                api_token=self.auth_token_or_credentials,
                url=urlparse(url).scheme + "://" + host,
            )

        print("Unknown host for repository suggestion.")

    def upload_data(self, metadata: dict, file_path: str, **kwargs) -> Optional[str]:
        """Inspects the specified file and decides in which repository system to upload it to."""
        service = None

        try:
            pd.read_csv(file_path)
            # If successful, it's tabular data
            service = DBRepo(self.url)
            username = input("Username for DBRepo: ")
            password = input("Password for DBRepo: ")
            service.authenticate(username, password)
            return service.upload(
                file_path, kwargs.get("database_id"), kwargs.get("table_name")
            )
        except pd.errors.EmptyDataError:
            return "Invalid file: Empty data"
        except pd.errors.ParserError:
            # File is not tabular or has parsing issues
            self.check_or_set_api_token()
            service = InvenioRDM(
                self.auth_token_or_credentials,
                urlparse(self.url).scheme + "://" + urlparse(self.url).netloc,
            )
            draft_id = service.create(metadata)
            return service.upload(file_path, draft_id, pathlib.Path(file_path).name)
        except Exception as e:
            return f"Error: {e}"

        finally:
            if service is not None:
                service.clear_auth()

    def download_data(self, file_name: str, **kwargs) -> Optional[str]:
        """Downloads file automatically based on the URL."""
        service = self.suggest_repository(self.url)
        if service is not None:
            modified_url = self._inject_api_route(self.url)
            return service.download(modified_url, file_name)

    def archive_data(
        self, metadata: dict, file_name: str, file_path: str
    ) -> Optional[str]:
        """Sends data to InvenioRDM for all file types."""
        service = self.suggest_repository(self.url)

        if service is not None:
            if isinstance(service, InvenioRDM):
                draft_id = service.create(metadata)
                return service.upload(draft_id, file_name, file_path)
            else:
                print(
                    "Archive data operation is only supported for InvenioRDM instances."
                )
