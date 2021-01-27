# Josh Aaron Miller 2021
# API calls for Abilities

import venntdb, uuid
from constants import *

# VenntHandler methods

def add_ability(self, args, username):
	ability = args[KEY_NAME]
		
	abiDict = self.server.db.get_ability(username, args[KEY_ID], ability)
	if abiDict is not None:
		return self.respond({"success":True, "info":"Ability already added."})
	
	abiDict = self.server.db.get_or_make_ability(ability)
	if abiDict is None:
		return self.respond({"success":True, "info":MSG_NO_ABI})
	
	self.server.db.add_ability(username, abiDict)
	
	return self.respond({"success":True})
	
def get_ability(self, args, username):
	ability = args[KEY_NAME]
	
	abiDict = self.server.db.get_ability(username, args[KEY_ID], ability)
	if abiDict is None:
		return self.respond({"success":True, "info":MSG_NO_ABI})
	
	return self.respond({"success":True, "value":abiDict})