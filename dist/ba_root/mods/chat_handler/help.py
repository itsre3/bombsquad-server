
msg = ""

class Helper:
    def __init__(self, msge: list):
        self.arg = msge
        global msg
        #self.ret_wrap = "test"
        if self.arg in ["commands", "command"]:
            msg = """
            
=====Commands List 1=====
    /list or /li
    /headless or /hl
    /invinsible or /inv
    /heal or /he
    /mine or /ml
    /freeze or /fr
    /unfreeze or /thaw
    /gloves or /g
    /sleep or /sl
    /celebrate or /cl
    /slow or /sm
    /check
    /fly or /fl
    """
            #self.ret_wrap == msg
        
        elif self.arg in ["coinsystem", "currency"]:
            msg = """
            
=====Coinsystem/Currency=====
This is a system that gives in-game currency
with which you can purchase in-game stuffs
only
Note: Will only work when enabled
    """
            #self.ret_wrap == msg

        elif self.arg in ["roles", "vip", "owner", "admin"]:
            msg = """
            
=====Roles=====
Roles, just as the name implies are given to players
by the owner.
Role bearers have access to special commands
They may also have special tags
Note: Will only work when enaled
Try not to misuse
    """
            #self.ret_wrap == msg
        self.ret_wrap = msg