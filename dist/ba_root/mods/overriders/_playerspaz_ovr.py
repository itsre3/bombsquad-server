

from __future__ import annotations

from typing import TYPE_CHECKING



import ba
from bastd.actor.spaz import Spaz
from bastd.actor.playerspaz import PlayerSpaz
from stats import mystats
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


def rank(owner, p):
    node = ba.newnode('math', 
               owner = owner,
               attrs = {
               'input1': (0, 1.2, 0),
               'operation': 'add'
               })
    
    owner.connectattr('torso_position', node, 'input2')
    
    text = ba.newnode('text',
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



def __init__(
    self,
    player: ba.Player,
    color: Sequence[float] = (1.0, 1.0, 1.0),
    highlight: Sequence[float] = (0.5, 0.5, 0.5),
    character: str = 'Spaz',
    powerups_expire: bool = True,
    ):
    """Create a spaz for the provided ba.Player.
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
    self.last_player_attacked_by: ba.Player | None = None
    self.last_attacked_time = 0.0
    self.last_attacked_type: tuple[str, str] | None = None
    self.held_count = 0
    self.last_player_held_by: ba.Player | None = None
    self._player = player
    self._drive_player_position()
    
    show_rank(self.node, self._player)
    _spaz_ovr.ProSurroundBall(Spaz.node)




def enable():
    PlayerSpaz.__init__ = __init__
