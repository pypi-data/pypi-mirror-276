# -*- coding: utf-8 -*-#
from .wx_info import BiasAddr, read_info, get_wechat_db, batch_decrypt, decrypt, get_core_db
import os, json

try:
    VERSION_LIST_PATH = os.path.join(os.path.dirname(__file__), "version_list.json")
    with open(VERSION_LIST_PATH, "r", encoding="utf-8") as f:
        VERSION_LIST = json.load(f)
except:
    VERSION_LIST = {}
    VERSION_LIST_PATH = None

__version__ = "3.0.26"