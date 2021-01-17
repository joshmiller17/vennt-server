# Josh Aaron Miller 2021
# Helper functions for managing stats and rolls

import venntdb, random, math
from constants import *

def d6():
	return random.randint(1,6)

def half(num):
	return int(math.floor (int(num)/2) )
	
def clean_modifier(v):
	if isinstance(v, str):
		v = v.replace("+", "")
	return int(v)
	
def compare_hp(current, max):
	percent = (1.0 * current) / (1.0 * max)
	if percent > 0.9:
		return "healthy"
	if percent >  0.7:
		return "scratched"
	if percent > 0.5:
		return "hurt"
	if percent > 0.3:
		return "bloodied"
	if percent > 0.1:
		return "severely wounded"
	if percent > 0:
		return "near death"
	return "dead"