from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("item")

def is_valid(item):
	req_keys = [ITEM_ID, ITEM_NAME, ITEM_DESC, ITEM_BULK]
	valid_keys = {
		ITEM_ID: str,
		ITEM_NAME: str,
		ITEM_DESC: str,
		ITEM_BULK: int,
		ITEM_TYPE: str,
		ITEM_COURSES: str,
		ITEM_COMMENT: str,
	}
	for key in req_keys:
		if key not in item:
			# Missing required key
			return False
	for key, val in item.items():
		if key not in valid_keys:
			# Has extra, invalud key
			return False
		if not isinstance(val, valid_keys[key]):
			# valid key, but invalid type
			return False
	return True
