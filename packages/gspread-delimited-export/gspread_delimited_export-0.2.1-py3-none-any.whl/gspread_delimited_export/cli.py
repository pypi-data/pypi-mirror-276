#!/usr/bin/env python
"""
cli.py - generate the CLI
"""

import json

import click
import gspread
from gspread_dataframe import get_as_dataframe


@click.command()
@click.option(
    "-c",
    "--credentials",
    envvar="SERVICE_ACCOUNT",
    required=True,
    help="Google service account JSON string value, typically provided by the SERVICE_ACCOUNT enviroment variable",
)
@click.option("-k", "--key", required=True, help="Google spreadsheet key id")
@click.option("-w", "--worksheet", required=True, help="Worksheet tab name")
@click.option(
    "-t",
    "--type",
    type=click.Choice(["csv", "tsv"]),
    required=True,
    default="csv",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    type=click.File("wb"),
    required=True,
    help='Output file ("-" for stdout)',
)
def cli(credentials, key, worksheet, type, output):
    gc = (
        gspread.service_account_from_dict(  # pyright: ignore [reportPrivateImportUsage]
            json.loads(credentials)
        )
    )
    sh = gc.open_by_key(key)
    ws = sh.worksheet(worksheet)

    df = get_as_dataframe(ws, evaluate_formulas=True, dtype=str, dialect="excel")
    df.dropna(axis="index", how="all", inplace=True)
    df.dropna(axis="columns", how="all", inplace=False)

    # normalize column names
    df.columns = ["_".join(header.split()).lower() for header in list(df.columns)]

    if type == "tsv":
        df.to_csv(output, index=False, sep="\t")
    else:
        output = df.to_csv(output, index=False)


if __name__ == "__main__":
    cli()
