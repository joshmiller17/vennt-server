import uuid
from constants import *
import utilities.ability as ability_util
import utilities.item as item_util

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("character")

def set_defaults(character, is_enemy=False):
    id_type = IDType.ENEMY if is_enemy else IDType.CHARACTER
    character[CHAR_ID] = id_type + str(uuid.uuid4())
    character[CHAR_IS_ENEMY] = is_enemy

    # set required attributes to 0 if unset
    for attr in ATTRIBUTES:
        if attr not in character:
            character[attr] = 0

    # Set character lists
    if CHAR_GIFT not in character:
        character[CHAR_GIFT] = "None"
    if CHAR_ABILITIES not in character:
        character[CHAR_ABILITIES] = []
    if CHAR_ITEMS not in character:
        character[CHAR_ITEMS] = []
    if CHAR_WEAPONS not in character:
        character[CHAR_WEAPONS] = []
    if CHAR_CHANGELOG not in character:
        character[CHAR_CHANGELOG] = []
    if CHAR_PATHS not in character:
        character[CHAR_PATHS] = []

    # Set random ID for all default items
    for item in character[CHAR_ITEMS]:
        item[ITEM_ID] = IDType.ITEM + str(uuid.uuid4())

def changelog_row_is_valid(row):
    req_keys = [CHANGE_ATTR, CHANGE_MSG, CHANGE_TIME]
    valid_keys = {
        CHANGE_ATTR: str,
        CHANGE_MSG: str,
        CHANGE_TIME: int,
        CHANGE_PREV: (int, float, str),
    }
    if not isinstance(row, dict):
        return False
    for key in req_keys:
        if key not in row:
            return False
    for key, val in row.items():
        if key not in valid_keys or not isinstance(val, valid_keys[key]):
            return False
    if len(row[CHANGE_MSG]) > MAX_CHANGELOG_LENGTH:
        return False
    return True

def changelog_is_valid(changelog):
    if not isinstance(changelog, list):
        return False
    if len(changelog) > MAX_CHANGELOG_LENGTH:
        return False
    return all(changelog_row_is_valid(row) for row in changelog)

def is_valid(character):
    other_req_keys = [CHAR_NAME, CHAR_ID, CHAR_GIFT, CHAR_ABILITIES, CHAR_ITEMS, CHAR_WEAPONS, CHAR_IS_ENEMY]
    for key in ATTRIBUTES + other_req_keys:
        if key not in character:
            # missing required attribute
            return False
    all_keys = ATTRIBUTES + OPTIONAL_ATTRIBUTES + other_req_keys + [CHAR_CHANGELOG, CHAR_PATHS]
    for key in character:
        if key not in all_keys:
            # includes invalid attribute
            return False
    # special checks:
    if len(character[CHAR_NAME]) > MAX_NAME_LENGTH:
        return False
    if character[CHAR_GIFT] not in GIFTS:
        return False
    if "NOTES" in character and len(character["NOTES"]) > MAX_NOTES_LENGTH:
        return False
    if CHAR_CHANGELOG in character and not changelog_is_valid(character[CHAR_CHANGELOG]):
        return False
    # check sub lists
    return (all(ability_util.is_valid(abi) for abi in character[CHAR_ABILITIES])
            and all(item_util.is_valid(it) for it in character[CHAR_ITEMS]))
