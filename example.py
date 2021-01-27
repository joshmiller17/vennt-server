# Josh Aaron Miller 2021
# Vennt API example client

import requests, json, uuid, argparse
url = 'http://localhost:3004/'

parser = argparse.ArgumentParser(description='Vennt API example client.')
parser.add_argument('--verify', action='store_true', help="Stop on failure")
parser.add_argument('--quiet', action='store_true', help="Don't print responses")


args = parser.parse_args()

def check_continue(response):
	if not args.quiet:
		print(response.text)
	if not args.verify:
		return True
	data = json.loads(response.text)
	if "success" not in data:
		print("No success key received")
		exit(1)
	if not data["success"]:
		print("Unsuccessful operation")
		print(data["info"])
		exit(1)

print("New account")
username = str(uuid.uuid4())
data = '{"register": "%s", "password": "pw"}' % username
response = requests.post(url, data=data.encode('utf-8'))
check_continue(response)

response = json.loads(response.text)
auth_token = response["auth_token"]

print("Logout")
data = {"auth_token":auth_token}
response = requests.get(url + 'logout?q=%s' % json.dumps(data))
check_continue(response)

print("Login")
data = '{"login": "%s", "password": "pw"}' % username
response = requests.post(url, data=data.encode('utf-8'))
check_continue(response)

response = json.loads(response.text)
auth_token = response["auth_token"]

print("Create campaign")
data = {"auth_token":auth_token,"name":"myfirstcampaign"}
response = requests.get(url + 'create_campaign?q=%s' % json.dumps(data))
check_continue(response)

response = json.loads(response.text)
campaign_id = response["campaign_id"]

print("create character")
data = {"auth_token":auth_token,"name":"myfirstcharacter","PER":"3"}
response = requests.get(url + 'create_character?q=%s' % json.dumps(data))
check_continue(response)

response = json.loads(response.text)
my_character_id = response["id"]

print("add ability")
data = {"auth_token":auth_token,"name":"Basic Cooking","id":my_character_id}
response = requests.get(url + 'add_ability?q=%s' % json.dumps(data))
check_continue(response)

print("get abilities")
data = {"auth_token":auth_token,"id":my_character_id}
response = requests.get(url + 'get_abilities?q=%s' % json.dumps(data))
check_continue(response)

print("get ability")
data = {"auth_token":auth_token,"name":"Basic Cooking","id":my_character_id}
response = requests.get(url + 'get_ability?q=%s' % json.dumps(data))
check_continue(response)

print("reset turn order")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
response = requests.get(url + 'reset_turn_order?q=%s' % json.dumps(data))
check_continue(response)

print("add turn")
data = {"auth_token":auth_token,"campaign_id":campaign_id, "id":my_character_id, "value":20}
response = requests.get(url + 'add_turn?q=%s' % json.dumps(data))
check_continue(response)

print("next turn")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
response = requests.get(url + 'next_turn?q=%s' % json.dumps(data))
check_continue(response)

print("get turn order")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
response = requests.get(url + 'get_turn_order?q=%s' % json.dumps(data))
check_continue(response)

print("get current turn")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
response = requests.get(url + 'get_current_turn?q=%s' % json.dumps(data))
check_continue(response)


print("create enemy")
data = {"auth_token":auth_token,"name":"myfirstenemy","WIS":"3"}
response = requests.get(url + 'create_enemy?q=%s' % json.dumps(data))
check_continue(response)

print("set attribute")
data = {"auth_token":auth_token,"id":my_character_id,"attr":"STR","value":"3"}
response = requests.get(url + 'set_attr?q=%s' % json.dumps(data))
check_continue(response)

print("get attribute")
data = {"auth_token":auth_token,"id":my_character_id,"attr":"STR"}
response = requests.get(url + 'get_attr?q=%s' % json.dumps(data))
check_continue(response)

print("Get campaigns")
data = {"auth_token":auth_token}
response = requests.get(url + 'get_campaigns?q=%s' % json.dumps(data))
check_continue(response)

response = json.loads(response.text)
campaign_id = response["value"][0]["id"]

print("Get characters")
data = {"auth_token":auth_token}
response = requests.get(url + 'get_characters?q=%s' % json.dumps(data))
check_continue(response)

print("Get character")
data = {"auth_token":auth_token,"id":my_character_id}
response = requests.get(url + 'get_character?q=%s' % json.dumps(data))
check_continue(response)

print("Send campaign invite")
data = {"auth_token":auth_token,"username":username,"campaign_id":campaign_id}
response = requests.get(url + 'send_campaign_invite?q=%s' % json.dumps(data))
check_continue(response)

print("View campaign invites")
data = {"auth_token":auth_token}
response = requests.get(url + 'view_campaign_invites?q=%s' % json.dumps(data))
check_continue(response)

print("Decline campaign invite")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
response = requests.get(url + 'decline_campaign_invite?q=%s' % json.dumps(data))
check_continue(response)

print("Accept campaign invite")
data = {"auth_token":auth_token,"username":username,"campaign_id":campaign_id}
response = requests.get(url + 'send_campaign_invite?q=%s' % json.dumps(data))
check_continue(response)
data = {"auth_token":auth_token,"id":campaign_id}
response = requests.get(url + 'accept_campaign_invite?q=%s' % json.dumps(data))
check_continue(response)

print("Set role")
data = {"auth_token":auth_token,"campaign_id":campaign_id,"username":username,"role":"GM"}
response = requests.get(url + 'set_role?q=%s' % json.dumps(data))
check_continue(response)

print("Get role")
data = {"auth_token":auth_token,"campaign_id":campaign_id,"username":username}
response = requests.get(url + 'get_role?q=%s' % json.dumps(data))
check_continue(response)

print("Add item")
data = {"auth_token":auth_token,"name":"donut","bulk":"1","desc":"Just a donut"}
response = requests.get(url + 'add_item?q=%s' % json.dumps(data))
check_continue(response)

response = json.loads(response.text)
item_id = response["id"]

print("View items")
data = {"auth_token":auth_token}
response = requests.get(url + 'view_items?q=%s' % json.dumps(data))
check_continue(response)

print("Remove item")
data = {"auth_token":auth_token,"id":item_id}
response = requests.get(url + 'remove_item?q=%s' % json.dumps(data))
check_continue(response)

print("Lookup ability")
data = {"auth_token":auth_token,"name":"Basic Cooking"}
response = requests.get(url + 'lookup_ability?q=%s' % json.dumps(data))
check_continue(response)

print("Add weapon")
data = {"auth_token":auth_token,"name":"myfirstweapon","attr":"STR","dmg":"1d6+6","mods":{"burning":"1d6"}}
response = requests.get(url + 'add_weapon?q=%s' % json.dumps(data))
check_continue(response)

print("Get weapon")
data = {"auth_token":auth_token,"name":"myfirstweapon"}
response = requests.get(url + 'get_weapon?q=%s' % json.dumps(data))
check_continue(response)

print("Remove weapon")
data = {"auth_token":auth_token,"name":"myfirstweapon"}
response = requests.get(url + 'remove_weapon?q=%s' % json.dumps(data))
check_continue(response)