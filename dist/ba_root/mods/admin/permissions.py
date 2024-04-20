

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
available_effects = [
    "ProSurround", "Rainbow", "Spark", "Slime", "Metal", "Ice", "Stickers"
]

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
    
def check_tag(account_id) -> str:
    if account_id in check_file(tags_file):
        return check_file(tags_file)[account_id]
    elif account_id in check_file(roles_file)["owners"]:
        return "owner"
    elif account_id in check_file(roles_file)["admins"]:
        return "admin"
    elif account_id in check_file(roles_file)["vips"]:
        return "vip"
    else:
        return None
    
def GiveRole(Role: str, accountid: str):
    rolesdata = check_file(roles_file)
    if Role == "owner":
        if accountid in rolesdata["owners"]:
            return False
        else:
            rolesdata["owners"].append(accountid)
            save_file(rolesdata, roles_file)
            return True
    elif Role == "admin":
        if accountid in rolesdata["admins"] or accountid in rolesdata["owners"]:
            return False
        else:
            rolesdata["admins"].append(accountid)
            save_file(rolesdata, roles_file)
            return True
    elif Role == "vip":
        if accountid in rolesdata["vips"] or accountid in rolesdata["owners"] or accountid in rolesdata["admins"]:
            return False
        else:
            rolesdata["vips"].append(accountid)
            save_file(rolesdata, roles_file)
            return True
    elif Role == "mute":
        if accountid in rolesdata["muted"]:
            return False
        else:
            rolesdata["muted"].append(accountid)
            save_file(rolesdata, roles_file)
            return True

def TakeRole(Role: str, accountid: str):
    rolesdata = check_file(roles_file)
    if Role == "owner":
        if accountid in rolesdata["owners"]:
            rolesdata["owners"].remove(accountid)
            save_file(rolesdata, roles_file)
            return True
        else:
            return False
    elif Role == "admin":
        if accountid in rolesdata["admins"]:
            rolesdata["ädmins"].remove(accountid)
            save_file(rolesdata, roles_file)
            return True
        else:
            return False
    elif Role == "vip":
        if accountid in rolesdata["vips"]:
            rolesdata["vips"].remove(accountid)
            save_file(rolesdata, roles_file)
            return True
        else:
            return False
    elif Role == "mute":
        if accountid in rolesdata["muted"]:
            rolesdata["muted"].remove(accountid)
            save_file(rolesdata, roles_file)
            return True
        else:
            return False
        
def Effect(action: str, effect: str, accountid: str) -> any:
    effectsdata = check_file(effect_file)
    if effect not in available_effects:
        return False
    elif action == "add":
        if accountid not in effectsdata:
            effectsdata[accountid] = []
            effectsdata[accountid].append(effect)
            save_file(effectsdata, effect_file)
            return True
        elif effect in effectsdata[accountid]:
            return "AlreadyHas"
        elif accountid in effectsdata and len(effectsdata[accountid]) < 2:
            effectsdata[accountid].append(effect)
            save_file(effectsdata, effect_file)
            return True
        else:
            return "Morethan2"
    elif action == "take":
        if accountid in effectsdata:
            if effect in effectsdata[accountid]:
                effectsdata[accountid].remove(effect)
                save_file(effectsdata, effect_file)
                return True
            else:
                return "Noeffect"
        else:
            return "Noeffects"


def Tag(accountid: str, tag: str, action: str) -> any:
    tagdata = check_file(tags_file)
    if action == "give":
        try:
            tagdata[accountid] = tag
            save_file(tagdata, tags_file)
            return True
        except:
            return False
    elif action == "remove":
        try:
            tagdata.pop(accountid)
            save_file(tagdata, tags_file)
            return True
        except:
            return False
    else:
        return None
    