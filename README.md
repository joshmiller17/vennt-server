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
  - `members`: a map of usernames to roles
  - `entities`: a map of character / enemy IDs to information that everyone in the campaign should be able to see
    - `owner`: The entity's owner
    - `name`: The entity's name - copied from the `characters` map
    - `gm_only`: If true, this entity can only be seen by GMs. Useful for adding enemies to a campaign without alerting players
    - `actions`: When in combat, the number of actions this entity has. If the character has actions, they can be spent regardless of whose turn it is
    - `reactions`: When in combat, the number of reactions this entity has
    - `health`: string description of health - this is just used for display. We don't want to provide actual numbers to anyone except the entity's owner
  - `init`: a list of maps containing initiative information regarding entities in the campaign.
    - `roll`: The entity's initiative roll
    - `bonus`: The entity's initiative attribute value
    - `entity_id`: The entity ID
  - `in_combat`: True when we are using initiative
  - `init_index`: Points to the index of the current turn in the `init` list.
  - `init_round`: The round of combat
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
6. Use `python3 venntserver.py --nocert` to run the server locally
7. Use `python3 example.py --verify --nocert` to run examples locally
8. Add the documentation to this README

### Adding a new method to the DB

Whenever a new function is added to the DB that is not in venntdb.py, it must also be imported at the top of the class
