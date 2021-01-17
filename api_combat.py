# Josh Aaron Miller 2021
# API calls for Combat

import venntdb, uuid
from constants import *
from api_campaigns import has_campaign_permissions


# VenntHandler methods


def has_permissions(self, username, campaign_id, gm_only=False):
	permission = has_campaign_permissions(self, username, campaign_id)
	
	# TODO if GM, always yes
	
	# TODO else use/cast if not in combat or its your turn
	
	# TODO attack if its your turn
	
	return permission
	

def attack(self, username, campaign_id, character_id, target_id, weapon_name):
	pass # TODO
	
	# if no permission, error
	
def use(self, username, campaign_id, character_id, ability_name, spell_strength=1):
	pass # TODO
	
	# if no permission, error
	
	