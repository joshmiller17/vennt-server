MAX_REQUEST_SIZE = 10000

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
}


KEY_AUTH = "auth_token"
KEY_ATTR = "attr"
KEY_VAL = "value"
KEY_NAME = "name"
KEY_ID = "id"
KEY_USERNAME = "username"
KEY_ROLE = "role"

MSG_BAD_AUTH = "Authentication invalid"
MSG_TOO_MANY_REQ = "Too many requests"
MSG_REQ_LARGE = "Request too large"
MSG_NO_USER = "No such user"
MSG_BAD_CAMP = "Invalid campaign ID"
MSG_INVITE_EXISTS = "User already invited"
MSG_BAD_ROLE = "Invalid role"

ROLES = ["player","GM"]