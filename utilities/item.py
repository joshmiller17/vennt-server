from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("item")

def is_valid(item, allow_partial=False):
	req_keys = [ITEM_ID, ITEM_NAME, ITEM_DESC, ITEM_BULK]
	valid_keys = {
		ITEM_ID: str,
		ITEM_NAME: str,
		ITEM_DESC: str,
		ITEM_BULK: int,
		ITEM_TYPE: str,
		ITEM_COURSES: str,
		ITEM_COMMENT: str,
		ITEM_CATEGORY: str,
		ITEM_WEAPON_TYPE: str,
		ITEM_RANGE: str,
		ITEM_ATTR: str,
		ITEM_DMG: str,
		ITEM_SPECIAL: str,
		ITEM_EQUIPPED: bool,
	}
	if not allow_partial:
		for key in req_keys:
			if key not in item:
				# Missing required key
				return False
	for key, val in item.items():
		if key not in valid_keys or not isinstance(val, valid_keys[key]):
			# Has extra, invalid key or the key has an invalid type
			return False
		if valid_keys[key] == str:
			if key in [ITEM_DESC, KEY_COMMENT, ITEM_SPECIAL]:
				if len(val) > MAX_DESC_LENGTH:
					return False
			elif len(val) > MAX_NAME_LENGTH:
				return False
	return True
