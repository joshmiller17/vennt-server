# Josh Aaron Miller 2021
# API calls for Enemies

import venntdb
import uuid
from constants import *

# VenntHandler methods


def create_enemy(self, args, username):
    name = args[KEY_NAME]
    id = IDType.ENEMY + str(uuid.uuid4())
    enemy = {"name": name, "id": id}
    for key in args:
        if key in ATTRIBUTES:
            try:
                enemy[key] = int(args[key])
            except ValueError:
                return self.respond({"success": False, "info": MSG_INVALID_ATTRIBUTE})
    self.server.db.create_character(username, enemy, is_enemy=True)

    ret = {"success": True, "id": id}
    return self.respond(ret)
