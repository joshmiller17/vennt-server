# Josh Aaron Miller 2021
# Vennt HTTP Request Handler

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
import hashlib, json, sys, time
import venntdb, rate_limiter

from api_campaigns import *
from api_characters import *
from api_enemies import *
from api_inventory import *
from api_initiative import *
from api_abilities import *
from api_combat import *
from authentication import *
from webscraper import *
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("webscraper")

class VenntHandler(BaseHTTPRequestHandler):

	def log_message(self, format, *args):
		client_short = hashlib.md5(('venntserver' + self.client_address[0]).encode('utf-8')).hexdigest()[:8]
		logger.log("log_message", "Client {} sent {}".format(client_short, args))

	def respond(self, data):
		if "success" not in data or not data["success"]:
			logger.log("respond", "Request failed: " + str(data))
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()
		self.wfile.write(json.dumps(data).encode('utf-8'))


	def check_keys(self, args, keys_req, keys_opt=[]):
		for key in keys_req:
			if key not in args:
				return 'Missing required key ' + key + '.'
		for key in args.keys():
			if key not in keys_req and key not in keys_opt:
				return 'Unknown key ' + key + '.'
		return None

	def do_HEAD(self):
		if rate_limiter.is_rate_limited(self.client_address[0]):
			return self.respond({"success":False, "info":MSG_TOO_MANY_REQ})
	
		parse = urlparse(self.path)
		path = parse.path
		if len(path) > MAX_REQUEST_SIZE:
			return self.respond({"success":False, "info":MSG_REQ_LARGE})

		if path in [val for key, val in PATHS.items()]:
			return self.respond({"success":True})
		else:
			return self.respond({"success":False})
			
	def do_OPTIONS(self):
			self.send_response(200)
			self.send_header('Access-Control-Allow-Methods', 'OPTIONS, GET, HEAD, POST')
			self.send_header('Access-Control-Allow-Origin','*')
			self.send_header('Access-Control-Allow-Headers', '*')
			self.end_headers()
			
	def do_POST(self):
		if rate_limiter.is_rate_limited(self.client_address[0]):
			return self.respond({"success":False, "info":MSG_TOO_MANY_REQ})
		
		content_length = int(self.headers['Content-Length'])
		if content_length > MAX_REQUEST_SIZE:
			return self.respond({"success":False, "info":MSG_REQ_LARGE})
			
		post_data = self.rfile.read(content_length)
		post_data = post_data.decode('utf-8')
		
		try:
			json_data = json.loads(post_data)
		except:
			self.respond({"success":False,"info":"Bad JSON"})
			return
		
		if "register" in json_data:
			handle_register(self, json_data)
		elif "login" in json_data:
			handle_login(self, json_data)
		else:
			self.respond({"success":False,"info":"POST must contain register or login key"})
			return
		

	def do_GET(self):
		if rate_limiter.is_rate_limited(self.client_address[0]):
			return self.respond({"success":False, "info":MSG_TOO_MANY_REQ})
	
		parse = urlparse(self.path)
		path = parse.path
		if len(path) > MAX_REQUEST_SIZE:
			return self.respond({"success":False, "info":MSG_REQ_LARGE})

		# get the JSON arguments
		query = parse_qs(parse.query)

		if 'q' not in query:
			return self.respond({"success":False, "info":'Missing query q.'})

		if len(query['q']) != 1:
			return self.respond({"success":False, "info":'Multiple query q.'})

		try:
			args = json.loads(query['q'][0])
		except:
			return self.respond({"success":False, "info":'Error parsing JSON'})
			
		logger.log("do_GET", "Args: " + str(args))
			
		if KEY_AUTH not in args:
			return self.respond({"success":False, "info":'Missing required key ' + KEY_AUTH + '.'})
		username = self.server.db.auth.check_and_fetch(self.client_address[0], args[KEY_AUTH])
		if username is None:
			return self.respond({"success":False, "info":MSG_BAD_AUTH})


		
		# ----------------  META -------------------------
		
		if path == PATHS["LOGOUT"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
			
			success = self.server.db.auth.deauthenticate(args[KEY_AUTH])
			return self.respond({"success":success})
			
		# ----------------  ABILITIES -----------------------
		
		elif path == PATHS["LOOKUP_ABILITY"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self.respond(key_error)
				
			return lookup_ability(self, args)
			
		elif path == PATHS["LOOKUP_ABILITY"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self.respond(key_error)
				
			return lookup_ability(self, args) # webscraper
			
		elif path == PATHS["ADD_ABILITY"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self.respond(key_error)
				
			return add_ability(self, args, username)
			
		elif path == PATHS["GET_ABILITIES"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
				
			return self.respond({"success":True, "value":self.server.db.get_abilities(username)})
			
		elif path == PATHS["GET_ABILITY"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
				
			return get_ability(self, args, username)
			
		# -------------  COMBAT -------------------------
		
		elif path == PATHS["GET_UNDO_HISTORY"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)
				
			return get_undo_history(self, args, username)
			
		# -------------  INITIATIVE -------------------------
		
		elif path == PATHS["ADD_TURN"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID, KEY_ID, KEY_VAL])
			if key_error:
				return self.respond(key_error)
				
			return add_turn(self, args, username)
			
		elif path == PATHS["RESET_TURN_ORDER"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)
				
			return reset_turn_order(self, args, username)
			
		elif path == PATHS["NEXT_TURN"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)
				
			return next_turn(self, args, username)
			
		elif path == PATHS["GET_TURN_ORDER"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)
				
			return get_turn_order(self, args, username)
			
		elif path == PATHS["GET_CURRENT_TURN"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)
				
			return get_current_turn(self, args, username)
		
		
		# ----------  INVENTORY / WEAPONS -----------------------
		
		elif path == PATHS["ADD_ITEM"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME, KEY_DESC, KEY_BULK])
			if key_error:
				return self.respond(key_error)
				
			return add_item(self, args, username)
			
		elif path == PATHS["VIEW_ITEMS"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
				
			items = self.server.db.view_items(username)
			return self.respond({"success":True, "value":items})
			
		elif path == PATHS["REMOVE_ITEM"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_ID])
			if key_error:
				return self.respond(key_error)
				
			return self.respond({"success":self.server.db.remove_item(username, args[KEY_ID])})
			
		elif path == PATHS["ADD_WEAPON"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME, KEY_ATTR, KEY_DMG], keys_opt=[KEY_MODS])
			if key_error:
				return self.respond(key_error)
				
			return add_weapon(self, args, username)
			
		elif path == PATHS["REMOVE_WEAPON"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self.respond(key_error)
				
			return self.respond({"success":self.server.db.remove_weapon(username, args[KEY_NAME])})
			
		elif path == PATHS["GET_WEAPON"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self.respond(key_error)
				
			return get_weapon(self, args, username)
		
		# -------------  CHARACTERS -------------------------
		
		elif path == PATHS["CREATE_CHARACTER"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME], keys_opt=ATTRIBUTES)
			if key_error:
				return self.respond(key_error)
			
			return create_character(self, args, username)
		
		elif path == PATHS["SET_ATTR"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_ID, KEY_ATTR, KEY_VAL])
			if key_error:
				return self.respond(key_error)
			
			return set_attr(self, args, username)
			
		elif path == PATHS["GET_ATTR"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_ID, KEY_ATTR])
			if key_error:
				return self.respond(key_error)
			
			return get_attr(self, args, username)
			
		elif path == PATHS["GET_CHARACTERS"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
				
			return self.respond({"success":True, "value":str(self.server.db.get_characters(username))})
			
		elif path == PATHS["GET_CHARACTER"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_ID])
			if key_error:
				return self.respond(key_error)
				
			return self.respond({"success":True, "value":str(self.server.db.get_character(username, args[KEY_ID]))})
			
		# -------------  CAMPAIGNS  -------------------------
			
		elif path == PATHS["CREATE_CAMPAIGN"]:
			# check args
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self.respond(key_error)
			
			return create_campaign(self, args, username)
			
		elif path == PATHS["GET_CAMPAIGNS"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
				
			return self.respond({"success":True, "value":self.server.db.get_campaigns(username)})
			
		elif path == PATHS["SEND_CAMPAIGN_INVITE"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_USERNAME, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)

			return send_campaign_invite(self, args, username)
			
		elif path == PATHS["VIEW_CAMPAIGN_INVITES"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
			
			invites = self.server.db.get_campaign_invites(username)
			return self.respond({"success":True, "value":invites})
			
		elif path == PATHS["ACCEPT_CAMPAIGN_INVITE"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)
			
			return accept_campaign_invite(self, args, username)
			
		elif path == PATHS["DECLINE_CAMPAIGN_INVITE"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID])
			if key_error:
				return self.respond(key_error)

			return decline_campaign_invite(self, args, username)
			
		elif path == PATHS["SET_ROLE"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID, KEY_USERNAME, KEY_ROLE])
			if key_error:
				return self.respond(key_error)
				
			return set_role(self, args, username)
			
		elif path == PATHS["GET_ROLE"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_CAMPAIGN_ID, KEY_USERNAME])
			if key_error:
				return self.respond(key_error)
				
			return get_role(self, args, username)
			
		# -------------  ENEMIES  -------------------------
		
		elif path == PATHS["CREATE_ENEMY"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME], keys_opt=ATTRIBUTES)
			if key_error:
				return self.respond(key_error)
			
			return create_enemy(self, args, username)
			

		elif path in PATHS:
			self.respond({"success":False, "info":"Not yet implemented"})
			
		else:
			# return error for unrecognized request
			return self.respond('Bad request path.')
