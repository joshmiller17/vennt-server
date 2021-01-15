# Josh Aaron Miller 2021
# API calls for Abilities

import venntdb, uuid
from constants import *

# VenntHandler methods

def add_ability(self, args, username):
	ability = args[KEY_NAME]
	
	abiObj = self.server.db.get_ability(username, ability)
	if abiObj is not None:
		return self.respond({"success":True, "info":"Ability already added."})
	
	abiObj = self.server.db.get_or_make_ability(ability)
	if abiObj is None:
		return self.respond({"success":True, "info":MSG_NO_ABI})
	
	self.server.db.add_ability(username, abiObj)
	
	return self.respond({"success":True})