


from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import settings
import coinsystem
from stats import mystats
from . import help
from ba._generated.enums import SpecialChar
from . import nfly
from admin import permissions

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
                        msg="Score:"+str(
                            stats["scores"]) + "\nGames:"+str(stats["games"]) + "\nKills:"+str(stats["kills"]) + "\nDeaths:"+str(stats["deaths"]) + "\nAvg.Score:"+str(stats["avg_score"])
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
                
            elif x == "/help":
                try:
                    message = str(help.Helper(z[0]))
                    ba.screenmessage(message, (1,0,0), transient=True, clients=[clid])
                except Exception as e:
                    print(e)

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
            if x in ["/headless", "/he"]:
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

            elif x in ["/impact", "/im"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.PowerupMessage("impact_bombs"))
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.PowerupMessage("impact_bombs"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.PowerupMessage("impact_bombs"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/sticky", "/st"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.PowerupMessage("sticky_bombs"))
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.PowerupMessage("sticky_bombs"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.PowerupMessage("sticky_bombs"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/icy", "/ic"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.PowerupMessage("ice_bombs"))
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.PowerupMessage("ice_bombs"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.PowerupMessage("ice_bombs"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/curse", "/cr"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(ba.PowerupMessage("curse"))
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(ba.PowerupMessage("curse"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(ba.PowerupMessage("curse"))
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/heal", "/hl"]:
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


            elif x in ["/freeze", "/fr"]:
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
                ba.screenmessage("Commands working :p", color=color, transient=True, clients=[clid])
            
            elif x in ["/fly", "/fl"]:
                try:
                    if z == []:
                            for i in activity.players:
                                if i.sessionplayer.inputdevice.client_id == clid:
                                    plr = i
                                    nfly.NewFly(plr)
                                    ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["all", "a"]:
                        for players in activity.players:
                            plr = players
                            nfly.NewFly(plr)
                            ba.screenmessage(
                                "You have wings, Fly!!", color=color)
                    else:
                        num = int(z[0])
                        player = activity.players[num]
                        nfly.NewFly(player)
                        ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except Exception as e:
                    print(e)
                    
            elif x in ["/godmode", "/gm"]:
                try:
                    for i in activity.players:
                        if z == []:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.invincible = True
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                        elif z[0] in ["all", "a"]:
                            for players in activity.players:
                                players.actor.node.invincible = True
                                ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                        else:
                            num = int(z[0])
                            body = activity.players[num].actor.node
                            body.invincible = True
                            nicks = activity.players[num].getname()
                            ba.screenmessage(confirmation, color=color, transient=True, clients=[clid])
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
        color = (1, 1, 0)
        confirmation = "Command Executed"
        
        with ba.Context(activity):
            if x == "/kick":
                kick_id = z[0]
                for i in ba.internal.get_game_roster():
                    try:
                        if i["client_id"] == kick_id:
                            ba.internal.disconnect_client(int(kick_id))
                            ba.screenmessage(confirmation, color, True, [clid])
                    except:
                        pass
            elif x == "/role":
                try:
                    pz = msg.split(' ', 1)[1]
                    z = pz.split(' ', 3)
                    num = int(z[2])
                    playerid = session.sessionplayers[num].activityplayer.node.playerID
                    if z[0] == "add":
                        response = permissions.GiveRole(z[1], playerid)
                        if response:
                            ba.screenmessage(confirmation, color, True, [clid])
                        elif response is None:
                            ba.screenmessage(f"Role {z[1]} does not exist", color, True, [clid])
                        elif not response:
                            ba.screenmessage(f"Player already has a higher role", color, True, [clid])
                    elif z[0] == "take":
                        response = permissions.TakeRole(z[1], playerid)
                        if response:
                            ba.screenmessage(confirmation, color, True, [clid])
                        elif not response:
                            ba.screenmessage(f"Player does not have {z[1]}", color, True, [clid])
                        elif response is None:
                            ba.screenmessage(f"Role does not exist", color, True, [clid])
                except Exception as e:
                    print(e)

            else:
                admin(msg, clid, acid)
