# vennt-server
A headless server for making API calls to the Vennt database.


### Running the server
`py -3 venntserver.py vennt.db`


# API Documentation
All communications with the server are done via JSON. Authentication is done via POST which gives you an `auth_token` that can be used to make GET calls.

See `example.py` for an example of API calls.


### Create an account
POST: `{"register":"myusername","password":"mypassword"}`

Returns a JSON:
- `success`: whether the operation was successful
- `info`: on failure, why
- `auth_token`: on success, your authentication token for making GET calls

### Login
POST: `{"login":"myusername","password":"mypassword"}`

Returns a JSON:
- `success`: whether the operation was successful
- `info`: on failure, why
- `auth_token`: on success, your authentication token for making GET calls


### Create a character
GET: `<baseURL>/create_character?q={"auth_token":"<auth_token>", "name":"myfirstcharacter"}`

Returns a JSON:
- `success`: whether the operation was successful
-`id`: on success, the unique ID of your new character

### Create a campaign
GET: `<baseURL>/create_campaign?q={"auth_token":"<auth_token>", "name":"myfirstcampaign"}`

Returns a JSON:
- `success`: whether the operation was successful
-`id`: on success, the unique ID of your new campaign


### Set an attribute
GET: `<baseURL>/set_attr?q={"auth_token":"<auth_token>", "char_id":"<character_id>", "attr":"ATTR", "val":"<num>"}`
**Valid attributes**: AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, HERO, INIT, SPEED

Returns a JSON:
- `success`: whether the operation was successful

### Get an attribute
GET: `<baseURL>/get_attr?q={"auth_token":"<auth_token>", "char_id":"<character_id>", "attr":"ATTR"}`
**Valid attributes**: AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, HERO, INIT, SPEED

Returns a JSON:
- `success`: whether the operation was successful
- `value`: the attribute value
