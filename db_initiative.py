# Josh Aaron Miller 2021
# VenntDB methods for Initiative

import venntdb
import operator
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("db_initiative")

# VenntDB Methods


def add_to_combat(self, campaign_id, entity_id, roll, bonus):
    init_list = self.db["campaigns"][campaign_id]["init"]

    # walk through init list and look for correct place to insert the new row
    index = 0
    for i in range(len(init_list)):
        index = i
        if init_list[i]["roll"] == roll:
            if init_list[i]["bonus"] == bonus:
                if init_list[i]["entity_id"][0] == IDType.ENEMY and entity_id[0] == IDType.CHARACTER:
                    break
            elif init_list[i]["bonus"] < bonus:
                break
        elif init_list[i]["roll"] < roll:
            break

    self.db["campaigns"][campaign_id]["init"].insert(
        index, {"roll": roll, "bonus": bonus, "entity_id": entity_id})

    # shift the current index forward to account for new item in the init list
    current_index = self.db["campaigns"][campaign_id]["init_index"]
    if current_index >= index:
        self.db["campaigns"][campaign_id]["init_index"] = current_index + 1

    # if the entity is gm_only - make it visible to everyone
    if self.db["campaigns"][campaign_id]["entities"][entity_id]["gm_only"]:
        self.db["campaigns"][campaign_id]["entities"][entity_id]["gm_only"] = False
    self.save_db()
    return True


def remove_from_combat(self, campaign_id, entity_id):
    if len(self.db["campaigns"][campaign_id]["init"]) == 0:
        return False
    # TODO: May need to implement some sort of multi-threaded locking mechanism on this table to prevent race conditions if this program is multi-threaded??
    init_list = self.db["campaigns"][campaign_id]["init"]
    self.db["campaigns"][campaign_id]["init"] = list(
        filter(lambda entity: entity["entity_id"] == entity_id, init_list))
    # TODO: Need to clear any pending attacks against this entity from the campaign
    # TODO: Need to update the init_index appropriately -> maybe just call next_turn?
    self.save_db()
    return True


def start_combat(self, campaign_id):
    if self.db["campaigns"][campaign_id]["in_combat"] or len(self.db["campaigns"][campaign_id]["init"]) == 0:
        return False
    self.db["campaigns"][campaign_id]["in_combat"] = True
    entity_id = self.db["campaigns"][campaign_id]["init"][0]
    self.db["campaigns"][campaign_id]["entities"][entity_id]["actions"] = 3
    self.db["campaigns"][campaign_id]["entities"][entity_id]["reactions"] = 1
    init_style = self.db["campaigns"][campaign_id]["init_styles"]
    if (init_style == INIT_ASYNC):
        # async style means we keep walking down the init list until we find an entity of a different type (so all players / enemies can go at once)
        # TODO: this calculation
        while __async_init_should_keep_checking(self, campaign_id, entity_id):
            __increment_init_index(self, campaign_id)
    self.save_db()
    return True


def end_combat(self, campaign_id):
    self.db["campaigns"][campaign_id]["in_combat"] = False
    self.db["campaigns"][campaign_id]["init"] = []
    self.db["campaigns"][campaign_id]["init_index"] = 0
    self.db["campaigns"][campaign_id]["init_round"] = 0
    # Reset actions and reactions
    for entity in self.db["campaigns"][campaign_id]["entities"]:
        self.db["campaigns"][campaign_id]["entities"][entity]["actions"] = 0
        self.db["campaigns"][campaign_id]["entities"][entity]["reactions"] = 0
    # do not clear any pending attacks since those still need to be resolved
    self.save_db()
    return True


def next_turn(self, campaign_id):
    if len(self.db["campaigns"][campaign_id]["init"]) == 0:
        return False
    init_style = self.db["campaigns"][campaign_id]["init_styles"]
    # always increment once
    init_index = __increment_init_index(self, campaign_id)
    if (init_style == INIT_ASYNC):
        # async style means we keep walking down the init list until we find an entity of a different type (so all players / enemies can go at once)
        # TODO: this calculation
        entity_id = self.db["campaigns"][campaign_id]["init"][init_index]
        while __async_init_should_keep_checking(self, campaign_id, entity_id):
            __increment_init_index(self, campaign_id)
    self.save_db()


# Helper functions
def __get_next_init(self, campaign_id):
    next_init = self.db["campaigns"][campaign_id]["init_index"] + 1
    init_length = len(self.db["campaigns"][campaign_id])
    if (next_init >= init_length):
        # wrap around
        return 0
    return next_init


def __async_init_should_keep_checking(self, campaign_id, starting_entity_id):
    next_init = __get_next_init(self, campaign_id)
    next_entity_id = self.db["campaigns"][campaign_id]["init"][next_init]["entity_id"]
    return next_entity_id[0] != starting_entity_id[0] and next_entity_id != starting_entity_id


def __increment_init_index(self, campaign_id):
    next_init = __get_next_init(self, campaign_id)
    if next_init == 0:
        # wrap around
        self.db["campaigns"][campaign_id]["init_round"] += 1
    self.db["campaigns"][campaign_id]["init_index"] = next_init
    # TODO: Do not reset actions of users who delayed actions
    # TODO: Do not reset actions / reactions if stunned / paralyzed
    entity_id = self.db["campaigns"][campaign_id]["init"][next_init]
    self.db["campaigns"][campaign_id]["entities"][entity_id]["actions"] = 3
    self.db["campaigns"][campaign_id]["entities"][entity_id]["reactions"] = 1
    return next_init
