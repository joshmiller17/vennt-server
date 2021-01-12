# Josh Aaron Miller 2021
# Vennt DB Dump

import sys
import venntdb


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('usage: %s [db]' % sys.argv[0])
		sys.exit(-1)

	db = sys.argv[1]

	db = venntdb.VenntDB(db)
	db.dump()
