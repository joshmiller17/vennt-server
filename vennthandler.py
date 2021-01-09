import BaseHTTPServer
import hashlib, json, sys, time, urlparse

PATH_REGISTER = '/register'
PATH_REPORT = '/reportMatch'
PATH_REQUEST = '/requestMatch'
PATH_INFO = '/info'

KEY_ID = 'id'
KEY_TOKEN = 'token'
KEY_TYPE = 'type'


# OPTIONAL KEYS



class VenntHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def log_message(self, format, *args):
		sys.stderr.write("%s - - [%s] %s\n" %
						 (hashlib.md5('venntserver' + self.client_address[0]).hexdigest(),
						  self.log_date_time_string(),
						  format % args))

	def _send_success(self, data):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()

		if data != None:
			result = { 'result': True, 'data': data }
			self.wfile.write(json.dumps(result))
		
	def _send_error(self, data):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()

		if data != None:
			result = { 'result': False, 'data': data }
			self.wfile.write(json.dumps(result))

	def _check_keys(self, args, keys_req, keys_opt=[]):
		for key in keys_req:
			if not args.has_key(key):
				return 'Missing required key ' + key + '.'
		for key in args.iterkeys():
			if key not in keys_req and key not in keys_opt:
				return 'Unknown key ' + key + '.'
		return None

	def do_HEAD(self):
		parse = urlparse.urlparse(self.path)
		path = parse.path

		if path in [PATH_REGISTER, PATH_REPORT, PATH_REQUEST, PATH_INFO]:
			return self._send_success(None)
		else:
			return self._send_error(None)
			
	def do_POST(self):
		print "do_POST received"
		self.do_GET()

	def do_GET(self):
		parse = urlparse.urlparse(self.path)
		path = parse.path

		# get the JSON arguments
		query = urlparse.parse_qs(parse.query)

		if not query.has_key('q'):
			return self._send_error('Missing query q.')

		if len(query['q']) != 1:
			return self._send_error('Multiple query q.')

		try:
			args = json.loads(query['q'][0])
		except ValueError:
			return self._send_error('Error parsing JSON.')

		# handle different path requests
		if path == PATH_REPORT:
			# check args
			key_error = self._check_keys(args, [KEY_TOKEN, KEY_ID1, KEY_ID2, KEY_SCORE1])
			if key_error:
				return self._send_error(key_error)
			
			# get arg match token
			token = args[KEY_TOKEN]

			# get arg id1
			id1 = args[KEY_ID1]

			# get arg id2
			id2 = args[KEY_ID2]

			# get arg score1
			try:
				score1 = float(args[KEY_SCORE1])
			except ValueError:
				return self._send_error('Score is not a float.')

			# playtime = float(args[KEY_TIME])

			# check if this is a duplicate match
			if self.server._db.get_match(token):
				return self._send_error('Duplicate match ' + token + '.')

			# get the first entity in the match and its rating
			e1 = self.server._db.get_entity(id1)
			if e1 == None:
				return self._send_error('No entity ' + id1 + '.')
			r1 = e1['mmdata']
	 
			# get the second entity in the match and its rating
			e2 = self.server._db.get_entity(id2)
			if e2 == None:
				return self._send_error('No entity ' + id2 + '.')
			r2 = e2['mmdata']

			player_skills = set(e1['skills'])
			#print 'Init pls: ', player_skills, '\tid: ', e1['id']
			level_skills = set(e2['skills'])

			#print 'Old ratings: ', id1, e1['mmdata']['rating'], id2, e2['mmdata']['rating']

			old1, old2 = e1['mmdata']['rating'], e2['mmdata']['rating']

			# return success
			return self._send_success(match)

		elif path == PATH_REQUEST:
			
			# check arguments
			key_error = self._check_keys(args, [KEY_ID], [KEY_NUMRECS, KEY_RECVARIANCE])
			if key_error:
				return self._send_error(key_error)

			# get arg id
			id = args[KEY_ID]

			# playtime = args[KEY_TIME]

			
			return self._send_success(ret)

		elif path == PATH_INFO:
			# check args
			key_error = self._check_keys(args, [KEY_ID])
			if key_error:
				return self._send_error(key_error)

			# get arg id
			id = args[KEY_ID]

			# look up entity in db
			result = self.server._db.get_entity(id)

			# return entity, if found, otherwise error
			if result:
				return self._send_success(result)
			else:
				return self._send_error('Unrecognized id ' + id + '.')
			
		else:
			# return error for unrecognized request
			return self._send_error('Bad request path.')
