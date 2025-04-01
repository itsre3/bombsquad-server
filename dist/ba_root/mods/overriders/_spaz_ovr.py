
#Did not write every single code here

from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs
import _babase
import bascenev1lib, weakref, random, math, time, base64, os, json
from bascenev1lib.actor import spaz
from bascenev1lib.gameutils import SharedObjects
from admin import permissions
if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any, Union

tt = bs.TimeType.SIM
tf = bs.TimeFormat.MILLISECONDS


class SurroundFactory(object):
    def __init__(self):
        self.bones_tex = bs.gettexture("powerupCurse")
        self.bones_model = bs.getmodel("bonesHead")
        self.bear_tex = bs.gettexture("bearColor")
        self.bear_model = bs.getmodel("bearHead")
        self.ali_tex = bs.gettexture("aliColor")
        self.ali_model = bs.getmodel("aliHead")
        self.b9000_tex = bs.gettexture("cyborgColor")
        self.b9000_model = bs.getmodel("cyborgHead")
        self.frosty_tex = bs.gettexture("frostyColor")
        self.frosty_model = bs.getmodel("frostyHead")
        self.cube_tex = bs.gettexture("crossOutMask")
        self.cube_model = bs.getmodel("powerup")
        try:
            self.miku_model = bs.getmodel("operaSingerHead")
            self.miku_tex = bs.gettexture("operaSingerColor")
        except:
            bs.print_exception()
        self.impact_sound = bs.getsound("impactMedium")
        shared = SharedObjects.get()
        self.surround_material = bs.Material()
        self.surround_material.add_actions(actions=("modify_node_collision", "collide", False))



class ProSurroundBall(bs.Actor):
    def __init__(self, spaz, shape="bones"):
        bs.Actor.__init__(self)
        self.spaz_ref = weakref.ref(spaz)
        self.source_player = spaz
        factory = self.getFactory()
        self.node = bs.newnode("prop",
                        attrs={"model": bs.getmodel("shield"),
                               "body": "sphere",
                               "color_texture": bs.gettexture("shield"),
                               "reflection": "soft",
                               "model_scale": 0,
                               "body_scale": 0,
                               "density": 0,
                               "reflection_scale": [0.15],
                               "shadow_size": 0.6,
                               "position": spaz.node.position,
                               "velocity": (0, 0, 0),
                               "materials": [SharedObjects.get().object_material, factory.surround_material]}, delegate=self)
        m = bs.newnode('math', attrs={
                    'input1': (0,0,0),
                    'operation': 'add'
            })
        self.shield = bs.newnode('shield',
                                 owner=self.node,
                                 attrs={
                                     'color': (0.3, 0.2, 2.0),
                                     'radius': 0.59
                                 })
        self.node.connectattr('position', m, 'input2')
        m.connectattr('output', self.shield, 'position')
        bs.animate_array(node=self.shield, attr='color', size=3,
            keys={0:(random.choice([1,2,3,4,5,6,7,8,9]), random.choice([1,2,3,4,5,6,7,8,9]), random.choice([1,2,3,4,5,6,7,8,9])),
                0.2: (2,0,2),
                0.4: (2,2,0),
                0.6: (0,2,0),
                0.8: (0,2,2),
                1: (0,0,2),
                1.2: (2,0,0)},
                loop = True)
        self.pro_surround_timer = None
        self.pro_surround_radius = 1.0
        self.angle_delta = math.pi / 12.0
        self.cur_angle = random.random() * math.pi * 2.0
        self.cur_height = 0.0
        self.cur_height_dir = 1
        self.height_delta = 0.2
        self.height_max = 1.0
        self.height_min = 0.1
        self.init_timer(spaz.node.position)
        if self.surround_timer:
            self.light_time = bs.timer(0.03, self.light, repeat=True)

    def light(self):
        flash_color = (1.0, 0.8, 0.4)
        if self.node.exists():
            flash = bs.newnode('flash',
                        attrs={
                           'position': self.node.position,
                           'size': 0.5,
                           'color': flash_color
                       })
            bs.timer(0.03, flash.delete)
            bs.animate_array(node=flash, attr='color', size=3,
                keys={0:(random.choice([0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]), random.choice([0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]), random.choice([0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95])),
                0.2: (2,0,2),
                0.4: (2,2,0),
                0.6: (0,2,0),
                0.8: (0,2,2),
                1: (0,0,2),
                1.2: (2,0,0)},
                loop = True)
        
    def get_target_position(self, spaz_position):
        p = spaz_position
        pt = (p[0] + self.pro_surround_radius * math.cos(self.cur_angle), p[1] + self.cur_height, p[2] + self.pro_surround_radius * math.sin(self.cur_angle))
        self.cur_angle += self.angle_delta
        self.cur_height += self.height_delta * self.cur_height_dir
        if (self.cur_height > self.height_max) or (self.cur_height < self.height_min): self.cur_height_dir = -self.cur_height_dir
        return pt

    def init_timer(self, p):
        self.node.position = self.get_target_position(p)
        self.surround_timer = bs.Timer(30, self.circle_move, repeat=True,  timetype=tt, timeformat=tf)

    def circle_move(self):
        spaz = self.spaz_ref()
        if spaz is None or not spaz.is_alive() or not spaz.node.exists():
            self.handlemessage(bs.DieMessage())
            return
        p = spaz.node.position
        pt = self.get_target_position(p)
        pn = self.node.position
        d = [pt[0] - pn[0], pt[1] - pn[1], pt[2] - pn[2]]
        speed = self.get_max_speed_by_dir(d)
        self.node.velocity = speed

    @staticmethod
    def get_max_speed_by_dir(direction):
        k = 7.0 / max((abs(x) for x in direction))
        return tuple(x * k for x in direction)

    def handlemessage(self, m):
        bs.Actor.handlemessage(self, m)
        if isinstance(m, bs.DieMessage):
            if self.surround_timer is not None: self.surround_timer = None
            self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage())


    def getFactory(cls):
        activity = bs.getactivity()
        if activity is None:
            raise Exception("no current activity")
        try:
            return activity._sharedSurroundFactory
        except Exception:
            f = activity._sharedSurroundFactory = SurroundFactory()
            return f

class Effects(bs.Actor):
    def __init__(self, spaz, player):
        bs.Actor.__init__(self)
        self.spaz = spaz
        self.player = player
        playernodeid = self.player.node.playerID
        
        for i in _babase.get_foreground_host_session().sessionplayers:
            if i.activityplayer is not None and i.activityplayer.node.playerID == playernodeid:
                accountid = i.get_v1_account_id()
        try:
            if permissions.check_effect(accountid):
                efct = permissions.check_effect(accountid)
                
                if "ProSurround" in efct:
                    if self.spaz is None:
                        return
                    ProSurroundBall(self.spaz)
                    pass
                    
                elif "Rainbow" in efct:
                    bs.timer(2, bs.Call(self.run_rainbow), repeat=True)
                    pass

                elif "Spark" in efct:
                    bs.timer(0.2, bs.Call(self.emit, "spark"), repeat=True)
                    pass

                elif "Slime" in efct:
                    bs.timer(0.2, bs.Call(self.emit, "slime"), repeat=True)
                    pass

                elif "Metal" in efct:
                    bs.timer(0.2, bs.Call(self.emit, "metal"), repeat=True)
                    pass

                elif "Ice" in efct:
                    bs.timer(0.2, bs.Call(self.emit, "ice"), repeat=True)
                    pass

                elif "Stickers" in efct:
                    bs.timer(0.2, self.stickers, repeat=True)
                    pass

        except Exception as e:
            print(e)
                    
    def emit(self, effect: str) -> None:
        new_spaz = self.spaz
        if new_spaz is None or not new_spaz.node.exists() or not new_spaz.is_alive():
            return
        bs.emitfx(position=self.spaz.node.position,
                  velocity=self.spaz.node.velocity,
                  count=int(16.0),
                  scale=0.6,
                  spread=0.8,
                  chunk_type=effect)
                  
    def run_rainbow(self) -> None:
        new_spaz = self.spaz
        if new_spaz is None or not new_spaz.node.exists() or not new_spaz.is_alive():
            return
        bs.animate_array(self.spaz.node,'color',3,
            {0:(random.choice([1,2,3,4,5,6,7,8,9]), random.choice([1,2,3,4,5,6,7,8,9]), random.choice([1,2,3,4,5,6,7,8,9])),
            0.2: (2,0,2),
            0.4: (2,2,0),
            0.6: (0,2,0),
            0.8: (0,2,2),
            1: (0,0,2),
            1.2: (2,0,0)},
            loop = True)
            
            
    def stickers(self) -> None:
        new_spaz = self.spaz
        if new_spaz is None or not new_spaz.node.exists() or not new_spaz.is_alive():
            return
        bs.emitfx(position=self.spaz.node.position,
                  velocity=self.spaz.node.velocity,
                  count=10,
                  spread=0.1,
                  scale=0.8,
                  chunk_type='spark',
                  emit_type='stickers')
