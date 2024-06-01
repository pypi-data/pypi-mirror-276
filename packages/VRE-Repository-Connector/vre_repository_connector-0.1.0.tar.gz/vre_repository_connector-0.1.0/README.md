# VRE/Repository Connector

The VRE/Repository Connector aims to simplify the reuse of research data by offering simple interfaces for downloading and uploading data to and from virtual research environments (VREs).


## Goals

The connector library aims to decrease the impact of the "last mile problem" by streamlining the process of fetching research data from various sources and pushing it to such.

In order to keep the usage as straight-forward as possible, the provided API is kept intentionally limited and only repository-agnostic use-cases are covered.

Of course, different types and instances of repositories can exhibit particular quirks and differences in behaviour which aren't accounted for in this library.
The connector library only provides very limited support for these cases.

As is stated in the name, the library is also intended to be used in VREs (such as Jupyter Notebooks), which are a somewhat interactive medium.
Thus, some of the higher-level operations may require interactive input from the user.


## Supported repository types

Since the VRE/Repository Connector is currently in a proof of concept stage, support for repository types is very limited.
It includes:
* [InvenioRDM](https://inveniordm.docs.cern.ch/)
* [DBRepo](https://www.ifs.tuwien.ac.at/infrastructures/dbrepo/)
