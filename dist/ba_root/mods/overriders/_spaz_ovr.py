
#Did not write every single code here

from __future__ import annotations
from typing import TYPE_CHECKING

import ba
import _ba
import bastd, weakref, random, math, time, base64, os, json
from bastd.actor import spaz
from bastd.gameutils import SharedObjects
if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any, Union

tt = ba.TimeType.SIM
tf = ba.TimeFormat.MILLISECONDS


class SurroundFactory(object):
    def __init__(self):
        self.bones_tex = ba.gettexture("powerupCurse")
        self.bones_model = ba.getmodel("bonesHead")
        self.bear_tex = ba.gettexture("bearColor")
        self.bear_model = ba.getmodel("bearHead")
        self.ali_tex = ba.gettexture("aliColor")
        self.ali_model = ba.getmodel("aliHead")
        self.b9000_tex = ba.gettexture("cyborgColor")
        self.b9000_model = ba.getmodel("cyborgHead")
        self.frosty_tex = ba.gettexture("frostyColor")
        self.frosty_model = ba.getmodel("frostyHead")
        self.cube_tex = ba.gettexture("crossOutMask")
        self.cube_model = ba.getmodel("powerup")
        try:
            self.miku_model = ba.getmodel("operaSingerHead")
            self.miku_tex = ba.gettexture("operaSingerColor")
        except:
            ba.print_exception()
        self.impact_sound = ba.getsound("impactMedium")
        shared = SharedObjects.get()
        self.surround_material = ba.Material()
        self.surround_material.add_actions(actions=("modify_node_collision", "collide", False))



class ProSurroundBall(ba.Actor):
    def __init__(self, spaz, shape="bones"):
        ba.Actor.__init__(self)
        self.spaz_ref = spaz
        self.source_player = spaz
        factory = self.getFactory()
        self.pro_surround_timer = None
        self.node = ba.newnode("prop",
                        attrs={"model": ba.getmodel("shield"),
                               "body": "sphere",
                               "color_texture": ba.gettexture("shield"),
                               "reflection": "soft",
                               "model_scale": 0,
                               "body_scale": 0,
                               "density": 0,
                               "reflection_scale": [0.15],
                               "shadow_size": 0.6,
                               "position": spaz.node.position,
                               "velocity": (0, 0, 0),
                               "materials": [SharedObjects.get().object_material, factory.surround_material]}, delegate=self)
        m = ba.newnode('math', attrs={
                    'input1': (0,0,0),
                    'operation': 'add'
            })
        self.shield = ba.newnode('shield',
                                 owner=self.node,
                                 attrs={
                                     'color': (0.3, 0.2, 2.0),
                                     'radius': 0.59
                                 })
        self.node.connectattr('position', m, 'input2')
        m.connectattr('output', self.shield, 'position')
        ba.animate_array(node=self.shield, attr='color', size=3,
            keys={0:(random.choice([1,2,3,4,5,6,7,8,9]), random.choice([1,2,3,4,5,6,7,8,9]), random.choice([1,2,3,4,5,6,7,8,9])),
                0.2: (2,0,2),
                0.4: (2,2,0),
                0.6: (0,2,0),
                0.8: (0,2,2),
                1: (0,0,2),
                1.2: (2,0,0)},
                loop = True)
        self.pro_surround_radius = 1.0
        self.angle_delta = math.pi / 12.0
        self.cur_angle = random.random() * math.pi * 2.0
        self.cur_height = 0.0
        self.cur_height_dir = 1
        self.height_delta = 0.2
        self.height_max = 1.0
        self.height_min = 0.1
        self.init_timer(spaz.node.position)
        if self.pro_surround_timer:
            self.light_time = ba.timer(0.03, self.light, repeat=True)

    def light(self):
        flash_color = (1.0, 0.8, 0.4)
        if self.node.exists():
            flash = ba.newnode('flash',
                        attrs={
                           'position': self.node.position,
                           'size': 0.5,
                           'color': flash_color
                       })
            ba.timer(0.03, flash.delete)
            ba.animate_array(node=flash, attr='color', size=3,
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
        self.pro_surround_timer = ba.Timer(30, self.circle_move, repeat=True,  timetype=tt, timeformat=tf)

    def circle_move(self):
        spaz = self.spaz_ref()
        if spaz is None or not spaz.is_alive() or not spaz.node.exists():
            self.handlemessage(ba.DieMessage())
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
        ba.Actor.handlemessage(self, m)
        if isinstance(m, ba.DieMessage):
            if self.pro_surround_timer is not None: self.pro_surround_timer = None
            self.node.delete()
        elif isinstance(m, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())


    def getFactory(cls):
        activity = ba.getactivity()
        if activity is None:
            raise Exception("no current activity")
        try:
            return activity._sharedSurroundFactory
        except Exception:
            f = activity._sharedSurroundFactory = SurroundFactory()
            return f

