
from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs
import random
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor import spaz
from bascenev1lib.actor.playerspaz import PlayerSpaz
from stats import mystats
from admin import  permissions
from overriders import _spaz_ovr

if TYPE_CHECKING:
    from typing import Any, Sequence, Literal


def show_rank(node, player):
    acid = player.sessionplayer.get_v1_account_id()
    f_stats = mystats.get_stats_by_id(acid)
    if f_stats:
        position = f_stats["rank"]
        rank(node, position)
    else:
        pass


def add_tag(node, player):
    acid = player.sessionplayer.get_v1_account_id()
    tag_text = permissions.check_tag(acid)
    if tag_text:
        tag(node, tag_text)
    else:
        pass


def rank(owner, p):
    node = bs.newnode('math', 
               owner = owner,
               attrs = {
               'input1': (0, 1.2, 0),
               'operation': 'add'
               })
    
    owner.connectattr('torso_position', node, 'input2')
    text = bs.newnode('text',
              owner = owner,
              attrs = {
              'text': str(p),
              'in_world': True,
              'shadow': 1.0,
              'color': (1, 1, 1),
              'scale': 0.01,
              'flatness': 1.0,
              'h_align': 'center'
              })
    node.connectattr('output', text, 'position')


def tag(owner, tagtext: str = "Nothing"):
    node = bs.newnode(
        "math",
        owner=owner,
        attrs={
            "input1": (0, 1.5, 0),
            "operation": "add"
        }
    )
    owner.connectattr("torso_position", node, "input2")
    text = bs.newnode(
        "text",
        owner=owner,
        attrs={
            "text": tagtext,
            "in_world": True,
            "shadow": 1.0,
            "color": (2, 1, 0.5),
            "scale": 0.01,
            "flatness": 1.0,
            "h_align": "center"
        }
    )
    node.connectattr("output", text, "position")
    if tagtext == "owner":
        bs.animate_array(
            text,
            'color',
            3,
            {
                0: (2,2,2),
                0.2: (2,0,2),
                0.4: (2,2,0),
                0.6: (0,2,0),
                0.8: (0,2,2),
                1: (0,0,2),
                1.2: (2,0,0)
            },
            loop = True)


def __init__(
    self,
    player: bs.Player,
    color: Sequence[float] = (1.0, 1.0, 1.0),
    highlight: Sequence[float] = (0.5, 0.5, 0.5),
    character: str = 'Spaz',
    powerups_expire: bool = True,
    ):
    """Create a spaz for the provided bs.Player.
    Note: this does not wire up any controls;
    you must call connect_controls_to_player() to do so.
    """

    Spaz.__init__(
        self,
        color=color,
        highlight=highlight,
        character=character,
        source_player=player,
        start_invincible=True,
        powerups_expire=powerups_expire,
    )
    self.last_player_attacked_by: bs.Player | None = None
    self.last_attacked_time = 0.0
    self.last_attacked_type: tuple[str, str] | None = None
    self.held_count = 0
    self.last_player_held_by: bs.Player | None = None
    self._player = player
    self._drive_player_position()
    
    show_rank(self.node, self._player)
    add_tag(self.node, self._player)
    _spaz_ovr.Effects(self, self._player)




def enable():
    PlayerSpaz.__init__ = __init__
    