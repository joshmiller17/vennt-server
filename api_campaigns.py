# Josh Aaron Miller 2021
# API calls for Campaigns

import venntdb
import uuid
from constants import *

# VenntHandler methods


def has_campaign_permissions(self, username, campaign_id, owner_only=False):
    campaign = self.server.db.get_campaign(campaign_id)
    if campaign is None:
        return False
    if owner_only:
        return campaign["owner"] == username
    return username in campaign["members"].keys()


def get_campaigns(self, args, username):
    return self.respond({"success": True, "value": self.server.db.get_campaigns(username)})


def create_campaign(self, args, username):
    name = args[KEY_NAME]
    id = IDType.CAMPAIGN + str(uuid.uuid4())
    self.server.db.create_campaign(username, id, name)

    ret = {"success": True, "campaign_id": id}
    return self.respond(ret)


def send_campaign_invite(self, args, username):
    user_to = args[KEY_USERNAME]
    user_from = username
    campaign_id = args[KEY_CAMPAIGN_ID]

    if not has_campaign_permissions(self, user_from, campaign_id, owner_only=True):
        return self.respond({"success": False, "info": MSG_BAD_CAMP})

    if has_campaign_permissions(self, user_to, campaign_id):
        return self.respond({"success": False, "info": MSG_DID_JOIN})

    if not self.server.db.is_valid("accounts", user_to):
        return self.respond({"success": False, "info": MSG_NO_USER})

    success = self.server.db.send_campaign_invite(
        user_from, user_to, campaign_id)

    if not success:
        return self.respond({"success": False, "info": MSG_INVITE_EXISTS})

    return self.respond({"success": success})


def accept_campaign_invite(self, args, username):
    invites = self.server.db.get_campaign_invites(username)
    campaign_id = args[KEY_CAMPAIGN_ID]

    campaign_owner = None
    for inv in invites:
        if campaign_id == inv["id"]:
            campaign_owner = inv["from"]
    if campaign_owner is None:
        return self.respond({"success": False, "info": MSG_BAD_CAMP})

    # Clear campaign invite even if adding the user fails
    self.server.db.remove_campaign_invite(username, campaign_id)

    if self.server.db.is_valid("campaigns", campaign_id, "members", username):
        return self.respond({"success": False, "info": MSG_DID_JOIN})

    self.server.db.add_user_to_campaign(username, campaign_id)

    return self.respond({"success": True})


def decline_campaign_invite(self, args, username):
    invites = self.server.db.get_campaign_invites(username)
    campaign_id = args[KEY_CAMPAIGN_ID]

    campaign_owner = None
    for inv in invites:
        if campaign_id == inv["id"]:
            campaign_owner = inv["from"]
    if campaign_owner is None:
        return self.respond({"success": False, "info": MSG_BAD_CAMP})

    self.server.db.remove_campaign_invite(username, campaign_id)

    return self.respond({"success": True})


def set_role(self, args, username):
    if args[KEY_ROLE] not in ROLES:
        return self.respond({"success": False, "info": MSG_BAD_ROLE})

    campaign_id = args[KEY_CAMPAIGN_ID]

    if not has_campaign_permissions(self, username, campaign_id, owner_only=True):
        return self.respond({"success": False, "info": MSG_BAD_CAMP})

    member = args[KEY_USERNAME]
    if not self.server.db.is_valid("campaigns", campaign_id, "members", member):
        return self.respond({"success": False, "info": MSG_NO_USER})

    self.server.db.set_role(member, campaign_id, args[KEY_ROLE])
    return self.respond({"success": True})


def get_role(self, args, username):
    campaign_id = args[KEY_CAMPAIGN_ID]

    if not has_campaign_permissions(self, username, campaign_id):
        return self.respond({"success": False, "info": MSG_BAD_CAMP})

    member = args[KEY_USERNAME]
    if not self.server.db.is_valid("campaigns", campaign_id, "members", member):
        return self.respond({"success": False, "info": MSG_NO_USER})

    role = self.server.db.get_role(member, campaign_id)
    return self.respond({"success": True, "value": role})

# APIs to add / refactor if present in some form:

# add_entity_to_campaign (campaign_id, entity_id) - 'player' members may add characters, 'GM' members may add enemies / characters
# remove_entity_from_campaign (campaign_id, entity_id) - 'player' members may remove characters, 'GM' members may remove enemies / characters
# start_combat (campaign_id) - 'GM' player may start a combat session, returns combat_id
# end_combat (campaign_id, combat_id) - 'GM' player may end an open combat session -> removes it from the database & clears pending combat stats & resolves any pending attacks
# add_entity_to_combat (campaign_id, combat_id, entity_id, init) -> init is either an entered number OR init is roll string
# remove_entity_from_combat (campaign_id, combat_id, entity_id) -> 'GM' may remove anyone
# create_attack (campaign_id, combat_id, from_entity_id, to_entity_id, damage, damage_type) -> returns attack_id
# resolve_attack (campaign_id, combat_id, attack_id, result)

# need getters for everything

# use_ability

# table full of attacks


# new things to add to each combat section
entities = [{
    "uuid of entity": {
        "owner": "uuid of owner",
        # only 'GM' members can see enemies
        "type": "type of entity - e.g. enemy, character"
    }
}]

# maintain as ordered list
initiative = {
    "init number": ["uuid of entities"]
}

combat = [{
    "id": "new uuid of attack",
    "attacker": "uuid of attacking entity",
    "receiver": "uuid of receiving entity",
    "state": "PENDING or COMPLETE",
    "damage": 12,  # full damage number
    "damage_type": "fire",
    "accuracy": 30,
    "status_effects": ["status effect caused"],
    "desc": "text description of cause for display"
}]

# need to move campaign name to campaigns section - not character section
