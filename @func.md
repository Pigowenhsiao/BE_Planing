# Function Catalog

Purpose: Track reusable functions/subroutines created in this project.

## wip_analysis/config/settings.py
- `u(text)`: Decode unicode escape sequences for sheet names.

## wip_analysis/etl/read_excel.py
- `normalize_column_name(name)`: Normalize column names by trimming and collapsing whitespace.
- `apply_column_map(df, column_map)`: Rename columns using a provided mapping.
- `add_serialnumber(df, columns, serial_col="serialnumber")`: Build a serialnumber column by joining selected fields.
- `read_excel(path)`: Read all sheets and return mapped DataFrames by logical key.
- `find_excel_files(folder, pattern=None)`: Find Excel files by regex pattern in a folder.

## wip_analysis/etl/load_sqlite.py
- `ensure_dirs()`: Ensure data/input directories exist.
- `get_connection(db_path=None)`: Open a SQLite connection to the configured DB path.
- `ensure_core_tables(conn)`: Create core tables (`manual_input`, `import_history`) if missing.
- `import_excel_to_sqlite(excel_path, db_path=None)`: Import Excel sheets into SQLite (replace tables) and log history.

## wip_analysis/ui/app.py
- `load_translations(locale)`: Load i18n JSON for the selected locale.
- `load_user_config()`: Load saved UI config (e.g., excel_path).
- `save_user_config(data)`: Persist UI config to disk.
- `t(key)`: Translate UI text by key.
- `quote_ident(name)`: Quote SQLite identifiers safely.
- `fetch_df(table_name, limit=500)`: Read a table into a DataFrame with a row limit.
- `fetch_import_history(limit=200)`: Read recent import history.
- `insert_manual_input(payload)`: Insert a manual input record.

## wip_analysis/main.py
- `_ensure_sys_path()`: Ensure project root is on `sys.path` for direct script execution.
- `main()`: CLI entry point for importing Excel into SQLite.
