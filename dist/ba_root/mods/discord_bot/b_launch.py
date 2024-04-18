
import ba
import _ba
import discord
from discord.ext import commands
import asyncio
import threading
import settings

setting = settings.get_settings_data()
feed_data = {}

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
        self.run_live_stats()

    def run_live_stats(self):
        global feed_data
        server = self.get_channel(992103710534680646)
        server.send("TEsting")

def get_live_feed():
    global feed_data
    players = {}
    for i in _ba.get_game_roster():
        try:
            players[i["account_id"]] = {
                "name": i["players"]["name"], "clientid": i["client_id"]
            }
        except:
            players[i["account_id"]] = {
                "name": "Joining", "clientid": i["client_id"]
            }
    feed_data = players
    

bot = BsBot()

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(setting["discord"]["token"]))
    threading.Thread(target=loop.run_forever).start()

