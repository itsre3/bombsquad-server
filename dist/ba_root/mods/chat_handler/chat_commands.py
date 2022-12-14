


from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import settings
import coinsystem
from stats import mystats
from .cmd_files import newfly as nfly, help
from ba._generated.enums import SpecialChar

if TYPE_CHECKING:
    from typing import Union, Sequence

class normal(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _ba.get_foreground_host_activity()
        session = _ba.get_foreground_host_session()
        sett = settings.get_settings_data()
        
        
        with ba.Context(activity):
            if x in ["/list", "/li"]:
                k = u'{0:^16}{1:^15}{2:^10}'
                space = '\n______________________________\n'
                li = k.format('Name', 'Client ID' , 'Player ID') + space
                
                for i, people in enumerate(session.sessionplayers):
                    li += k.format(people.getname(icon=False), people.inputdevice.client_id, i) + "\n"
                
                _ba.screenmessage(li, transient=True, clients=[clid])
                
            elif x in ["/me", "/stats", "/i"]:
                if sett["stats"]["enabled"]:
                    stats = mystats.get_stats_by_id(acid)
                    if stats != None:
                        msg="Score:"+str(stats["scores"])+"\nGames:"+str(stats["games"])+"\nKills:"+str(stats["kills"])+"\nDeaths:"+str(stats["deaths"])+"\nAvg.Score:"+str(stats["avg_score"])
                        ba.screenmessage(msg, (1,0,1), transient=True, clients=[clid])
                    else:
                        ba.screenmessage("Play some games first", (1,0,0), transient=True, clients=[clid])
                else:
                    ba.screenmessage("Category Disabled", (1,0,0), transient=True, clients=[clid])
                
            elif x in ["/balance", "/cash", "/bal", "/money"]:
                if sett["currency"]["enabled"]:
                    balance = coinsystem.get_coins_by_pbid(acid)
                    ba.screenmessage(f"You have {_ba.charstr(SpecialChar.TICKET)}{balance}", (0,0,1), transient=True, clients=[clid])
                else:
                    ba.screenmessage("Category Disabled", (1,0,0), transient=True, clients=[clid])
                
            else:
                ba.screenmessage("Command not found", (1,0,0), transient=True, clients=[clid])
                
                
class vip(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _ba.get_foreground_host_activity()
        session = _ba.get_foreground_host_session()
        confirmation = "Command Executed"
        color = (1, 1, 0)

        with ba.Context(activity):
            if x in ["/headless", "/hl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                if i.actor.node.head_model != None:
                                    i.actor.node.head_model = None
                                    ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for player in activity.players:
                            body = player.actor.node
                            if body.head_model != None:
                                body.head_model = None
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        if body.head_model != None:
                            body.head_model = None
                            ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass
                
            
            elif x in ["/inv", "/invisible"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                body = i.actor.node
                                if body.head_model != None:
                                    body.style = "cyborg"
                                    body.upper_leg_model = None
                                    body.hand_model = None
                                    body.pelvis_model = None
                                    body.toes_model = None
                                    body.forearm_model = None
                                    body.lower_leg_model = None
                                    body.upper_arm_model = None
                                    body.torso_model = None
                                    body.head_model = None
                                    ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["all", "a"]:
                        for player in activity.players:
                            body = player.actor.node
                            if body.head_model != None:
                                body.style = "cyborg"
                                body.lower_leg_model = None
                                body.upper_leg_model = None
                                body.toes_model = None
                                body.hand_model = None
                                body.pelvis_model = None
                                body.forearm_model = None
                                body.upper_arm_model = None
                                body.torso_model = None
                                body.head_model = None
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        if body.head_model != None:
                            body.style = "cyborg"
                            body.upper_leg_model = None
                            body.hand_model = None
                            body.pelvis_model = None
                            body.toes_model = None
                            body.forearm_model = None
                            body.lower_leg_model = None
                            body.upper_arm_model = None
                            body.torso_model = None
                            body.head_model = None
                            ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass
            
            
            
            elif x in ["/heal", "/h"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.PowerupMessage("health"))
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.PowerupMessage("health"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.PowerupMessage("health"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass



            elif x in ["/mine", "/ml"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.PowerupMessage("land_mines"))
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.PowerupMessage("land_mines"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.PowerupMessage("land_mines"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/unfreeze", "/thaw"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.ThawMessage())
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.ThawMessage())
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.ThawMessage())
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/gloves", "/g"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.PowerupMessage("punch"))
                                nicks = i.getname()
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.PowerupMessage("punch"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.PowerupMessage("punch"))
                        nicks = activity.players[num].getname()
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/freze", "/fr"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.FreezeMessage())
                                nicks = i.getname()
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.FreezeMessage())
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.FreezeMessage())
                        nicks = activity.players[num].getname()
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/sleep", "/sl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage("knockout", 10000)
                                nicks = i.getname()
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage("knockout", 10000)
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage("knockout", 10000)
                        nicks = activity.players[num].getname()
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/celebrate", "/cl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage("celebrate", 10000)
                                nicks = i.getname()
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage("celebrate", 10000)
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage("celebrate", 10000)
                        nicks = activity.players[num].getname()
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            else:
                normal(msg, clid, acid)



class admin(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _ba.get_foreground_host_activity()
        session = _ba.get_foreground_host_session()
        color = (1, 1, 0)
        confirmation = "Command Executed"
        
        
        with ba.Context(activity):
            if x in ["/slow", "/sm"]:
                try:
                    if activity.globalsnode.slow_motion != True:
                        activity.globalsnode.slow_motion = True
                    else:
                        activity.globalsnode.slow_motion = False
                    ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x == "/check":
                ba.screenmessage("Commands working :p", color=color)
            
            elif x in ["/fly", "/fl"]:
                try:
                    for i in activity.players:
                        if i.sessionplayer.inputdevice.client_id == clid:
                            plr = i
                            nfly.NewFly(plr)
                except Exception as e:
                    print(e)
                
            else:
                vip(msg, clid, acid)




class owner(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _ba.get_foreground_host_activity()
        session = _ba.get_foreground_host_session()
        
        with ba.Context(activity):
            if x == "/kick":
                ba.screenmessage("Kick u")
                
            else:
                admin(msg, clid, acid)
