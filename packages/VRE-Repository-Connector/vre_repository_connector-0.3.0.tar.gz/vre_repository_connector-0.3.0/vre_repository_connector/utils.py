# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""Utility functions."""

import re

doi_regex = re.compile(r"^((https?://)?doi.org/)?(10\.\d+)/(.*)$")
url_regex = re.compile(r"^((.*?)://)?(.*)$")
