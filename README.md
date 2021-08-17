# vennt-server

A headless server for making API calls to the Vennt database.

# API Documentation

API documentation can be found in API.md.

# Server Documentation

### Running the server

`py -3 venntserver.py vennt.db --nocert`
Or `py -3 venntserver.py --help` for more information on running the server securely.

### Organization of the database

venntDB.db is organized in this way:

- `accounts`: a map of usernames to accounts
  - `characters`: a map of character IDs to character dictionaries
    - Includes `name`, `id`, and many attributes (see `Data Types` in API documentation)
    - Includes `items`; each item has:
      - `name`: item name
      - `bulk`: item bulk (numeric)
      - `desc`: item description
  - `campaign_invites`: a list of campaign invites
    - `from`: username of sender
    - `id`: campaign ID
  - `campaigns`: a list of campaign IDs joined by the user
- `campaigns`: a map of campaign IDs to campaign dictionaries
  - 'members': a map of usernames to roles
- `weapons`: a dictionary of standard weapons read in from `weapons.json`
- `abilities`: a dictionary of abilities read in from `abilities.json` which is scraped using `scrapePaths.py`
- `ability_cache`: a storage of ability objects cached on query
- `ability_cache_index`: the index of the oldest used cache slot in `ability_cache`

## Contributing

### Adding a new API call

1. Add the data handling logic to venntdb.py (see Adding a new method to the DB below)
2. Add the API call to the relevant api_x.py (even if it's a one-line function); **the burden of permission-checking must happen at this step**
3. Add the API call to vennthandler.py
4. Add the API call to constants.py
5. Add an example to example.py, test the new function locally
6. Add the documentation to this README

### Adding a new method to the DB

Whenever a new function is added to the DB that is not in venntdb.py, it must also be imported at the top of the class
