# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

import re

doi_regex = re.compile(r"^((https?://)?doi.org/)?(10\.\d+)/(.*)$")
url_regex = re.compile(r"^((.*?)://)?(.*)$")
