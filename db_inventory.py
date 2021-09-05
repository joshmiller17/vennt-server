# Josh Aaron Miller 2021
# VenntDB methods for Inventory

import venntdb
from constants import *

# VenntDB Methods


def get_standard_weapon(self, weapon_name):
    for weapon in self.weapons:
        if weapon["name"] == weapon_name:
            return weapon
    return None


def get_custom_weapon(self, username, weapon_name):
    self.assert_valid("accounts", username, "weapons")
    for weapon in self.db["accounts"][username]["weapons"]:
        if weapon["name"] == weapon_name:
            return weapon
    return None


def get_weapon(self, username, weapon_name):
    weapon = self.get_standard_weapon(weapon_name)
    if weapon is None:
        weapon = self.get_custom_weapon(username, weapon_name)
    return weapon


def remove_weapon(self, username, weapon_name):
    self.assert_valid("accounts", username, "weapons")
    for weapon in self.db["accounts"][username]["weapons"]:
        if weapon["name"] == weapon_name:
            self.db["accounts"][username]["weapons"].remove(weapon)
            self.save_db()
            return True
    return False


def add_weapon(self, username, weapon):
    self.assert_valid("accounts", username, "weapons")
    self.db["accounts"][username]["weapons"].append(weapon)
    self.save_db()


def add_item(self, username, character_id, item):
    self.assert_valid("accounts", username, "characters",
                      character_id, "items")
    if len(self.db["accounts"][username]["characters"][character_id]["items"]) >= MAX_INVENTORY_SIZE:
        return False
    self.db["accounts"][username]["characters"][character_id]["items"].append(
        item)
    self.save_db()
    return True


def view_items(self, username, character_id):
    self.assert_valid("accounts", username, "characters",
                      character_id, "items")
    return self.db["accounts"][username]["characters"][character_id]["items"]


def remove_item(self, username, character_id, item_id):
    self.assert_valid("accounts", username, "characters",
                      character_id, "items")
    for item in self.db["accounts"][username]["characters"][character_id]["items"]:
        if item["id"] == item_id:
            self.db["accounts"][username]["characters"][character_id]["items"].remove(
                item)
            self.save_db()
            return True
    return False
