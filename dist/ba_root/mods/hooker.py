
from __future__ import annotations

from typing import TYPE_CHECKING

import _ba
import ba
from chat_handler import chat_handler


if TYPE_CHECKING:
    from typing import Sequence, Any


def filter_chat_message(msg: str, client_id: int) -> str:
    """Intercept/filter chat messages.

    Called for all chat messages while hosting.
    Messages originating from the host will have clientID -1.
    Should filter and return the string to be displayed, or return None
    to ignore the message.
    """
    return chat_handler.check_perms(msg, client_id)

