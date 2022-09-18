#pylint:disable=E0101
import ba
import _ba
import settings
from . import _hashes as perms
from . import chat_commands as chatcmd
import coinsystem


sett = settings.get_settings_data()

class check_perms:
    def __init__(self,
                 message: str,
                 client_id: int):
        self.message = message
        self.client_id = client_id
        ret = self.message
        if not sett["chat"]["enabled"]:
            return None
        
        for i in _ba.get_game_roster():
            if i["client_id"] == client_id:
                self.acc_id = i["account_id"]
        # start the main 
        try:
            on_mute = self.check_mute(self.acc_id)
            if not on_mute:
                if self.message.startswith("/"):
                    if sett["chat"]["settings"]["cht_cmd"]:
                        if self.permissions(self.acc_id, "owner"):
                            chatcmd.owner(msg=self.message, clid=self.client_id, acid=self.acc_id)
                        elif self.permissions(self.acc_id, "admin"):
                            chatcmd.admin(msg=self.message, clid=self.client_id, acid=self.acc_id)
                        elif self.permissions(self.acc_id, "vip"):
                            chatcmd.vip(msg=self.message, clid=self.client_id, acid=self.acc_id)
                        else:
                            chatcmd.normal(msg=self.message, clid=self.client_id, acid=self.acc_id)
                        return None
                    else:
                        ba.screenmessage("Chat Commands not enabled", color=(1, 0, 0), transient=True, clients=[self.client_id])
                        _ba.playsound(_ba.getsound("error"))
                        return None
                
                if self.message == coinsystem.correct_answer:
                    coinsystem.check_answer(self.message, self.client_id)
                    return None

            else:
                return None
        except:
            pass

        #return ret
        
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
            
            elif sett["currency"]["enabled"] and self.coinsystem(acctid):
                return True
            

    def coinsystem(self, acctid: str):
        if not sett["currency"]["enabled"]:
            return False
        elif not sett["currency"]["settings"]["shop"][" commands"]["enabled"]:
            return False
        # check the value of the command and run transaction
        new_msg = self.message.split(" ")[0]
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
