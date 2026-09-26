#!/usr/bin/env python3
"""Query the mock table uploaded by process.py."""

import logging
import os
import re

import mysql.connector

DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def _connect():
    """Open a connection using DBHOST, DBUSER, DBPASS, and DBNAME."""
    if not all([DBHOST, DBUSER, DBPASS, DBNAME]):
        raise mysql.connector.Error("Set DBHOST, DBUSER, DBPASS, and DBNAME before querying")
    return mysql.connector.connect(
        host=DBHOST,
        user=DBUSER,
        password=DBPASS,
        database=DBNAME,
    )


def _quote_identifier(name):
    """Return a backticked column name after rejecting anything that is not a plain identifier."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError(f"Column name is not a safe identifier: {name}")
    return f"`{name}`"


def get_data_by_group(value):
    """Return every mock row whose group column equals value.

    The filter column is `group`. That name is reserved in MySQL, so the
    SQL quotes it with backticks. The compared value is passed as %s.

    Args:
        value: Group label to match, such as "alpha".

    Returns:
        A list of row tuples, or None if the query fails.
    """
    query = "SELECT * FROM `mock` WHERE `group` = %s"
    connection = None
    cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        rows = cursor.fetchall()
        logger.info("Found %s rows where group = %s", len(rows), value)
        return rows
    except mysql.connector.Error as error:
        logger.error("Group query failed: %s", error)
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def plot_counts(groupby):
    """Count rows for each distinct value of one column.

    Args:
        groupby: Column to group by, for example "group". The name is quoted
            as an identifier. Placeholders cannot be used for column names.

    Returns:
        A list of (value, count) tuples, or None if the query fails.
    """
    column = _quote_identifier(groupby)
    # Count rows per distinct value. Column names cannot be bound with %s.
    query = f"SELECT {column}, COUNT(*) FROM `mock` GROUP BY {column}"
    connection = None
    cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor()
        cursor.execute(query)
        counts = cursor.fetchall()
        logger.info("Counted %s distinct values in %s", len(counts), groupby)
        return counts
    except (mysql.connector.Error, ValueError) as error:
        logger.error("Count query failed: %s", error)
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def main():
    """Show one group and the count of rows in each group."""
    print("=== by group ===")
    print(get_data_by_group("alpha"))

    print("=== counts ===")
    print(plot_counts("group"))


if __name__ == "__main__":
    main()
