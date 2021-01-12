# Josh Aaron Miller 2021
# Vennt API example client

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

print("Create campaign")
response = requests.get(url + 'create_campaign?q={"auth_token":"%s","name":"myfirstcampaign"}' % auth_token)
print(response.text)

print("create character")
response = requests.get(url + 'create_character?q={"auth_token":"%s","name":"myfirstcharacter","PER":"3"}' % auth_token)
print(response.text)

response = json.loads(response.text)
my_character_id = response["id"]

print("create enemy")
response = requests.get(url + 'create_enemy?q={"auth_token":"%s","name":"myfirstenemy","WIS":"3"}' % auth_token)
print(response.text)

print("set attribute")
response = requests.get(url + 'set_attr?q={"auth_token":"%s","id":"%s", "attr":"STR", "value": "3"}' % (auth_token, my_character_id))
print(response.text)

print("get attribute")
response = requests.get(url + 'get_attr?q={"auth_token":"%s","id":"%s", "attr":"STR"}' % (auth_token, my_character_id))
print(response.text)

print("Get campaigns")
response = requests.get(url + 'get_campaigns?q={"auth_token":"%s"}' % (auth_token))
print(response.text)

response = json.loads(response.text)
campaigns = response["value"]
campaigns = campaigns.replace("'",'"')
json_campaigns = json.loads(campaigns) # nested JSONs
campaign_id = json_campaigns[0]["id"]

print("Get characters")
response = requests.get(url + 'get_characters?q={"auth_token":"%s"}' % (auth_token))
print(response.text)

print("Get character")
response = requests.get(url + 'get_character?q={"auth_token":"%s", "id":"%s"}' % (auth_token,my_character_id))
print(response.text)

print("Send campaign invite")
response = requests.get(url + 'send_campaign_invite?q={"auth_token":"%s","username":"%s", "id":"%s"}' % (auth_token,username,campaign_id))
print(response.text)

print("View campaign invites")
response = requests.get(url + 'view_campaign_invites?q={"auth_token":"%s"}' % (auth_token))
print(response.text)

print("Accept campaign invite")
response = requests.get(url + 'accept_campaign_invite?q={"auth_token":"%s","id":"%s"}' % (auth_token,campaign_id))
print(response.text)

print("Set role")
response = requests.get(url + 'set_role?q={"auth_token":"%s","id":"%s","role":"GM","username":"%s"}' % (auth_token,campaign_id,username))
print(response.text)

print("Get role")
response = requests.get(url + 'get_role?q={"auth_token":"%s","id":"%s","username":"%s"}' % (auth_token,campaign_id,username))
print(response.text)

print("Logout")
response = requests.get(url + 'logout?q={"auth_token":"%s"}' % (auth_token))
print(response.text)