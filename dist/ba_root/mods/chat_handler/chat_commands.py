


from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
import _babase
import settings
import coinsystem
from stats import mystats
from . import help
from bascenev1._generated.enums import SpecialChar
from . import nfly
from admin import permissions

if TYPE_CHECKING:
    from typing import Union, Sequence

class normal(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _babase.get_foreground_host_activity()
        session = _babase.get_foreground_host_session()
        sett = settings.get_settings_data()
        
        
        with bs.Context(activity):
            if x in ["/list", "/li"]:
                k = u'{0:^16}{1:^15}{2:^10}'
                space = '\n______________________________\n'
                li = k.format('Name', 'Client ID' , 'Player ID') + space
                
                for i, people in enumerate(session.sessionplayers):
                    li += k.format(people.getname(icon=False), people.inputdevice.client_id, i) + "\n"
                
                bs.screenmessage(li, transient=True, clients=[clid])
                
            elif x in ["/me", "/stats", "/i"]:
                if sett["stats"]["enabled"]:
                    stats = mystats.get_stats_by_id(acid)
                    if stats != None:
                        msg="Score:"+str(
                            stats["scores"]) + "\nGames:"+str(stats["games"]) + "\nKills:"+str(stats["kills"]) + "\nDeaths:"+str(stats["deaths"]) + "\nAvg.Score:"+str(stats["avg_score"])
                        bs.screenmessage(msg, (1,0,1), transient=True, clients=[clid])
                    else:
                        bs.screenmessage("Play some games first", (1,0,0), transient=True, clients=[clid])
                else:
                    bs.screenmessage("Category Disabled", (1,0,0), transient=True, clients=[clid])
                
            elif x in ["/balance", "/cash", "/bs.", "/money"]:
                if sett["currency"]["enabled"]:
                    balance = coinsystem.get_coins_by_pbid(acid)
                    bs.screenmessage(f"You have {_banase.charstr(SpecialChar.TICKET)}{balance}", (0,0,1), transient=True, clients=[clid])
                else:
                    bs.screenmessage("Category Disabled", (1,0,0), transient=True, clients=[clid])
                
            elif x == "/help":
                try:
                    message = str(help.Helper(z[0]))
                    bs.screenmessage(message, (1,0,0), transient=True, clients=[clid])
                except Exception as e:
                    print(e)

            else:
                bs.screenmessage("Command not found", (1,0,0), transient=True, clients=[clid])
                
class vip(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _babase.get_foreground_host_activity()
        session = _babase.get_foreground_host_session()
        confirmation = "Command Executed"
        color = (1, 1, 0)

        with bs.Context(activity):
            if x in ["/headless", "/he"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                if i.actor.node.head_model != None:
                                    i.actor.node.head_model = None
                                    bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for player in activity.players:
                            body = player.actor.node
                            if body.head_model != None:
                                body.head_model = None
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        if body.head_model != None:
                            body.head_model = None
                            bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
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
                                    bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
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
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
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
                            bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass
            
            elif x in ["/heal", "/h"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("health"))
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("health"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("health"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/mine", "/ml"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("land_mines"))
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("land_mines"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("land_mines"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/impact", "/im"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("impact_bombs"))
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("impact_bombs"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("impact_bombs"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/sticky", "/st"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("sticky_bombs"))
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("sticky_bombs"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("sticky_bombs"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/icy", "/ic"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("ice_bombs"))
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("ice_bombs"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("ice_bombs"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/curse", "/cr"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("curse"))
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("curse"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("curse"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/heal", "/hl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("health"))
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("health"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("health"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass



            elif x in ["/unfreeze", "/thaw"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.ThawMessage())
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.ThawMessage())
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.ThawMessage())
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/gloves", "/g"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("punch"))
                                nicks = i.getname()
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("punch"))
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("punch"))
                        nicks = activity.players[num].getname()
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/freeze", "/fr"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.FreezeMessage())
                                nicks = i.getname()
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.FreezeMessage())
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.FreezeMessage())
                        nicks = activity.players[num].getname()
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/sleep", "/sl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage("knockout", 10000)
                                nicks = i.getname()
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage("knockout", 10000)
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage("knockout", 10000)
                        nicks = activity.players[num].getname()
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/celebrate", "/cl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage("celebrate", 10000)
                                nicks = i.getname()
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage("celebrate", 10000)
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage("celebrate", 10000)
                        nicks = activity.players[num].getname()
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            else:
                normal(msg, clid, acid)



class admin(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _babase.get_foreground_host_activity()
        session = _babase.get_foreground_host_session()
        color = (1, 1, 0)
        confirmation = "Command Executed"
        
        
        with bs.Context(activity):
            if x in ["/slow", "/sm"]:
                try:
                    if activity.globalsnode.slow_motion != True:
                        activity.globalsnode.slow_motion = True
                    else:
                        activity.globalsnode.slow_motion = False
                    bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x == "/check":
                bs.screenmessage("Commands working :p", color=color, transient=True, clients=[clid])
            
            elif x in ["/fly", "/fl"]:
                try:
                    if z == []:
                            for i in activity.players:
                                if i.sessionplayer.inputdevice.client_id == clid:
                                    plr = i
                                    nfly.NewFly(plr)
                                    bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["all", "a"]:
                        for players in activity.players:
                            plr = players
                            nfly.NewFly(plr)
                            bs.screenmessage(
                                "You have wings, Fly!!", color=color)
                    else:
                        num = int(z[0])
                        player = activity.players[num]
                        nfly.NewFly(player)
                        bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except Exception as e:
                    print(e)
                    
            elif x in ["/godmode", "/gm"]:
                try:
                    for i in activity.players:
                        if z == []:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.invincible = True
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                        elif z[0] in ["all", "a"]:
                            for players in activity.players:
                                players.actor.node.invincible = True
                                bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                        else:
                            num = int(z[0])
                            body = activity.players[num].actor.node
                            body.invincible = True
                            nicks = activity.players[num].getname()
                            bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                except Exception as e:
                    print(e)
                
            else:
                vip(msg, clid, acid)




class owner(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = _babase.get_foreground_host_activity()
        session = _babase.get_foreground_host_session()
        color = (1, 1, 0)
        confirmation = "Command Executed"
        
        with bs.Context(activity):
            if x == "/kick":
                kick_id = z[0]
                for i in _babase.get_game_roster():
                    try:
                        if i["client_id"] == kick_id:
                            _babase.disconnect_client(int(kick_id))
                            bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                    except Exception as e:
                        print(e)
            elif x == "/role":
                try:
                    pz = msg.split(' ', 1)[1]
                    z = pz.split(' ', 3)
                    num = z[2]
                    for i in session.sessionplayers:
                        if i.activityplayer.node.playerID == int(num):
                            playerid = i.get_v1_account_id()
                            if z[0] == "add":
                                response = permissions.GiveRole(z[1], playerid)
                                if response:
                                    bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                                elif response is None:
                                    bs.screenmessage(f"Role {z[1]} does not exist", color=color, transient=True, clients=[clid])
                                elif not response:
                                    bs.screenmessage(f"Player already has a higher role", color=color, transient=True, clients=[clid])
                            elif z[0] == "take":
                                response = permissions.TakeRole(z[1], playerid)
                                if response:
                                    bs.screenmessage(confirmation, color=color, transient=True, clients=[clid])
                                elif not response:
                                    bs.screenmessage(f"Player does not have {z[1]}", color=color, transient=True, clients=[clid])
                                elif response is None:
                                    bs.screenmessage(f"Role does not exist", color=color, transient=True, clients=[clid])
                except Exception as e:
                    print(e)

            elif x in ["/effect", "/effects"]:
                try:
                    pz = msg.split(' ', 1)[1]
                    z = pz.split(' ', 3)
                    num = z[2]
                    for i in session.sessionplayers:
                        if i.activityplayer.node.playerID == int(num):
                            playerid = i.get_v1_account_id()
                        else:
                            for i in _babase.get_game_roster():
                                if i["client_id"] == int(num):
                                    playerid = i["accountid"]
                        responsedata = permissions.Effect(z[0], z[1], playerid)
                        if not responsedata:
                            bs.screenmessage(f"Effect {z[1]} does not exist", color=color, transient=True, clients=[clid])
                            return
                        if z[0] == "add":
                            if responsedata == "AlreadyHas":
                                bs.screenmessage(
                                    f"Player already has effect {z[1]}", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata == "Morethan2":
                                bs.screenmessage(
                                    f"Player has two effects already", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata:
                                bs.screenmessage(
                                    confirmation, color=color, transient=True, clients=[clid]
                                )
                        elif z[0] == "take":
                            if responsedata == "Noeffects":
                                bs.screenmessage(
                                    f"Player do not have any effect", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata == "Noeffect":
                                bs.screenmessage(
                                    f"Player do not have {z[1]}", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata:
                                bs.screenmessage(
                                    confirmation, color=color, transient=True, clients=[clid]
                                )
                except Exception as e:
                    print(e)

            elif x == "/tag":
                try:
                    pz = msg.split(' ', 1)[1]
                    z = pz.split(' ', 3)
                    num = z[2]
                    for i in session.sessionplayers:
                        if i.activityplayer.node.playerID == int(num):
                            playerid = i.get_v1_account_id()
                        else:
                            for i in _babase.get_game_roster():
                                if i["client_id"] == int(num):
                                    playerid = i["accountid"]
                        response = permissions.Tag(playerid, z[1], z[0])
                        if response == None:
                            bs.screenmessage(
                                "Either give or remove tag", color=color, transient=True, clients=[clid]
                            )
                            return
                        elif z[0] == "give":
                            if response:
                                bs.screenmessage(
                                    confirmation, color=color, transient=True, clients=[clid]
                                )
                            else:
                                bs.screenmessage(
                                    "Error when adding tag", color=color, transient=True, clients=[clid]
                                )
                        elif z[0] == "remove":
                            if response:
                                bs.screenmessage(
                                    confirmation, color=color, transient=True, clients=[clid]
                                )
                            else:
                                bs.screenmessage(
                                    "Error when removing tag", color=color, transient=True, clients=[clid]
                                )
                except Exception as e:
                    print(e)              

            else:
                admin(msg, clid, acid)
