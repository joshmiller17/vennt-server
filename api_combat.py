# Josh Aaron Miller 2021
# API calls for Combat

import venntdb
import uuid
from constants import *
from stats import *
from api_campaigns import has_campaign_permissions

# TODO: Character may not make any combat actions until they resolve any pending attacks
# TODO: When in combat: ensure user has the actions to do their action
# TODO: when outside of combat: actions are ignored, do not adjust values in entities table
# We should check if init table is empty rather than relying on flag here, since we don't want people attacking while rolling for initiative)


# not sure this is really worth having since we don't keep track of locations or anything - users can just end turn instead of doing this
def combat_move(self, args, username):
    return self.respond({"success": False, "info": MSG_NO_IMP})


def combat_delay(self, args, username):
    return self.respond({"success": False, "info": MSG_NO_IMP})


def attack(self, args, username):
    # create pending attack in table - add pending attack to list in entities table
    # the attack can then be resolved by the player receiving the attack (e.g. they can take the damage / block / dodge / negate damage somehow)
    return self.respond({"success": False, "info": MSG_NO_IMP})


def resolve_attack(self, args, username):
    return self.respond({"success": False, "info": MSG_NO_IMP})


def use_ability(self, args, username):
    return self.respond({"success": False, "info": MSG_NO_IMP})


def use_item(self, args, username):
    return self.respond({"success": False, "info": MSG_NO_IMP})


'''# Helper funcs

def has_permissions(self, username, campaign_id, gm_only=False, character_id=None):
	if not has_campaign_permissions(self, username, campaign_id):
		return False

	role = self.server.db["campaigns"][campaign_id]
	if role == "GM":
		return True
	elif role == "player":
		whose_turn = self.server.db.get_current_turn(campaign_id)
		if whose_turn is None or character_id == whose_turn:
			return True
	return False



# VenntHandler methods

def get_undo_history(self, args, username):
	campaign_id = args[KEY_CAMPAIGN_ID]
	if not has_campaign_permissions(self, username, campaign_id):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})

	history = self.server.db.get_undo_history(self, campaign_id)
	return self.respond({"success":True, "value":history})


def attack(self, username, campaign_id, character_id, target_id, weapon_name):
	if not has_permissions(self, username, campaign_id, gm_only=False, character_id=character_id):
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
		
	return # TODO unfinished
	
def use(self, username, campaign_id, character_id, ability_name, spell_strength=1):
	if not has_permissions(self, username, campaign_id, gm_only=False, character_id=character_id):
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	
	abiDict = self.server.db.get_ability(username, character_id, ability_name)
		
		
		
	return # TODO unfinished'''
