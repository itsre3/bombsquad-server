import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from stats import mystats
import settings
from core import Core
setting = settings.get_settings_data()


class BackButton(Button):
    def __init__(self, embeds: [discord.Embed], label: str = ""):
        super().__init__(label=label, emoji="◀")
        self.colors = { "red": discord.ButtonStyle.red,
                        "blurple": discord.ButtonStyle.blurple,
                        "green": discord.ButtonStyle.green,
                        "grey": discord.ButtonStyle.grey}
        self.embeds = embeds
        self.style = self.colors["blurple"]

    async def callback(self, interaction: discord.Interaction):
        self.view.interaction = interaction
        self.view.interaction_set = True
        if self.view.cur_page == 0:
            await self.view.ctx.send("You can't go back")
        else:
            self.view.cur_page -= 1
            if self.view.cur_page == 0:
                self.view.clear_items()
                button = ForwardButton(self.embeds)
                self.view.add_item(button)
            elif self.view.cur_page != len(self.embeds)-1:
                self.view.clear_items()
                button = BackButton(self.embeds)
                self.view.add_item(button)
                button = ForwardButton(self.embeds)
                self.view.add_item(button)
        await interaction.response.edit_message(embed=self.embeds[self.view.cur_page], view=self.view)


class LeaderBoardView(View):
    def __init__(self, ctx, embeds: [discord.Embed]):
        super().__init__(timeout=30)
        self.embeds = embeds
        self.MAX_PAGES = len(embeds)
        self.forward_button = ForwardButton(self.embeds)
        self.add_item(self.forward_button)
        self.cur_page = 0
        self.interaction_set = False
        self.interaction = ctx

    async def on_timeout(self):
        self.clear_items()
        await self.msg.delete()
        self.stop()


class ForwardButton(Button):
    def __init__(self, embeds: [discord.Embed], label: str = ""):
        super().__init__(label=label, emoji="▶")
        self.colors = { "red": discord.ButtonStyle.red,
                        "blurple": discord.ButtonStyle.blurple,
                        "green": discord.ButtonStyle.green,
                        "grey": discord.ButtonStyle.grey}
        self.embeds = embeds
        self.style = self.colors["blurple"]

    async def callback(self, interaction: discord.Interaction):
        self.view.interaction = interaction
        self.view.interaction_set = True
        if self.view.cur_page == len(self.embeds):
            await self.view.ctx.send("You can't go forward")
        else:
            self.view.cur_page += 1
            if self.view.cur_page == len(self.embeds)-1:
                self.view.clear_items()
                button = BackButton(self.embeds)
                self.view.add_item(button)
            elif self.view.cur_page != 0:
                self.view.clear_items()
                button = BackButton(self.embeds)
                self.view.add_item(button)
                button = ForwardButton(self.embeds)
                self.view.add_item(button)
        await interaction.response.edit_message(embed=self.embeds[self.view.cur_page], view=self.view)


class Normal(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="stats",
        description="Check your game progress"
    )
    @app_commands.describe(
        playerid="Player Id"
    )
    async def stats(
        self, interaction: discord.Interaction, playerid: str
    ):
        stats = mystats.get_stats_by_id(playerid)
        if stats != None:
            msg="Score:"+str(stats["scores"]) + "\nGames:"+str(stats["games"]) + "\nKills:"+str(stats["kills"]) + "\nDeaths:"+str(stats["deaths"]) + "\nAvg.Score:"+str(stats["avg_score"])
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Play some games first", ephemeral=True
            )

    @app_commands.command(
            name='leaderboard',
            description="Displays server leaderboard"
    )
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        stats = mystats.get_all_stats()
        stats = dict(sorted(stats.items(), key = lambda x: x[1]["rank"]))
        count = 0
        if len(stats) > 10:
            embeds = []
            embed = discord.Embed(
                title="Leaderboard",
                description="",
                color=discord.Colour.blue()
            )
            interaction=interaction
            for i in stats:
                name = stats[i]["name"]
                rank = str(stats[i]["rank"])
                embed.add_field(name=f"", value=f"{rank} => {name}\n")
                count += 1
                if count == 10:
                    embeds.append(embed)
                    embed = discord.Embed(
                        title="Leaderboard",
                        description="",
                        color=discord.Colour.blue()
                    )
                    count = 0
            embeds.append(embed)
            view = LeaderBoardView(interaction, embeds)
            message = await interaction.followup.send(embed=embeds[0], view=view)
            view.msg = message
        else:
            embed = discord.Embed(
                title="Leaderboard",
                description="",
                color=discord.Colour.blue()
            )
            for i in stats:
                name = stats[i]["name"]
                rank = str(stats[i]["rank"])
                embed.add_field(name="", value=f"{rank} => {name}\n")
            await interaction.followup.send(embed=embed)




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Normal(bot),
        guilds=[discord.Object(id=setting["discord"]["serverid"])])