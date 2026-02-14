"""
traconisdanilo_sqlite_civic_event.py

Purpose:
- Build a small SQLite database from civic_event CSV files.
- Run SQL queries from files and print results (like the DuckDB example).
"""

import logging
from pathlib import Path
import sqlite3
from typing import Final

from datafun_toolkit.logger import get_logger, log_header
import pandas as pd

LOG: logging.Logger = get_logger("P05", level="DEBUG")

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data" / "civic_event"
SQL_DIR: Final[Path] = ROOT_DIR / "sql" / "sqlite"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts" / "sqlite"
DB_PATH: Final[Path] = ARTIFACTS_DIR / "civic_event.sqlite"

EVENT_CSV: Final[Path] = DATA_DIR / "civic_event.csv"
ATTENDANCE_CSV: Final[Path] = DATA_DIR / "attendance.csv"


def read_sql(sql_path: Path) -> str:
    return sql_path.read_text(encoding="utf-8")


def run_sql_script(con: sqlite3.Connection, sql_path: Path) -> None:
    LOG.info(f"RUN SQL script: {sql_path}")
    con.executescript(read_sql(sql_path))
    LOG.info(f"DONE SQL script: {sql_path}")


def run_sql_query(con: sqlite3.Connection, sql_path: Path) -> None:
    LOG.info("")
    LOG.info(f"RUN SQL query: {sql_path}")

    cur = con.cursor()
    cur.execute(read_sql(sql_path))

    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    LOG.info("====================================")
    LOG.info(sql_path.name)
    LOG.info("====================================")
    LOG.info(", ".join(columns))

    for row in rows:
        LOG.info(", ".join(str(v) for v in row))


def load_data(con: sqlite3.Connection) -> None:
    # Load parent first
    event_df = pd.read_csv(EVENT_CSV)
    event_df.to_sql("civic_event", con, if_exists="append", index=False)

    # Load child second
    attendance_df = pd.read_csv(ATTENDANCE_CSV)
    attendance_df.to_sql("attendance", con, if_exists="append", index=False)


def main() -> None:
    log_header(LOG, "P05 Civic Event Pipeline (SQLite)")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(DB_PATH)

    try:
        # 1) Clean
        run_sql_script(con, SQL_DIR / "traconisdanilo_civic_event_clean.sql")

        # 2) Bootstrap (create tables)
        run_sql_script(con, SQL_DIR / "traconisdanilo_civic_event_bootstrap.sql")

        # 3) Load data
        load_data(con)
        con.commit()

        # 4) Queries
        run_sql_query(con, SQL_DIR / "traconisdanilo_civic_event_query_event_count.sql")
        run_sql_query(
            con, SQL_DIR / "traconisdanilo_civic_event_query_attendance_count.sql"
        )
        run_sql_query(
            con, SQL_DIR / "traconisdanilo_civic_event_query_attendance_aggregate.sql"
        )
        run_sql_query(
            con, SQL_DIR / "traconisdanilo_civic_event_query_attendance_by_type.sql"
        )
        run_sql_query(
            con, SQL_DIR / "traconisdanilo_civic_event_query_kpi_contributions.sql"
        )

    finally:
        con.close()

    LOG.info("END main()")


if __name__ == "__main__":
    main()
