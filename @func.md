# Function Catalog

Purpose: Track reusable functions/subroutines created in this project.

## wip_analysis/config/settings.py
- `u(text)`: Decode unicode escape sequences for sheet names.

## wip_analysis/etl/read_excel.py
- `normalize_header(value)`: Normalize header text by trimming and collapsing whitespace.
- `has_value(value)`: Check if a cell value should be treated as non-empty.
- `translate_header(header)`: Translate headers with the predefined mapping.
- `make_unique_headers(headers)`: Add -1/-2 suffixes for duplicate headers.
- `build_headers(raw_headers, translate, sheet_name, mapping_entries)`: Build final headers and collect field mappings.
- `add_serialnumber(df, columns, serial_col="serialnumber")`: Build a serialnumber column by joining selected fields.
- `forward_fill(values)`: Forward-fill header values for merged header rows.
- `is_summary_row(values)`: Detect subtotal/total rows to skip.
- `read_simple_sheet(wb, sheet_name, header_row, data_start_row, translate, mapping_entries)`: Read a sheet using a single header row.
- `read_shipping_plan(wb, mapping_entries)`: Read ShippingPlan with a two-row merged header.
- `read_build_plan(wb, mapping_entries)`: Read Build Plan into Mapping_Table and Build+Plan.
- `build_field_mapping(entries)`: Build the Field_Mapping table from header translations.
- `read_excel(path)`: Read all required sheets and return DataFrames keyed by table name.
- `find_excel_files(folder, pattern=None)`: Find Excel files by regex pattern in a folder.

## wip_analysis/etl/load_sqlite.py
- `ensure_dirs()`: Ensure data/input directories exist.
- `get_connection(db_path=None)`: Open a SQLite connection to the configured DB path.
- `ensure_core_tables(conn)`: Create core tables (`import_history`) if missing.
- `import_excel_to_sqlite(excel_path, db_path=None)`: Import Excel tables into SQLite (replace tables) and log history.

## wip_analysis/ui/app.py
- `load_translations(locale)`: Load i18n JSON for the selected locale.
- `load_user_config()`: Load saved UI config (e.g., excel_path).
- `save_user_config(data)`: Persist UI config to disk.
- `t(key)`: Translate UI text by key.
- `quote_ident(name)`: Quote SQLite identifiers safely.
- `fetch_df(table_name, limit=None)`: Read a table into a DataFrame with an optional row limit.
- `fetch_import_history(limit=None)`: Read import history with an optional row limit.
- `list_tables()`: List available SQLite tables.
- `filter_df(df, column, text)`: Filter a DataFrame by search text and optional column.

## wip_analysis/main.py
- `_ensure_sys_path()`: Ensure project root is on `sys.path` for direct script execution.
- `main()`: CLI entry point for importing Excel into SQLite.
