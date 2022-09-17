import ba
import _ba
import settings
from . import _hashes as perms
from . import chat_commands as chatcmd
import coinsystem


sett = settings.get_settings_data()

class check_perms:
    def __init__(self,
                 memssage: str,
                 client_id: int
                 ):
         
        if not sett["chat"]["enabled"]:
            return None
        
        
        for i in _ba.get_game_roster():
            if i["client_id"] == client_id:
                acc_id = i["account_id"]
        # start the main 
        on_mute = self.check_mute(acc_id)
        if not on_mute:
            if message.startswith("/"):
                if sett["chat"]["settings"]["cht_cmd"]:
                    if self.permissions(acc_id, "owner"):
                        return chatcmd.owner(msg=message, clid=client_id, acid=acc_id)
                    elif self.permissions(acc_id, "admin"):
                        return chatcmd.admin(msg=message, clid=client_id, acid=acc_id)
                    elif self.permissions(acc_id, "vip"):
                        return chatcmd.vip(msg=message, clid=client_id, acid=acc_id)
                    else:
                        return chatcmd.normal(msg=message, clid=client_id, acid=acc_id)
                else:
                    ba.screenmessage("Chat Commands not enabled", color=(1, 0, 0), transient=True, clients=[client_id])
                    _ba.playsound(_ba.getsound("error"))
            else:
                return message
        
    def check_mute(self, acc_id):
        #profile = profile.get_player_profile(acc_id)
        #if profile["on_mute"]:
        #     return True
        return False

    def permissions(self, acctid, toc):
        if toc == "owner" and acctid in perms.owner:
            return True
        
        elif toc == "admin" and acctid in perms.admin:
            return True
       
        elif toc == "vip":
            # generally, vip commands are useless
            # we can buy vip commands if coinsystem is available
            if acctid in perms.vip:
                return True
            
            elif sett["currency"]["enabled"] and self.coinsytem(acctid):
                return True
            

    def coinsystem(self, acctid: str):
        if not sett["currency"]["enabled"]:
            return False
        elif not sett["currency"]["settings"]["shop"][" commands"]["enabled"]:
            return False
        # check the value of the command and run transaction
        new_msg = message.split(" ")[0]
        amount = coinsystem.get_command_price(newmsg)
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