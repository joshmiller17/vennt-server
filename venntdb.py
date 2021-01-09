import cPickle, json, os



class VenntDB:
	def dump(self):
		pass

	def get_entity(self, id):
		return None

	def set_entity(self, entity):
		pass
	
	def list_entities(self, type):
		return []



class VenntDBDict(VenntDB):
	def __init__(self, filename):
		self._filename = filename

		if os.path.exists(self._filename):
			self._entities  = cPickle.load(open(self._filename, 'rb'))
		else:
			self._entities = {}

	def _save_db(self):
		cPickle.dump((self._entities), open(self._filename, 'wb'), cPickle.HIGHEST_PROTOCOL)
		
	def dump(self):
		to_dump = {
			'entities': self._entities.values()
			}
		print json.dumps(to_dump, indent=4, separators=(',', ': '), sort_keys=True)

	def get_entity(self, id):
		if self._entities.has_key(id):
			return self._entities[id]
		else:
			return None

	def set_entity(self, entity):
		id = entity['id']

		self._entities[id] = entity
		self._save_db()

	def list_entities(self, type):
		ret = []
		for id, entity in self._entities.iteritems():
			if type == entity['type']:
				ret.append(entity)
		return ret
