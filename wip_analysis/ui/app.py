import json
from datetime import datetime

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


def fetch_df(table_name, limit=500):
    with get_connection() as conn:
        try:
            query = f"SELECT * FROM {quote_ident(table_name)} LIMIT {int(limit)}"
            return pd.read_sql_query(query, conn)
        except Exception:
            return pd.DataFrame()


def fetch_import_history(limit=200):
    with get_connection() as conn:
        try:
            return pd.read_sql_query(
                "SELECT * FROM import_history ORDER BY id DESC LIMIT ?", conn, params=(limit,)
            )
        except Exception:
            return pd.DataFrame()


def insert_manual_input(payload):
    with get_connection() as conn:
        conn.execute(
            '''
            INSERT INTO manual_input (
                serialnumber, input_date, site, input_type, quantity, note,
                created_by, created_at, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                payload.get("serialnumber"),
                payload.get("input_date"),
                payload.get("site"),
                payload.get("input_type"),
                payload.get("quantity"),
                payload.get("note"),
                payload.get("created_by"),
                payload.get("created_at"),
                payload.get("source"),
            ),
        )
        conn.commit()


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

row_limit = st.sidebar.number_input(t("label.row_limit"), min_value=50, max_value=5000, value=500, step=50)

(tab_overview,
 tab_raw_sheet1,
 tab_raw_wip_list,
 tab_raw_complete,
 tab_raw_shipping,
 tab_manual,
 tab_extend_sheet4,
 tab_extend_wip,
 tab_extend_vs_ship,
 tab_extend_build,
 tab_settings,
 tab_import_log) = st.tabs([
    t("tab.overview"),
    t("tab.raw_sheet1"),
    t("tab.raw_wip_list"),
    t("tab.raw_complete_count"),
    t("tab.raw_shipping_plan"),
    t("tab.manual_input"),
    t("tab.extend_sheet4"),
    t("tab.extend_wip_summary"),
    t("tab.extend_vs_ship"),
    t("tab.extend_build_plan"),
    t("tab.settings"),
    t("tab.import_log"),
])

with tab_overview:
    st.subheader(t("overview.last_import"))
    hist = fetch_import_history(limit=20)
    st.dataframe(hist, use_container_width=True)

with tab_raw_sheet1:
    df = fetch_df("raw_sheet1", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_raw_wip_list:
    df = fetch_df("raw_wip_list", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_raw_complete:
    df = fetch_df("raw_completion_count", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_raw_shipping:
    df = fetch_df("raw_shipping_plan", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_manual:
    st.subheader(t("manual.form.title"))
    with st.form("manual_input_form"):
        serialnumber = st.text_input(t("manual.form.serialnumber"))
        input_date = st.date_input(t("manual.form.date"))
        site = st.text_input(t("manual.form.site"))
        input_type = st.text_input(t("manual.form.type"))
        quantity = st.number_input(t("manual.form.quantity"), value=0.0, step=1.0)
        note = st.text_input(t("manual.form.note"))
        created_by = st.text_input(t("manual.form.user"))
        submitted = st.form_submit_button(t("manual.form.submit"))
        if submitted:
            payload = {
                "serialnumber": serialnumber,
                "input_date": input_date.isoformat(),
                "site": site,
                "input_type": input_type,
                "quantity": quantity,
                "note": note,
                "created_by": created_by,
                "created_at": datetime.utcnow().isoformat(),
                "source": "ui",
            }
            insert_manual_input(payload)
            st.success(t("manual.form.success"))

    st.subheader("Manual: Excel Import")
    df_excel = fetch_df("manual_completion_after_0000", row_limit)
    st.dataframe(df_excel, use_container_width=True)

    st.subheader("Manual: UI Input")
    df_ui = fetch_df("manual_input", row_limit)
    st.dataframe(df_ui, use_container_width=True)

with tab_extend_sheet4:
    df = fetch_df("extend_sheet4", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_extend_wip:
    df = fetch_df("extend_wip_summary", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_extend_vs_ship:
    df = fetch_df("extend_vs_ship", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_extend_build:
    df = fetch_df("extend_build_plan", row_limit)
    st.dataframe(df, use_container_width=True)

with tab_settings:
    st.subheader("Serialnumber Rules")
    st.json(settings.SERIALNUMBER_RULES)
    st.subheader("Column Maps")
    st.json(settings.COLUMN_MAPS)

with tab_import_log:
    hist = fetch_import_history(limit=200)
    st.dataframe(hist, use_container_width=True)
