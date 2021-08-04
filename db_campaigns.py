# Josh Aaron Miller 2021
# VenntDB methods for Campaigns

import venntdb
from constants import *

# VenntDB Methods


def get_role(self, username, campaign_id):
    return self.db["campaigns"][campaign_id][username]


def set_role(self, username, campaign_id, role):
    self.db["campaigns"][campaign_id][username] = role
    self.save_db()


def create_campaign(self, username, campaign_id, name):
    self.assert_valid("accounts", username, "campaigns")
    self.db["accounts"][username]["campaigns"].append(
        {"id": campaign_id, "name": name})
    self.db["campaigns"][campaign_id] = {}
    self.db["campaigns"][campaign_id]["name"] = name
    self.db["campaigns"][campaign_id]["owner"] = username
    self.db["campaigns"][campaign_id]["members"] = {}
    self.db["campaigns"][campaign_id]["members"][username] = "spectator"
    self.save_db()


def get_campaign_invites(self, username):
    self.assert_valid("accounts", username, "campaign_invites")
    return self.db["accounts"][username]["campaign_invites"]


def send_campaign_invite(self, user_from, user_to, campaign_id):
    invite = {"from": user_from, "id": campaign_id}
    self.assert_valid("accounts", user_to, "campaign_invites")
    for invites in self.db["accounts"][user_to]["campaign_invites"]:
        if invites["id"] == campaign_id:
            return False
    self.db["accounts"][user_to]["campaign_invites"].append(invite)
    self.save_db()
    return True


def remove_campaign_invite(self, username, campaign_id):
    self.assert_valid("accounts", username, "campaign_invites")
    for inv in self.db["accounts"][username]["campaign_invites"]:
        if inv["id"] == campaign_id:
            self.db["accounts"][username]["campaign_invites"].remove(inv)
            self.save_db()
            return True
    return False


def add_user_to_campaign(self, username, campaign_id):
    if username in self.db["campaigns"][campaign_id]["members"]:
        raise AssertionError(username + " already in campaign.")
    name = self.db["campaigns"][campaign_id]["name"]
    self.db["campaigns"][campaign_id]["members"][username] = "spectator"
    self.assert_valid("accounts", username, "campaigns")
    self.db["accounts"][username]["campaigns"].append(
        {"id": campaign_id, "name": name})
    self.save_db()


def get_campaign(self, campaign_id):
    if campaign_id in self.db["campaigns"]:
        return self.db["campaigns"][campaign_id]
    else:
        return None


def get_campaigns(self, username):
    self.assert_valid("accounts", username, "campaigns")
    return self.db["accounts"][username]["campaigns"]
