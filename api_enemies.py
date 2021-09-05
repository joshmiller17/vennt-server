# Josh Aaron Miller 2021
# API calls for Enemies

import venntdb
import uuid
from constants import *
from api_campaigns import *

# VenntHandler methods


def create_enemy(self, args, username):
    name = args[KEY_NAME]
    campaign_id = None
    if KEY_CAMPAIGN_ID in args:
        # automatically add the enemy to the campaign if its a valid campaign
        campaign_id = args[KEY_CAMPAIGN_ID]
        if not has_gm_permissions(self, username, campaign_id):
            return self.respond({"success": False, "info": MSG_BAD_CAMP})

    id = IDType.ENEMY + str(uuid.uuid4())
    enemy = {"name": name, "id": id}
    for key in args:
        if key in ATTRIBUTES:
            try:
                enemy[key] = int(args[key])
            except ValueError:
                return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})
    self.server.db.create_character(username, enemy, is_enemy=True)

    ret = {"success": True, "id": id}

    if campaign_id:
        self.server.db.add_to_campaign(campaign_id, username, id, gm_only=True)

    return self.respond(ret)
