

import discord
from discord.ext import commands
import asyncio
import threading
import settings

setting = settings.get_settings_data()

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
        await bot.tree.sync(guild = discord.Object(id=setting["discord"]["serverid"]))

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')



bot = BsBot()

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(setting["discord"]["token"]))
    threading.Thread(target=loop.run_forever).start()

