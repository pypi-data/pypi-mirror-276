"""Library for connecting VRE of TU Wien with the research data repositories."""

from .api import AutoAPI, DBRepo, InvenioRDM

__all__ = [
    AutoAPI,
    DBRepo,
    InvenioRDM,
]
