
# ba_meta require api 7

from __future__ import annotations

from typing import TYPE_CHECKING

import _ba
import ba
import settings
from chat_handler import chat_handler
import coinsystem
from overriders import _stats_ovr


if TYPE_CHECKING:
    from typing import Sequence, Any

sett = settings.get_settings_data()

def filter_chat_message(msg: str, client_id: int) -> str | None:
    try:
        return chat_handler.check_perms(msg, client_id)
    except:
        return msg


def launcher() -> None:
    if sett["currency"]["enabled"]:
        if sett["currency"]["settings"]["askquestions"]:
            coinsystem.run_questions()
        _stats_ovr.enable()
    
    if sett["stats"]["enabled"]:
        from stats import mystats
        mystats.run_stats()