# Josh Aaron Miller 2021
# Web scraping helper file via beautiful soup

import time, requests, datetime, re
from bs4 import Tag, BeautifulSoup

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
		# should add to cache here or no?
		return self.respond({"success":True, "value":ability})

# Returns list of matches and URL string (if found)
def find_ability(self, name):
	name = name.replace("'", "’") # Wiki uses smart quotes
	logger.log("find_ability", "Looking for " + name)
	approximations, URL, _ = self.server.db.find_ability(name)
	return approximations, URL

# Returns contents of ability as list of lines
def get_ability_contents(ability, URL):
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	found_match = False
	contents = []
	last_had_newline = False
	best_match = 999
	for hit in soup.find_all('p'):
		text = hit.get_text()
		text = text.replace("’", "'") # I hate smart quotes
		# Goes through the whole page, takes the *shortest* valid line which matches the given description
		if ability in text and len(text) < best_match:
			found_match = True
			best_match = len(text)
			contents = []
		if found_match and (text.isspace() or (text.startswith('\n') and last_had_newline)):
			found_match = False
		if found_match:
			# special case to try to pull out flavor text in italic
			if hit.i != None and hit.i.get_text() == text.replace("\n", ""):
				logger.log("get_ability_contents", hit.i.get_text())
				contents.append("Flavor: " + text)
			else:
				contents.append(text)
			# special case for capturing lists
			if isinstance(hit.next_sibling.next_sibling, Tag) and hit.next_sibling.next_sibling.name == "ul":
				for li in hit.next_sibling.next_sibling.children:
					if (isinstance(li, Tag) and li.name == "li"):
						contents.append("- " + li.get_text() + "\n")
			if text.endswith('\n'):
				last_had_newline = True
			else:
				last_had_newline = False
	return contents