
import bascenev1 as bs
import atexit
import _babase
import discord
import babase
from discord.ext import commands, tasks
from discord import Embed
import coinsystem
import asyncio
import threading
import settings
import logging


#logging.getLogger('discord.client').setLevel(logging.ERROR)

setting = settings.get_settings_data()
feed_data = {}
statsmessage = None

class BsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or('$'),
            intents=intents,
            application_id=setting["discord"]["applicationid"])
            
    async def setup_hook(self):
        await self.load_extension(f"discord_bot.cogs.currency")
        await self.load_extension(f"discord_bot.cogs.admin")
        await self.load_extension(f"discord_bot.cogs.normal")
        await bot.tree.sync(guild = discord.Object(id=setting["discord"]["serverid"]))

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        await self.run_live_stats()

    async def run_live_stats(self):
        global feed_data
        global statsmessage
        server = self.get_channel(980277690508648498)
        embed = Embed(
            title="Live Stats",
            description="For live feed",
            color=discord.Colour.blue()
        )
        statsmessage = await server.send(embed=embed)
        await self.refresh_feed.start()

    @tasks.loop(seconds=10)
    async def refresh_feed(self):
        global statsmessage
        new_msg = statsmessage.embeds[0]
        new_msg.description = livestatsmessage()
        await statsmessage.edit(embed=new_msg)
        #asyncio.sleep(3)

def livestatsmessage():
    message = "Live Stats\n\n"
    for i in feed_data:
        name = str(feed_data[i]["name"])
        clid = str(feed_data[i]["clientid"])
        id = str(i)
        message += name + " " + clid + " " + id + "\n"
    if message is None:
        message = "Blank"
    return message

def get_live_feed():
    try:
        global feed_data
        players = {}
        for i in bs.get_game_roster():
            try:
                players[i["account_id"]] = {
                    "name": i["players"][0]["name"], "clientid": i["client_id"]
                }
            except:
                players[i["account_id"]] = {
                    "name": "Joining", "clientid": i["client_id"]
                }
        feed_data = players
    except Exception as e:
        print(e)
    return 
    
bot = BsBot()
loop = None
def run_bot():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(setting["discord"]["token"]))
    babase.app.add_shutdown_task(loop.stop)

def cleanup():
    global loop
    if loop and loop.is_running():
        loop.call_soon_threadsafe(loop.stop)
        

def init():
    global loop
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
 