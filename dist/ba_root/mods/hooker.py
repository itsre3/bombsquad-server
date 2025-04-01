
# ba_meta require api 7

from __future__ import annotations

from typing import TYPE_CHECKING

import _babase
import bascenev1 as bs
import settings
from chat_handler import chat_handler
import coinsystem
from overriders import _stats_ovr
from core import Core


if TYPE_CHECKING:
    from typing import Sequence, Any

sett = settings.get_settings_data()

def filter_chat_message(msg: str, client_id: int) -> str | None:
    return chat_handler.check_perms(msg, client_id)


def launcher() -> None:
    if sett["currency"]["enabled"]:
        if sett["currency"]["settings"]["askquestions"]:
            coinsystem.run_questions()
        _stats_ovr.enable()
    
    if sett["stats"]["enabled"]:
        from stats import mystats
        from overriders import _playerspaz_ovr
        mystats.run_stats()
        _playerspaz_ovr.enable()
    
    if sett["discord"]["enabled"]:
        from discord_bot import b_launch
        b_launch.init()
        
    if sett["website"]["enabled"]:
        from web import webst
        webst.run()
        
    Core.run()