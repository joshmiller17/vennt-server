# Josh Aaron Miller 2021
# API calls for Initiative

import venntdb
from constants import *
from api_campaigns import has_campaign_permissions
from api_combat import has_permissions

# VenntHandler methods


def add_entity_to_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    entity_id = args[KEY_ID]
    roll = int(args[KEY_ROLL])

    campaign = self.server.db.get_campaign(campaign_id)
    role = campaign["members"][username]

    entity = campaign["entities"][entity_id]
    if not entity:
        return self.respond({"success": False, "info": MSG_NO_ENTITY})

    if entity_id[0] == IDType.CHARACTER and len(list(filter(lambda init: init["entity_id"] == entity_id, campaign["init"]))) > 0:
        # characters cannot go into the init list more than once a round (enemies can though)
        return self.respond({"success": False, "info": MSG_NO_PERMISSION})

    if (role == ROLE_PLAYER and entity_id[0] == IDType.CHARACTER and entity["owner"] == username and not entity["gm_only"]) or role == ROLE_GM:
        owner_username = entity["owner"]
        character = self.server.db.get_character(owner_username, entity_id)
        bonus = int(character["init"])
    else:
        return self.respond({"success": False, "info": MSG_NO_PERMISSION})

    self.server.db.add_to_combat(campaign_id, entity_id, roll, bonus)
    return self.respond({"success": True})


def remove_entity_from_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    entity_id = args[KEY_ID]

    campaign = self.server.db.get_campaign(campaign_id)
    role = campaign["members"][username]

    entity = campaign["entities"][entity_id]
    if not entity or not len(list(filter(lambda init: init["entity_id"] == entity_id, campaign["init"]))) > 0:
        # the entity needs to be in the list for us to be able to remove it
        return self.respond({"success": False, "info": MSG_NO_ENTITY})

    if (role == ROLE_PLAYER and entity_id[0] == IDType.CHARACTER and entity["owner"] == username) or role == ROLE_GM:
        self.server.db.remove_from_combat(campaign_id, entity_id)
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})


def start_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    campaign = self.server.db.get_campaign(campaign_id)
    role = campaign["members"][username]

    if role == ROLE_GM and self.server.db.start_combat(campaign_id):
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})


def end_combat(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]
    campaign = self.server.db.get_campaign(campaign_id)
    role = campaign["members"][username]

    if role == ROLE_GM and self.server.db.end_combat(campaign_id):
        return self.respond({"success": True})

    return self.respond({"success": False, "info": MSG_NO_PERMISSION})
