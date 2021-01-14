# Josh Aaron Miller 2021
# API calls for Initiative

import venntdb
from constants import *
from api_campaigns import has_campaign_permissions

# VenntHandler methods

def reset_turn_order(self, args, username):
	campaign_id = args[KEY_CAMPAIGN_ID]
	if not has_campaign_permissions(self, username, campaign_id):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
	
	self.server.db.reset_turn_order(campaign_id)
	return self.respond({"success":True})
	
def add_turn(self, args, username):
	campaign_id = args[KEY_CAMPAIGN_ID]
	if not has_campaign_permissions(self, username, campaign_id):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
	
	self.server.db.add_turn(campaign_id, args[KEY_ID], args[KEY_VAL])
	return self.respond({"success":True})
	
def next_turn(self, args, username):
	campaign_id = args[KEY_CAMPAIGN_ID]
	if not has_campaign_permissions(self, username, campaign_id):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
		
	entity_id = self.server.db.next_turn(campaign_id)
	return self.respond({"success":True, "value":entity_id})
	
def get_turn_order(self, args, username):
	campaign_id = args[KEY_CAMPAIGN_ID]
	if not has_campaign_permissions(self, username, campaign_id):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
		
	turns = self.server.db.get_turn_order(campaign_id)
	return self.respond({"success":True, "value":turns})
	
def get_current_turn(self, args, username):
	campaign_id = args[KEY_CAMPAIGN_ID]
	if not has_campaign_permissions(self, username, campaign_id):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
		
	turn = self.server.db.get_current_turn(campaign_id)
	return self.respond({"success":True, "value":turn})