

import bascenev1 as bs
import babase
from bascenev1._activity import Activity
import coinsystem
from discord_bot import b_launch
import settings


sett = settings.get_settings_data()


cstimer = None
lftimer = None
def new_trans_in(self) -> None:
    global lftimer
    global cstimer
    if sett["currency"]["settings"]["askquestions"]:
        cstimer = bs.Timer(30, coinsystem.ask_question, repeat=True)
    if sett["discord"]["enabled"]:
        lftimer = bs.Timer(8, b_launch.get_live_feed, repeat=True)

def enable():
    Activity.on_transition_in = new_trans_in