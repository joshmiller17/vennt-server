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

    # Set random ID for all default items
    for item in character[CHAR_ITEMS]:
        item[ITEM_ID] = IDType.ITEM + str(uuid.uuid4())

def is_valid(character):
    other_req_keys = [CHAR_NAME, CHAR_ID, CHAR_GIFT, CHAR_ABILITIES, CHAR_ITEMS, CHAR_WEAPONS, CHAR_IS_ENEMY]
    for key in ATTRIBUTES + other_req_keys:
        if key not in character:
            # missing required attribute
            return False
    all_keys = ATTRIBUTES + OPTIONAL_ATTRIBUTES + other_req_keys
    for key in character:
        if key not in all_keys:
            # includes invalid attribute
            return False
    # special checks:
    if len(character[CHAR_NAME]) > MAX_NAME_LENGTH:
        return False
    if character[CHAR_GIFT] not in GIFTS:
        return False
    # check sub lists
    return (all(ability_util.is_valid(abi) for abi in character[CHAR_ABILITIES])
            and all(item_util.is_valid(it) for it in character[CHAR_ITEMS]))
