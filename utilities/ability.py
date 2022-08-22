# Josh Aaron Miller 2021
# Ability class

import re
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("ability")
	
# Input: ability contents
# Output: Ability dict
def make_ability(contents, path):
	if contents == []:
		return {
			ABI_DICT_NAME:"NULL",
			ABI_DICT_EFFECT: "",
			ABI_DICT_CONTENTS:[],
			ABI_DICT_ACTIVATION:"Passive",
			ABI_DICT_COST: {"Passive": True}
		}

	abiDict = {}
	abiDict[ABI_DICT_CONTENTS] = contents

	for line in contents:
		if line.startswith("Cost:"):
			abiDict[ABI_DICT_PURCHASE] = parse_purchase_cost(line)
		elif line.startswith("Expedited for:"):
			abiDict[ABI_DICT_EXPEDITED] = parse_expedited(line)
		elif line.startswith("Unlocks:"):
			abiDict[ABI_DICT_UNLOCKS] = parse_unlocks(line)
		elif line.startswith("Partially Unlocks:"):
			abiDict[ABI_DICT_PARTIAL_UNLOCKS] = parse_partial_unlocks(line)
		elif line.startswith("Prereq"):
			abiDict[ABI_DICT_PREREQ] = parse_prereq(line)
		elif line.startswith("MP Cost:"):
			abiDict[ABI_DICT_MP_COST] = parse_mp_costs(line)
		elif line.startswith("Casting DL:"):
			abiDict[ABI_DICT_CAST_DL] = parse_casting_dl(line)
		elif line.startswith("DC:"):
			abiDict[ABI_DICT_BUILD_DC] = parse_dc(line)
		elif line.startswith("Build time:"):
			abiDict[ABI_DICT_BUILD_TIME] = parse_build_time(line)
		elif line.startswith("Activation:"):
			abiDict[ABI_DICT_COST] = parse_activation_cost(line)
			abiDict[ABI_DICT_ACTIVATION] = line[12:-1]
		elif line.startswith("Range:"):
			abiDict[ABI_DICT_RANGE] = parse_range(line)
		elif "is not required for the Path Completion Bonus" in line:
			abiDict[ABI_DICT_NOT_REQ] = True
		elif line.startswith("Flavor:"):
			abiDict[ABI_DICT_FLAVOR] = parse_flavor(line)
		elif ABI_DICT_NAME in abiDict:
			if ABI_DICT_EFFECT not in abiDict:
				abiDict[ABI_DICT_EFFECT] = ""
			abiDict[ABI_DICT_EFFECT] += line

		if ABI_DICT_NAME not in abiDict:
			abiDict[ABI_DICT_NAME] = line.replace("\n", "") # chop off all \n

	if ABI_DICT_COST not in abiDict and ABI_DICT_ACTIVATION not in abiDict:
		abiDict[ABI_DICT_COST] = {"Passive": True} # default to Passive if nothing given
		abiDict[ABI_DICT_ACTIVATION] = "Passive"

	abiDict[ABI_DICT_PATH] = path
			
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

def parse_partial_unlocks(line):
	return line[19:-1] # just get string for now
	
def parse_prereq(line):
	logger.log("parse_prereq", line[12:14])
	if line[12] == 's':
		return line[15:-1] # just get string for now
	else:
		return line[14:-1] # just get string for now

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
			if ABI_DICT_ACTIVATION not in match: # skip "capture all" group
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

def parse_flavor(line):
	return line[8:-1] # just get string for now


def is_valid(abiDict, must_be_custom=False):
	req_keys = [ABI_DICT_NAME, ABI_DICT_EFFECT, ABI_DICT_COST]
	if must_be_custom:
		req_keys.append(ABI_DICT_SPECIAL_TYPE)
	valid_keys = {
		ABI_DICT_CONTENTS: list,
		ABI_DICT_NAME: str,
		ABI_DICT_PURCHASE: str,
		ABI_DICT_EXPEDITED: str,
		ABI_DICT_UNLOCKS: str,
		ABI_DICT_PARTIAL_UNLOCKS: str,
		ABI_DICT_PREREQ: str,
		ABI_DICT_MP_COST: str,
		ABI_DICT_CAST_DL: str,
		ABI_DICT_BUILD_DC: str,
		ABI_DICT_BUILD_TIME: str,
		ABI_DICT_COST: dict,
		ABI_DICT_ACTIVATION: str,
		ABI_DICT_RANGE: str,
		ABI_DICT_NOT_REQ: str,
		ABI_DICT_FLAVOR: str,
		ABI_DICT_EFFECT: str,
		ABI_DICT_PATH: str,
		ABI_DICT_SPECIAL_TYPE: str,
		ABI_DICT_AP: int,
		ABI_DICT_COMMENT: str,
	}
	for key in req_keys:
		if key not in abiDict:
			# Missing required key
			return False
	for key, val in abiDict.items():
		if key not in valid_keys or not isinstance(val, valid_keys[key]):
			# Has extra, invalid key or the key has an invalid type
			return False
	return True
	
def is_spendable(abiDict):
	if ABI_DICT_COST not in abiDict or abiDict[ABI_DICT_COST] == {}:
		return False
	for key, val in abiDict[ABI_DICT_COST].items():
		if key in ['A', 'R', 'V', 'M', 'P']:
			return True
	return False
