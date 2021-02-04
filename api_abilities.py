# Josh Aaron Miller 2021
# API calls for Abilities

import venntdb, uuid
from constants import *

# VenntHandler methods

def get_abilities(self, args, username):
	# TODO assert username has view permission to character
	return self.respond({"success":True, "value":self.server.db.get_abilities(username, args[KEY_ID])})

def add_ability(self, args, username):
	ability = args[KEY_NAME]
	character_id = args[KEY_ID]
	# TODO assert username has ownership permission to character
	
	abiDict = self.server.db.get_ability(username, character_id, ability)
	if abiDict is not None:
		return self.respond({"success":True, "info":"Ability already added."})
	
	abiDict = self.server.db.get_or_make_ability(ability)
	if abiDict is None:
		return self.respond({"success":True, "info":MSG_NO_ABI})
	
	self.server.db.add_ability(username, character_id, abiDict)
	
	return self.respond({"success":True})
	
def get_ability(self, args, username):
	ability = args[KEY_NAME]
	
	# TODO assert username has view permission to character
	
	abiDict = self.server.db.get_ability(username, args[KEY_ID], ability)
	if abiDict is None:
		return self.respond({"success":True, "info":MSG_NO_ABI})
	
	return self.respond({"success":True, "value":abiDict})