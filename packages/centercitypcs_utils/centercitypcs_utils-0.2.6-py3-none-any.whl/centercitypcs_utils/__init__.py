"""
Utility Functions
"""

__version__ = "0.2.6"

from pathlib import Path

import gspread
import gspread_dataframe
import pandas as pd
import records
import sqlalchemy


def get_sql_as_df(
    database_url: str | None, query_file_name: Path, params: dict
) -> pd.DataFrame | None:
    if not database_url:
        return

    with open(query_file_name, "r") as query_file:
        query: sqlalchemy.TextClause = sqlalchemy.sql.text(query_file.read())

    with sqlalchemy.create_engine(
        database_url, max_identifier_length=128
    ).connect() as db:
        df = pd.read_sql_query(query, db, params=params)

    return df


def ps_query_to_df(
    database_url: str, query_file_name: str, params: dict = {}
) -> pd.DataFrame:
    db = records.Database(database_url, max_identifier_length=128)
    rows = db.query_file(query_file_name, **params)
    df = rows.export("df")
    db.close()
    return df


def get_google_sheet_as_df(
    spreadsheet_key: str,
    service_account: dict,
    worksheet_number: int = 0,
    **kwargs,
) -> pd.DataFrame:
    access = gspread.service_account_from_dict(service_account)
    spreadsheet = access.open_by_key(spreadsheet_key)
    sheet = spreadsheet.get_worksheet(worksheet_number)
    df = gspread_dataframe.get_as_dataframe(sheet, evaluate_formulas=True, **kwargs)

    df.dropna(axis="index", how="all", inplace=True)
    df.dropna(axis="columns", how="all", inplace=True)

    return df
