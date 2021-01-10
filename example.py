import requests, json, uuid

url = 'http://localhost:3004/'

# create a new account
print("New account")
username = str(uuid.uuid4())
data = '{"register": "%s", "password": "pw"}' % username
response = requests.post(url, data=data.encode('utf-8'))
print(response.text)

# login
print("Login")
data = '{"login": "%s", "password": "pw"}' % username
response = requests.post(url, data=data.encode('utf-8'))
print(response.text)

response = json.loads(response.text)
auth_token = response["auth_token"]

# create a new campaign
print("New campaign")
response = requests.get(url + 'create_campaign?q={"auth_token":"%s","name":"myfirstcampaign"}' % auth_token)
print(response.text)

# create a new character
print("New character")
response = requests.get(url + 'create_character?q={"auth_token":"%s","name":"myfirstcharacter"}' % auth_token)
print(response.text)

response = json.loads(response.text)
my_character_id = response["id"]

# set an attribute
print("Set attr")
response = requests.get(url + 'set_attr?q={"auth_token":"%s","id":"%s", "attr":"STR", "val": "3"}' % (auth_token, my_character_id))
print(response.text)

# get an attribute
print("Get attr")
response = requests.get(url + 'get_attr?q={"auth_token":"%s","id":"%s", "attr":"STR"}' % (auth_token, my_character_id))
print(response.text)