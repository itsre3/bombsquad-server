

import ba
import _ba
import os
import json
import settings
import coinsystem


sett = settings.get_settings_data()
base_dir = os.path.join(_ba.env()['python_directory_user'], "admin" + os.sep)
roles_file = base_dir+"roles.json"
effect_file = base_dir+"effects.json"
tags_file = base_dir+"tags.json"

def check_file(file):
    if os.path.exists(file):
        with open(file) as f:
            od_file = json.loads(f.read())
    else:
        od_file = {}
    return od_file

class CheckRole:
    def __init__(self, clientid, role: str, msg):
        self.clientid = clientid
        self.accountid = None
        self.check()

    def check(self):
        for i in _ba.get_game_roster():
            if i["client_id"] == self.clientid:
                #global self.accountid
                self.accountid = i["account_id"]
        perms_data = check_file(roles_file)
        if roles == "owner" and self.accountid in perms_data["owners"]:
            return True
        elif roles == "admin" and self.accountid in perms_data["admins"]:
            return True
        elif roles == "vip":
            if self.accountid in perms_data["vips"]:
                return True
            elif sett["currency"]["enanbled"]:
                self.coinsystem_c()

    def coinsystem_c(self):
        if not sett["currency"]["settings"]["shop"]["commands"]["enabled"]:
            return False
        # check the value of the command and run transaction
        new_msg = msg.split(" ")[0]
        amount = coinsystem.get_command_price(new_msg)
        cash_owned = coinsystem.get_coins_by_pbid(self.accountid)
        try:
            assert amount is not None
            if cash_owned >= amount:
                th = 0 - amount
                coinsystem.add_coins_by_pbid(self.accountid, th)
                return True
            else:
                return False
        
        except Exception as e:
            print(e)
            return False

def check_effect(account_id):
    if account_id in check_file(effect_file):
        return check_file(effect_file)[account_id]
    else:
        return None

def check_mute(client_id):
    for i in _ba.get_game_roster():
        if i["client_id"] == client_id:
            account_id = i["account_id"]
    if account_id in check_file(roles_file)["owners"]:
        return False
    else:
        return True