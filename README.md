# vennt-server
A headless server for making API calls to the Vennt database.


# API Documentation
All communications with the server are done via JSON. Authentication is done via POST which gives you an `auth_token` that can be used to make GET calls. Note that all interactions with the API are case-sensitive.

See `example.py` for an example of API calls.

All API calls return a JSON with these keys:
- `success`: whether the operation was successful
- `info`: on failure, why the operation failed

Each method describes additional JSON keys provided, if any.

## Data Types
- `attr`: Valid attributes are AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, HERO, INIT, SPEED, XP, SP
- `role`: Valid roles are "player" and "GM"
- `<rollstr>`: Any key marked as `<rollstr>` requires a dice roll in standard die roll notation, e.g. "1d6+6". Comments can go in brackets. For full documentation on possible parses, see the [Python d20 library](https://pypi.org/project/d20/).

## Meta / Accounts

### Create an account
POST: `{"register":"myusername","password":"mypassword"}`

Additional keys:
- `auth_token`: on success, your authentication token for making GET calls

### Login
POST: `{"login":"myusername","password":"mypassword"}`

Additional keys:
- `auth_token`: on success, your authentication token for making GET calls

### Logout
GET: `<baseURL>/logout?q={"auth_token":"<auth_token>"}`

The operation succeeding means that `auth_token` was valid prior to logout.


## Characters

### Create a character
GET: `<baseURL>/create_character?q={"auth_token":"<auth_token>", "name":"myfirstcharacter"[,"ATTR":"<num>"...]}`

Setting attribute properties are optional.

Additional keys:
-`id`: on success, the unique ID of your new character

### Get characters
GET: `<baseURL>/get_characters?q={"auth_token":"<auth_token>"}`

Additional keys:
-`value`: on success, returns a list of IDs for your characters

### Get character details
GET: `<baseURL>/get_character?q={"auth_token":"<auth_token>"}`

Additional keys:
- `value`: on success, returns your character (JSON)

### Set an attribute
GET: `<baseURL>/set_attr?q={"auth_token":"<auth_token>", "char_id":"<character_id>", "attr":"ATTR", "value":"<num>"}`


### Get an attribute
GET: `<baseURL>/get_attr?q={"auth_token":"<auth_token>", "char_id":"<character_id>", "attr":"ATTR"}`

Additional keys:
- `value`: the attribute value

## Abilities

### Lookup ability
GET: `<baseURL>/add_item?q={"auth_token":"<auth_token>", "name":"abilityname"}`

When a partial match is provided, the lookup will succeed if exactly one match is found, by assuming that match.

Additional keys:
-`matches` (on failure): The list of abilities which contain your query as a substring.

## Inventory

### Add an item
GET: `<baseURL>/add_item?q={"auth_token":"<auth_token>", "name":"itemname", "bulk":"<num>", "desc":"item description"}`

Additional keys:
-`id`: on success, the unique ID of your new item

### View items
GET: `<baseURL>/view_items?q={"auth_token":"<auth_token>"}`

Additional keys:
-`value`: on success, a list of item dictionaries
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

Additional keys:
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

Additional keys:
-`id`: on success, the unique ID of your new enemy

## Campaigns

### Create a campaign
GET: `<baseURL>/create_campaign?q={"auth_token":"<auth_token>", "name":"myfirstcampaign"}`

Additional keys:
-`campaign_id`: on success, the unique ID of your new campaign

### Get campaigns
GET: `<baseURL>/get_campaigns?q={"auth_token":"<auth_token>"}`

Additional keys:
-`value`: on success, returns a list of IDs for your campaigns

### Invite someone to a campaign
GET: `<baseURL>/send_campaign_invite?q={"auth_token":"<auth_token>", "campaign_id": "<campaign_id>", "username":"<recipient>"}`

### View active campaign invites
GET: `<baseURL>/view_campaign_invites?q={"auth_token":"<auth_token>"}`

Additional keys:
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

Additional keys:
- `value`: the user's role (GM or player)



# Server Documentation


### Running the server
`py -3 venntserver.py vennt.db`

### Adding a new method to the DB
Whenever a new function is added to the DB that is not in venntdb.py, it must also be imported at the top of the class

### Organization of the database
venntDB.db is organized in this way:

- `accounts`: a map of usernames to accounts
  - `characters`: a map of character IDs to character dictionaries
    - Includes `name`, `id`, and many attributes (see `Data Types` in API documentation)
  - `campaign_invites`: a list of campaign invites
    - `from`: username of sender
    - `id`: campaign ID
  - `campaigns`: a list of campaign IDs owned by the user
  - `joined_campaigns`: a list of campaign IDs joined by the user
- `campaigns`: a map of campaign IDs to campaign dictionaries
- `weapons`: a dictionary of standard weapons read in from `weapons.json`
- `abilities`: a dictionary of abilities read in from `abilities.json` which is scraped using `scrapePaths.py`
- `ability_cache`: a storage of ability objects cached on query
- `ability_cache_index`: the index of the oldest used cache slot in `ability_cache`
