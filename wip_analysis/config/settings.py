from pathlib import Path


def u(text):
    if "\\u" in text:
        return text.encode("ascii").decode("unicode_escape")
    return text


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
DB_PATH = DATA_DIR / "local.db"
I18N_DIR = BASE_DIR / "i18n"
USER_CONFIG_PATH = DATA_DIR / "user_config.json"

DEFAULT_LOCALE = "zh-TW"
SUPPORTED_LOCALES = ["zh-TW", "en", "ja"]

EXCEL_PATTERN = r"Q3FY26\(WK3\).+_260109_Update_ rev2  0110\.xlsx"

SHEET_NAMES = {
    "WIP_Raw_data": "Sheet1",
    "WIP_Raw_DATE": u("\u4ed5\u639b\u308a\u30ea\u30b9\u30c8"),
    "Complete_WIP": u("\u5b8c\u6210\u6570"),
    "Extra_Completed_WIP": u("0\u6642\u4ee5\u964d\u306e\u5b8c\u6210\u6570"),
    "Shipping_Plan": "ShippingPlan",
    "Build_Plan": "Build Plan",
}

SERIALNUMBER_RULES = {
    "WIP_Raw_data": ["ORDER_NUMBER", "LINE"],
    "WIP_Raw_DATE": ["Manufacturing Order", "Lot Number"],
    "Complete_WIP": ["Factory", "Family Name", "Product Name"],
    "Extra_Completed_WIP": ["Factory", "Family Name", "Product Name"],
    "Shipping_Plan": ["Item"],
    "Mapping_Table": ["Classification 1", "Classification 2", "Production Site"],
    "Build+Plan": ["P/N"],
}

FIELD_TRANSLATIONS = {
    u("\u5de5\u5834"): "Factory",
    u("\u30d5\u30a1\u30df\u30ea"): "Family",
    u("\u30d5\u30a1\u30df\u30ea\u540d"): "Family Name",
    u("\u54c1\u540d"): "Product Name",
    u("Wafer\u30ed\u30c3\u30c8"): "Wafer Lot",
    u("\u88fd\u9020\u30aa\u30fc\u30c0"): "Manufacturing Order",
    u("\u30ed\u30c3\u30c8\u756a\u53f7"): "Lot Number",
    u("\u524d\u5de5\u7a0b\u5b9f\u884c\u65e5"): "Previous Process Date",
    u("\u6700\u7d42\u66f4\u65b0\u65e5\u6642"): "Last Updated At",
    u("\u6570\u91cf"): "Quantity",
    u("\u6570\u91cf2"): "Quantity 2",
    u("\u6570\u91cf\uff12"): "Quantity 2",
    u("\u5de5\u7a0b"): "Process",
    u("\u958b\u59cb"): "Start",
    u("\u539f\u4fa1\u5de5\u7a0b"): "Cost Process",
    u("\u4fdd\u7559\u7406\u7531"): "Hold Reason",
    u("\u5148\u884c\u7d50\u679c"): "Advance Result",
    u("\u5148\u884c\u7d50\u679c\u66f4\u65b0\u65e5"): "Advance Result Updated At",
    u("\u30b3\u30e1\u30f3\u30c8"): "Comment",
    u("\u51fa\u8377\u53ef\u80fd\u6642\u671f"): "Shippable Date",
    u("Wafer\u5b8c\u4e86\u65e5"): "Wafer Completed Date",
}
