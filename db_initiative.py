# Josh Aaron Miller 2021
# VenntDB methods for Initiative

import venntdb
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("db_initiative")

# VenntDB Methods


def add_to_combat(self, campaign_id, entity_id, roll, bonus):
    init_list = self.db["campaigns"][campaign_id]["init"]

    # walk through init list and look for correct place to insert the new row
    insert_index = len(init_list)
    for i in range(len(init_list)):
        if init_list[i]["roll"] == roll:
            if init_list[i]["bonus"] == bonus:
                if init_list[i]["entity_id"][0] == IDType.ENEMY and entity_id[0] == IDType.CHARACTER:
                    insert_index = i
                    break
            elif init_list[i]["bonus"] < bonus:
                insert_index = i
                break
        elif init_list[i]["roll"] < roll:
            insert_index = i
            break

    self.db["campaigns"][campaign_id]["init"].insert(
        insert_index, {"roll": roll, "bonus": bonus, "entity_id": entity_id})

    # shift the current index forward to account for new item in the init list
    if self.db["campaigns"][campaign_id]["in_combat"]:
        current_index = self.db["campaigns"][campaign_id]["init_index"]
        if current_index >= insert_index:
            self.db["campaigns"][campaign_id]["init_index"] = current_index + 1
    else:
        # entities start combat with 1 reaction (only when not in combat)
        self.db["campaigns"][campaign_id]["entities"][entity_id]["reactions"] = 1

    # if the entity is gm_only - make it visible to everyone
    if self.db["campaigns"][campaign_id]["entities"][entity_id]["gm_only"]:
        self.db["campaigns"][campaign_id]["entities"][entity_id]["gm_only"] = False
    self.save_db()
    return True


def remove_from_combat(self, campaign_id, entity_id):
    if len(self.db["campaigns"][campaign_id]["init"]) == 0:
        return False
    init_list = self.db["campaigns"][campaign_id]["init"]
    self.db["campaigns"][campaign_id]["init"] = list(
        filter(lambda entity: entity["entity_id"] == entity_id, init_list))
    # Increment turn if needed
    if not next_turn(self, campaign_id):
        self.save_db()
    return True


def start_combat(self, campaign_id):
    if self.db["campaigns"][campaign_id]["in_combat"] or len(self.db["campaigns"][campaign_id]["init"]) == 0:
        return False
    self.db["campaigns"][campaign_id]["in_combat"] = True
    self.db["campaigns"][campaign_id]["init_index"] = 0
    self.db["campaigns"][campaign_id]["init_round"] = 0
    # grab iniative from the top of the order
    entity = self.db["campaigns"][campaign_id]["init"][0]
    entity_id = entity["entity_id"]
    self.db["campaigns"][campaign_id]["entities"][entity_id]["actions"] = 3
    self.db["campaigns"][campaign_id]["entities"][entity_id]["reactions"] = 1
    # increment additional times following init style rules
    while __should_keep_incrementing_init(self, campaign_id, entity):
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


def update_initiative_style(self, campaign_id, style):
    self.db["campaigns"][campaign_id]["init_styles"] = style
    self.save_db()


def reset_actions(self, campaign_id, entity_id):
    self.db["campaigns"][campaign_id]["entities"][entity_id]["actions"] = 0


def next_turn(self, campaign_id, save_db=True):
    if len(self.db["campaigns"][campaign_id]["init"]) == 0 and not self.db["campaigns"][campaign_id]["in_combat"]:
        return False
    # Check if we are ready to increment (no one has actions any more)
    for init in self.db["campaigns"][campaign_id]["init"]:
        entity = self.db["campaigns"][campaign_id]["entities"][init["entity_id"]]
        if entity["actions"] > 0 and not entity["delayed_actions"]:
            return False
    # always increment once
    init_index = __increment_init_index(self, campaign_id)
    # increment additional times following init style rules
    init_details = self.db["campaigns"][campaign_id]["init"][init_index]
    while __should_keep_incrementing_init(self, campaign_id, init_details):
        __increment_init_index(self, campaign_id)
    if save_db:
        self.save_db()
    return True


# Helper functions
def __get_next_init(self, campaign_id):
    next_init = self.db["campaigns"][campaign_id]["init_index"] + 1
    init_length = len(self.db["campaigns"][campaign_id]["init"])
    if (next_init >= init_length):
        # wrap around
        return 0
    return next_init


def __should_keep_incrementing_init(self, campaign_id, starting_init_details):
    next_init = __get_next_init(self, campaign_id)
    next_init_details = self.db["campaigns"][campaign_id]["init"][next_init]

    starting_entity_id = starting_init_details["entity_id"]
    next_entity_id = next_init_details["entity_id"]

    init_style = self.db["campaigns"][campaign_id]["init_styles"]

    style_detail = init_style == INIT_ASYNC or (
        next_init_details["roll"] == starting_init_details["roll"] and next_init_details["bonus"] == starting_init_details["bonus"])

    return next_entity_id[0] == starting_entity_id[0] and next_entity_id != starting_entity_id and style_detail


def __increment_init_index(self, campaign_id):
    next_init = __get_next_init(self, campaign_id)
    if next_init == 0:
        # wrap around
        self.db["campaigns"][campaign_id]["init_round"] += 1
    self.db["campaigns"][campaign_id]["init_index"] = next_init
    # TODO: Do not reset actions / reactions if stunned / paralyzed
    entity_id = self.db["campaigns"][campaign_id]["init"][next_init]["entity_id"]
    # Do not reset actions of users who delayed actions
    if self.db["campaigns"][campaign_id]["entities"][entity_id]["actions"] > 1 and self.db["campaigns"][campaign_id]["entities"][entity_id]["delayed_actions"]:
        return next_init
    self.db["campaigns"][campaign_id]["entities"][entity_id]["actions"] = 3
    self.db["campaigns"][campaign_id]["entities"][entity_id]["reactions"] = 1
    return next_init
