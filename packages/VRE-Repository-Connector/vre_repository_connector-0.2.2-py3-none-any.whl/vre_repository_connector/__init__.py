"""Library for connecting VRE of TU Wien with the research data repositories."""

from .api import DBRepo, InvenioRDM
from .auto import download, download_all, suggest_repository, upload

__all__ = [
    DBRepo,
    InvenioRDM,
    download,
    download_all,
    suggest_repository,
    upload,
]
