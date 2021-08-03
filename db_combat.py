# Josh Aaron Miller 2021
# VenntDB methods for Combat

import venntdb
import webscraper
from constants import *

# VenntDB Methods


def push_undo(self, campaign_id, changeDict):
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
    return ret
