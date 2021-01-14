# Josh Aaron Miller 2021
# API calls for Inventory

import venntdb, uuid
from constants import *

# VenntHandler methods

def add_item(self, args, username):
	name = args[KEY_NAME]
	if len(name) > MAX_NAME_LENGTH:
		return self.respond({"success":False, "info":MSG_NAME_LONG})
		
	desc = args[KEY_DESC]
	if len(desc) > MAX_DESC_LENGTH:
		return self.respond({"success":False, "info":MSG_DESC_LONG})
		
	try:
		bulk = int(args[KEY_BULK])
	except:
		return self.respond({"success":False, "info":MSG_NOT_INT.format(KEY_BULK)})
	
	id = IDType.ITEM + str(uuid.uuid4())
	item = {"name":name, "id":id, "desc":desc, "bulk":bulk}
	success = self.server.db.add_item(username, item)
	
	if not success:
		return self.respond({"success":False, "info":"Max items exceeded"})
	
	ret = {"success":True, "id":id}
	return self.respond(ret)
	
def get_weapon(self, args, username):
	weapon = self.server.db.get_weapon(username, args[KEY_NAME])
	if weapon is None:
		return self.respond({"success":False, "info":"No such weapon"})
		
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