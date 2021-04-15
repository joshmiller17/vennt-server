# Josh Aaron Miller 2021
# Vennt API example client

import requests, json, uuid, argparse, urllib
url = 'http://localhost:3004/'

parser = argparse.ArgumentParser(description='Vennt API example client.')
parser.add_argument('--verify', action='store_true', help="Stop running the example when a failure occurs")
parser.add_argument('--quiet', action='store_true', help="Don't print server responses")
parser.add_argument('--nocert', action='store_true', help="Don't use a secure connection")


args = parser.parse_args()

do_ssl = not args.nocert

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
data = {"register": username, "password": "pw"}
data = urllib.parse.urlencode(data)
response = requests.post(url, data=data.encode('utf-8'), verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
auth_token = response["auth_token"]

print("Logout")
data = {"auth_token":auth_token}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'logout?%s' % data, verify=do_ssl)
check_continue(response)

print("Login")
data = {"login": username, "password": "pw"}
data = urllib.parse.urlencode(data)
response = requests.post(url, data=data.encode('utf-8'), verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
auth_token = response["auth_token"]

print("Create campaign")
data = {"auth_token":auth_token,"name":"myfirstcampaign"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'create_campaign?%s' % data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
campaign_id = response["campaign_id"]

print("create character")
data = {"auth_token":auth_token,"name":"myfirstcharacter","PER":"3"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'create_character?%s' % data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
my_character_id = response["id"]

print("add ability")
data = {"auth_token":auth_token,"name":"Basic Cooking","id":my_character_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'add_ability?%s' % data, verify=do_ssl)
check_continue(response)

print("get abilities")
data = {"auth_token":auth_token,"id":my_character_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_abilities?%s' % data, verify=do_ssl)
check_continue(response)

print("get ability")
data = {"auth_token":auth_token,"name":"Basic Cooking","id":my_character_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_ability?%s' % data, verify=do_ssl)
check_continue(response)

print("reset turn order")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'reset_turn_order?%s' % data, verify=do_ssl)
check_continue(response)

print("add turn")
data = {"auth_token":auth_token,"campaign_id":campaign_id, "id":my_character_id, "value":20}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'add_turn?%s' % data, verify=do_ssl)
check_continue(response)

print("next turn")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'next_turn?%s' % data, verify=do_ssl)
check_continue(response)

print("get turn order")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_turn_order?%s' % data, verify=do_ssl)
check_continue(response)

print("get current turn")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_current_turn?%s' % data, verify=do_ssl)
check_continue(response)


print("create enemy")
data = {"auth_token":auth_token,"name":"myfirstenemy","WIS":"3"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'create_enemy?%s' % data, verify=do_ssl)
check_continue(response)

print("set attribute")
data = {"auth_token":auth_token,"id":my_character_id,"attr":"STR","value":"3"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'set_attr?%s' % data, verify=do_ssl)
check_continue(response)

print("get attribute")
data = {"auth_token":auth_token,"id":my_character_id,"attr":"STR"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_attr?%s' % data, verify=do_ssl)
check_continue(response)

print("Get campaigns")
data = {"auth_token":auth_token}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_campaigns?%s' % data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
campaign_id = response["value"][0]["id"]

print("Get characters")
data = {"auth_token":auth_token}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_characters?%s' % data, verify=do_ssl)
check_continue(response)

print("Get character")
data = {"auth_token":auth_token,"id":my_character_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_character?%s' % data, verify=do_ssl)
check_continue(response)

print("Send campaign invite")
data = {"auth_token":auth_token,"username":username,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'send_campaign_invite?%s' % data, verify=do_ssl)
check_continue(response)

print("View campaign invites")
data = {"auth_token":auth_token}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'view_campaign_invites?%s' % data, verify=do_ssl)
check_continue(response)

print("Decline campaign invite")
data = {"auth_token":auth_token,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'decline_campaign_invite?%s' % data, verify=do_ssl)
check_continue(response)

print("Accept campaign invite (will fail)")
data = {"auth_token":auth_token,"username":username,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'send_campaign_invite?%s' % data, verify=do_ssl)
check_continue(response)
data = {"auth_token":auth_token,"campaign_id":campaign_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'accept_campaign_invite?%s' % data, verify=do_ssl)
check_continue(response)

print("Set role")
data = {"auth_token":auth_token,"campaign_id":campaign_id,"username":username,"role":"GM"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'set_role?%s' % data, verify=do_ssl)
check_continue(response)

print("Get role")
data = {"auth_token":auth_token,"campaign_id":campaign_id,"username":username}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_role?%s' % data, verify=do_ssl)
check_continue(response)

print("Add item")
data = {"auth_token":auth_token,"id":my_character_id,"name":"donut","bulk":"1","desc":"Just a donut"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'add_item?%s' % data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
item_id = response["id"]

print("View items")
data = {"auth_token":auth_token, "id":my_character_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'view_items?%s' % data, verify=do_ssl)
check_continue(response)

print("Remove item")
data = {"auth_token":auth_token, "id":my_character_id,"id2":item_id}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'remove_item?%s' % data, verify=do_ssl)
check_continue(response)

print("Lookup ability")
data = {"auth_token":auth_token,"name":"Basic Cooking"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'lookup_ability?%s' % data, verify=do_ssl)
check_continue(response)

print("Add weapon")
data = {"auth_token":auth_token,"name":"myfirstweapon","attr":"STR","dmg":"1d6+6","mods":{"burning":"1d6"}}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'add_weapon?%s' % data, verify=do_ssl)
check_continue(response)

print("Get weapon")
data = {"auth_token":auth_token,"name":"myfirstweapon"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'get_weapon?%s' % data, verify=do_ssl)
check_continue(response)

print("Remove weapon")
data = {"auth_token":auth_token,"name":"myfirstweapon"}
data = urllib.parse.urlencode(data)
response = requests.get(url + 'remove_weapon?%s' % data, verify=do_ssl)
check_continue(response)