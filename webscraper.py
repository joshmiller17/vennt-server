# Josh Aaron Miller 2021
# Web scraping helper file via beautiful soup

import time, requests, datetime, re
from bs4 import BeautifulSoup

import venntdb
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("webscraper")


# VenntHandler methods

def lookup_ability(self, args):
	name = args[KEY_NAME]
	
	abiDict = self.server.db.get_cached_ability(name)
	if abiDict is not None:
		logger.log("lookup_ability", "cache hit")
		return self.respond({"success":True, "value":abiDict["contents"]})
	
	logger.log("lookup_ability", "cache miss")
	approximations, URL = find_ability(self, name)
	if len(approximations) == 0:
		return self.respond({"success":False, "info":"No such ability"})
	elif len(approximations) > 1:
		return self.respond({"success":False, "info":"More than one match", "matches":approximations})
	else:
		ability = "\n".join(get_ability_contents(approximations[0], URL))
		# TODO create ability object and add to cache
		return self.respond({"success":True, "value":ability})

# Returns list of matches and URL string (if found)
def find_ability(self, name):
	name = name.replace("'", "’") # Wiki uses smart quotes
	logger.log("find_ability", "Looking for " + name)
	return self.server.db.find_ability(name)
	
def ability_exists(self, *args):
	approximations, URL = self.find_ability(" ".join(args[:]))
	if len(approximations) != 1:
		return False
	return True

# Returns contents of ability as list of lines
def get_ability_contents(ability, URL):
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	found = False
	contents = []
	last_had_newline = False
	best_match = 999
	for hit in soup.find_all('p'):
		text = hit.get_text()
		text = text.replace("’", "'") # I hate smart quotes
		if ability in text and len(text) < best_match: # Goes through the whole page, takes the *shortest* valid line which matches the given description
			found = True
			best_match = len(text)
			contents = []
		if found and (text.isspace() or (text.startswith('\n') and last_had_newline)):
			found = False
		if found:
			contents.append(text)
			if text.endswith('\n'):
				last_had_newline = True
			else:
				last_had_newline = False
	return contents