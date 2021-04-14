# Josh Aaron Miller 2021
# API calls for Combat

import venntdb, uuid
from constants import *
from stats import *
from api_campaigns import has_campaign_permissions


# Helper funcs

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
		
		
		
	return # TODO unfinished