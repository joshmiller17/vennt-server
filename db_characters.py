# Josh Aaron Miller 2021
# VenntDB methods for Characters

import time
import venntdb
from constants import *

# VenntDB Methods


def character_exists(self, username, char_id):
    return self.get_character(username, char_id) is not None


def get_character(self, username, char_id):
    self.assert_valid("accounts", username, "characters")
    if self.is_valid("accounts", username, "characters", char_id):
        return self.db["accounts"][username]["characters"][char_id]
    return None


def create_character(self, username, character):
    self.assert_valid("accounts", username, "characters")
    self.db["accounts"][username]["characters"][character["id"]] = character
    self.save_db()


def get_characters(self, username):
    self.assert_valid("accounts", username, "characters")
    return self.db["accounts"][username]["characters"]


def get_attr(self, username, char_id, attr):
    self.assert_valid("accounts", username, "characters", char_id)
    return self.get_character(username, char_id)[attr]


def set_attr(self, username, char_id, attr, val):
    self.assert_valid("accounts", username, "characters", char_id)
    self.get_character(username, char_id)[attr] = val
    self.save_db()

def update_attrs(self, username, char_id, attrs, msg=None):
    self.assert_valid("accounts", username, "characters", char_id)
    char = self.get_character(username, char_id)

    if CHAR_CHANGELOG not in self.db["accounts"][username]["characters"][char_id]:
        # safety fallback for older characters
        self.db["accounts"][username]["characters"][char_id][CHAR_CHANGELOG] = []

    for (attr, val) in attrs.items():
        if msg != None:
            __add_to_changelog(self, username, char_id, attr, msg)
        char[attr] = val
    self.save_db()

def filter_changelog(self, username, char_id, attr=None):
    self.assert_valid("accounts", username, "characters", char_id, CHAR_CHANGELOG)
    if attr == None:
        new_log = []
    else:
        logs = self.db["accounts"][username]["characters"][char_id][CHAR_CHANGELOG]
        new_log = [log for log in logs if log[CHANGE_ATTR] != attr]
    self.db["accounts"][username]["characters"][char_id][CHAR_CHANGELOG] = new_log
    self.save_db()


def __add_to_changelog(self, username, char_id, attr, msg):
    if attr == "NOTES":
        # do not add NOTES to the changelog because they can be very long
        return
    
    log = { CHANGE_ATTR: attr, CHANGE_MSG: msg, CHANGE_TIME: int(time.time()) }
    if attr in self.db["accounts"][username]["characters"][char_id]:
        log[CHANGE_PREV] = self.db["accounts"][username]["characters"][char_id][attr]

    self.db["accounts"][username]["characters"][char_id][CHAR_CHANGELOG].append(log)
