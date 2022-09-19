import ba
import _ba
import settings
from . import _hashes as perms
from . import chat_commands as chatcmd
import coinsystem
from coinsystem.coinSystem import correct_answer

sett = settings.get_settings_data()


def check_perms(msg, client_id):
    if client_id == -1:
        if msg.startswith("/"):
            chatcmd.owner(msg, client_id, None)
            return None
        return msg

    for i in _ba.get_game_roster():
        if i['client_id'] == client_id:
            acid = i['account_id']
            
    chatfilter(msg, client_id, acid)

def chatfilter(msg, client_id, acid):
    on_mute = check_mute(acid)
    if not on_mute:
        if msg.startswith("/"):
            if sett["chat"]["settings"]["cht_cmd"]["enabled"]:
                if permissions(msg, acid, "owner"):
                    chatcmd.owner(msg, client_id, acid)
                elif permissions(msg, acid, "admin"):
                    chatcmd.admin(msg, client_id, acid)
                elif permissions(msg, acid, "vip"):
                    chatcmd.vip(msg, client_id, acid)
                else:
                    chatcmd.normal(msg, client_id, acid)
                return None
            else:
                ba.screenmessage("Chat Commands not enabled", color=(1, 0, 0), transient=True, clients=[client_id])
                _ba.playsound(_ba.getsound("error"))
                return None

        coinsystem.check_answer(msg, client_id)
        return msg

    else:
        return None


def check_mute(acc_id):
    #profile = profile.get_player_profile(acc_id)
    #if profile["on_mute"]:
    #     return True
    del acc_id
    return False



def permissions(msg, acctid, toc):
    if toc == "owner" and acctid in perms.owner:
        return True
    elif toc == "admin" and acctid in perms.admin:
        return True
    elif toc == "vip":
        # generally, vip commands are useless
        # we can buy vip commands if coinsystem is available
        if acctid in perms.vip:
            return True
        elif sett["currency"]["enabled"] and coinsystem_c(msg, cctid):
            return True


def coinsystem_c(msg, acctid):
    if not sett["currency"]["enabled"]:
        return False
    elif not sett["currency"]["settings"]["shop"][" commands"]["enabled"]:
        return False
    # check the value of the command and run transaction
    new_msg = msg.split(" ")[0]
    amount = coinsystem.get_command_price(new_msg)
    cash_owned = coinsystem.get_coins_by_pbid(acctid)
    try:
        if cash_owned >= amount:
            th = cash_owned - amount
            coinsystem.add_coins_by_pbid(acctid, th)
            return True
            
        else:
            return False
    
    except Exception as e:
        print(e)
