MAX_REQUEST_SIZE = 10000
MAX_INVENTORY_SIZE = 100
MAX_NAME_LENGTH = 100
MAX_DESC_LENGTH = 500
MAX_ABILITY_CACHE = 100
MAX_INIT = 100
MAX_UNDO_HISTORY = 100
MAX_CHANGELOG_LENGTH = 300
MAX_NOTES_LENGTH = 10000

FULL_UUID_LEN = 37  # uuid is 36 + prefix

POST_PATHS = {
    "LOGIN_SIGNUP": "",
    "LOGIN_SIGNUP2": "/",
    "CREATE_CHARACTER": "/create_character",
    "CREATE_ENEMY": "/create_enemy",
    "CREATE_ABILITIY": "/create_ability",
    "UPDATE_ABILITY": "/update_ability",
}

PATHS = {
    "LOGOUT": "/logout",
    "CREATE_CHARACTER": "/create_character",
    "GET_ATTR": "/get_attr",
    "SET_ATTR": "/set_attr",
    "UPDATE_ATTRS": "/update_attrs",
    "CLEAR_CHANGELOG": "/clear_changelog",
    "GET_CHARACTERS": "/get_characters",
    "GET_CHARACTER": "/get_character",
    "ADD_ITEM": "/add_item",
    "VIEW_ITEMS": "/view_items",
    "REMOVE_ITEM": "/remove_item",
    "ADD_WEAPON": "/add_weapon",
    "REMOVE_WEAPON": "/remove_weapon",
    "GET_WEAPON": "/get_weapon",
    "LOOKUP_ABILITY": "/lookup_ability",
    "ADD_ABILITY": "/add_ability",
    "GET_ABILITIES": "/get_abilities",
    "GET_ABILITY": "/get_ability",
    "REMOVE_ABILITY": "/remove_abillty",
    "REFRESH_ABILITY": "/refresh_abillty",
    "UPDATE_ABILITY_COMMENT": "/update_ability_comment",
    "CREATE_ENEMY": "/create_enemy",
    "CREATE_CAMPAIGN": "/create_campaign",
    "GET_CAMPAIGNS": "/get_campaigns",
    "SEND_CAMPAIGN_INVITE": "/send_campaign_invite",
    "VIEW_CAMPAIGN_INVITES": "/view_campaign_invites",
    "ACCEPT_CAMPAIGN_INVITE": "/accept_campaign_invite",
    "DECLINE_CAMPAIGN_INVITE": "/decline_campaign_invite",
    "SET_ROLE": "/set_role",
    "GET_ROLE": "/get_role",
    "GET_CAMPAIGN": "/get_campaign",
    "ADD_TO_CAMPAIGN": "/add_to_campaign",
    "REMOVE_FROM_CAMPAIGN": "/remove_from_campaign",
    "ADD_TO_COMBAT": "/add_to_combat",
    "REMOVE_FROM_COMBAT": "/remove_from_combat",
    "START_COMBAT": "/start_combat",
    "END_COMBAT": "/end_combat",
    "UPDATE_INITIATIVE_STYLE": "/update_initiative_style",
    "END_TURN": "/end_turn",
    "COMBAT_MOVE": "/combat_move",
    "COMBAT_DELAY": "/combat_delay",
    "ATTACK": "/attack",
    "RESOLVE_ATTACK": "resolve_attack",
    "USE_ABILITY": "use_ability",
    "USE_ITEM": "use_item",
}

ATTRIBUTES = [
    "AGI", "CHA", "DEX", "INT", "PER", "SPI",
    "STR", "TEK", "WIS", "HP", "MAX_HP", "MP",
    "MAX_MP", "VIM", "MAX_VIM", "ARMOR", "INIT",
    "SPEED", "XP", "SP", "HERO", "MAX_HERO",
]

OPTIONAL_ATTRIBUTES = [
    "TEMPLATE", # Cog template
    "COG_TYPE", # Cog type
    "LEVEL", # Used when level is not determined by XP levels
    "ACC", # Used when accuracy has a special definition for a character
    "RADIUS", # Used for the size of a character
    "REACH", # Used for when a character has an unusual reach
    "NOTES", # this is for taking notes on the character
    "MAX_BULK", # this is now deprecated for using a "container" type item
]

# Need to add combat attributes here:
# actions, reactions, all of the status effects, etc

GIFTS = [
    "Alertness", "Craft", "Alacrity",
    "Finesse", "Mind", "Magic", "Rage",
    "Science", "Charm", "None"
]

KEY_AUTH = "auth_token"
KEY_ATTR = "attr"
KEY_VAL = "value"
KEY_NAME = "name"
KEY_ID = "id"
KEY_ID2 = "id2"
KEY_COURSE = "course"
KEY_CHAR = "character_id"
KEY_CAMPAIGN_ID = "campaign_id"
KEY_USERNAME = "username"
KEY_ROLE = "role"
KEY_DESC = "desc"
KEY_BULK = "bulk"
KEY_DMG = "dmg"
KEY_MODS = "mods"
KEY_ROLL = "roll"
KEY_GIFT = "gift"
KEY_STYLE = "style"
KEY_COMMENT = "comment"
KEY_MSG = "msg"

MSG_TOO_MANY_REQ = "Too many requests"
MSG_REQ_LARGE = "Request too large"
MSG_INVITE_EXISTS = "User already invited"
MSG_NAME_LONG = "Name too long"
MSG_INVALID_GIFT = "Invalid gift"
MSG_CHANGELOG_TOO_LONG = "Character changelog is too long. Clear some history first"
MSG_INVALID_ATTRIBUTE = "Invalid attribute value"
MSG_DESC_LONG = "Description too long"
MSG_NOT_INT = "Key {} should be an integer"
MSG_DID_JOIN = "User already joined this campaign"

MSG_BAD_AUTH = "Authentication invalid"
MSG_BAD_CAMP = "Invalid campaign ID"
MSG_BAD_ROLE = "Invalid role"

MSG_NO_USER = "No such user"
MSG_NO_CHAR = "No such character"
MSG_NO_ENTITY = "No such entity"
MSG_NO_ATTR = "No such attribute"
MSG_NO_ABI = "No such ability"
MSG_NO_INIT_STYLE = "No such initiative style"
MSG_NO_PERMISSION = "Invalid permissions"
MSG_NO_IMP = "Not yet implemented."

ROLE_PLAYER = "player"
ROLE_GM = "GM"
ROLE_SPECTATOR = "spectator"
ROLES = [ROLE_PLAYER, ROLE_GM, ROLE_SPECTATOR]

# traditional campaign style - Each player should use all of their actions before the next player can go (unless they choose to delay)
INIT_TRADITIONAL = "traditional"
INIT_ASYNC = "async"  # groups of players can all go at the same time
INIT_STYLES = [INIT_TRADITIONAL, INIT_ASYNC]


class IDType:

    CAMPAIGN = 'G'  # Group
    CHARACTER = 'C'
    ITEM = 'I'
    ENEMY = 'E'


class Permission:
    NONE = 0  # no access
    PUBLIC_VIEW = 1  # can view basic character info
    COMBAT = 2  # can make modifications to combat stats
    ADD = 3  # can give resources but not subtract
    PRIVATE_VIEW = 4  # can see detailed information
    EDIT = 5  # can edit all details -- UNUSED
    OWN = 6  # owner-only

CHAR_NAME = "name"
CHAR_ID = "id"
CHAR_GIFT = "gift"
CHAR_ABILITIES = "abilities"
CHAR_ITEMS = "items"
CHAR_WEAPONS = "weapons"
CHAR_IS_ENEMY = "is_enemy"
CHAR_CHANGELOG = "changelog"
CHAR_PATHS = "paths"

# Ability dictionary keys
ABI_DICT_CONTENTS = "contents"
ABI_DICT_NAME = "name"
ABI_DICT_PURCHASE = "purchase"
ABI_DICT_EXPEDITED = "expedited"
ABI_DICT_UNLOCKS = "unlocks"
ABI_DICT_PARTIAL_UNLOCKS = "partial_unlocks"
ABI_DICT_PREREQ = "prereq"
ABI_DICT_MP_COST = "mp_cost"
ABI_DICT_CAST_DL = "cast_dl"
ABI_DICT_BUILD_DC = "build_dc"
ABI_DICT_BUILD_TIME = "build_time"
ABI_DICT_COST = "cost"
ABI_DICT_ACTIVATION = "activation"
ABI_DICT_RANGE = "range"
ABI_DICT_NOT_REQ = "not_required"
ABI_DICT_FLAVOR = "flavor"
ABI_DICT_EFFECT = "effect"
ABI_DICT_PATH = "path"
ABI_DICT_SPECIAL_TYPE = "special_ability_type" # used for seperating custom abilities from default abilities
ABI_DICT_AP = "ap" # when making a cog, the AP cost of the ability
ABI_DICT_COMMENT = "comment" # used for leaving a personal comment on an ability - e.g. how many times you have used it

# Item dictionary keys
ITEM_ID = "id"
ITEM_NAME = "name"
ITEM_DESC = "desc"
ITEM_BULK = "bulk"
ITEM_TYPE = "type" # Special types used by the frontend are: "equipment", "consumable", "container", and "weapon"
ITEM_COURSES = "courses"
ITEM_COMMENT = "comment" # used for leaving a personal comment on an item

# Changelog dictionary keys
CHANGE_ATTR = "attr"
CHANGE_MSG = "msg"
CHANGE_TIME = "time" # unix timestamp of the change
CHANGE_PREV = "prev" # not required, has the previous attribute data
