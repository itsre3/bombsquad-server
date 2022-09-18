
# ba_meta require api 7

from __future__ import annotations

from typing import TYPE_CHECKING

import _ba
import ba
import settings
from chat_handler import chat_handler
import coinsystem


if TYPE_CHECKING:
    from typing import Sequence, Any

sett = settings.get_settings_data()

def filter_chat_message(msg: str, client_id: int) -> str | None:
    """Intercept/filter chat messages.

    Called for all chat messages while hosting.
    Messages originating from the host will have clientID -1.
    Should filter and return the string to be displayed, or return None
    to ignore the message.
    """
    chat_handler.check_perms(msg, client_id)
    return msg


def launcher():
    if sett["currency"]["enabled"] and settings["currency"]["settings"]["askquestions"]:
        coinsystem.run_questions()
        

launcher()