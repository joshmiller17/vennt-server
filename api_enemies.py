# Josh Aaron Miller 2021
# API calls for Characters

import venntdb, uuid
from constants import *

# VenntHandler methods

def create_enemy(self, args, username):
	name = args[KEY_NAME]		
	id = str(uuid.uuid4())
	enemy = {"name":name, "id":id}
	for key in args:
		if key in venntdb.ATTRIBUTES:
			enemy[key] = args[key]
	self.server.db.create_enemy(username, enemy)
	
	ret = {"success":True, "id":id}
	return self.respond(ret)