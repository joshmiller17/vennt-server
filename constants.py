MAX_REQUEST_SIZE = 10000
MAX_INVENTORY_SIZE = 100
MAX_NAME_LENGTH = 100
MAX_DESC_LENGTH = 500
MAX_ABILITY_CACHE = 100
MAX_INIT = 100
MAX_UNDO_HISTORY = 100

FULL_UUID_LEN = 37  # uuid is 36 + prefix

PATHS = {
    "LOGOUT": "/logout",
    "CREATE_CHARACTER": "/create_character",
    "GET_ATTR": '/get_attr',
    "SET_ATTR": '/set_attr',
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
    "MAX_MP", "VIM", "MAX_VIM", "ARMOR", "HERO",
    "MAX_HERO", "INIT", "SPEED", "XP", "SP",
    "MAX_BULK"
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

MSG_TOO_MANY_REQ = "Too many requests"
MSG_REQ_LARGE = "Request too large"
MSG_INVITE_EXISTS = "User already invited"
MSG_NAME_LONG = "Name too long"
MSG_INVALID_GIFT = "Invalid gift"
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
