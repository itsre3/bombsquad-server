
# Default settings file. Enable and disable
# unwanted stuff and change values of items


# ===== Coinsystem Settings ===== 
def currency():
    return {
        "enabled": True,
        "settings": {
            "askquestions": {
                "enabled": False,
                "questiontimer": 20,
                "questions": {
                    "Who is the owner of this server?": "smoothy",
                    "Who is the editor of this server?": "smoothy",
                    "Have you subscribed to Hey Smoothy YouTube?": "maybe",
                    "multiplications": None,
                    "additions": None
                }
            },
            "shop": {
                "roles": {
                    "enabled": True,
                    "prices": {
                        "owner": 100000,
                        "admin": 70000,
                        "vip": 50000
                    }
                },
                "characters": {
                    "enabled": True,
                    "prices": {
                        "Kronk": 150,
                        "Zoe": 250,
                        "Jack Morgan": 350,
                        "Mel": 450,
                        "Snake Shadow": 550,
                        "Bones": 650,
                        "Bearnard": 700,
                        "Agent Johnson": 800,
                        "Frosty": 850,
                        "Pascal": 900,
                        "Grumbledorf": 950,
                        "B-9000": 1000,
                        "Easter Bunny": 1050,
                        "Taobao Mascot": 1150,
                        "Santa Claus": 900
                    }
                },
                "commands": {
                    "enabled": True,
                    "prices": {
                        "gloves": 50,
                        "gm": 100,
                        "sm": 100,
                        "end": 100
                    }
                }
            }
        }
    }

# ===== Chat commands =====
def cht():
    return {
        "enabled": True,
        "settings": {
            "cht_cmds": {
                "enabled": True
            }
        }
    }
