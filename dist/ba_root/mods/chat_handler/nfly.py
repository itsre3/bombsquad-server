
from __future__ import annotations
from typing import TYPE_CHECKING

import ba
import _ba

if TYPE_CHECKING:
    from typing import Union, Sequence

def on_dfly_press(player):
    if player.actor.node:
        player.actor.node.handlemessage(
            'impulse',
            player.actor.node.position[0], player.actor.node.position[1], player.actor.node.position[2],
            0,0,0,200,200,0,0,0,1,0)

def NewFly(player):
    player.assigninput(ba.InputType.JUMP_PRESS, ba.Call(
        on_dfly_press, player))
