# Josh Aaron Miller 2021
# API calls for Campaigns

import venntdb, uuid
from constants import *

# VenntHandler methods

def create_campaign(self, args, username):
	name = args[KEY_NAME]		
	id = str(uuid.uuid4())
	campaign = {"name":name, "id":id}
	self.server.db.create_campaign(username, campaign)
	
	ret = {"success":True, "id":id}
	return self.respond(ret)
	
def send_campaign_invite(self, args, username):
	user_to = args[KEY_USERNAME]
	user_from = username
	users_campaigns = self.server.db.get_campaigns(user_from)
	campaign_id = args[KEY_ID]
	
	if campaign_id not in [c["id"] for c in users_campaigns]:
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
		
	if not self.server.db.account_exists(user_to):
		return self.respond({"success":False, "info":MSG_NO_USER})

	success = self.server.db.send_campaign_invite(user_from, user_to, campaign_id)
	
	if not success:
		return self.respond({"success":False, "info":MSG_INVITE_EXISTS})
	
	return self.respond({"success":success})
	
def accept_campaign_invite(self, args, username):
	invites = self.server.db.get_campaign_invites(username)
	campaign_id = args[KEY_ID]
	
	campaign_owner = None
	for inv in invites:
		if campaign_id == inv["id"]:
			campaign_owner = inv["from"]
	if campaign_owner is None:
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
		
	self.server.db.add_user_to_campaign(username, campaign_id)
	
	return self.respond({"success":True})
	
def decline_campaign_invite(self, args, username):
	invites = self.server.db.get_campaign_invites(username)
	campaign_id = args[KEY_ID]
	
	campaign_owner = None
	for inv in invites:
		if campaign_id == inv["id"]:
			campaign_owner = inv["from"]
	if campaign_owner is None:
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
		
	self.server.db.remove_campaign_invite(username, campaign_id)
	
	return self.respond({"success":True})
	
def set_role(self, args, username):
	if args[KEY_ROLE] not in ROLES:
		return self.respond({"success":False, "info":MSG_BAD_ROLE})
				
	campaign_id = args[KEY_ID]
	
	campaign = self.server.db.get_campaign(campaign_id)
	if campaign is None or campaign["owner"] != username:
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
		
	for member in campaign["members"]:
		if member["username"] == args[KEY_USERNAME]:
			member["role"] = args[KEY_ROLE]
			return self.respond({"success":True})
	return self.respond({"success":False, "info":MSG_NO_USER}) 
	
	
def get_role(self, args, username):
	campaign_id = args[KEY_ID]
	campaign = self.server.db.get_campaign(campaign_id)
	if campaign is None or (campaign_id not in self.server.db.get_campaigns(username) and campaign_id not in self.server.db.get_joined_campaigns(username)):
		return self.respond({"success":False, "info":MSG_BAD_CAMP})
	
	for member in campaign["members"]:
		if member["username"] == args[KEY_USERNAME]:
			return self.respond({"success":True, "value":member["role"]})
	return self.respond({"success":False, "info":MSG_NO_USER}) 
	