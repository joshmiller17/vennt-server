# Josh Aaron Miller 2021
# Vennt API example client

import requests
import json
import uuid
import argparse
import time
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
    time.sleep(1)  # need to sleep so we don't get rate limited
    if not args.quiet:
        print(response.text)
    if not args.verify:
        return True
    data = json.loads(response.text)
    if "success" not in data:
        print("No success key received")
        exit(1)
    if data["success"] and expectError:
        print("Operation succeeded but was expected to fail")
        print(data["info"])
        exit(1)
    if not data["success"]:
        if expectError:
            return True
        print("Unsuccessful operation")
        print(data["info"])
        exit(1)

def get_character(token, id):
    data = {"auth_token": token, "id": id}
    response = requests.get(url + 'get_character', params=data, verify=do_ssl)
    check_continue(response)
    response = json.loads(response.text)
    return response["value"]

def get_campaign(token, id):
    data = {"auth_token": token, "campaign_id": id}
    response = requests.get(url + 'get_campaign', params=data, verify=do_ssl)
    check_continue(response)
    response = json.loads(response.text)
    return response["value"]

#################### ACCOUNT APIS ####################


print("New account")
gm_username = str(uuid.uuid4())
gm_password = str(uuid.uuid4())
data = {"register": gm_username, "password": gm_password}
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
data = {"login": gm_username, "password": gm_password}
response = requests.post(
    url, json=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
gm_token = response["auth_token"]
assert(not args.verify or old_auth_token != gm_token)

print("New account 2")
player_username = str(uuid.uuid4())
player_password = str(uuid.uuid4())
data = {"register": player_username, "password": player_password}
response = requests.post(
    url, json=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
player_token = response["auth_token"]
assert(not args.verify or player_token != gm_token)

#################### CHARACTER APIS ####################

print("create character")
random_name = str(uuid.uuid4())
data = {"auth_token": gm_token, "name": random_name,
        "PER": 3, "MAX_HP": 10, "HP": 5, "gift": "Mind"}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
my_character_id = response["id"]

print("create character - invalid gift value - will fail")
data = {"auth_token": gm_token, "name": "bad character", "gift": "fake gift"}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("create character - invalid attribute value - will fail")
data = {"auth_token": gm_token,
        "name": "bad character", "INT": "not a number"}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("Get characters")
data = {"auth_token": gm_token}
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
char = get_character(gm_token, my_character_id)
assert(not args.verify or char["name"] == random_name)

# ATTRIBUTES

print("set attribute")
data = {"auth_token": gm_token,
        "id": my_character_id, "attr": "STR", "value": 3}
response = requests.get(url + 'set_attr', params=data, verify=do_ssl)
check_continue(response)

print("get attribute")
data = {"auth_token": gm_token, "id": my_character_id, "attr": "STR"}
response = requests.get(url + 'get_attr', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or response["value"] == 3)

print("update multiple attributes")
example_update_msg = "Example attr update"
data = {"auth_token": gm_token, "id": my_character_id, "INT": 3, "SPEED": 5, "REACH": 2, "msg": example_update_msg}
response = requests.get(url + 'update_attrs', params=data, verify=do_ssl)
check_continue(response)

char = get_character(gm_token, my_character_id)
assert(not args.verify or char["INT"] == 3)
assert(not args.verify or char["SPEED"] == 5)
assert(not args.verify or char["REACH"] == 2)
assert(not args.verify or len(char["changelog"]) == 3)
assert(not args.verify or char["changelog"][0]["msg"] == example_update_msg)
assert(not args.verify or char["changelog"][0]["attr"] == "INT")
assert(not args.verify or char["changelog"][0]["prev"] == 0)
assert(not args.verify or "time" in char["changelog"][0])
assert(not args.verify or char["changelog"][2]["msg"] == example_update_msg)
assert(not args.verify or char["changelog"][2]["attr"] == "REACH")
assert(not args.verify or "prev" not in char["changelog"][2])

print("update character name")
random_name = "Updated name"
new_gift = "Alertness"
data = {"auth_token": gm_token, "id": my_character_id, "name": random_name, "gift": new_gift}
response = requests.get(url + 'update_attrs', params=data, verify=do_ssl)
check_continue(response)

char = get_character(gm_token, my_character_id)
assert(not args.verify or char["name"] == random_name)
assert(not args.verify or char["gift"] == new_gift)
assert(not args.verify or len(char["changelog"]) == 3) # no new logs

# CHANGELOG

print("clear attribute's changelog")
data = {"auth_token": gm_token, "id": my_character_id, "attr": "SPEED"}
response = requests.get(url + 'clear_changelog', params=data, verify=do_ssl)
check_continue(response)

char = get_character(gm_token, my_character_id)
assert(not args.verify or len(char["changelog"]) == 2)
assert(not args.verify or char["changelog"][1]["attr"] == "REACH")

print("clear all changelogs")
data = {"auth_token": gm_token, "id": my_character_id}
response = requests.get(url + 'clear_changelog', params=data, verify=do_ssl)
check_continue(response)

char = get_character(gm_token, my_character_id)
assert(not args.verify or len(char["changelog"]) == 0)

# ABILITIES

example_ability = "Basic Cooking"

print("Lookup ability")
data = {"auth_token": gm_token, "name": example_ability}
response = requests.get(url + 'lookup_ability', params=data, verify=do_ssl)
check_continue(response)

print("add ability")
data = {"auth_token": gm_token,
        "name": example_ability, "id": my_character_id}
response = requests.get(url + 'add_ability', params=data, verify=do_ssl)
check_continue(response)

print("get abilities")
data = {"auth_token": gm_token, "id": my_character_id}
response = requests.get(url + 'get_abilities',
                        params=data, verify=do_ssl)
check_continue(response)

print("get ability")
data = {"auth_token": gm_token,
        "name": example_ability, "id": my_character_id}
response = requests.get(url + 'get_ability', params=data, verify=do_ssl)
check_continue(response)

print("update ability comment")
comment = "test comment" + str(uuid.uuid4())
data = {"auth_token": gm_token,
        "name": example_ability, "id": my_character_id, "comment": comment}
response = requests.get(url + 'update_ability_comment', params=data, verify=do_ssl)
check_continue(response)
data = {"auth_token": gm_token,
        "name": example_ability, "id": my_character_id}
response = requests.get(url + 'get_ability', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or response["value"]["comment"] == comment)

print("refresh ability")
data = {"auth_token": gm_token,
        "name": example_ability, "id": my_character_id}
response = requests.get(url + 'refresh_abillty', params=data, verify=do_ssl)
check_continue(response)
data = {"auth_token": gm_token,
        "name": example_ability, "id": my_character_id}
response = requests.get(url + 'get_ability', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or "comment" not in response["value"])

print("remove ability")
data = {"auth_token": gm_token,
        "name": example_ability, "id": my_character_id}
response = requests.get(url + 'remove_abillty', params=data, verify=do_ssl)
check_continue(response)

print("create custom ability")
custom_ability = {"name": "custom ability", "effect": "fancy custom ability", "cost": {"Passive": True},
                    "special_ability_type": "custom_ability"}
data = {"auth_token": gm_token, "id": my_character_id}
response = requests.post(url + 'create_ability', json=custom_ability, params=data, verify=do_ssl)
check_continue(response)
data = {"auth_token": gm_token,
        "name": custom_ability["name"], "id": my_character_id}
response = requests.get(url + 'get_ability', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or response["value"]["name"] == custom_ability["name"])
assert(not args.verify or response["value"]["effect"] == custom_ability["effect"])
assert(not args.verify or response["value"]["cost"] == custom_ability["cost"])

print("update ability")
custom_ability["effect"] = "new custom effect"
custom_ability["range"] = "12m"
data = {"auth_token": gm_token,
        "name": custom_ability["name"], "id": my_character_id}
response = requests.post(url + 'update_ability', json=custom_ability, params=data, verify=do_ssl)
check_continue(response)
data = {"auth_token": gm_token,
        "name": custom_ability["name"], "id": my_character_id}
response = requests.get(url + 'get_ability', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
assert(not args.verify or response["value"]["name"] == custom_ability["name"])
assert(not args.verify or response["value"]["effect"] == custom_ability["effect"])
assert(not args.verify or response["value"]["cost"] == custom_ability["cost"])
assert(not args.verify or response["value"]["range"] == custom_ability["range"])

# Character creation via post APIs

print("create character post")
custom_item = {"name": "Fashionable Outfit", "type": "container", "bulk": 5, "desc" : "Stylish", "courses": ""}
custom_character = {"name": str(uuid.uuid4()), "MAX_HP": 30, "HP": 3, "REACH": 2,
                    "items": [custom_item], "abilities": [custom_ability]}
data = {"auth_token": gm_token}
response = requests.post(url + 'create_character', json=custom_character, params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
custom_character_id = response["id"]

char = get_character(gm_token, custom_character_id)
assert(not args.verify or char["name"] == custom_character["name"])
assert(not args.verify or char["is_enemy"] == False)
assert(not args.verify or len(char["items"]) == 1)
assert(not args.verify or char["items"][0]["name"] == custom_item["name"])
assert(not args.verify or len(char["abilities"]) == 1)
assert(not args.verify or char["abilities"][0]["name"] == custom_ability["name"])

print("create enemy post")
data = {"auth_token": gm_token}
response = requests.post(url + 'create_enemy', json=custom_character, params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
custom_enemy_id = response["id"]

char = get_character(gm_token, custom_enemy_id)
assert(not args.verify or char["name"] == custom_character["name"])
assert(not args.verify or char["is_enemy"] == True)
assert(not args.verify or len(char["items"]) == 1)
assert(not args.verify or char["items"][0]["name"] == custom_item["name"])
assert(not args.verify or len(char["abilities"]) == 1)
assert(not args.verify or char["abilities"][0]["name"] == custom_ability["name"])

# ITEMS

print("Add item")
data = {"auth_token": gm_token, "id": my_character_id,
        "name": "donut", "bulk": "1", "desc": "Just a donut"}
response = requests.get(url + 'add_item', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
item_id = response["id"]

print("View items")
data = {"auth_token": gm_token, "id": my_character_id}
response = requests.get(url + 'view_items', params=data, verify=do_ssl)
check_continue(response)

print("Remove item")
data = {"auth_token": gm_token, "id": my_character_id, "id2": item_id}
response = requests.get(url + 'remove_item', params=data, verify=do_ssl)
check_continue(response)

# WEAPONS (WIP)

print("Add weapon")
data = {"auth_token": gm_token, "name": "myfirstweapon",
        "attr": "STR", "dmg": "1d6+6", "mods": {"burning": "1d6"}}
response = requests.get(url + 'add_weapon', params=data, verify=do_ssl)
check_continue(response)

print("Get weapon")
data = {"auth_token": gm_token, "name": "myfirstweapon"}
response = requests.get(url + 'get_weapon', params=data, verify=do_ssl)
check_continue(response)

print("Remove weapon")
data = {"auth_token": gm_token, "name": "myfirstweapon"}
response = requests.get(url + 'remove_weapon', params=data, verify=do_ssl)
check_continue(response)

# ENEMIES

print("create enemy")
data = {"auth_token": gm_token, "name": "myfirstenemy",
        "WIS": 3, "MAX_HP": 10, "HP": 10}
response = requests.get(url + 'create_enemy', params=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
enemy_id = response["id"]

char = get_character(gm_token, enemy_id)
assert(not args.verify or char["name"] == "myfirstenemy")
assert(not args.verify or char["WIS"] == 3)
assert(not args.verify or char["INT"] == 0)
assert(not args.verify or char["is_enemy"] == True)


#################### CAMPAIGN APIS ####################

print("Create campaign")
data = {"auth_token": gm_token, "name": "myfirstcampaign"}
response = requests.get(url + 'create_campaign?', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
campaign_id = response["campaign_id"]

# CAMPAIGN INVITES

print("Send campaign invite - self invite - will fail")
data = {"auth_token": gm_token,
        "username": gm_username, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("Send campaign invite - not owner of campaign - will fail")
data = {"auth_token": player_token,
        "username": gm_username, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response,  expectError=True)

print("Send campaign invite")
data = {"auth_token": gm_token,
        "username": player_username, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response)

print("View campaign invites")
data = {"auth_token": player_token}
response = requests.get(url + 'view_campaign_invites',
                        params=data, verify=do_ssl)
check_continue(response)

print("Decline campaign invite")
data = {"auth_token": player_token, "campaign_id": campaign_id}
response = requests.get(url + 'decline_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response)

print("Accept campaign invite")
data = {"auth_token": gm_token,
        "username": player_username, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response)
data = {"auth_token": player_token, "campaign_id": campaign_id}
response = requests.get(url + 'accept_campaign_invite?',
                        params=data, verify=do_ssl)
check_continue(response)

print("Set role")
data = {"auth_token": gm_token, "campaign_id": campaign_id,
        "username": gm_username, "role": "GM"}
response = requests.get(url + 'set_role', params=data, verify=do_ssl)
check_continue(response)

print("Get role")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "username": gm_username}
response = requests.get(url + 'get_role', params=data, verify=do_ssl)
check_continue(response)

print("Get campaigns")
data = {"auth_token": player_token, "name": "mySecondCampaign"}
response = requests.get(url + 'create_campaign?', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
campaign_id_2 = response["campaign_id"]

data = {"auth_token": player_token}
response = requests.get(url + 'get_campaigns', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
assert(not args.verify or len(response["value"]) == 2)
assert(not args.verify or response["value"][0]["id"] == campaign_id)
assert(not args.verify or response["value"][0]["name"] == "myfirstcampaign")
assert(not args.verify or response["value"][1]["id"] == campaign_id_2)
assert(not args.verify or response["value"][1]["name"] == "mySecondCampaign")

# ENTITY MANAGEMENT

data = {"auth_token": gm_token, "campaign_id": campaign_id,
        "username": player_username, "role": "player"}
response = requests.get(url + 'set_role', params=data, verify=do_ssl)
check_continue(response)

spectator_username = str(uuid.uuid4())
spectator_password = str(uuid.uuid4())
data = {"register": spectator_username, "password": spectator_password}
response = requests.post(
    url, json=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
spectator_token = response["auth_token"]

no_perms_username = str(uuid.uuid4())
no_perms_password = str(uuid.uuid4())
data = {"register": no_perms_username, "password": no_perms_password}
response = requests.post(
    url, json=data, verify=do_ssl)
check_continue(response)
response = json.loads(response.text)
no_perms_token = response["auth_token"]

data = {"auth_token": gm_token,
        "username": spectator_username, "campaign_id": campaign_id}
response = requests.get(url + 'send_campaign_invite',
                        params=data, verify=do_ssl)
check_continue(response)
data = {"auth_token": spectator_token, "campaign_id": campaign_id}
response = requests.get(url + 'accept_campaign_invite?',
                        params=data, verify=do_ssl)
check_continue(response)

print("Add character to the campaign - GM")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "id": my_character_id}
response = requests.get(url + 'add_to_campaign', params=data, verify=do_ssl)
check_continue(response)

print("Add character to the campaign - player")
data = {"auth_token": player_token,
        "name": "player character!", "INIT": 5, "SPEED": 6, "MAX_HP": 100, "HP": 52}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
player_character_id = response["id"]

data = {"auth_token": player_token,
        "campaign_id": campaign_id, "id": player_character_id}
response = requests.get(url + 'add_to_campaign', params=data, verify=do_ssl)
check_continue(response)

print("Add character to the campaign - spectator - will fail")
data = {"auth_token": spectator_token, "name": random_name}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
spectator_character_id = response["id"]

data = {"auth_token": spectator_token,
        "campaign_id": campaign_id, "id": spectator_character_id}
response = requests.get(url + 'add_to_campaign', params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("Add enemy to the campaign - GM")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "id": enemy_id}
response = requests.get(url + 'add_to_campaign', params=data, verify=do_ssl)
check_continue(response)

print("Add enemy to the campaign - player - will fail")
data = {"auth_token": player_token, "name": "player enemy"}
response = requests.get(url + 'create_enemy', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
player_enemy_id = response["id"]

data = {"auth_token": player_token,
        "campaign_id": campaign_id, "id": player_enemy_id}
response = requests.get(url + 'add_to_campaign', params=data, verify=do_ssl)
check_continue(response, expectError=True)


print("Get campaign - player")
player_campaign = get_campaign(player_token, campaign_id)
assert(not args.verify or player_campaign["name"] == "myfirstcampaign")
assert(not args.verify or player_campaign["owner"] == gm_username)
assert(not args.verify or len(player_campaign["members"]) == 3)
assert(not args.verify or player_campaign["members"][gm_username] == "GM")
assert(
    not args.verify or player_campaign["members"][player_username] == "player")
assert(
    not args.verify or player_campaign["members"][spectator_username] == "spectator")
assert(not args.verify or len(player_campaign["entities"]) == 2)
assert(
    not args.verify or player_campaign["entities"][my_character_id]["owner"] == gm_username)
assert(
    not args.verify or player_campaign["entities"][my_character_id]["name"] == random_name)
assert(
    not args.verify or player_campaign["entities"][my_character_id]["gm_only"] == False)
assert(
    not args.verify or player_campaign["entities"][my_character_id]["actions"] == 0)
assert(
    not args.verify or player_campaign["entities"][my_character_id]["reactions"] == 0)
assert(
    not args.verify or player_campaign["entities"][my_character_id]["health"] == "bloodied")
assert(
    not args.verify or player_campaign["entities"][player_character_id]["owner"] == player_username)
assert(not args.verify or player_campaign["init_styles"] == "traditional")
assert(not args.verify or len(player_campaign["init"]) == 0)
assert(not args.verify or player_campaign["init_index"] == 0)
assert(not args.verify or player_campaign["init_round"] == 0)
assert(not args.verify or player_campaign["in_combat"] == False)

print("Get campaign - spectator")
camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp == player_campaign)

print("Get campaign - no permission - will fail")
data = {"auth_token": no_perms_token, "campaign_id": campaign_id}
response = requests.get(url + 'get_campaign', params=data, verify=do_ssl)
check_continue(response, expectError=True)

print("Get campaign - GM")
gm_campaign = get_campaign(gm_token, campaign_id)
assert(not args.verify or gm_campaign != player_campaign)
assert(not args.verify or len(gm_campaign["entities"]) == 3)
assert(not args.verify or gm_campaign["entities"]
       [enemy_id]["owner"] == gm_username)
assert(not args.verify or gm_campaign["entities"]
       [enemy_id]["name"] == "myfirstenemy")
assert(not args.verify or gm_campaign["entities"][enemy_id]["gm_only"] == True)
assert(not args.verify or gm_campaign["entities"][enemy_id]["actions"] == 0)
assert(not args.verify or gm_campaign["entities"][enemy_id]["reactions"] == 0)
assert(not args.verify or gm_campaign["entities"]
       [enemy_id]["health"] == "healthy")

#################### INITIATIVE APIS ####################

print("Add character to combat - GM")
data = {"auth_token": gm_token, "campaign_id": campaign_id,
        "id": my_character_id, "roll": 10}
response = requests.get(url + 'add_to_combat', params=data, verify=do_ssl)
check_continue(response)

print("Add character to combat - GM - adds player character")
data = {"auth_token": gm_token, "campaign_id": campaign_id,
        "id": player_character_id, "roll": 10}
response = requests.get(url + 'add_to_combat', params=data, verify=do_ssl)
check_continue(response)

print("Add enemies to combat - GM")
data = {"auth_token": gm_token, "campaign_id": campaign_id,
        "id": enemy_id, "roll": 10}
response = requests.get(url + 'add_to_combat', params=data, verify=do_ssl)
check_continue(response)

data = {"auth_token": gm_token, "name": "second enemy",
        "INIT": 1, "MAX_HP": 10, "HP": 5, "campaign_id": campaign_id}
response = requests.get(url + 'create_enemy', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
second_enemy_id = response["id"]

data = {"auth_token": gm_token, "campaign_id": campaign_id,
        "id": second_enemy_id, "roll": 18}
response = requests.get(url + 'add_to_combat', params=data, verify=do_ssl)
check_continue(response)

print("Add character to combat - Player")
data = {"auth_token": player_token,
        "name": "player character 2!", "STR": 6, "MP": 12, "MAX_MP": 12, "MAX_HP": 50, "HP": 50}
response = requests.get(url + 'create_character', params=data, verify=do_ssl)
check_continue(response)

response = json.loads(response.text)
player_second_character_id = response["id"]

data = {"auth_token": player_token,
        "campaign_id": campaign_id, "id": player_second_character_id}
response = requests.get(url + 'add_to_campaign', params=data, verify=do_ssl)
check_continue(response)

data = {"auth_token": player_token, "campaign_id": campaign_id,
        "id": player_second_character_id, "roll": 10}
response = requests.get(url + 'add_to_combat', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["entities"][enemy_id]["gm_only"] == False)
assert(not args.verify or len(camp["init"]) == 5)
assert(not args.verify or camp["init"][0]["entity_id"] == second_enemy_id)
assert(not args.verify or camp["init"][1]["entity_id"] == player_character_id)
assert(not args.verify or camp["init"][2]["entity_id"] == my_character_id)
assert(not args.verify or camp["init"][3]["entity_id"] == player_second_character_id)
assert(not args.verify or camp["init"][4]["entity_id"] == enemy_id)
assert(not args.verify or camp["entities"][enemy_id]["reactions"] == 1)
assert(not args.verify or camp["init_index"] == 0)
assert(not args.verify or camp["init_round"] == 0)
assert(not args.verify or camp["in_combat"] == False)

print("Start combat")
data = {"auth_token": gm_token, "campaign_id": campaign_id}
response = requests.get(url + 'start_combat', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 0)
assert(not args.verify or camp["init_round"] == 0)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or camp["entities"][second_enemy_id]["actions"] == 3)
assert(not args.verify or camp["entities"][second_enemy_id]["reactions"] == 1)

print("End turn - GM")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "id": second_enemy_id}
response = requests.get(url + 'end_turn', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 1)
assert(not args.verify or camp["init_round"] == 0)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or camp["entities"][second_enemy_id]["actions"] == 0)
assert(not args.verify or camp["entities"][second_enemy_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][player_character_id]["actions"] == 3)
assert(not args.verify or camp["entities"][player_character_id]["reactions"] == 1)

print("End turn - player - init jumps forward 2")
data = {"auth_token": player_token,
        "campaign_id": campaign_id, "id": player_character_id}
response = requests.get(url + 'end_turn', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 3)
assert(not args.verify or camp["init_round"] == 0)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or camp["entities"][player_character_id]["actions"] == 0)
assert(not args.verify or camp["entities"][player_character_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][my_character_id]["actions"] == 3)
assert(not args.verify or camp["entities"][my_character_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][player_second_character_id]["actions"] == 3)
assert(not args.verify or camp["entities"][player_second_character_id]["reactions"] == 1)

print("End turn - player - init does not move")
data = {"auth_token": player_token,
        "campaign_id": campaign_id, "id": player_second_character_id}
response = requests.get(url + 'end_turn', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 3)
assert(not args.verify or camp["init_round"] == 0)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or camp["entities"][player_character_id]["actions"] == 0)
assert(not args.verify or camp["entities"][player_character_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][my_character_id]["actions"] == 3)
assert(not args.verify or camp["entities"][my_character_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][player_second_character_id]["actions"] == 0)
assert(not args.verify or camp["entities"][player_second_character_id]["reactions"] == 1)

print("End turn - GM - init moves 1")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "id": my_character_id}
response = requests.get(url + 'end_turn', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 4)
assert(not args.verify or camp["init_round"] == 0)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or camp["entities"][player_character_id]["actions"] == 0)
assert(not args.verify or camp["entities"][player_character_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][my_character_id]["actions"] == 0)
assert(not args.verify or camp["entities"][my_character_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][player_second_character_id]["actions"] == 0)
assert(not args.verify or camp["entities"][player_second_character_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][enemy_id]["actions"] == 3)
assert(not args.verify or camp["entities"][enemy_id]["reactions"] == 1)

print("End turn - GM - init wraps around again")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "id": enemy_id}
response = requests.get(url + 'end_turn', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 0)
assert(not args.verify or camp["init_round"] == 1)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or camp["entities"][second_enemy_id]["actions"] == 3)
assert(not args.verify or camp["entities"][second_enemy_id]["reactions"] == 1)
assert(not args.verify or camp["entities"][enemy_id]["actions"] == 0)
assert(not args.verify or camp["entities"][enemy_id]["reactions"] == 1)

print("Remove from combat - GM")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "id": player_second_character_id}
response = requests.get(url + 'remove_from_combat', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 0)
assert(not args.verify or camp["init_round"] == 1)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or len(list(filter(
    lambda init: init["entity_id"] == player_second_character_id, camp["init"]))) == 0)

print("Remove from combat - GM - init_index remains the same")
data = {"auth_token": gm_token,
        "campaign_id": campaign_id, "id": second_enemy_id}
response = requests.get(url + 'remove_from_combat', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 0)
assert(not args.verify or camp["init_round"] == 1)
assert(not args.verify or camp["in_combat"] == True)
assert(not args.verify or len(list(filter(
    lambda init: init["entity_id"] == second_enemy_id, camp["init"]))) == 0)

print("End combat")
data = {"auth_token": gm_token, "campaign_id": campaign_id}
response = requests.get(url + 'end_combat', params=data, verify=do_ssl)
check_continue(response)

camp = get_campaign(spectator_token, campaign_id)
assert(not args.verify or camp["init_index"] == 0)
assert(not args.verify or camp["init_round"] == 0)
assert(not args.verify or camp["in_combat"] == False)
assert(not args.verify or len(camp["init"]) == 0)

# Print user information for further testing purposes
print("----------------------------------------------------------------------------------")
print("GM username: '{}' password: '{}' auth_token: '{}'".format(
    gm_username, gm_password, gm_token))
print("Player username: '{}' password: '{}' auth_token: '{}'".format(
    player_username, player_password, player_token))
print("Spectator username: '{}' password: '{}' auth_token: '{}'".format(
    spectator_username, spectator_password, spectator_token))
print("No Perms username: '{}' password: '{}' auth_token: '{}'".format(
    no_perms_username, no_perms_password, no_perms_token))
