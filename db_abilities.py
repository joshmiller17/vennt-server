# Josh Aaron Miller 2021
# VenntDB methods for Abilities

import venntdb
from constants import *

# VenntDB Methods

def get_cached_ability(self, name):
	for ability in self.db["ability_cache"]:
		if name == ability.name:
			return ability
	return None
		
def cache_ability(self, abiObj):
	self.db["ability_cache"][self.db["ability_cache_index"]] = abiObj
	self.db["ability_cache_index"] += 1
	if self.db["ability_cache_index"] > MAX_ABILITY_CACHE:
		self.db["ability_cache_index"] = 0

def find_ability(self, ability_name):
	approximations = []
	URL = ""
	for a in self.db["abilities"]:
		if ability_name.lower() in a["ability"].lower(): # approximate
			if a["ability"].lower() == ability_name.lower():
				URL = a["url"]
				return [a["ability"]], URL
			else:
				approximations.append(a["ability"])
				URL = a["url"]
	return approximations, URL