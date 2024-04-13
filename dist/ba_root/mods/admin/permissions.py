

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

def save_file(data, file):
    with open(file, "w") as f:
        f.write(json.dumps(data, indent=4))

def CheckRole(accountid, roles, mseg):
    perms_data = check_file(roles_file)
    if roles == "owner" and accountid in perms_data["owners"]:
        return True
    elif roles == "admin" and accountid in perms_data["admins"]:
        return True
    elif roles == "vip":
        if accountid in perms_data["vips"]:
            return True
        elif sett["currency"]["enabled"]:
            return coinsystem_c(msg=mseg, accountid=accountid)

def coinsystem_c(msg, accountid):
    if not sett["currency"]["settings"]["shop"]["commands"]["enabled"]:
            return False
    # check the value of the command and run transaction
    new_msg = msg.split(" ")[0]
    amount = coinsystem.get_command_price(new_msg)
    cash_owned = coinsystem.get_coins_by_pbid(accountid)
    try:
        assert amount is not None
        if cash_owned >= amount:
            th = 0 - amount
            coinsystem.add_coins_by_pbid(accountid, th)
            return True
        else:
            return False
        
    except Exception as e:
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
    elif account_id in check_file(roles_file)["muted"]:
        return True
    else:
        return False
    
def check_tag(accountid):
    if accountid in check_file(tags_file):
        return check_file(tags_file)[accountid]
    else:
        return None
    
def GiveRole(Role: str, accountid: str):
    rolesdata = check_file(roles_file)
    if Role == "owner":
        if accountid in rolesdata["owners"]:
            return None
        else:
            rolesdata["owners"].append(accountid)
            save_file(rolesdata, roles_file)
            return True
    elif Role == "admin":
        if accountid in rolesdata["admins"] or accountid in rolesdata["owners"]:
            return None
        else:
            rolesdata["admins"].append(accountid)
            save_file(rolesdata, roles_file)
            return True
    elif Role == "vip":
        if accountid in rolesdata["vips"] or accountid in rolesdata["owners"] or accountid in rolesdata["admins"]:
            return None
        else:
            rolesdata["vips"].append(accountid)
            save_file(rolesdata, roles_file)
            return True
    elif Role == "mute":
        if accountid in rolesdata["muted"]:
            return None
        else:
            rolesdata["muted"].append(accountid)
            save_file(rolesdata, roles_file)
            return True
    else:
        return False