import sqlite3
from datetime import datetime

from wip_analysis.config import settings
from wip_analysis.etl.read_excel import read_excel


def ensure_dirs():
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_connection(db_path=None):
    ensure_dirs()
    return sqlite3.connect(str(db_path or settings.DB_PATH))


def ensure_core_tables(conn):
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS import_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imported_at TEXT,
            source_file TEXT,
            table_name TEXT,
            row_count INTEGER
        )
        '''
    )
    conn.commit()


def import_excel_to_sqlite(excel_path, db_path=None):
    tables = read_excel(excel_path)
    summary = {}
    with get_connection(db_path) as conn:
        ensure_core_tables(conn)
        for table_name, df in tables.items():
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            summary[table_name] = len(df)
        imported_at = datetime.utcnow().isoformat()
        for table_name, row_count in summary.items():
            conn.execute(
                "INSERT INTO import_history (imported_at, source_file, table_name, row_count) VALUES (?, ?, ?, ?)",
                (imported_at, str(excel_path), table_name, row_count),
            )
        conn.commit()
    return summary
