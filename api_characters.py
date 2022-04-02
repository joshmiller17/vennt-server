# Josh Aaron Miller 2021
# API calls for Characters

import venntdb
import uuid
from constants import *
import utilities.character as character_util

# VenntHandler methods


def get_characters(self, args, username):
    return self.respond({"success": True, "value": self.server.db.get_characters(username)})


def get_character(self, args, username):
    return self.respond({"success": True, "value": self.server.db.get_character(username, args[KEY_ID])})


def create_character(self, args, username):
    name = args[KEY_NAME]
    if len(name) > MAX_NAME_LENGTH:
        return self.respond({"success": False, "info": MSG_NAME_LONG})

    if KEY_GIFT not in args:
        args[KEY_GIFT] = "None"
    elif args[KEY_GIFT] not in GIFTS:
        return self.respond({"success": False, "info": MSG_INVALID_GIFT})

    character = { CHAR_NAME: name, CHAR_GIFT: args[KEY_GIFT] }
    character_util.set_defaults(character)

    for key in args:
        if key in ATTRIBUTES:
            try:
                character[key] = int(args[key])
            except ValueError:
                return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})
        elif key in OPTIONAL_ATTRIBUTES:
            character[key] = args[key]

    if not character_util.is_valid(character):
        return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})
    self.server.db.create_character(username, character)

    ret = { "success": True, "id": character[CHAR_ID] }
    return self.respond(ret)


def create_character_post(self, json_data, username):
    # define some defaults if unset
    character_util.set_defaults(json_data)
    if not character_util.is_valid(json_data):
        return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})

    self.server.db.create_character(username, json_data)

    ret = { "success": True, "id": json_data[CHAR_ID] }
    return self.respond(ret)
    

def set_attr(self, args, username):
    char_id = args[KEY_ID]
    attr = args[KEY_ATTR]
    try:
        val = int(args[KEY_VAL])
    except ValueError:
        return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})

    if attr not in ATTRIBUTES:
        return self.respond({"success": False, "info": MSG_NO_ATTR})

    if not self.server.db.character_exists(username, char_id):
        return self.respond({"success": False, "info": MSG_NO_CHAR})

    self.server.db.set_attr(username, char_id, attr, val)
    return self.respond({"success": True})


def get_attr(self, args, username):
    char_id = args[KEY_ID]
    attr = args[KEY_ATTR]

    if attr not in ATTRIBUTES:
        return self.respond({"success": False, "info": MSG_NO_ATTR})

    if not self.server.db.character_exists(username, char_id):
        return self.respond({"success": False, "info": MSG_NO_CHAR})

    val = self.server.db.get_attr(username, char_id, attr)
    return self.respond({"success": True, "value": val})
