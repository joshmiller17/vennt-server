# Josh Aaron Miller 2021
# VenntDB methods for Abilities

import venntdb
import webscraper
import time
import utilities.ability as ability
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("db_abilities")

# VenntDB Methods


def add_ability(self, username, character_id, abiDict):
    self.assert_valid("accounts", username, "characters",
                      character_id, CHAR_ABILITIES)
    self.db["accounts"][username]["characters"][character_id][CHAR_ABILITIES].append(
        abiDict)
    self.save_db()


def get_abilities(self, username, character_id):
    self.assert_valid("accounts", username, "characters",
                      character_id, CHAR_ABILITIES)
    return [abiDict[ABI_DICT_NAME] for abiDict in self.db["accounts"][username]["characters"][character_id][CHAR_ABILITIES]]


def get_ability(self, username, character_id, ability):
    self.assert_valid("accounts", username, "characters",
                      character_id, CHAR_ABILITIES)
    for abiDict in self.db["accounts"][username]["characters"][character_id][CHAR_ABILITIES]:
        if ability == abiDict[ABI_DICT_NAME]:
            return abiDict
    return None


def remove_ability(self, username, character_id, ability):
    self.assert_valid("accounts", username, "characters",
                      character_id, CHAR_ABILITIES)
    abilities = self.db["accounts"][username]["characters"][character_id][CHAR_ABILITIES]
    new_abilities = [a for a in abilities if a[ABI_DICT_NAME] != ability]
    if len(abilities) - len(new_abilities) > 0:
        # If there are multiple abilities with the same name, we remove all of them
        self.db["accounts"][username]["characters"][character_id][CHAR_ABILITIES] = new_abilities
        return True
    return False


def get_cached_ability(self, name):
    for ability in self.db["ability_cache"]:
        if ability is not None:
            if name == ability[ABI_DICT_NAME]:
                return ability
    return None


def cache_ability(self, abiDict):
    self.db["ability_cache"][self.db["ability_cache_index"]] = abiDict
    self.db["ability_cache_index"] += 1
    if self.db["ability_cache_index"] > MAX_ABILITY_CACHE:
        self.db["ability_cache_index"] = 0


def remove_cached_ability(self, name):
    ability_idx = -1
    for idx, ability in enumerate(self.db["ability_cache"]):
        if ability is not None:
            if name == ability[ABI_DICT_NAME]:
                ability_idx = idx
                break
    if ability_idx >= 0:
        # Clear cache record
        self.db["ability_cache"][ability_idx] = None


def find_ability(self, ability_name):
    ability_name = ability_name.replace("’", "'") # webscaper replaces any smart quotes
    approximations = []
    URL = ""
    path = ""
    for a in self.abilities:
        if ability_name.lower() in a["ability"].lower():  # approximate
            if a["ability"].lower() == ability_name.lower():
                URL = a["url"]
                path = a["path"]
                return [a["ability"]], URL, path
            else:
                approximations.append(a["ability"])
                URL = a["url"]
                path = a["path"]
    return approximations, URL, path


def get_or_make_ability(self, name):
    approximations, URL, path = self.find_ability(name)
    if len(approximations) != 1:
        raise AssertionError("Bad call to db_abilities.get_or_make_ability, incorrect number of approximations")
    found_name = approximations[0]
    cached = self.get_cached_ability(found_name)
    if cached is not None:
        return cached
    contents = webscraper.get_ability_contents(found_name, URL)
    if contents == []:
        pass  # TODO?
    new_ability = ability.make_ability(contents, path)
    self.cache_ability(new_ability)
    return new_ability


def validate_abilities(self):
    for a in self.abilities:
        ability = a["ability"]
        logger.log("validate_abilities", ability)
        abiDict = self.get_or_make_ability(ability)
        if abiDict["contents"] == []:
            logger.warn("validate_abilities",
                        "No contents found for " + ability)
        # TODO check if spendable
        time.sleep(1)
