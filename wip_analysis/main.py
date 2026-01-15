import argparse
from pathlib import Path
import sys


def _ensure_sys_path():
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


_ensure_sys_path()

from wip_analysis.etl.load_sqlite import import_excel_to_sqlite


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", required=True, help="Path to Excel file")
    parser.add_argument("--db", default=None, help="SQLite DB path")
    args = parser.parse_args()
    summary = import_excel_to_sqlite(args.excel, args.db)
    for name, count in summary.items():
        print(f"{name}: {count}")


if __name__ == "__main__":
    main()
