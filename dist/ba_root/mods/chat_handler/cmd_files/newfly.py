
from __future__ import annotations
from typing import TYPE_CHECKING
import ba
import _ba
from bastd.gameutils import SharedObjects
from bastd.actor.popuptext import PopupText
from ba._generated.enums import InputType
if TYPE_CHECKING:
    from typing import Optional

class simplebox(ba.Actor):
    def __init__(self, position=(0,1,0), velocity=(0,0,0)):
        ba.Actor.__init__(self)
        shared = SharedObjects.get()
        self.bombmaterial = ba.Material()
        self.bombmaterial.add_actions(
            conditions = ((("we_are_younger_than", 100),
                            "or", ("they_are_younger_than", 100)),
                            "and", ("they_have_material", shared.object_material)),
            actions = ("modify_node_collision", "collide", False))
        
        self.bombmaterial.add_actions(
            conditions = ("they_have_material", shared.pickup_material),
            actions = ("modify_part_collision", "use_node_collide", False))
        self.bombmaterial.add_actions(
            actions = ("modify_part_collision", "friction", 0.3))
            
        self.node = ba.newnode(
                        "prop",
                        delegate=self,
                        owner=None,
                        attrs={"model": ba.getmodel("tnt"),
                               "body": "sphere",
                               "color_texture": ba.gettexture("tnt"),
                               "reflection": "soft",
                               "model_scale": 1,
                               "body_scale": 1,
                               "density": 1,
                               "reflection_scale": [0.23],
                               "shadow_size": 0.6,
                               "position": position,
                               "velocity": velocity,
                               "materials": [shared.object_material,
                                             shared.footing_material,
                                             self.bombmaterial]})
                               
    def handlemessage(self, msg):
        if isinstance(msg, ba.DieMessage):
            self.node.delete()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            ba.screenmessage("Dieee")
            self.handlemessage(ba.DieMessage())
        else:
            super().handlemessage(msg)

        

class NewFly(object):
    def __init__(self, owner=None):
        self.owner = owner
        if self.owner.exists():
            self.box = simplebox(
                position=self.owner.actor.node.position).autoretain()
            
            self.owner.actor.node.hold_node = self.box.node
            self.owner.actor.node.hold_body = 1
            self.box.node.model = None
            self.owner.actor.node.handlemessage(
                'impulse', self.box.node.position[0], self.box.node.position[1], self.box.node.position[2],
                 0.0, 0.0, 0.0, 200.0, 200.0, 0.0, 0.0, 0.0, 1.0, 0.0)
            self.set_fly()
            
        else:
            ba.screenmessage("Error", (1,0,0))
            
    def move(self, type_name: str):
        if self.box.exists():
            if type_name == "up":
                self.box.node.velocity = (0, 45, 0)
            elif type_name == "down":
                self.box.node.velocity = (0, 10, 0)
            elif type_name == "go":
                self.box.node.velocity = (-50, 0, 0)
            elif type_name == "back":
                self.box.node.velocity = (50, 0, 0)
            elif type_name == "left":
                self.box.node.velocity = (0, 0, -50)
            elif type_name == "right":
                self.box.node.velocity = (0, 0, 50)
             
             
    def reset_move(self):
        if self.box.node.exists() and self.owner.exists():
            PopupText("flying stopped by player",
                      color=(1,1,0),
                      scale=1,
                      position=self.owner.actor.node.position).autoretain()
            
            self.owner.actor.node.hold_body = 0
            self.box.node.delete()
            self.owner.actor.connect_controls_to_player()
            
        elif self.box.exists() and not self.owner.exists():
            self.box.node.delete()

        elif self.owner.exists() and not self.box.exists():
            self.owner.actor.node.hold_body = 0
            self.owner.actor.disconnect_controls_from_player()
            self.owner.actor.connect_controls_to_player()
            
    def set_fly(self):
        self.owner.assigninput(InputType.PICK_UP_PRESS, ba.Call(self.move, "up"))
        self.owner.assigninput(InputType.JUMP_PRESS, ba.Call(self.move, "down"))
        self.owner.assigninput(InputType.LEFT_PRESS, ba.Call(self.move, "go"))
        self.owner.assigninput(InputType.RIGHT_PRESS, ba.Call(self.move, "back"))
        self.owner.assigninput(InputType.UP_PRESS, ba.Call(self.move, "left"))
        self.owner.assigninput(InputType.DOWN_PRESS, ba.Call(self.move, "right"))
      #  self.owner.assigninput(InputType.JUMP_PRESS, ba.Call(self.reset_move))
        self.owner.assigninput(InputType.PUNCH_PRESS, ba.Call(self.reset_move))
        
