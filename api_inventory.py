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
	
	id = str(uuid.uuid4())
	item = {"name":name, "id":id, "desc":desc, "bulk":bulk}
	success = self.server.db.add_item(username, item)
	
	if not success:
		return self.respond({"success":False, "info":"Max items exceeded"})
	
	ret = {"success":True, "id":id}
	return self.respond(ret)