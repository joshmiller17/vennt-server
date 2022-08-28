# Josh Aaron Miller 2021
# API calls for Inventory

import venntdb, uuid
from constants import *
import utilities.item as item_util

# VenntHandler methods

def view_items(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.PRIVATE_VIEW:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	items = self.server.db.view_items(username, args[KEY_ID])
	return self.respond({"success":True, "value":items})
	
def remove_item(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	return self.respond({"success":self.server.db.remove_item(username, args[KEY_ID], args[KEY_ID2])})

def add_item(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.ADD:
		return self.respond({"success": False, "info":MSG_NO_PERMISSION})

	item = __item_from_args(args)
	if isinstance(item, str):
		return self.respond({"success": False, "info": item})

	success = self.server.db.add_item(username, character_id, item)
	if not success:
		return self.respond({"success": False, "info": "Max items exceeded"})
	ret = {"success": True, "id": item[ITEM_ID]}
	return self.respond(ret)

def update_item(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.ADD:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})

	item = __item_from_args(args, True)
	if isinstance(item, str):
		return self.respond({"success": False, "info": item})

	updated_item = self.server.db.update_item(username, character_id, item)
	if not updated_item:
		return self.respond({"success": False, "info": MSG_NO_ITEM})
	return self.respond({"success": True, "value": updated_item})
	
def get_weapon(self, args, username):
	weapon = self.server.db.get_weapon(username, args[KEY_NAME])
	if weapon is None:
		return self.respond({"success": False, "info": MSG_NO_ITEM})
		
	return self.respond({"success":True, "value":weapon})
	
def add_weapon(self, args, username):
	weapon_name = args[KEY_NAME]
	if len(weapon_name) > MAX_NAME_LENGTH:
		return self.respond({"success":False, "info":MSG_NAME_LONG})
		
	if self.server.db.get_weapon(username, weapon_name) is not None:
		return self.respond({"success":False, "info":"Weapon already exists"})
		
	attr = args[KEY_ATTR]
	if attr not in ATTRIBUTES:
		return self.respond({"success":False,"info":MSG_NO_ATTR})
		
	dmg = args[KEY_DMG]
	# TODO verify dmg is well-ordered
	
	if KEY_MODS in args:
		mods = args[KEY_MODS]
		# TODO verify mods are well-ordered
		
	weapon = {"name":weapon_name, "attr":attr, "dmg":dmg, "mods":mods}
	self.server.db.add_weapon(username, weapon)
	
	return self.respond({"success":True})
	
def remove_weapon(self, args, username):
	return self.respond({"success":self.server.db.remove_weapon(username, args[KEY_NAME])})

def __item_from_args(args, allow_partial=False):
	id = IDType.ITEM + str(uuid.uuid4())
	if KEY_ID2 in args:
		id = args[KEY_ID2]
	
	item = { ITEM_ID: id }

	string_args = [
		ITEM_NAME, ITEM_DESC, ITEM_TYPE, ITEM_COURSES, ITEM_COMMENT, ITEM_CATEGORY, 
		ITEM_WEAPON_TYPE, ITEM_RANGE, ITEM_ATTR, ITEM_DMG, ITEM_SPECIAL]
	for key in string_args:
		if key in args:
			item[key] = args[key]

	if KEY_BULK in args:
		try:
			item[ITEM_BULK] = int(args[KEY_BULK])
		except:
			return MSG_NOT_INT.format(KEY_BULK)
	if ITEM_EQUIPPED in args:
		# cannot use the bool function because it will convert any string to True (even "false")
		item[ITEM_EQUIPPED] = args[ITEM_EQUIPPED] == 'true'
	
	if not item_util.is_valid(item, allow_partial):
		return MSG_ARGS_NOT_VALID

	return item
