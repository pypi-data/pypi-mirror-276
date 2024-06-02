# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""Wrappers for repository APIs."""

from .dbrepo import DBRepo
from .inveniordm import InvenioRDM

__all__ = [
    DBRepo,
    InvenioRDM,
]
