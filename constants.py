MAX_REQUEST_SIZE = 10000
MAX_INVENTORY_SIZE = 100
MAX_NAME_LENGTH = 100
MAX_DESC_LENGTH = 500
MAX_ABILITY_CACHE = 100
MAX_INIT = 100

PATHS = {
	"GET_ATTR" : '/get_attr',
	"SET_ATTR" : '/set_attr',
	"CREATE_CHARACTER" : "/create_character",
	"CREATE_CAMPAIGN" : "/create_campaign",
	"LOGOUT" : "/logout",
	"GET_CAMPAIGNS" : "/get_campaigns",
	"GET_CHARACTERS" : "/get_characters",
	"GET_CHARACTER" : "/get_character",
	"SEND_CAMPAIGN_INVITE": "/send_campaign_invite",
	"VIEW_CAMPAIGN_INVITES": "/view_campaign_invites",
	"ACCEPT_CAMPAIGN_INVITE": "/accept_campaign_invite",
	"DECLINE_CAMPAIGN_INVITE": "/decline_campaign_invite",
	"SET_ROLE" : "/set_role",
	"GET_ROLE" : "/get_role",
	"ADD_ITEM" : "/add_item",
	"VIEW_ITEMS" : "/view_items",
	"REMOVE_ITEM" : "/remove_item",
	"ADD_WEAPON": "/add_weapon",
	"REMOVE_WEAPON": "/remove_weapon",
	"GET_WEAPON": "/get_weapon",
	"CREATE_ENEMY": "/create_enemy",
	"LOOKUP_ABILITY": "/lookup_ability",
	"ADD_TURN": "/add_turn",
	"RESET_TURN_ORDER": "/reset_turn_order",
	"NEXT_TURN": "/next_turn",
	"GET_TURN_ORDER": "/get_turn_order",
	"GET_CURRENT_TURN": "/get_current_turn",
	"ADD_ABILITY" : "/add_ability",
	"GET_ABILITIES": "/get_abilities",
	"GET_ABILITY": "/get_ability"
}

ATTRIBUTES = [
"AGI", "CHA", "DEX", "INT", "PER", "SPI",
"STR", "TEK", "WIS", "HP", "MAX_HP", "MP",
"MAX_MP", "VIM", "MAX_VIM", "ARMOR", "HERO",
"INIT", "SPEED", "XP", "SP"
]


KEY_AUTH = "auth_token"
KEY_ATTR = "attr"
KEY_VAL = "value"
KEY_NAME = "name"
KEY_ID = "id"
KEY_CAMPAIGN_ID = "campaign_id"
KEY_USERNAME = "username"
KEY_ROLE = "role"
KEY_DESC = "desc"
KEY_BULK = "bulk"
KEY_DMG = "dmg"
KEY_MODS = "mods"

MSG_BAD_AUTH = "Authentication invalid"
MSG_TOO_MANY_REQ = "Too many requests"
MSG_REQ_LARGE = "Request too large"
MSG_NO_USER = "No such user"
MSG_NO_CHAR = "No such character"
MSG_NO_ATTR = "No such attribute"
MSG_NO_ABI = "No such ability"
MSG_BAD_CAMP = "Invalid campaign ID"
MSG_INVITE_EXISTS = "User already invited"
MSG_BAD_ROLE = "Invalid role"
MSG_NAME_LONG = "Name too long"
MSG_DESC_LONG = "Description too long"
MSG_NOT_INT = "Key {} should be an integer"

ROLES = ["player","GM"]

class IDType:

	CAMPAIGN = 'G' # Group
	CHARACTER = 'C'
	ITEM = 'I'
	ENEMY = 'E'