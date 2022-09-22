
from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import settings
import os
import random
import json
from ba._generated.enums import SpecialChar
if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any

sett = settings.get_settings_data()
correct_answer = None
answered_by = None
base_dir = os.path.join(_ba.env()['python_directory_user'], "coinsystem" + os.sep
)
bankfile = base_dir+"bank.json"
questionslist = sett["currency"]["settings"]["askquestions"]["questions"]

def ask_question():
    global answered_by
    global correct_answer
    keys = []
    for x in questionslist:
        keys.append(x)
    question = keys[random.randrange(len(keys))]
    correct_answer = questionslist[question]
    if question == 'additions':
        a = random.randrange(100, 999)
        b = random.randrange(10, 99)
        correct_answer = str(a + b)
        question = f'What is {str(a)} + {str(b)}?'
    elif question == 'multiplications':
        a = random.randrange(100, 999)
        availableb = [0, 1, 2, 5, 10]
        b = availableb[random.randrange(4)]
        correct_answer = str(a * b)
        question = f'What is {str(a)} x {str(b)}?'
    _ba.chatmessage(question)
    answered_by = None
    return


def check_answer(msg, clientID):
    global answered_by
    global correct_answer

    if msg == correct_answer:
        if answered_by is not None:
            ba.screenmessage(f'Already awarded to {answered_by}.', (0.8,1,0))
        else:
            ros = _ba.get_game_roster()
            for i in ros:
                if (i is not None) and (i != {}) and (i['client_id'] == clientID):
                    answered_by = i['players'][0]['name']
                    account_id = i['account_id']
            try:
                ba.screenmessage(f"Congratulations {answered_by}!, You won {_ba.charstr(SpecialChar.TICKET)}10.", (0,1,0), transient=True, clients=[clientID])
                add_coins_by_pbid(account_id, 10)
            except:
                pass
    return None

def convert_alias(cmd):
    # also using this as a log for commands created
    if cmd in ["/gloves", "/gl", "/g"]:
        return "gloves"
        
    elif cmd in ["/slow", "/sm"]:
        return "sm"

    elif cmd in ["/end", "/e"]:
        return "end"


def get_command_price(cmd):
    print(cmd)
    cnv_cmd = convert_alias(cmd)
    if cnv_cmd is not None:
        if cnv_cmd in sett["currency"]["settings"]["shop"]["commands"]["prices"]: #very long xd
            return int(sett["currency"]["settings"]["shop"]["commands"]["prices"][cnv_cmd])
    else:
        _ba.playsound(_ba.getsound("error"))
        return None


def add_coins_by_pbid(account_id, amount):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.loads(f.read())
    else:
        bank = {}
    if account_id not in bank:
        bank[account_id] = {}
        bank[account_id]["cash"] = 0
        bank[account_id]["dc_id"] = 0
    bank[account_id]["cash"] += amount
    with open(bankfile, 'w') as f:
        f.write(json.dumps(bank, indent=4))


def get_coins_by_pbid(account_id):
    if os.path.exists(bankfile):
        with open(bankfile, 'r') as f:
            coins = json.loads(f.read())
        if account_id in coins:
            return coins[account_id]["cash"]
    return 0

def add_coins_by_dcid(dcid, amount):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.loads(f.read())
    for x in bank:
        if bank[x]["dc_id"] == dcid:
            bank[x]["cash"] += amount
            with open(bankfile, 'w') as f:
                f.write(json.dumps(bank, indent=4))
        else:
            return None

def get_coins_by_dcid(dcid):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.loads(f.read())
    else:
        bank = {}
    for x in bank:
        if bank[x]["dc_id"] == dcid:
            bal = bank[x]["cash"]
            return bal
        else:
            return None


cstimer = None
def run_questions():
    global cstimer
    cstimer = ba.timer(20, ask_question, repeat=True)
