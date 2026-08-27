

from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
import _babase
import babase
import settings
import coinsystem
from stats import mystats
from . import help
from babase import SpecialChar
from . import nfly
from admin import permissions

if TYPE_CHECKING:
    from typing import Union, Sequence

class normal(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = bs.get_foreground_host_activity()
        session = bs.get_foreground_host_session()
        sett = settings.get_settings_data()
        
        
        with bs.ContextRef():
            if x in ["/list", "/li"]:
                k = u'{0:^16}{1:^15}{2:^10}'
                space = '\n______________________________\n'
                li = k.format('Name', 'Client ID' , 'Player ID') + space
                
                for i, people in enumerate(session.sessionplayers):
                    li += k.format(people.getname(icon=False), people.inputdevice.client_id, i) + "\n"
                
                bs.broadcastmessage(li, transient=True, clients=[clid])
                
            elif x in ["/me", "/stats", "/i"]:
                if sett["stats"]["enabled"]:
                    stats = mystats.get_stats_by_id(acid)
                    if stats != None:
                        msg="Score:"+str(
                            stats["scores"]) + "\nGames:"+str(stats["games"]) + "\nKills:"+str(stats["kills"]) + "\nDeaths:"+str(stats["deaths"]) + "\nAvg.Score:"+str(stats["avg_score"])
                        bs.broadcastmessage(msg, (1,0,1), transient=True, clients=[clid])
                    else:
                        bs.broadcastmessage("Play some games first", (1,0,0), transient=True, clients=[clid])
                else:
                    bs.broadcastmessage("Category Disabled", (1,0,0), transient=True, clients=[clid])
                
            elif x in ["/balance", "/cash", "/bs.", "/money"]:
                if sett["currency"]["enabled"]:
                    balance = coinsystem.get_coins_by_pbid(acid)
                    bs.broadcastmessage(f"You have {babase.charstr(SpecialChar.TICKET)}{balance}", (0,0,1), transient=True, clients=[clid])
                else:
                    bs.broadcastmessage("Category Disabled", (1,0,0), transient=True, clients=[clid])
                
            elif x == "/help":
                try:
                    message = str(help.Helper(z[0]))
                    bs.broadcastmessage(message, (1,0,0), transient=True, clients=[clid])
                except Exception as e:
                    print(e)

            else:
                bs.broadcastmessage("Command not found", (1,0,0), transient=True, clients=[clid])
                
class vip(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = bs.get_foreground_host_activity()
        session = bs.get_foreground_host_session()
        confirmation = "Command Executed"
        color = (1, 1, 0)

        with bs.ContextRef():
            if x in ["/headless", "/he"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                if i.actor.node.head_model != None:
                                    i.actor.node.head_model = None
                                    bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for player in activity.players:
                            body = player.actor.node
                            if body.head_model != None:
                                body.head_model = None
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        if body.head_model != None:
                            body.head_model = None
                            bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass
                
            
            elif x in ["/inv", "/invisible"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                body = i.actor.node
                                body = i.actor.node
                                if body.head_mesh != None:
                                    body.style = "cyborg"
                                    body.upper_leg_mesh = None
                                    body.hand_mesh = None
                                    body.pelvis_mesh = None
                                    body.toes_mesh = None
                                    body.forearm_mesh = None
                                    body.lower_leg_mesh = None
                                    body.upper_arm_mesh = None
                                    body.torso_mesh = None
                                    body.head_mesh = None
                                    bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["all", "a"]:
                        for player in activity.players:
                            body = player.actor.node
                            if body.head_model != None:
                                body.style = "cyborg"
                                body.lower_leg_mesh = None
                                body.upper_leg_mesh = None
                                body.toes_mesh = None
                                body.hand_mesh = None
                                body.pelvis_mesh = None
                                body.forearm_mesh = None
                                body.upper_arm_mesh = None
                                body.torso_mesh = None
                                body.head_mesh = None
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        if body.head_model != None:
                            body.style = "cyborg"
                            body.upper_leg_mesh = None
                            body.hand_mesh = None
                            body.pelvis_mesh = None
                            body.toes_mesh = None
                            body.forearm_mesh = None
                            body.lower_leg_mesh = None
                            body.upper_arm_mesh = None
                            body.torso_mesh = None
                            body.head_mesh = None
                            bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass
            
            elif x in ["/heal", "/h"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("health"))
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("health"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("health"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/mine", "/ml"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("land_mines"))
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("land_mines"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("land_mines"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/impact", "/im"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("impact_bombs"))
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("impact_bombs"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("impact_bombs"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/sticky", "/st"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("sticky_bombs"))
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("sticky_bombs"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("sticky_bombs"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/icy", "/ic"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("ice_bombs"))
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("ice_bombs"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("ice_bombs"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/curse", "/cr"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("curse"))
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("curse"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("curse"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/heal", "/hl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("health"))
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("health"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("health"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass



            elif x in ["/unfreeze", "/thaw"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.ThawMessage())
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.ThawMessage())
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.ThawMessage())
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/gloves", "/g"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.PowerupMessage("punch"))
                                nicks = i.getname()
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.PowerupMessage("punch"))
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.PowerupMessage("punch"))
                        nicks = activity.players[num].getname()
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/freeze", "/fr"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage(bs.FreezeMessage())
                                nicks = i.getname()
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage(bs.FreezeMessage())
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage(bs.FreezeMessage())
                        nicks = activity.players[num].getname()
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass


            elif x in ["/sleep", "/sl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage("knockout", 10000)
                                nicks = i.getname()
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage("knockout", 10000)
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage("knockout", 10000)
                        nicks = activity.players[num].getname()
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x in ["/celebrate", "/cl"]:
                try:
                    if z == []:
                        for i in activity.players:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.handlemessage("celebrate", 10000)
                                nicks = i.getname()
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["a", "all"]:
                        for players in activity.players:
                            players.actor.node.handlemessage("celebrate", 10000)
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    else:
                        num = int(z[0])
                        body = activity.players[num].actor.node
                        body.handlemessage("celebrate", 10000)
                        nicks = activity.players[num].getname()
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            else:
                normal(msg, clid, acid)



class admin(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = bs.get_foreground_host_activity()
        session = bs.get_foreground_host_session()
        color = (1, 1, 0)
        confirmation = "Command Executed"
        
        
        with bs.ContextRef():
            if x in ["/slow", "/sm"]:
                try:
                    if activity.globalsnode.slow_motion != True:
                        activity.globalsnode.slow_motion = True
                    else:
                        activity.globalsnode.slow_motion = False
                    bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except:
                    pass

            elif x == "/check":
                bs.broadcastmessage("Commands working :p", color=color, transient=True, clients=[clid])
            
            elif x in ["/fly", "/fl"]:
                try:
                    if z == []:
                            for i in activity.players:
                                if i.sessionplayer.inputdevice.client_id == clid:
                                    plr = i
                                    nfly.NewFly(plr)
                                    bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                    elif z[0] in ["all", "a"]:
                        for players in activity.players:
                            plr = players
                            nfly.NewFly(plr)
                            bs.broadcastmessage(
                                "You have wings, Fly!!", color=color)
                    else:
                        num = int(z[0])
                        player = activity.players[num]
                        nfly.NewFly(player)
                        bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except Exception as e:
                    print(e)
                    
            elif x in ["/godmode", "/gm"]:
                try:
                    for i in activity.players:
                        if z == []:
                            if i.sessionplayer.inputdevice.client_id == clid:
                                i.actor.node.invincible = True
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                        elif z[0] in ["all", "a"]:
                            for players in activity.players:
                                players.actor.node.invincible = True
                                bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                        else:
                            num = int(z[0])
                            body = activity.players[num].actor.node
                            body.invincible = True
                            nicks = activity.players[num].getname()
                            bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                except Exception as e:
                    print(e)
                
            else:
                vip(msg, clid, acid)




class owner(object):
    def __init__(self, msg, clid, acid):
        x = msg.split(' ')[0]
        z = msg.split(' ', 1)[1:5]
        activity = bs.get_foreground_host_activity()
        session = bs.get_foreground_host_session()
        color = (1, 1, 0)
        confirmation = "Command Executed"
        
        with bs.ContextRef():
            if x == "/kick":
                kick_id = z[0]
                for i in bs.get_game_roster():
                    try:
                        if i["client_id"] == kick_id:
                            bs.disconnect_client(int(kick_id))
                            bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
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
                                    bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                                elif response is None:
                                    bs.broadcastmessage(f"Role {z[1]} does not exist", color=color, transient=True, clients=[clid])
                                elif not response:
                                    bs.broadcastmessage(f"Player already has a higher role", color=color, transient=True, clients=[clid])
                            elif z[0] == "take":
                                response = permissions.TakeRole(z[1], playerid)
                                if response:
                                    bs.broadcastmessage(confirmation, color=color, transient=True, clients=[clid])
                                elif not response:
                                    bs.broadcastmessage(f"Player does not have {z[1]}", color=color, transient=True, clients=[clid])
                                elif response is None:
                                    bs.broadcastmessage(f"Role does not exist", color=color, transient=True, clients=[clid])
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
                            for i in bs.get_game_roster():
                                if i["client_id"] == int(num):
                                    playerid = i["accountid"]
                        responsedata = permissions.Effect(z[0], z[1], playerid)
                        if not responsedata:
                            bs.broadcastmessage(f"Effect {z[1]} does not exist", color=color, transient=True, clients=[clid])
                            return
                        if z[0] == "add":
                            if responsedata == "AlreadyHas":
                                bs.broadcastmessage(
                                    f"Player already has effect {z[1]}", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata == "Morethan2":
                                bs.broadcastmessage(
                                    f"Player has two effects already", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata:
                                bs.broadcastmessage(
                                    confirmation, color=color, transient=True, clients=[clid]
                                )
                        elif z[0] == "take":
                            if responsedata == "Noeffects":
                                bs.broadcastmessage(
                                    f"Player do not have any effect", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata == "Noeffect":
                                bs.broadcastmessage(
                                    f"Player do not have {z[1]}", color=color, transient=True, clients=[clid]
                                )
                                return
                            elif responsedata:
                                bs.broadcastmessage(
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
                            for i in bs.get_game_roster():
                                if i["client_id"] == int(num):
                                    playerid = i["accountid"]
                        response = permissions.Tag(playerid, z[1], z[0])
                        if response == None:
                            bs.broadcastmessage(
                                "Either give or remove tag", color=color, transient=True, clients=[clid]
                            )
                            return
                        elif z[0] == "give":
                            if response:
                                bs.broadcastmessage(
                                    confirmation, color=color, transient=True, clients=[clid]
                                )
                            else:
                                bs.broadcastmessage(
                                    "Error when adding tag", color=color, transient=True, clients=[clid]
                                )
                        elif z[0] == "remove":
                            if response:
                                bs.broadcastmessage(
                                    confirmation, color=color, transient=True, clients=[clid]
                                )
                            else:
                                bs.broadcastmessage(
                                    "Error when removing tag", color=color, transient=True, clients=[clid]
                                )
                except Exception as e:
                    print(e)              

            else:
                admin(msg, clid, acid)
                