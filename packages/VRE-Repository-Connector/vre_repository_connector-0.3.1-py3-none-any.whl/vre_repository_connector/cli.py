# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#

"""CLI commands for the VRE Repository Connector."""

import sys
import urllib.parse

import click

from .auto import download, suggest_repository


@click.group()
def connector():
    """CLI commands for the VRE Repository Connector."""


@connector.command("download")
@click.argument("url")
@click.option(
    "--all",
    "-a",
    default=False,
    is_flag=True,
    help="Download all files (overrides interactivity)",
)
@click.option(
    "--select-interactive/--non-interactive",
    "-i/-I",
    default=True,
    help="Select the files to download interactively",
)
def download_files(url: str, all: bool, select_interactive: bool):
    """Download the files from the given URL."""
    if (repo := suggest_repository(url)) is None:
        click.secho("Couldn't deduce a repository from the URL!", fg="red", err=True)

    repo_type, host = type(repo).__name__, urllib.parse.urlparse(repo.base_url).netloc
    click.echo(f"Downloading from {repo_type} @ {host}")
    files = download(url, all=all, interactive=select_interactive)
    if files is None:
        click.secho("No files downloaded.", fg="red", err=True)
        sys.exit(1)

    if isinstance(files, str):
        files = [files]

    for f in files:
        click.echo(f)
