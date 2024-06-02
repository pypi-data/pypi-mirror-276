# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

import csv
import getpass
import json
import logging
import os
import re
import urllib.parse
from collections import Counter
from typing import Iterable, List, Optional, Tuple

import requests
from dbrepo.api.dto import (
    CreateDatabase,
    CreateTable,
    CreateTableColumn,
    CreateTableConstraints,
    DatatypeAnalysis,
)
from dbrepo.RestClient import RestClient
from pandas import concat

from ..utils import url_regex
from .base import BaseWrapper

db_tbl_regex = re.compile(r"(/api)?/database/([0-9]+)(/table/([0-9]+)(/.*)?)?")


def columns_from_analysis(analysis: DatatypeAnalysis) -> List[CreateTableColumn]:
    """Turn the datatype analysis into a list of table column definitions."""
    columns = []
    for name, col_type in analysis.columns.items():
        col = CreateTableColumn(
            name=name, type=col_type, primary_key=(name == "id"), null_allowed=False
        )
        columns.append(col)

    return columns


class DBRepo(BaseWrapper):
    """Utility class for connecting to a DBRepo instance."""

    CSV_SEPARATORS = [",", ";", "\t"]

    @classmethod
    def _guess_separator_character(cls, filename: str, max_num_lines=100) -> str:
        """Guess the character for separting values in the file.

        Estimates the separator to be the most common character out of the
        ``CSV_SEPARATORS`` list.

        Read at most ``max_num_lines`` lines from the file.
        If this value is set to a value of zero or lower, read all lines.
        """
        totals = {sep: 0 for sep in cls.CSV_SEPARATORS}
        line_count = 0
        with open(filename, "r") as f:
            while line := f.readline():
                if max_num_lines > 0 and line_count >= max_num_lines:
                    break

                counter = Counter(line)
                for sep in totals:
                    totals[sep] += counter.get(sep, 0)

                line_count += 1

        # return the most common of the separators
        return max(totals.items(), key=lambda i: i[1])[0]

    @classmethod
    def _file_to_data_dicts(cls, filename: str, separator: Optional[str] = None):
        """Parse the CSV file into data dictionaries.

        The CSV file is expected to have the columns defined in the first row.
        """
        sep = separator or cls._guess_separator_character(filename)
        columns = None

        with open(filename, "r") as f:
            reader = csv.reader(f, delimiter=sep)
            for row in reader:
                if columns is None:
                    columns = row
                else:
                    # return {col1: val1, col2: val2, col3: val3, ...} per line
                    yield dict(zip(columns, row))

    def __init__(self, url: str):
        """DBRepo constructor."""
        if match := url_regex.match(url):
            scheme, host = match.group(2) or "https", match.group(3)
            endpoint = f"{scheme}://{host}"

            logging.basicConfig(level=logging.WARNING)
            self.client = RestClient(endpoint=endpoint)

        else:
            raise ValueError(f"Invalid DBRepo URL: {url}")

    def _create_database(self, name, container_id, is_public):
        """Create the database."""
        cdb = CreateDatabase(name=name, container_id=container_id, is_public=is_public)
        response = requests.post(
            url=f"{self.client.endpoint}/api/database",
            json=json.loads(cdb.model_dump_json()),
            auth=(self.client.username, self.client.password),
        )

        return response.json()["id"]

    def _create_table(
        self, database_id: int, table_name: str, columns: List[CreateTableColumn]
    ) -> int:
        """Create the described table in the given database.

        Custom implementation of ``self.client.create_table()``.
        """
        create_table = CreateTable(
            name=table_name,
            description="description to be provided",
            columns=columns,
            constraints=CreateTableConstraints(),
        )

        # fix the payload structure
        pks = []
        data = json.loads(create_table.model_dump_json())
        for column in data["columns"]:
            if column.get("size", None) is None:
                column["size"] = 255

            if column.pop("primary_key", False):
                pks.append(column["name"])

            column.pop("index_length", None)

        data["constraints"]["primary_key"] = pks

        response = requests.post(
            url=f"{self.client.endpoint}/api/database/{database_id}/table",
            json=data,
            auth=(self.client.username, self.client.password),
        )

        return response.json()["id"]

    def _create_table_data(self, database_id: int, table_id: int, row: dict) -> None:
        """Insert row of data into the table."""
        response = requests.post(
            url=f"{self.client.endpoint}/api/database/{database_id}/table/{table_id}/data",  # noqa
            json={"data": row},
            auth=(self.client.username, self.client.password),
        )
        assert 200 <= response.status_code < 300

    def ask_credentials(self):
        """Ask the user interactively for credentials."""
        print(f"(DBRepo) Enter your credentials for '{self.client.endpoint}'")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        return {"auth_str": username, "password": password}

    def authenticate(self, auth_str, password=None):
        """Authenticate the client with a username and password.

        If only one positional argument is supplied, it is expected to be a string
        with the shape "username:password".

        Alternatively, the username can be supplied as the first positional argument
        and the password can be passed as the second positional argument or a keyword
        argument ``password``.
        """
        if password is None:
            username, password = auth_str.split(":", 1)

        else:
            username = auth_str
            password = password

        self.client.username = username
        self.client.password = password

    def clear_auth(self):
        """Clear the DBRepo client's credentials."""
        self.client.username, self.client.password = None, None

    def list_files(self, database_id: int) -> Iterable[str]:
        """List all tables by name for the container."""
        url = f"{self.client.endpoint}/api/database/{database_id}/table"
        response = requests.get(url, auth=(self.client.username, self.client.password))
        return [tbl["name"] for tbl in response.json()]

    def url_to_parts(self, url: str) -> Tuple[Optional[int], Optional[int]]:
        """Get the database ID and table ID from the URL."""
        db_id, tbl_id = None, None

        try:
            path = urllib.parse.urlparse(url).path
            match = db_tbl_regex.match(path)
            db_id, tbl_id = match.group(2), match.group(4)
        except AttributeError:
            # e.g. happens if the URL doesn't match the pattern
            pass

        return (int(db_id) if db_id else None, int(tbl_id) if tbl_id else None)

    def upload(
        self,
        file_path: str,
        database_id: Optional[int] = None,
        table_name: Optional[str] = None,
    ) -> Tuple[Optional[int], Optional[int]]:
        """Uploads a table to the specified database.

        If no database is specified, a new one will be created.
        Returns the IDs of the database and the created table.
        """
        sep = self._guess_separator_character(file_path)
        analysis = self.client.analyse_datatypes(file_path, separator=sep, upload=True)
        filename = os.path.basename(file_path)

        if database_id is None:
            # TODO find better logic than this
            container_id = min([c.id for c in self.client.get_containers()])
            database_id = self._create_database(
                filename, container_id=container_id, is_public=True
            )

        table_id = self._create_table(
            database_id, table_name or filename, columns_from_analysis(analysis)
        )

        for line_data in self._file_to_data_dicts(file_path, separator=sep):
            self._create_table_data(database_id, table_id, line_data)

        return (database_id, table_id)

    def download(self, database_id: str, table: str | int) -> Optional[str]:
        """Downloads specified table from the database.

        Returns the path to the downloaded file.
        """

        # get the required infos about the table in question
        table_id, table_name = table, table
        if isinstance(table, str):
            url = f"{self.client.endpoint}/api/database/{database_id}/table"
            response = requests.get(
                url, auth=(self.client.username, self.client.password)
            )
            matching_tables = [
                tbl["id"] for tbl in response.json() if tbl["name"] == table_id
            ]

            if matching_tables:
                table = self.client.get_table(database_id, matching_tables[0])
                table_id = table.id
            else:
                return None
        else:
            table = self.client.get_table(database_id, table)
            table_name = table.name

        # download the data chunk-wise
        data = None
        p, fetched_count = 0, 0
        data_count = self.client.get_table_data_count(database_id, table_id)
        while fetched_count < data_count:
            part = self.client.get_table_data(
                database_id, table_id, page=p, size=10000, df=True
            )
            if data is None:
                data = part
            else:
                data = concat([data, part])

            fetched_count += part.shape[0]
            p += 1

        if data is None:
            return None

        # write the dataframe to a CSV file, with the columns in the same order
        # as they were uploaded, and without index column
        name = f"{table_name}.csv"
        data.to_csv(name, index=False, columns=[c.name for c in table.columns])
        return name
