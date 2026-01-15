import re
from pathlib import Path
import pandas as pd
from wip_analysis.config import settings


def normalize_column_name(name):
    text = str(name).strip()
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def apply_column_map(df, column_map):
    if not column_map:
        return df
    return df.rename(columns=column_map)


def add_serialnumber(df, columns, serial_col="serialnumber"):
    if not columns:
        return df
    if not all(col in df.columns for col in columns):
        return df
    safe_df = df[columns].fillna("").astype(str)
    df[serial_col] = safe_df.agg("|".join, axis=1)
    return df


def read_excel(path):
    all_sheets = pd.read_excel(path, sheet_name=None)
    name_map = {v: k for k, v in settings.SHEET_NAME_MAP.items()}
    tables = {}

    for sheet_name, df in all_sheets.items():
        if sheet_name not in name_map:
            continue
        key = name_map[sheet_name]
        column_map = settings.COLUMN_MAPS.get(key, {})
        df = apply_column_map(df, column_map)
        df.columns = [normalize_column_name(c) for c in df.columns]
        serial_cols = settings.SERIALNUMBER_RULES.get(key)
        df = add_serialnumber(df, serial_cols)
        tables[key] = df
    return tables


def find_excel_files(folder, pattern=None):
    folder = Path(folder)
    if not folder.exists():
        return []
    regex = re.compile(pattern or settings.EXCEL_PATTERN)
    return [p for p in folder.iterdir() if p.is_file() and regex.match(p.name)]
