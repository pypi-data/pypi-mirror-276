# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""Helpers for interacting automatically with various repository types."""

from typing import List, Optional, Tuple
from urllib.parse import urlparse

import pandas as pd
import requests

from .api.base import BaseWrapper
from .api.dbrepo import DBRepo
from .api.inveniordm import InvenioRDM
from .utils import url_regex

KNOWN_INSTANCES = {
    "test.dbrepo.tuwien.ac.at": DBRepo,
    "dbrepo1.ec.tuwien.ac.at": DBRepo,
    "zenodo.org": InvenioRDM,
    "researchdata.tuwien.ac.at": InvenioRDM,
    "researchdata.tuwien.at": InvenioRDM,
    "test.researchdata.tuwien.at": InvenioRDM,
    "s168.dl.hpc.tuwien.ac.at": InvenioRDM,
}

DEFAULT_URLS = {
    repo: [url for url, r in KNOWN_INSTANCES.items() if r == repo][0]
    for repo in set(KNOWN_INSTANCES.values())
}


def _resolve_service(host: str, full_url: str) -> Optional[BaseWrapper]:
    """Resolve service based on known URLs."""
    # TODO maybe we could utilize re3data here, or deduce the repository type
    #      from a hint in the HTML
    return KNOWN_INSTANCES.get(host, None)


def _follow_redirects(url: str) -> str:
    """Follow HTTP redirects and returns the final URL."""
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url

    except requests.RequestException as e:
        raise ValueError(f"Following redirect for '{url}' failed: {e}")


def suggest_repository(url: str) -> Optional[BaseWrapper]:
    """Return the suggested repository system according to the URL provided.

    The returned repository wrapper isn't authenticated yet, as not all operations
    require authentication.
    If the URL doesn't provide sufficient hints to deduce a repository type,
    ``None`` will be returned.
    """
    if match := url_regex.match(url):
        scheme, rest = match.group(2) or "https", match.group(3)
        url = f"{scheme}://{rest}"
        host = urlparse(url).netloc

    else:
        raise ValueError(f"invalid url: {url}")

    # if we get a DOI, we need to resolve it
    if host == "doi.org":
        return suggest_repository(_follow_redirects(url))

    # resolve the service and return an instance
    service_cls = _resolve_service(host, url)
    if service_cls is None:
        return None

    return service_cls(f"{scheme}://{host}")


def _download(
    service: BaseWrapper, container_id: str, files: List[str] | str, interactive: bool
) -> List[str] | str:
    """Download one or more files."""
    results = []
    already_auth, single_file = False, False

    if isinstance(files, (str, int)):
        files, single_file = [files], True

    for file in files:
        try:
            dl = service.download(container_id, file)
            results.append(dl)
        except Exception as e:
            if interactive and not already_auth:
                service.authenticate_interactive()
                already_auth = True
                dl = service.download(container_id, file)
                results.append(dl)
            else:
                raise e

    return results[0] if single_file else results


def download(
    url: str, all: bool = False, interactive: bool = True
) -> List[str] | str | None:
    """Download file automatically based on the URL."""
    if (service := suggest_repository(url)) is None:
        return None

    # fish out the container & file from the URL
    cid, fid, fids = (*service.url_to_parts(url), [])
    if cid is None and fid is None:
        cid, fid = service.url_to_parts(_follow_redirects(url))

    # if we couldn't determine a file from the URL...
    if fid is None:
        avail_files = list(service.list_files(cid))
        if len(avail_files) == 1:
            fid = avail_files[0]

        elif all:
            # we either take all of them
            fids = avail_files

        elif interactive:
            # or we ask the user
            selection = 0
            for idx, file_ in enumerate(avail_files):
                print(f"{idx+1}) {file_}")

            while not (0 < selection <= len(avail_files)):
                try:
                    selection = int(input(f"Select [1-{len(avail_files)}]: "))
                except ValueError:
                    selection = 0

            fid = avail_files[selection - 1]
        else:
            # or we give up
            return None

    try:
        return _download(service, cid, fid or fids, interactive)

    finally:
        service.clear_auth()


def download_all(url: str) -> List[str] | str | None:
    """Download all files from a URL."""
    return download(url, all=True, interactive=False)


def upload(
    file_path: str, url: Optional[str] = None
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Upload the file to an auto-selected repository.

    Return a triple with the repository's URL, the container ID and the file ID.
    """
    service = None

    if url is None:
        # if no URL has been specified, base the choice on the file's content
        try:
            pd.read_csv(file_path)
            url = DEFAULT_URLS[DBRepo]
            service = DBRepo(url)

        except pd.errors.ParserError:
            url = DEFAULT_URLS[InvenioRDM]
            service = InvenioRDM(url)

    else:
        service = suggest_repository(url)

    try:
        service.authenticate_interactive()
        return url, *service.upload(file_path)

    finally:
        if service is not None:
            service.clear_auth()

    return None, None, None
