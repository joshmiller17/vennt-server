# Josh Aaron Miller 2021
# API calls for Enemies

import venntdb
import uuid
from constants import *
from api_campaigns import *
import utilities.character as character_util

# VenntHandler methods


def create_enemy(self, args, username):
    name = args[KEY_NAME]
    if len(name) > MAX_NAME_LENGTH:
        return self.respond({"success": False, "info": MSG_NAME_LONG})

    campaign_id = None
    if KEY_CAMPAIGN_ID in args:
        # automatically add the enemy to the campaign if its a valid campaign
        campaign_id = args[KEY_CAMPAIGN_ID]
        if not has_gm_permissions(self, username, campaign_id):
            return self.respond({"success": False, "info": MSG_BAD_CAMP})


    enemy = { CHAR_NAME: name }
    character_util.set_defaults(enemy, True)

    for key in args:
        if key in ATTRIBUTES:
            try:
                enemy[key] = int(args[key])
            except ValueError:
                return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})
        elif key in OPTIONAL_ATTRIBUTES:
            enemy[key] = args[key]

    if not character_util.is_valid(enemy):
        return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})

    self.server.db.create_character(username, enemy)
    ret = { "success": True, "id": enemy[CHAR_ID] }

    if campaign_id:
        self.server.db.add_to_campaign(campaign_id, username, enemy[CHAR_ID], gm_only=True)

    return self.respond(ret)


def create_enemy_post(self, json_data, args, username):
    campaign_id = None
    if KEY_CAMPAIGN_ID in args:
        # automatically add the enemy to the campaign if its a valid campaign
        campaign_id = args[KEY_CAMPAIGN_ID]
        if not has_gm_permissions(self, username, campaign_id):
            return self.respond({"success": False, "info": MSG_BAD_CAMP})

    # define some defaults if unset
    character_util.set_defaults(json_data, True)
    if not character_util.is_valid(json_data):
        return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})

    self.server.db.create_character(username, json_data)
    ret = { "success": True, "id": json_data[CHAR_ID] }

    if campaign_id:
        self.server.db.add_to_campaign(campaign_id, username, json_data[CHAR_ID], gm_only=True)
    
    return self.respond(ret)
