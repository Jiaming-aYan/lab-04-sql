#!/usr/bin/env python3
"""Read MOCK_DATA.csv, drop incomplete rows, and load the rest into MySQL."""

import logging
import os
from pathlib import Path

import mysql.connector
import pandas as pd

# Connection settings come from the environment, same as the lab setup.
DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

# pandas dtypes from read_csv, mapped to MySQL column types.
type_mapping = {
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "datetime64[us]": "DATETIME",
    "object": "VARCHAR(255)",
    "string": "VARCHAR(255)",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def read_data(filename):
    """Load a CSV file into a pandas DataFrame.

    Args:
        filename: CSV path. A bare name is also checked at the repo root,
            because this script lives in src/sql_lab/.

    Returns:
        The loaded DataFrame.
    """
    path = Path(filename)
    if not path.is_file():
        # Running from src/sql_lab/ still finds MOCK_DATA.csv next to README.md.
        path = Path(__file__).resolve().parents[2] / filename

    data = pd.read_csv(path)
    logger.info("Read %s rows from %s", len(data), path)
    logger.info("Column dtypes: %s", data.dtypes.to_dict())
    return data


def clean_data(data):
    """Drop rows that contain any missing value.

    Args:
        data: DataFrame returned by read_data.

    Returns:
        A copy of the DataFrame with incomplete rows removed.
    """
    before = len(data)
    # Mockaroo blanks become NaN; those rows cannot be inserted cleanly.
    cleaned = data.dropna().copy()
    logger.info("Removed %s rows with missing values; %s remain", before - len(cleaned), len(cleaned))
    return cleaned


def load_data(data, table):
    """Create the destination table if needed and insert each row.

    Args:
        data: Cleaned DataFrame to upload.
        table: Destination table name. The lab expects "mock".

    Returns:
        Number of rows inserted, or None if the upload fails.
    """
    if not all([DBHOST, DBUSER, DBPASS, DBNAME]):
        logger.error("Set DBHOST, DBUSER, DBPASS, and DBNAME before uploading")
        return None

    columns = list(data.columns)
    # Identifiers are quoted; row values stay in the %s placeholders below.
    column_sql = ", ".join(f"`{column}`" for column in columns)
    column_defs = []
    for column in columns:
        dtype_name = str(data[column].dtype)
        sql_type = type_mapping.get(dtype_name, "VARCHAR(255)")
        column_defs.append(f"`{column}` {sql_type}")

    create_sql = f"CREATE TABLE IF NOT EXISTS `{table}` ({', '.join(column_defs)})"
    placeholders = ", ".join(["%s"] * len(columns))
    insert_sql = f"INSERT INTO `{table}` ({column_sql}) VALUES ({placeholders})"

    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DBHOST,
            user=DBUSER,
            password=DBPASS,
            database=DBNAME,
        )
        cursor = connection.cursor()
        cursor.execute(create_sql)
        # A second run should replace the previous upload, not append duplicates.
        cursor.execute(f"DELETE FROM `{table}`")

        inserted = 0
        for row in data.itertuples(index=False, name=None):
            values = []
            for value in row:
                if isinstance(value, pd.Timestamp):
                    values.append(value.to_pydatetime())
                elif hasattr(value, "item"):
                    values.append(value.item())
                else:
                    values.append(value)
            cursor.execute(insert_sql, tuple(values))
            inserted += 1

        connection.commit()
        logger.info("Inserted %s rows into %s.%s", inserted, DBNAME, table)
        return inserted
    except mysql.connector.Error as error:
        logger.error("Upload failed: %s", error)
        if connection is not None:
            connection.rollback()
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def main():
    """Read the CSV, drop incomplete rows, and upload the rest to mock."""
    data = read_data("MOCK_DATA.csv")
    cleaned = clean_data(data)
    load_data(cleaned, "mock")


if __name__ == "__main__":
    main()
