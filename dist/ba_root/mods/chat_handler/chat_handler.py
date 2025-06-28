import bascenev1 as bs
import _babase
import settings
from . import chat_commands as chatcmd
from admin.permissions import CheckRole, check_mute
import coinsystem
from coinsystem.coinSystem import correct_answer

sett = settings.get_settings_data()


def check_perms(msg, client_id):
    if client_id == -1:
        if msg.startswith("/"):
            chatcmd.owner(msg, client_id, None)
            return None
        return msg
    
    if check_mute(client_id):
        bs.screenmessage("Muted", (0,0,1), transient=True, clients=[client_id])
        return None
        
    if msg.startswith("/"):
        for i in _babase.get_game_roster():
            if i["client_id"] == client_id:
                acid = i["account_id"]
        if sett["chat"]["settings"]["cht_cmd"]["enabled"]:
            if CheckRole(acid, "owner", msg):
                chatcmd.owner(msg, client_id, acid)
            elif CheckRole(acid, "admin", msg):
                chatcmd.admin(msg, client_id, acid)
            elif CheckRole(acid, "vip", msg):
                chatcmd.vip(msg, client_id, acid)
            else:
                chatcmd.normal(msg, client_id, acid)
            return None
        else:
            bs.screenmessage("Chat Commands not enabled", color=(1, 0, 0), transient=True, clients=[client_id])
            _babase.playsound(_babase.getsound("error"))
            return None
    
    coinsystem.check_answer(msg, client_id)
    
    return msg

