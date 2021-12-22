# API Documentation

All communications with the server are done via standard POST and GET calls. Authentication is done via POST which gives you an `auth_token` that can be used to make GET calls. Note that all interactions with the API are case-sensitive. See `example.py` for an example of API calls. Calls follow standard URL parsing, i.e., `<baseurl>/request_type?arg1=val1&arg2=val2...`

All API calls return a JSON with these keys:

- `success`: whether the operation was successful
- `info`: on failure, why the operation failed

Each method describes additional JSON keys provided, if any.

## Data Types

- `attr`: Valid attributes are AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, HERO, MAX_HERO, INIT, SPEED, XP, SP, MAX_BULK, GIFT
- `role`: Valid roles are "player", "GM", and "spectator"
- `<rollstr>`: Any key marked as `<rollstr>` requires a dice roll in standard die roll notation, e.g. "1d6+6". Comments can go in brackets. For full documentation on possible parses, see the [Python d20 library](https://pypi.org/project/d20/).

## Meta / Accounts

### Create an account

POST: `<baseURL>`

- `register`: desired username
- `password`: desired password

Additional keys returned:

- `auth_token`: on success, your authentication token for making GET calls

### Login

POST: `<baseURL>`

- `login`: username
- `password`: password

Additional keys returned:

- `auth_token`: on success, your authentication token for making GET calls

### Logout

GET: `<baseURL>/logout`

- `auth_token`: auth token

The operation succeeding means that `auth_token` was valid prior to logout.

## Characters

### Create a character

GET: `<baseURL>/create_character`

- `auth_token`: auth token
- `name`: desired character name

Optional args:

- `attr`: attribute value, see Data Types above
- `gift`: one of "Alertness", "Craft", "Alacrity", "Finesse", "Mind", "Magic", "Rage", "Science", "Charm", or "None". If not provided, we default to "None"

Additional keys returned: -`id`: on success, the unique ID of your new character

### List characters

GET: `<baseURL>/get_characters`

- `auth_token`: auth token

Additional keys returned: -`value`: on success, returns a list of IDs for your characters

### Get character details

GET: `<baseURL>/get_character`

- `auth_token`: auth token
- `id`: character ID

Additional keys returned:

- `value`: on success, returns your character (JSON)

### Set an attribute

GET: `<baseURL>/set_attr`

- `auth_token`: auth token
- `char_id`: character ID
- `attr`: attribute name
- `value`: attribute value

### Get an attribute

GET: `<baseURL>/get_attr`

- `auth_token`: auth token
- `char_id`: character ID
- `attr`: attribute name

Additional keys returned:

- `value`: the attribute value

## Abilities

### Lookup ability

GET: `<baseURL>/lookup_ability`

- `auth_token`: auth token
- `name`: ability name

When a partial match is provided, the lookup will succeed if exactly one match is found, by assuming that match.

Additional keys returned: -`matches` (on failure): The list of abilities which contain your query as a substring.

### Add ability

GET: `<baseURL>/add_ability`

- `auth_token`: auth token
- `id`: character ID
- `name`: ability name

### Get abilities

GET: `<baseURL>/get_abilities`

- `auth_token`: auth token
- `id`: character ID

Additional keys returned: -`value` (on success): The list of names of your abilities.

### Get ability

GET: `<baseURL>/get_ability`

- `auth_token`: auth token
- `id`: character ID
- `name` : ability name

Additional keys returned:

- `value` (on success): A dictionary describing your ability.
  - `purchase`: The cost to purchase the ability (str)
  - `expedited`: Who the ability is expedited for (str)
  - `unlocks`: What is unlocked by this ability (str)
  - `partial_unlocks`: What is partially unlocked by this ability (str)
  - `not_required`: True if this ability is not required for the path completion bonus (boolean)
  - `prereq`: What is listed as prerequisites for this ability (str)
  - `mp_cost`: For spells, the MP costs for this ability as a list of 3 numbers (half, normal, double)
  - `cast_dl`: For spells, the DL to cast this ability as a list of 3 numbers (half, normal, double)
  - `range`: For spells, the spell's range (str)
  - `build_dc`: For tinker devices, the DC to build (str)
  - `build_time`: For tinker devices, the time to build (str)
  - `effect`: The description of the ability (str)
  - `flavor`: Flavor text for the ability (str)
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

## Inventory

### Add an item

GET: `<baseURL>/add_item`

- `auth_token`: auth token
- `id`: character ID
- `name`: item name
- `bulk`: item bulk
- `desc`: item description

Additional keys returned: -`id`: on success, the unique ID of your new item

### View items

GET: `<baseURL>/view_items`

- `auth_token`: auth token
- `id`: character ID

Additional keys returned: -`value`: on success, a list of item dictionaries

- `name`: item name
- `bulk`: the item's bulk value
- `desc`: the item's description

### Remove item

GET: `<baseURL>/remove_item`

- `auth_token`: auth token
- `id`: character ID
- `id2`: item ID to remove

### Add weapon

GET: `<baseURL>/add_weapon?q={"auth_token":"<auth_token>", "name":"weapon_name", "attr":"ATTR", "dmg": "<rollstr>" [, "mods" : { "key" : value } }`

- `auth_token`: auth token
- `name`: weapon name
- `attr`: attribute for the owner's entity to use
- `dmg`: \<rollstr\>

Optional args:

- `mods`:

Modifiers go in the `mods` dict, such as `"burning" : "1d6"`. Weapons added are account-specific.

### Get weapon

GET: `<baseURL>/get_weapon?q={"auth_token":"<auth_token>", "name":"weapon_name"}`

- `auth_token`: auth token
- `name`: ability name

The `get_weapon` call can also retrieve standard Vennt weapons like `Blade` and `Rifle`.

Additional keys returned:

- `weapon`: on success, a weapon dictionary
  - `name`: the weapon's name
  - `attr`: the weapon's attribute
  - `dmg`: the weapon's damage
  - `mods` the weapon's modifiers, as a dictionary of key/value pairs

### Remove weapon

GET: `<baseURL>/remove_weapon`

- `auth_token`: auth token
- `name`: weapon name

## Enemies

### Create an enemy

GET: `<baseURL>/create_enemy?q={"auth_token":"<auth_token>", "name":"myfirstenemy"[,"ATTR":"<num>"...]}`

- `auth_token`: auth token
- `name`: enemy name

Optional args:

- `attr`: attribute value, see Data Types above
- `campaign_id`: if this user is a GM in the given campaign, this enemy will be automatically added to the campaign and hidden to users.

Additional keys returned: -`id`: on success, the unique ID of your new enemy

## Campaigns

### Create a campaign

GET: `<baseURL>/create_campaign`

- `auth_token`: auth token
- `name`: campaign name

Additional keys returned: -`campaign_id`: on success, the unique ID of your new campaign

### List campaigns

GET: `<baseURL>/get_campaigns`

- `auth_token`: auth token

Additional keys returned: -`value`: on success, returns a list of IDs for your campaigns

### Get campaign info

GET: `<baseURL>/get_campaign`

- `auth_token`: auth token
- `campaign_id`: campaign ID

Additional keys returned: -`value`: on success, returns all relavent campaign information, including campaign members and roles, entities, initiative, etc.

### Invite someone to a campaign

GET: `<baseURL>/send_campaign_invite`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `username`: recipient's username

You need to be the owner of the campaign in order to call this API.

### View active campaign invites

GET: `<baseURL>/view_campaign_invites`

- `auth_token`: auth token

Additional keys returned:

- `value`: list of campaign invites
  - `from`: username of inviter
  - `campaign_id`: campaign ID

### Accept campaign invite

GET: `<baseURL>/accept_campaign_invite`

- `auth_token`: auth token
- `campaign_id`: campaign ID

### Decline campaign invite

GET: `<baseURL>/decline_campaign_invite`

- `auth_token`: auth token
- `campaign_id`: campaign ID

### Set campaign role

GET: `<baseURL>/set_role`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `username`: target's username
- `role`: One of "player", "GM", "spectator"

You need to be the owner of the campaign in order to call this API.

### Get campaign role

GET: `<baseURL>/set_role`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `username`: target's username

Additional keys returned:

- `value`: the user's role (GM or player)

You need to be a member of the campaign in order to call this API.

### Add entity to campaign

GET: `<baseURL>/add_to_campaign`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `id`: entity ID

Note: if adding an enemy, it will not be visible to non-GM campaign members.

### Remove entity from campaign

GET: `<baseURL>/remove_from_campaign`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `id`: entity ID

## Initiative

### Add entity to combat

GET: `<baseURL>/add_to_combat`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `id`: entity ID

Optional args:

- `roll`: your roll + attribute bonus. If not provided, the server will roll 3d6 and add your bonus automatically.

Note: if adding an enemy, it will automatically become visible to all campaign members.

### Remove entity from combat

GET: `<baseURL>/remove_from_combat`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `id`: entity ID

### Start combat

GET: `<baseURL>/start_combat`

- `auth_token`: auth token
- `campaign_id`: campaign ID

You need to be the owner of the campaign in order to call this API.

### End combat

GET: `<baseURL>/end_combat`

- `auth_token`: auth token
- `campaign_id`: campaign ID

You need to be the owner of the campaign in order to call this API.

### End turn

GET: `<baseURL>/end_turn`

- `auth_token`: auth token
- `campaign_id`: campaign ID
- `id`: entity ID
