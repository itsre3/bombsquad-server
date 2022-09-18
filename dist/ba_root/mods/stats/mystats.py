damage_data = {}
#Don't touch the above line
"""
mystats module for BombSquad version 1.5.29
Provides functionality for dumping player stats to disk between rounds.
"""

import threading,json,os,urllib,ba,_ba
from ba._activity import Activity
from ba._music import setmusic, MusicType
from ba._generated.enums import InputType, UIScale
# False-positive from pylint due to our class-generics-filter.
from ba._player import EmptyPlayer  # pylint: disable=W0611
from ba._team import EmptyTeam  # pylint: disable=W0611
from typing import Any, Dict, Optional
from ba._lobby import JoinInfo
from ba._activitytypes import ScoreScreenActivity
import _thread

stats_path = os.path.join(_ba.env()['python_directory_user'], "stats" + os.sep)['python_directory_user']
html_file = stats_path + "stats.json"
stats_file = stats_path + "stats_page.html"



table_style = "{width:100%;border: 3px solid black;border-spacing: 5px;border-collapse:collapse;text-align:center;background-color:#fff}"
heading_style = "{border: 3px solid black;text-align:center;}"
html_start = f'''<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Test Server</title>
        <style>table{table_style} th{heading_style}</style>
    </head>
    <body>
        <h3 style="text-align:center">Top 200 Players of Phoenix Epic Teams</h3>
        <table border=1>
            <tr>
                <th><b>Rank</b></th>
                <th style="text-align:center"><b>Name</b></th>
                <th><b>Score</b></th>
                <th><b>Kills</b></th>
                <th><b>Deaths</b></th>
                <th><b>Games Played</b></th>
            </tr>
''' 

def get_stats():
    try:
        with open (stats_file, 'r') as f:
            stats = json.load(f)
        return stats
    except:
        return {}


def get_all_stats():
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf8') as f:
            try:
                jsonData = json.loads(f.read())
                return jsonData
            except:
                return {}
    else:
        return {}

def get_stats_by_id(ID: str):
    a = get_all_stats()
    if ID in a:
        return a[ID]
    else:
        return None


def refreshStats():
    # lastly, write a pretty html version.
    # our stats url could point at something like this...
    stats = get_stats()
    f=open(html_file, 'w')
    f.write(html_start)
    entries = [(a['scores'], a['kills'], a['deaths'], a['games'], a['name'], a['aid']) for a in stats.values()]
    # this gives us a list of kills/names sorted high-to-low
    entries.sort(reverse=True)
    rank = 0
    for entry in entries:
        if True:
            rank += 1
            scores = str(entry[0])
            kills = str(entry[1])
            deaths = str(entry[2])
            games = str(entry[3])
            name = str(entry[4])
            aid = str(entry[5])

            #The below kd and avg_score will not be added to website's html document, it will be only added in stats.json
            try:
                kd = str(float(kills) / float(deaths))
                kd_int = kd.split('.')[0]
                kd_dec = kd.split('.')[1]
                p_kd = kd_int + '.' + kd_dec[:3]
            except Exception:
                p_kd = "0"
            try:
                avg_score = str(float(scores) / float(games))
                avg_score_int = avg_score.split('.')[0]
                avg_score_dec = avg_score.split('.')[1]
                p_avg_score = avg_score_int + '.' + avg_score_dec[:3]
            except Exception:
                p_avg_score = "0"
            if damage_data and aid in damage_data:
                dmg = damage_data[aid]
                dmg = str(str(dmg).split('.')[0] + '.' + str(dmg).split('.')[1][:3])
            else: dmg = 0
            stats[str(aid)]["rank"] = int(rank)
            stats[str(aid)]["scores"] = int(scores)
            stats[str(aid)]["total_damage"] = float(dmg) #not working properly
            stats[str(aid)]["games"] = int(games)
            stats[str(aid)]["kills"] = int(kills)
            stats[str(aid)]["deaths"] = int(deaths)
            stats[str(aid)]["kd"] = float(p_kd)
            stats[str(aid)]["avg_score"] = float(p_avg_score)

            if rank < 201:
                #<td>{str(dmg)}</td> #removed this line as it isn't crt data
                f.write(f'''
            <tr>
                <td>{str(rank)}</td>
                <td style="text-align:center">{str(name)}</td>
                <td>{str(scores)}</td>
                <td>{str(kills)}</td>
                <td>{str(deaths)}</td>
                <td>{str(games)}</td>
            </tr>''')
    f.write('''
        </table>
    </body>
</html>''')
    f.close()

    f2 = open(stats_file, "w")
    f2.write(json.dumps(stats, indent=4))
    f2.close()

def update(score_set):
    """
    Given a Session's ScoreSet, tallies per-account kills
    and passes them to a background thread to process and
    store.
    """ 
    # look at score-set entries to tally per-account kills for this round

    account_kills = {}
    account_deaths = {}
    account_scores = {}


    for p_entry in score_set.get_records().values():
        account_id = p_entry.player.get_account_id()
        if account_id is not None:
            account_kills.setdefault(account_id, 0)  # make sure exists
            account_kills[account_id] += p_entry.accum_kill_count
            account_deaths.setdefault(account_id, 0)  # make sure exists
            account_deaths[account_id] += p_entry.accum_killed_count
            account_scores.setdefault(account_id, 0)  # make sure exists
            account_scores[account_id] += p_entry.accumscore
    # Ok; now we've got a dict of account-ids and kills.
    # Now lets kick off a background thread to load existing scores
    # from disk, do display-string lookups for accounts that need them,
    # and write everything back to disk (along with a pretty html version)
    # We use a background thread so our server doesn't hitch while doing this.
    if account_scores: UpdateThread(account_kills, account_deaths, account_scores).start()

class UpdateThread(threading.Thread):
    def __init__(self, account_kills, account_deaths, account_scores):
        threading.Thread.__init__(self)
        self._account_kills = account_kills
        self.account_deaths = account_deaths
        self.account_scores = account_scores
    def run(self):
        # pull our existing stats from disk
        try:
            stats = get_stats()
        except:
            return   

        # now add this batch of kills to our persistant stats
        for account_id, kill_count in self._account_kills.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                stats[account_id] = {'rank': 0,
                                     'name': "myname"
                                     'scores': 0,
                                     'total_damage': 0,
                                     'kills': 0,
                                     'deaths': 0,
                                     'games': 0,
                                     'kd': 0,
                                     'avg_score': 0,
                                     'aid': str(account_id),
                                     'last_seen': str(datetime.datetime.now())}
                                     
            # This will change the name to user real name
            url = "http://bombsquadgame.com/bsAccountInfo?buildNumber=20258&accountID=" + account_id
            data = urllib.request.urlopen(url)
            if data is not None:
                try:
                    name = json.loads(data.read())["profileDisplayString"]
                except ValueError:
                    stats[account_id]['name'] = "???"
                else:
                    stats[account_id]['name'] = name

            # now increment their kills whether they were already there or not
            stats[account_id]['kills'] += kill_count
            stats[account_id]['deaths'] += self.account_deaths[account_id]
            stats[account_id]['scores'] += self.account_scores[account_id]
            # also incrementing the games played and adding the id
            stats[account_id]['games'] += 1
            stats[account_id]['aid'] = str(account_id)
        # dump our stats back to disk

        from datetime import datetime
        with open(stats_file, 'w') as f:
            f.write(json.dumps(stats))
        refreshStats()



def on_begin(self) -> None:
    # pylint: disable=cyclic-import
    from bastd.actor.text import Text
    from ba import _language
    super().on_begin()
    update(self._stats)
    # Pop up a 'press any button to continue' statement after our
    # min-view-time show a 'press any button to continue..'
    # thing after a bit.
    if _ba.app.ui.uiscale is UIScale.LARGE:
        # FIXME: Need a better way to determine whether we've probably
        #  got a keyboard.
        sval = _language.Lstr(resource='pressAnyKeyButtonText')
    else:
        sval = _language.Lstr(resource='pressAnyButtonText')

    Text(self._custom_continue_message
         if self._custom_continue_message is not None else sval,
         v_attach=Text.VAttach.BOTTOM,
         h_align=Text.HAlign.CENTER,
         flash=True,
         vr_depth=50,
         position=(0, 10),
         scale=0.8,
         color=(0.5, 0.7, 0.5, 0.5),
         transition=Text.Transition.IN_BOTTOM_SLOW,
         transition_delay=self._min_view_time).autoretain()


def run_stats():
    ScoreScreenActivity.on_begin = on_begin
    _thread.start_new_thread(mystats.refreshStats, ())
    