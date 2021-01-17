# Josh Aaron Miller 2021
# API calls for Combat

import venntdb, uuid
from constants import *
from stats import *
from api_campaigns import has_campaign_permissions


# Helper funcs

def has_permissions(self, username, campaign_id, gm_only=False, character_id=None):
	permission = has_campaign_permissions(self, username, campaign_id)
	if not permission:
		return False
	# TODO if GM, always yes
	role = self.server.db["campaigns"][campaign_id]
	
	# TODO else use/cast if not in combat or its your turn
	
	# TODO attack if its your turn
	
	return permission




# VenntHandler methods

def get_undo_history(self, args, username):
	campaign_id = args[KEY_CAMPAIGN_ID]
	if not has_campaign_permissions(self, username, campaign_id):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})

	history = self.server.db.get_undo_history(self, campaign_id)
	return self.respond({"success":True, "value":history})



def attack(self, username, campaign_id, character_id, target_id, weapon_name):
	if not has_permissions(self, username, campaign_id)
	
	# if no permission, error
	
def use(self, username, campaign_id, character_id, ability_name, spell_strength=1):
	pass # TODO
	
	# if no permission, error
	
	