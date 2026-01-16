import json

import pandas as pd
import streamlit as st

from wip_analysis.config import settings
from wip_analysis.etl.load_sqlite import get_connection, import_excel_to_sqlite
from wip_analysis.etl.read_excel import find_excel_files


def load_translations(locale):
    path = settings.I18N_DIR / f"{locale}.json"
    if not path.exists():
        path = settings.I18N_DIR / "en.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_user_config():
    path = settings.USER_CONFIG_PATH
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_user_config(data):
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.USER_CONFIG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def t(key):
    return st.session_state.get("i18n", {}).get(key, key)


def quote_ident(name):
    return '"' + name.replace('"', '""') + '"'


def fetch_df(table_name, limit=None):
    with get_connection() as conn:
        try:
            if limit is None:
                query = f"SELECT * FROM {quote_ident(table_name)}"
            else:
                query = f"SELECT * FROM {quote_ident(table_name)} LIMIT {int(limit)}"
            return pd.read_sql_query(query, conn)
        except Exception:
            return pd.DataFrame()


def fetch_import_history(limit=None):
    with get_connection() as conn:
        try:
            if limit is None:
                return pd.read_sql_query(
                    "SELECT * FROM import_history ORDER BY id DESC", conn
                )
            return pd.read_sql_query(
                "SELECT * FROM import_history ORDER BY id DESC LIMIT ?", conn, params=(limit,)
            )
        except Exception:
            return pd.DataFrame()


def list_tables():
    with get_connection() as conn:
        try:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
            return [row[0] for row in rows]
        except Exception:
            return []


def filter_df(df, column, text):
    if df.empty or not text:
        return df
    if column and column in df.columns:
        return df[df[column].astype(str).str.contains(text, case=False, na=False)]
    mask = df.astype(str).apply(
        lambda row: row.str.contains(text, case=False, na=False).any(), axis=1
    )
    return df[mask]


st.set_page_config(page_title="WIP Analysis MVP", layout="wide")

locale = st.sidebar.selectbox("Language", settings.SUPPORTED_LOCALES, index=0)
translations = load_translations(locale)
st.session_state["i18n"] = translations

st.title(t("app.title"))

user_config = load_user_config()
default_excel_path = user_config.get("excel_path", "")
if "excel_path" not in st.session_state:
    st.session_state["excel_path"] = default_excel_path

excel_files = find_excel_files(settings.INPUT_DIR, settings.EXCEL_PATTERN)
excel_options = [str(p) for p in excel_files]
if default_excel_path and default_excel_path not in excel_options:
    excel_options.insert(0, default_excel_path)

selected_excel = ""
if excel_options:
    selected_excel = st.sidebar.selectbox(t("sidebar.excel_select"), excel_options)
    if selected_excel and selected_excel != st.session_state["excel_path"]:
        st.session_state["excel_path"] = selected_excel

path_col, load_col = st.sidebar.columns([4, 1])
with path_col:
    st.text_input(t("sidebar.excel_path"), key="excel_path")
with load_col:
    if st.button(t("sidebar.load_button")):
        excel_path = st.session_state.get("excel_path", "")
        if excel_path:
            summary = import_excel_to_sqlite(excel_path)
            save_user_config({"excel_path": excel_path})
            st.sidebar.success(f"{t('label.import_result')}: {summary}")
        else:
            st.sidebar.error(t("label.no_data"))

(tab_overview, tab_query, tab_import_log) = st.tabs(
    [t("tab.overview"), t("tab.query"), t("tab.import_log")]
)

with tab_overview:
    st.subheader(t("overview.last_import"))
    hist = fetch_import_history()
    st.dataframe(hist, use_container_width=True)
    table_names = list_tables()
    if table_names:
        st.subheader("Tables")
        st.write(table_names)

with tab_query:
    st.subheader(t("query.title"))
    table_options = list_tables()
    if not table_options:
        st.info(t("query.no_tables"))
    else:
        selected_table = st.selectbox(t("query.table"), table_options)
        df = fetch_df(selected_table)
        if df.empty:
            st.info(t("query.no_data"))
        else:
            columns = [t("query.all_columns")] + list(df.columns)
            selected_column = st.selectbox(t("query.column"), columns)
            query_text = st.text_input(t("query.text"))
            col = None if selected_column == t("query.all_columns") else selected_column
            filtered = filter_df(df, col, query_text)
            st.dataframe(filtered, use_container_width=True)

with tab_import_log:
    hist = fetch_import_history()
    st.dataframe(hist, use_container_width=True)
