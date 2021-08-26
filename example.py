# Josh Aaron Miller 2021
# Vennt API example client

import requests
import json
import uuid
import argparse
url = 'http://localhost:3004/'

parser = argparse.ArgumentParser(description='Vennt API example client.')
parser.add_argument('--verify', action='store_true',
                    help="Stop running the example when a failure occurs")
parser.add_argument('--quiet', action='store_true',
                    help="Don't print server responses")
parser.add_argument('--nocert', action='store_true',
                    help="Don't use a secure connection")


args = parser.parse_args()

do_ssl = not args.nocert


def check_continue(response, expectError=False):
    if not args.quiet:
        print(response.text)
    if not args.verify:
        return True
    data = json.loads(response.text)
    if "success" not in data:
        print("No success key received")
        exit(1)
    if not data["success"]:
        if expectError:
            return True
        print("Unsuccessful operation")
        print(data["info"])
        exit(1)

#################### ACCOUNT APIS ####################


print("New account")
username = str(uuid.uuid4())
password = str(uuid.uuid4())
data = {"register": username, "password": password}
response = requests.post(
    url, json=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
old_auth_token = response["auth_token"]

print("Logout")
data = {"auth_token": old_auth_token}
response = requests.get(
    url + 'logout?', params=data, verify=do_ssl)
check_continue(response)

print("Login")
data = {"login": username, "password": password}
response = requests.post(
    url, json=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
auth_token = response["auth_token"]
assert(not args.verify or old_auth_token != auth_token)

print("New account 2")
username2 = str(uuid.uuid4())
password2 = str(uuid.uuid4())
data = {"register": username2, "password": password2}
response = requests.post(
    url, json=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
auth_token2 = response["auth_token"]
assert(not args.verify or auth_token2 != auth_token)

#################### CHARACTER APIS ####################

print("create character")
random_name = str(uuid.uuid4())
data = {"auth_token": auth_token, "name": random_name, "PER": 3, "gift": "Mind"}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
my_character_id = response["id"]

print("create character - invalid gift value - will fail")
data = {"auth_token": auth_token, "name": "bad character", "gift": "fake gift"}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("create character - invalid attribute value - will fail")
data = {"auth_token": auth_token,
        "name": "bad character", "INT": "not a number"}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("Get characters")
data = {"auth_token": auth_token}
response = requests.get(url + 'get_characters', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or len(response["value"]) == 1)
assert(not args.verify or response["value"]
       [my_character_id]["name"] == random_name)
assert(not args.verify or response["value"][my_character_id]["PER"] == 3)
assert(not args.verify or response["value"][my_character_id]["INT"] == 0)
assert(not args.verify or response["value"][my_character_id]["gift"] == "Mind")
assert(not args.verify or response["value"]
       [my_character_id]["is_enemy"] == False)

print("Get character")
data = {"auth_token": auth_token, "id": my_character_id}
response = requests.get(url + 'get_character', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or response["value"]["name"] == random_name)

# ATTRIBUTES

print("set attribute")
data = {"auth_token": auth_token,
        "id": my_character_id, "attr": "STR", "value": 3}
response = requests.get(url + 'set_attr', params=data, verify=do_ssl)
check_continue(response)

print("get attribute")
data = {"auth_token": auth_token, "id": my_character_id, "attr": "STR"}
response = requests.get(url + 'get_attr', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or response["value"] == 3)

# ABILITIES

print("Lookup ability")
data = {"auth_token": auth_token, "name": "Basic Cooking"}
response = requests.get(url + 'lookup_ability', params=data, verify=do_ssl)
check_continue(response)

print("add ability")
data = {"auth_token": auth_token,
        "name": "Basic Cooking", "id": my_character_id}
response = requests.get(url + 'add_ability', params=data, verify=do_ssl)
check_continue(response)

print("get abilities")
data = {"auth_token": auth_token, "id": my_character_id}
response = requests.get(url + 'get_abilities',
                        params=data, verify=do_ssl)
check_continue(response)

print("get ability")
data = {"auth_token": auth_token,
        "name": "Basic Cooking", "id": my_character_id}
response = requests.get(url + 'get_ability', params=data, verify=do_ssl)
check_continue(response)

# ITEMS

print("Add item")
data = {"auth_token": auth_token, "id": my_character_id,
        "name": "donut", "bulk": "1", "desc": "Just a donut"}
response = requests.get(url + 'add_item', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
item_id = response["id"]

print("View items")
data = {"auth_token": auth_token, "id": my_character_id}
response = requests.get(url + 'view_items', params=data, verify=do_ssl)
check_continue(response)

print("Remove item")
data = {"auth_token": auth_token, "id": my_character_id, "id2": item_id}
response = requests.get(url + 'remove_item', params=data, verify=do_ssl)
check_continue(response)

# WEAPONS (WIP)

print("Add weapon")
data = {"auth_token": auth_token, "name": "myfirstweapon",
        "attr": "STR", "dmg": "1d6+6", "mods": {"burning": "1d6"}}
response = requests.get(url + 'add_weapon', params=data, verify=do_ssl)
check_continue(response)

print("Get weapon")
data = {"auth_token": auth_token, "name": "myfirstweapon"}
response = requests.get(url + 'get_weapon', params=data, verify=do_ssl)
check_continue(response)

print("Remove weapon")
data = {"auth_token": auth_token, "name": "myfirstweapon"}
response = requests.get(url + 'remove_weapon', params=data, verify=do_ssl)
check_continue(response)

# ENEMIES

print("create enemy")
data = {"auth_token": auth_token, "name": "myfirstenemy", "WIS": 3}
response = requests.get(url + 'create_enemy', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
enemy_id = response["id"]

data = {"auth_token": auth_token, "id": enemy_id}
response = requests.get(url + 'get_character', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or response["value"]["name"] == "myfirstenemy")
assert(not args.verify or response["value"]["WIS"] == 3)
assert(not args.verify or response["value"]["INT"] == 0)
assert(not args.verify or response["value"]["is_enemy"] == True)


#################### CAMPAIGN APIS ####################

print("Create campaign")
data = {"auth_token": auth_token, "name": "myfirstcampaign"}
response = requests.get(url + 'create_campaign?', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
campaign_id = response["campaign_id"]

# CAMPAIGN INVITES

print("Send campaign invite - self invite - will fail")
data = {"auth_token": auth_token,
        "username": username, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("Send campaign invite - not owner of campaign - will fail")
data = {"auth_token": auth_token2,
        "username": username, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response,  expectError=True)

print("Send campaign invite")
data = {"auth_token": auth_token,
        "username": username2, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response)

print("View campaign invites")
data = {"auth_token": auth_token2}
response = requests.get(url + 'view_campaign_invites',
                        params=data, verify=do_ssl)
check_continue(response)

print("Decline campaign invite")
data = {"auth_token": auth_token2, "campaign_id": campaign_id}
response = requests.get(url + 'decline_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response)

print("Accept campaign invite")
data = {"auth_token": auth_token,
        "username": username2, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response)
data = {"auth_token": auth_token2, "campaign_id": campaign_id}
response = requests.get(url + 'accept_campaign_invite?',
                        params=data, verify=do_ssl)
check_continue(response)

print("Set role")
data = {"auth_token": auth_token, "campaign_id": campaign_id,
        "username": username, "role": "GM"}
response = requests.get(url + 'set_role', params=data, verify=do_ssl)
check_continue(response)

print("Get role")
data = {"auth_token": auth_token,
        "campaign_id": campaign_id, "username": username}
response = requests.get(url + 'get_role', params=data, verify=do_ssl)
check_continue(response)

print("Get campaigns")
data = {"auth_token": auth_token2, "name": "mySecondCampaign"}
response = requests.get(url + 'create_campaign?', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
campaign_id_2 = response["campaign_id"]

data = {"auth_token": auth_token2}
response = requests.get(url + 'get_campaigns', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
assert(not args.verify or len(response["value"]) == 2)
assert(not args.verify or response["value"][0]["id"] == campaign_id)
assert(not args.verify or response["value"][0]["name"] == "myfirstcampaign")
assert(not args.verify or response["value"][1]["id"] == campaign_id_2)
assert(not args.verify or response["value"][1]["name"] == "mySecondCampaign")

# INITIATIVE
