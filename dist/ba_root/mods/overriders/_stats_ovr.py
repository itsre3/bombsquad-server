#

# ba_meta require api 7
from __future__ import annotations

import bascenev1 as bs
import _ba
from bs._language import Lstr
from bs._stats import Stats as sta, PlayerScoredMessage, PlayerRecord
import settings, coinsystem
from bs._error import print_exception
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any, Sequence



def player_scored(self,
                  player: bs.Player,
                  base_points: int = 1,
                  target: Sequence[float] | None = None,
                  kill: bool = False,
                  victim_player: bs.Player | None = None,
                  scale: float = 1.0,
                  color: Sequence[float] | None = None,
                  title: str | bs.Lstr | None = None,
                  screenmessage: bool = True,
                  display: bool = True,
                  importance: int = 1,
                  showpoints: bool = True,
                  big_message: bool = False) -> int:
    """Register a score for the player.

    Return value is actual score with multipliers and such factored in.
    """
    # FIXME: Tidy this up.
    # pylint: disable=cyclic-import
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    from bascenev1lib.actor.popuptext import PopupText
    from bs import _math
    from bs._gameactivity import GameActivity
    name = player.getname()
    s_player = self._player_records[name]

    if kill:
        s_player.submit_kill(showpoints=showpoints)

    display_color: Sequence[float] = (1.0, 1.0, 1.0, 1.0)
    if color is not None:
        display_color = color
    elif importance != 1:
        display_color = (1.0, 1.0, 0.4, 1.0)
    points = base_points

    # If they want a big announcement, throw a zoom-text up there.
    if display and big_message:
        try:
            assert self._activity is not None
            activity = self._activity()
            if isinstance(activity, GameActivity):
                name_full = player.getname(full=True, icon=False)
                activity.show_zoom_message(
                    Lstr(resource='nameScoresText',
                         subs=[('${NAME}', name_full)]),
                    color=_math.normalized_color(player.team.color))
        except Exception:
            print_exception('error showing big_message')

        # If we currently have a actor, pop up a score over it.
    if display and showpoints:
        our_pos = player.node.position if player.node else None
        if our_pos is not None:
            if target is None:
                target = our_pos

            # If display-pos is *way* lower than us, raise it up
            # (so we can still see scores from dudes that fell off cliffs).
            display_pos = (target[0], max(target[1], our_pos[1] - 2.0),
                           min(target[2], our_pos[2] + 2.0))
            activity = self.getactivity()
            if activity is not None:
                if title is not None:
                    sval = Lstr(value='+${A} ${B}',
                                subs=[('${A}', str(points)),
                                      ('${B}', title)])
                else:
                    sval = Lstr(value='+${A}',
                                subs=[('${A}', str(points))])
                PopupText(sval,
                          color=display_color,
                          scale=1.2 * scale,
                          position=display_pos).autoretain()
    # Tally kills.
    if kill:
        s_player.accum_kill_count += 1
        s_player.kill_count += 1
        

    # Report non-kill scorings.
    try:
        if screenmessage and not kill:
            _babase.screenmessage(Lstr(resource='nameScoresText',
                                   subs=[('${NAME}', name)]),
                              top=True,
                              color=player.color,
                              image=player.get_icon())
    except Exception:
        print_exception('error announcing score')

    s_player.score += points
    s_player.accumscore += points

    # Inform a running game of the score.
    if points != 0:
        activity = self._activity() if self._activity is not None else None
        if activity is not None:
            activity.handlemessage(PlayerScoredMessage(score=points))
    
    id = player._sessionplayer.get_v1_account_id()
    try:
        sett = settings.get_settings_data()
        if sett["currency"]["enabled"]:
            coinsystem.add_coins_by_pbid(id, 2)
    except Exception:
        print_exception("Cant add coins")
        pass

    return points


def enable():
    sta.player_scored = player_scored