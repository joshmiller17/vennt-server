# Josh Aaron Miller 2021
# VenntDB methods for Abilities

import venntdb
import webscraper
import time
import ability as Ability
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("db_abilities")

# VenntDB Methods


def add_ability(self, username, character_id, abiDict):
    self.assert_valid("accounts", username, "characters",
                      character_id, "abilities")
    self.db["accounts"][username]["characters"][character_id]["abilities"].append(
        abiDict)


def get_abilities(self, username, character_id):
    self.assert_valid("accounts", username, "characters",
                      character_id, "abilities")
    return [abiDict["name"] for abiDict in self.db["accounts"][username]["characters"][character_id]["abilities"]]


def get_ability(self, username, character_id, ability):
    self.assert_valid("accounts", username, "characters",
                      character_id, "abilities")
    for abiDict in self.db["accounts"][username]["characters"][character_id]["abilities"]:
        if ability == abiDict["name"]:
            return abiDict
    return None


def get_cached_ability(self, name):
    for ability in self.db["ability_cache"]:
        if ability is not None:
            if name == ability["name"]:
                return ability
    return None


def cache_ability(self, abiDict):
    self.db["ability_cache"][self.db["ability_cache_index"]] = abiDict
    self.db["ability_cache_index"] += 1
    if self.db["ability_cache_index"] > MAX_ABILITY_CACHE:
        self.db["ability_cache_index"] = 0


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
    cached = self.get_cached_ability(name)
    if cached is not None:
        return cached
    approximations, URL, path = self.find_ability(name)
    if len(approximations) != 1:
        raise AssertionError("Bad call to db_abilities.get_or_make_ability, incorrect number of approximations")
    contents = webscraper.get_ability_contents(approximations[0], URL)
    if contents == []:
        pass  # TODO?
    new_ability = Ability.make_ability(contents, path)
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
