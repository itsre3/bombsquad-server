
# ba_meta require api 9
from __future__ import annotations

from typing import TYPE_CHECKING

import _babase
import bascenev1 as bs
import babase
import settings
from chat_handler import chat_handler
import coinsystem
from overriders import _stats_ovr, _trans_in_ovr
from core import Core


if TYPE_CHECKING:
    from typing import Sequence, Any

sett = settings.get_settings_data()

def filter_chat_message(msg: str, client_id: int) -> str | None:
    return chat_handler.check_perms(msg, client_id)


def launcher() -> None:
    if sett["currency"]["enabled"]:
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
        
    _trans_in_ovr.enable()


# ba_meta export babase.Plugin
class Main(babase.Plugin):
    def on_app_running(self):
        launcher()