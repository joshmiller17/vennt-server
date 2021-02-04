# Josh Aaron Miller 2021
# Ability class

import re

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("ability")
	
# Input: ability contents
# Output: Ability dict
def make_ability(contents):
	abiDict = {}
	abiDict["contents"] = contents

	for line in contents:
		if line.startswith("Cost:"):
			abiDict["purchase"] = parse_purchase_cost(line)
		elif line.startswith("Expedited for:"):
			abiDict["expedited"] = parse_expedited(line)
		elif line.startswith("Unlocks:"):
			abiDict["unlocks"] = parse_unlocks(line)
		elif line.startswith("Prereq"):
			abiDict["prereq"] = parse_prereq(line)
		elif line.startswith("MP Cost:"):
			abiDict["mp_cost"] = parse_mp_costs(line)
		elif line.startswith("Casting DL:"):
			abiDict["cast_dl"] = parse_casting_dl(line)
		elif line.startswith("DC:"):
			abiDict["build_dc"] = parse_dc(line)
		elif line.startswith("Build time:"):
			abiDict["build_time"] = parse_build_time(line)
		elif line.startswith("Activation:"):
			abiDict["cost"] = parse_activation_cost(line)
			abiDict["activation"] = line[12:-1]
		elif line.startswith("Range:"):
			abiDict["range"] = parse_range(line)
		elif "name" in abiDict:
			if "effect" not in abiDict:
				abiDict["effect"] = ""
			abiDict["effect"] += line
		
		if not "name" in abiDict:
			abiDict["name"] = line[:-1] # chop off \n
			
	logger.log("make_ability", str(abiDict))
	return abiDict

def parse_dc(line):
	return line[4:-1] # just get string for now	

def parse_build_time(line):
	return line[12:-1] # just get string for now	

def parse_purchase_cost(line):
	return line[6:-1] # just get string for now

def parse_expedited(line):
	return line[15:-1] # just get string for now
	
def parse_unlocks(line):
	return line[9:-1] # just get string for now
	
def parse_prereq(line):
	logger.log("parse_prereq", line[12:14])
	if line[12] == 's':
		return line[16:-1] # just get string for now
	else:
		return line[15:-1] # just get string for now

def parse_mp_costs(line):
	matches = re.findall("\[ ?(\d*) ?\/ ?(\d*) ?\/ ?(\d*) ?\]", line)
	for match_tuple in matches:
		return match_tuple[0:3]

def parse_casting_dl(line):
	matches = re.findall("\[ ?(\d*) ?\/ ?(\d*) ?\/ ?(\d*) ?\]", line)
	for match_tuple in matches:
		return match_tuple[0:3]

def parse_activation_cost(line):
	cost = {}
	matches = re.findall("Activation: ((?:Passive)|(\d*\**X? Hero Points?)|(\d*\**X? Actions?)|(Attack)|(?:, )|(\d*\**X? Actions?)|(\d*\**X? Reactions?)|(\d*\**X? Vim)|(\d*\**X? MP))*", line)
	for match_tuple in matches:
		#logger.log("parse_activation_cost", "tuple: " + str(match_tuple))
		for match in match_tuple:
			if match == "" or match == ", ":
				continue
			if "Attack" in match: # currently ignoring the distinction of "Ranged Attack" or "Melee Attack"
				cost["Attack"] = True
				continue
			if match == "Passive":
				cost["Passive"] = True
				continue
			if "Activation" not in match: # skip "capture all" group
				match = match.replace("Hero Point", "Point")
				cost_str = match.split(' ')
				type = cost_str[1][0] # first char of word
				amt = cost_str[0]
				try:
					cost[type] = int(amt)
				except:
					cost["Special"] = match # captures X Vim, 3* MP, etc -- deal with this later
	return cost

def parse_range(line):
	return line[7:-1] # just get string for now


def is_valid(abiDict):
	req_keys = ["name", "effect", "cost"]
	for key in req_keys:
		if key not in abiDict:
			return False
	return True
	
def is_spendable(abiDict):
	if "cost" not in abiDict or abiDict["cost"] == {}:
		return False
	for key, val in abiDict["cost"].items():
		if key in ['A', 'R', 'V', 'M', 'P']:
			return True
	return False