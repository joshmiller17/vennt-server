# Josh Aaron Miller 2021
# API calls for Abilities

import venntdb, uuid
from constants import *
import utilities.ability as ability_util

# VenntHandler methods

def get_abilities(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.PRIVATE_VIEW:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	
	return self.respond({"success":True, "value":self.server.db.get_abilities(username, args[KEY_ID])})

def add_ability(self, args, username):
	ability = args[KEY_NAME]
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	
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
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.PRIVATE_VIEW:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	
	abiDict = self.server.db.get_ability(username, args[KEY_ID], ability)
	if abiDict is None:
		return self.respond({"success":True, "info":MSG_NO_ABI})
	
	return self.respond({"success":True, "value":abiDict})

def add_custom_ability(self, json_data, args, username):
	# Validate json_data
	if not ability_util.is_valid(json_data, True):
		return self.respond({"success":False, "info":"Invalid ability shape"})

	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})

	abiDict = self.server.db.get_ability(username, character_id, json_data[ABI_DICT_NAME])
	if abiDict is not None:
		return self.respond({"success":False, "info":"Ability of the same name already exists."})

	self.server.db.add_ability(username, character_id, json_data)
	return self.respond({"success":True})

def update_ability(self, json_data, args, username):
	if not ability_util.is_valid(json_data):
		return self.respond({"success":False, "info":"Invalid ability shape"})

	ability_name = args[KEY_NAME]
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})

	if not self.server.db.remove_ability(username, character_id, ability_name):
		return self.respond({"success":False, "info":"Ability does not exist to be updated"})

	self.server.db.add_ability(username, character_id, json_data)
	return self.respond({"success":True})

def remove_ability(self, args, username):
	ability_name = args[KEY_NAME]
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})

	if not self.server.db.remove_ability(username, character_id, ability_name):
		return self.respond({"success":True, "info":"Ability already removed"})
	return self.respond({"success":True})

def refresh_ability(self, args, username):
	ability_name = args[KEY_NAME]
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})

	current_ability = self.server.db.get_ability(username, character_id, ability_name)
	if current_ability is None:
		return self.respond({"success":False, "info":"Ability of the same name does not already exist."})
	elif ABI_DICT_SPECIAL_TYPE in current_ability:
		return self.respond({"success":False, "info":"Custom abilities may not be refreshed"})

	# Refresh ability by removing it from the character, clearing the ability from the cache,
	# and then re-add the ability to the user.
	self.server.db.remove_ability(username, character_id, ability_name)
	self.server.db.remove_cached_ability(ability_name)
	abiDict = self.server.db.get_or_make_ability(ability_name)
	if abiDict is None:
		return self.respond({"success":True, "info":MSG_NO_ABI}) # Ability was probably renamed or removed - rip
	self.server.db.add_ability(username, character_id, abiDict)

	return self.respond({"success":True})

def update_ability_comment(self, args, username):
	ability_name = args[KEY_NAME]
	character_id = args[KEY_ID]
	comment = args[KEY_COMMENT]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})

	abiDict = self.server.db.get_ability(username, args[KEY_ID], ability_name)
	if abiDict is None:
		return self.respond({"success":True, "info":MSG_NO_ABI})

	abiDict[ABI_DICT_COMMENT] = comment
	return self.respond({"success":True})
