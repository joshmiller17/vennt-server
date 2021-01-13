# Josh Aaron Miller 2021
# API calls for Characters

import venntdb, uuid
from constants import *

# VenntHandler methods

def create_character(self, args, username):
	name = args[KEY_NAME]
	if len(name) > MAX_NAME_LENGTH:
		return self.respond({"success":False, "info":MSG_NAME_LONG})
	
	id = str(uuid.uuid4())
	character = {"name":name, "id":id}
	for key in args:
		if key in ATTRIBUTES:
			character[key] = args[key]
	self.server.db.create_character(username, character)
	
	ret = {"success":True, "id":id}
	return self.respond(ret)
	
def set_attr(self, args, username):
	char_id = args[KEY_ID]
	attr = args[KEY_ATTR]
	val = args[KEY_VAL]
	
	if attr not in ATTRIBUTES:
		return self.respond({"success":False,"info":MSG_NO_ATTR})
						
	if not self.server.db.character_exists(username, char_id):
		return self.respond({"success":False,"info":MSG_NO_CHAR})
	
	self.server.db.set_attr(username, char_id, attr, val)
	return self.respond({"success":True})
	
def get_attr(self, args, username):
	char_id = args[KEY_ID]
	attr = args[KEY_ATTR]
	
	if attr not in ATTRIBUTES:
		return self.respond({"success":False,"info":MSG_NO_ATTR})
						
	if not self.server.db.character_exists(username, char_id):
		return self.respond({"success":False,"info":MSG_NO_CHAR})
	
	val = self.server.db.get_attr(username, char_id, attr)
	return self.respond({"success":True, "value":str(val)})