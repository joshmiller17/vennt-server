# Josh Aaron Miller 2021
# VenntDB methods for Initiative

import venntdb, operator
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("db_initiative")

# VenntDB Methods

def reset_turn_order(self, campaign_id):
	self.db["campaigns"][campaign_id]["turns"] = {} # result : entity_id
	self.db["campaigns"][campaign_id]["init_index"] = MAX_INIT
	self.db["campaigns"][campaign_id]["whose_turn"] = None

def add_turn(self, campaign_id, entity_id, result):
	id_type = entity_id[0]
	if id_type != IDType.CHARACTER and id_type != IDType.Enemy:
		raise TypeError("ID {} is not a character or enemy".format(entity_id))
	
	if not "turns" in self.db["campaigns"][campaign_id] or self.db["campaigns"][campaign_id]["turns"] == {}:
		self.reset_turn_order(campaign_id)
	
	self.db["campaigns"][campaign_id]["turns"][result] = entity_id
	
def next_turn(self, campaign_id):
	sorted_turns = sorted(self.db["campaigns"][campaign_id]["turns"].items(), key=operator.itemgetter(0),reverse=True)
	logger.log("next_turn",str(sorted_turns))
	for value, entity_id in sorted_turns:
		if value < self.db["campaigns"][campaign_id]["init_index"]:
			self.db["campaigns"][campaign_id]["init_index"] = value
			self.db["campaigns"][campaign_id]["whose_turn"] = entity_id
			return entity_id
			
	# reached the bottom, wrap around
	self.db["campaigns"][campaign_id]["init_index"] = MAX_INIT
	# TODO things happen at the end of the round
	self.next_turn(campaign_id)
	
def get_turn_order(self, campaign_id):
	return self.db["campaigns"][campaign_id]["turns"]
	
def get_current_turn(self, campaign_id):
	return self.db["campaigns"][campaign_id]["whose_turn"]