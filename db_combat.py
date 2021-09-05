# Josh Aaron Miller 2021
# VenntDB methods for Combat

import venntdb
from constants import *

# VenntDB Methods

# Shape of combat table as Jack imagines it - entities should have a list of pending attacks aimed at them so its easy to see what needs to be resolved

# combat = {
#    "uuid of attack": {
#       "attacker": "uuid of attacking entity",
#       "receiver": "uuid of receiving entity",
#       "state": "PENDING or COMPLETE",
#       "damage": 12,  # full damage number
#       "damage_type": "fire",
#       "accuracy": 30,
#       "status_effects": ["status effect caused"],
#       "desc": "text description of cause for display"
#   }
# }

'''def push_undo(self, campaign_id, changeDict):
    self.assert_valid("campaigns", campaign_id)
    if not "undo" in self.db["campaigns"][campaign_id]:
        self.db["campaigns"][campaign_id]["undo"] = [
            None] * (MAX_UNDO_HISTORY + 1)
        self.db["campaigns"][campaign_id]["undo_index"] = 0
    self.db["campaigns"][campaign_id]["undo"][self.db["campaigns"]
                                              [campaign_id]["undo_index"]] = changeDict
    self.db["campaigns"][campaign_id]["undo_index"] += 1
    if self.db["campaigns"][campaign_id]["undo_index"] > MAX_UNDO_HISTORY:
        self.db["campaigns"][campaign_id]["undo_index"] = 0


def pop_undo(self, campaign_id):
    self.assert_valid("campaigns", campaign_id)
    self.db["campaigns"][campaign_id]["undo_index"] -= 1
    if self.db["campaigns"][campaign_id]["undo_index"] < 0:
        self.db["campaigns"][campaign_id]["undo_index"] = MAX_UNDO_HISTORY
    return self.db["campaigns"][campaign_id]["undo"][self.db["campaigns"][campaign_id]["undo_index"]]


def get_undo_history(self, campaign_id):
    ret = []
    self.assert_valid("campaigns", campaign_id)
    self.db["campaigns"][campaign_id]["undo"][self.db["campaigns"]
                                              [campaign_id]["undo_index"]] = None
    index = self.db["campaigns"][campaign_id]["undo_index"] - 1
    done = False
    while not done:
        if index < 0:
            index = MAX_UNDO_HISTORY
        next = self.db["campaigns"][campaign_id]["undo"][index]
        if next is None:
            done = True
        else:
            ret.append(next)
    return ret'''
