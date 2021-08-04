# vennt-server

A headless server for making API calls to the Vennt database.

# API Documentation

All communications with the server are done via standard POST and GET calls. Authentication is done via POST which gives you an `auth_token` that can be used to make GET calls. Note that all interactions with the API are case-sensitive. See `example.py` for an example of API calls. Calls follow standard URL parsing, i.e., `<baseurl>/request_type?arg1=val1&arg2=val2...`

All API calls return a JSON with these keys:

- `success`: whether the operation was successful
- `info`: on failure, why the operation failed

Each method describes additional JSON keys provided, if any.

## Data Types

- `attr`: Valid attributes are AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, MAX_HERO, INIT, SPEED, XP, SP, MAX_BULK, GIFT
- `role`: Valid roles are "player", "GM", and "spectator"
- `<rollstr>`: Any key marked as `<rollstr>` requires a dice roll in standard die roll notation, e.g. "1d6+6". Comments can go in brackets. For full documentation on possible parses, see the [Python d20 library](https://pypi.org/project/d20/).

## Meta / Accounts

### Create an account

POST:

- `register`: desired username
- `password`: desired password

Additional keys returned:

- `auth_token`: on success, your authentication token for making GET calls

### Login

- `login`: username
- `password`: password

Additional keys returned:

- `auth_token`: on success, your authentication token for making GET calls

### Logout

GET:

- `auth_token`: auth token

The operation succeeding means that `auth_token` was valid prior to logout.

## Characters

### Create a character

GET:

- `auth_token`: auth token
- `name` : desired character name

Optional args:

- `attr` : attribute value, see Data Types above

Additional keys returned: -`id`: on success, the unique ID of your new character

### Get characters

GET:

- `auth_token`: auth token

Additional keys returned: -`value`: on success, returns a list of IDs for your characters

### Get character details

GET:

- `auth_token`: auth token
- `id` : character ID

Additional keys returned:

- `value`: on success, returns your character (JSON)

### Set an attribute

GET:

- `auth_token`: auth token
- `char_id` : character ID
- `attr` : attribute name
- `value` : attribute value

### Get an attribute

GET:

- `auth_token`: auth token
- `char_id` : character ID
- `attr` : attribute name

Additional keys returned:

- `value`: the attribute value

## Abilities

### Lookup ability

GET:

- `auth_token`: auth token
- `name` : ability name

When a partial match is provided, the lookup will succeed if exactly one match is found, by assuming that match.

Additional keys returned: -`matches` (on failure): The list of abilities which contain your query as a substring.

### Add ability

GET:

- `auth_token`: auth token
- `id`: character ID
- `name` : ability name

# TODO FIXME documentation from here and below is out of date, needs to be formatted as above

### Get abilities

GET: `<baseURL>/get_abilities?q={"auth_token":"<auth_token>", "id":"<character_id>"}`

Additional keys returned: -`value` (on success): The list of names of your abilities.

### Get ability

GET: `<baseURL>/get_ability?q={"auth_token":"<auth_token>", "id":"<character_id>", "name":"<ability_name>"}`

Additional keys returned:

- `value` (on success): A dictionary describing your ability.
  - `purchase`: The cost to purchase the ability (str)
  - `expedited`: Who the ability is expedited for (str)
  - `unlocks`: What is unlocked by this ability (str)
  - `prereq`: What is listed as prerequisites for this ability (str)
  - `mp_cost`: For spells, the MP costs for this ability as a list of 3 numbers (half, normal, double)
  - `cast_dl`: For spells, the DL to cast this ability as a list of 3 numbers (half, normal, double)
  - `range`: For spells, the spell's range (str)
  - `build_dc`: For tinker devices, the DC to build (str)
  - `build_time`: For tinker devices, the time to build (str)
  - `effect`: The description of the ability (str)
  - `activation`: The human-readable cost to activate this ability (str)
  - `cost`: The Activation cost parsed into a dict
    - `A`: Actions
    - `R`: Reactions
    - `M`: MP
    - `V`: Vim
    - `P`: Hero Points
    - `Attack`: If key is present, this ability is part of an attack -- the parser currently does not distinguish between ranged and melee attacks
    - `Passive`: If key is present, this ability is passive
    - `Special`: Anything which cannot be currently parsed, e.g. "3\* Actions" or "X Vim"

## Initiative

### Reset turn order

GET: `<baseURL>/reset_turn_order?q={"auth_token":"<auth_token>", "campaign_id":"<campaign_id>"}`

### Add a turn

GET: `<baseURL>/add_turn?q={"auth_token":"<auth_token>", "campaign_id":"<campaign_id>", "id":"<entity_id>", "value":"<num>"}`

### Advance turn order

GET: `<baseURL>/next_turn?q={"auth_token":"<auth_token>", "campaign_id":"<campaign_id>"}`

### Get turn order

GET: `<baseURL>/get_turn_order?q={"auth_token":"<auth_token>", "campaign_id":"<campaign_id>"}`

Additional keys returned: -`value` (on success): The dictionary of turns as a mapping of initiative rolls to entity IDs

### Get current turn

GET: `<baseURL>/get_current_turn?q={"auth_token":"<auth_token>", "campaign_id":"<campaign_id>"}`

Additional keys returned: -`value` (on success): The entity ID of whose turn it is

## Inventory

### Add an item

GET: `<baseURL>/add_item?q={"auth_token":"<auth_token>", "name":"itemname", "bulk":"<num>", "desc":"item description"}`

Additional keys returned: -`id`: on success, the unique ID of your new item

### View items

GET: `<baseURL>/view_items?q={"auth_token":"<auth_token>"}`

Additional keys returned: -`value`: on success, a list of item dictionaries

- `name`: item name
- `bulk`: the item's bulk value
- `desc`: the item's description

### Remove item

GET: `<baseURL>/remove_item?q={"auth_token":"<auth_token>", "id":"<item_id>"}`

### Add weapon

GET: `<baseURL>/add_weapon?q={"auth_token":"<auth_token>", "name":"weapon_name", "attr":"ATTR", "dmg": "<rollstr>" [, "mods" : { "key" : value } }`

Modifiers go in the `mods` dict, such as `"burning" : "1d6"`. Weapons added are account-specific.

### Get weapon

GET: `<baseURL>/get_weapon?q={"auth_token":"<auth_token>", "name":"weapon_name"}`

The `get_weapon` call can also retrieve standard Vennt weapons like `Blade` and `Rifle`.

Additional keys returned:

- `weapon`: on success, a weapon dictionary
  - `name`: the weapon's name
  - `attr`: the weapon's attribute
  - `dmg`: the weapon's damage
  - `mods` the weapon's modifiers, as a dictionary of key/value pairs

### Remove weapon

GET: `<baseURL>/remove_weapon?q={"auth_token":"<auth_token>", "name":"weapon_name"}`

## Enemies

### Create an enemy

GET: `<baseURL>/create_enemy?q={"auth_token":"<auth_token>", "name":"myfirstenemy"[,"ATTR":"<num>"...]}`

Setting attribute properties are optional.

Additional keys returned: -`id`: on success, the unique ID of your new enemy

## Campaigns

### Create a campaign

GET: `<baseURL>/create_campaign?q={"auth_token":"<auth_token>", "name":"myfirstcampaign"}`

Additional keys returned: -`campaign_id`: on success, the unique ID of your new campaign

### Get campaigns

GET: `<baseURL>/get_campaigns?q={"auth_token":"<auth_token>"}`

Additional keys returned: -`value`: on success, returns a list of IDs for your campaigns

### Invite someone to a campaign

GET: `<baseURL>/send_campaign_invite?q={"auth_token":"<auth_token>", "campaign_id": "<campaign_id>", "username":"<recipient>"}`

### View active campaign invites

GET: `<baseURL>/view_campaign_invites?q={"auth_token":"<auth_token>"}`

Additional keys returned:

- `value`: list of campaign invites
  - `from`: username of inviter
  - `campaign_id`: campaign ID

### Accept campaign invite

GET: `<baseURL>/accept_campaign_invite?q={"auth_token":"<auth_token>","campaign_id":"<campaign_id>"}`

### Decline campaign invite

GET: `<baseURL>/decline_campaign_invite?q={"auth_token":"<auth_token>","campaign_id":"<campaign_id>"}`

### Set campaign role

You must be the campaign owner to set a role.
GET: `<baseURL>/set_role?q={"auth_token":"<auth_token>","campaign_id":"<campaign_id>", "username":"<target>","role":"[GM/player]"}`

### Get campaign role

You must be the campaign owner or a member of the campaign to view someone's role.
GET: `<baseURL>/set_role?q={"auth_token":"<auth_token>", "campaign_id":"<campaign_id>", "username":"<target>"}`

Additional keys returned:

- `value`: the user's role (GM or player)

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
