from pathlib import Path


def u(text):
    return text.encode("ascii").decode("unicode_escape")


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
DB_PATH = DATA_DIR / "local.db"
I18N_DIR = BASE_DIR / "i18n"
USER_CONFIG_PATH = DATA_DIR / "user_config.json"

DEFAULT_LOCALE = "zh-TW"
SUPPORTED_LOCALES = ["zh-TW", "en", "ja"]

EXCEL_PATTERN = r"Q3FY26\(WK3\).+_260109_Update_ rev2  0110\.xlsx"

SHEET_NAME_MAP = {
    "sheet1": "Sheet1",
    "sheet4": "Sheet4",
    "wip_summary": u("\u4ed5\u639b"),
    "wip_list": u("\u4ed5\u639b\u308a\u30ea\u30b9\u30c8"),
    "complete_count": u("\u5b8c\u6210\u6570"),
    "build_plan": "Build Plan",
    "shipping_plan": "ShippingPlan",
    "completion_after_0000": u("0\u6642\u4ee5\u964d\u306e\u5b8c\u6210\u6570"),
    "how_to": u("\u4f7f\u3044\u65b9"),
    "vs_ship": "vs ship",
}

TABLE_NAME_MAP = {
    "sheet1": "raw_sheet1",
    "wip_list": "raw_wip_list",
    "complete_count": "raw_completion_count",
    "shipping_plan": "raw_shipping_plan",
    "completion_after_0000": "manual_completion_after_0000",
    "sheet4": "extend_sheet4",
    "wip_summary": "extend_wip_summary",
    "vs_ship": "extend_vs_ship",
    "build_plan": "extend_build_plan",
}

COLUMN_MAPS = {
    "wip_list": {
        u("\u5de5\u5834"): "Factory",
        u("\u30d5\u30a1\u30df\u30ea"): "Family",
        u("\u54c1\u540d"): "Product Name",
        u("Wafer\u30ed\u30c3\u30c8"): "Wafer Lot",
        u("\u88fd\u9020\u30aa\u30fc\u30c0"): "Manufacturing Order",
        u("\u30ed\u30c3\u30c8\u756a\u53f7"): "Lot Number",
        u("\u524d\u5de5\u7a0b\u5b9f\u884c\u65e5"): "Previous Process Date",
        u("\u6700\u7d42\u66f4\u65b0\u65e5\u6642"): "Last Updated At",
        u("\u6570\u91cf"): "Quantity",
        u("\u6570\u91cf2"): "Quantity 2",
        u("\u5de5\u7a0b"): "Process",
        u("\u958b\u59cb"): "Start",
        u("Seq"): "Seq",
        u("\u539f\u4fa1\u5de5\u7a0b"): "Cost Process",
        u("\u4fdd\u7559\u7406\u7531"): "Hold Reason",
        u("\u5148\u884c\u7d50\u679c"): "Advance Result",
        u("\u5148\u884c\u7d50\u679c\u66f4\u65b0\u65e5"): "Advance Result Updated At",
        u("\u30b3\u30e1\u30f3\u30c8"): "Comment",
        u("\u51fa\u8377\u53ef\u80fd\u6642\u671f"): "Shippable Date",
        u("Wafer\u5b8c\u4e86\u65e5"): "Wafer Completed Date",
    },
    "complete_count": {
        u("\u5de5\u5834"): "Factory",
        u("\u30d5\u30a1\u30df\u30ea\u540d"): "Family Name",
        u("\u54c1\u540d"): "Product Name",
        u("\u6570\u91cf"): "Quantity",
        u("\u6570\u91cf2"): "Quantity 2",
    },
    "completion_after_0000": {
        u("\u5de5\u5834"): "Factory",
        u("\u30d5\u30a1\u30df\u30ea\u540d"): "Family Name",
        u("\u54c1\u540d"): "Product Name",
        u("\u6570\u91cf"): "Quantity",
        u("\u6570\u91cf2"): "Quantity 2",
    },
}

SERIALNUMBER_RULES = {
    "sheet1": ["ORDER_NUMBER", "LINE"],
    "wip_list": ["Manufacturing Order", "Lot Number"],
    "complete_count": ["Factory", "Family Name", "Product Name"],
    "completion_after_0000": ["Factory", "Family Name", "Product Name"],
    "shipping_plan": ["Item"],
    "sheet4": ["P/N"],
    "wip_summary": ["Product Name"],
    "vs_ship": ["Product Name"],
    "build_plan": ["P/N"],
}
