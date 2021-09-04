# Josh Aaron Miller 2021
# API calls for Initiative

import venntdb
import d20
from api_campaigns import *
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("api_initiative")

# VenntHandler methods


def entity_in_init_list(campaign, entity_id):
    for init in campaign["init"]:
        if init["entity_id"] == entity_id:
            return True
    return False


def add_entity_to_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    entity_id = args[KEY_ID]

    campaign = self.server.db.get_campaign(campaign_id)
    if campaign is None or not username in campaign["members"]:
        return self.respond({"success": False, "info": MSG_BAD_CAMP})
    role = campaign["members"][username]

    if not entity_id in campaign["entities"]:
        return self.respond({"success": False, "info": MSG_NO_ENTITY})
    entity = campaign["entities"][entity_id]

    if entity_id[0] == IDType.CHARACTER and entity_in_init_list(campaign, entity_id):
        # characters cannot go into the init list more than once a round (enemies can though)
        return self.respond({"success": False, "info": MSG_NO_PERMISSION})

    if (role == ROLE_PLAYER and entity_id[0] == IDType.CHARACTER and entity["owner"] == username and not entity["gm_only"]) or role == ROLE_GM:
        owner_username = entity["owner"]
        character = self.server.db.get_character(owner_username, entity_id)
        bonus = int(character["INIT"])
    else:
        return self.respond({"success": False, "info": MSG_NO_PERMISSION})

    response = {}
    if KEY_ROLL in args:
        try:
            roll = int(args[KEY_ROLL])
        except ValueError:
            return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})
    else:
        roll_result = d20.roll("3d6 + " + str(bonus))
        roll = roll_result.total
        response["roll_str"] = str(roll_result)

    # TODO: if the enemy is already in the campaign, ensure it has been seperated by a character
    self.server.db.add_to_combat(campaign_id, entity_id, roll, bonus)
    response["success"] = True
    return self.respond(response)


def remove_entity_from_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    entity_id = args[KEY_ID]

    campaign = self.server.db.get_campaign(campaign_id)
    if campaign is None or not username in campaign["members"]:
        return self.respond({"success": False, "info": MSG_BAD_CAMP})
    role = campaign["members"][username]

    if not entity_id in campaign["entities"] or not entity_in_init_list(campaign, entity_id):
        # the entity needs to be in the list for us to be able to remove it
        return self.respond({"success": False, "info": MSG_NO_ENTITY})
    entity = campaign["entities"][entity_id]

    if (role == ROLE_PLAYER and entity_id[0] == IDType.CHARACTER and entity["owner"] == username) or role == ROLE_GM:
        self.server.db.remove_from_combat(campaign_id, entity_id)
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})


def start_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    if has_gm_permissions(self, username, campaign_id) and self.server.db.start_combat(campaign_id):
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})


def end_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    if has_gm_permissions(self, username, campaign_id) and self.server.db.end_combat(campaign_id):
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})


def update_initiative_style(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    style = args[KEY_STYLE]
    if style not in INIT_STYLES:
        return self.respond({"success": False, "info": MSG_NO_INIT_STYLE})
    if has_gm_permissions(self, username, campaign_id):
        self.server.db.update_initiative_style(campaign_id, style)
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})


def end_turn(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    entity_id = args[KEY_ID]

    campaign = self.server.db.get_campaign(campaign_id)
    if campaign is None or not username in campaign["members"]:
        return self.respond({"success": False, "info": MSG_BAD_CAMP})
    role = campaign["members"][username]

    if not entity_id in campaign["entities"] or not entity_in_init_list(campaign, entity_id):
        # the entity needs to be in the init list in order for us to be able to end its turn!
        return self.respond({"success": False, "info": MSG_NO_ENTITY})
    entity = campaign["entities"][entity_id]

    if (role == ROLE_PLAYER and entity_id[0] == IDType.CHARACTER and entity["owner"] == username) or role == ROLE_GM:
        self.server.db.reset_actions(campaign_id, entity_id)
        self.server.db.next_turn(campaign_id)
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})
