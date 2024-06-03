# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""Utility functions."""

import pathlib
import re
import tempfile
from typing import Optional

doi_regex = re.compile(r"^((https?://)?doi.org/)?(10\.\d+)/(.*)$")
url_regex = re.compile(r"^((.*?)://)?(.*)$")

_tempdir = tempfile.mkdtemp()
"""Randomly named temporary directory, fixed for the duration of the run.

The outcome can be influenced by setting ``tempfile.tempdir`` before first use.
"""


def create_download_file(
    container_id: str | int, file_name: str, dir: Optional[str] = None
) -> str:
    """Create a file for storing downloaded content."""
    cid = str(container_id)
    dir = pathlib.Path(dir or _tempdir) / cid
    dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    file_path = dir / file_name
    file_path.touch(0o700)
    return str(file_path)
