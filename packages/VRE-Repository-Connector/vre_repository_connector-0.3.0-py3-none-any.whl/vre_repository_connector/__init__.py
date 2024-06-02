# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""Wrappers for common operations regarding research data repositories."""

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
