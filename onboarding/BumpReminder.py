import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import get
from disnake.ext import tasks
from datetime import datetime, time

class BumpPings(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        # Set the ID and name of the first server
        tortopia_id = 912725322166829116
        tortoGuild = disnake.utils.get(self.bot.guilds, id=tortopia_id)
        # Set the ID and name of the second server     
  
    @tasks.loop(minutes=120)
    async def tortoRemind(self):
        bot = self.bot
        tortopia_id = 826107409906008085
        tortoGuild = disnake.utils.get(bot.guilds, id=tortopia_id)
        role = disnake.utils.get(tortoGuild.roles, name="Bump Pings")
        channel = disnake.utils.get(tortoGuild.channels, name="🤖│bot-commands")
        await channel.send(f"Remember to bump the server! {role.mention}")

    @tasks.loop(minutes=720)
    async def wacaRemind(self):
        bot = self.bot
        smpwaca_id = 912725322166829116
        smpwacaGuild = disnake.utils.get(bot.guilds, id=smpwaca_id)
        role = disnake.utils.get(smpwacaGuild.roles, name="Bump Pings")
        channel = disnake.utils.get(smpwacaGuild.channels, name="🤜│bump")
        await channel.send(f"Remember to bump the server! {role.mention}")

        
    @slash_command(description="Remind all servers to bump!")
    async def bumpremind(self, inter: disnake.ApplicationCommandInteraction):
        bot = self.bot
        
        smpwaca_id = 912725322166829116
        smpwacaGuild = disnake.utils.get(bot.guilds, id=smpwaca_id)
        role = disnake.utils.get(smpwacaGuild.roles, name="Bump Pings")
        channel = disnake.utils.get(smpwacaGuild.channels, name="🤜│bump")
        await channel.send(f"Remember to bump the server! {role.mention}")

        tortopia_id = 826107409906008085
        tortoGuild = disnake.utils.get(bot.guilds, id=tortopia_id)
        role = disnake.utils.get(tortoGuild.roles, name="Bump Pings")
        channel = disnake.utils.get(tortoGuild.channels, name="🤖│bot-commands")
        await channel.send(f"Remember to bump the server! {role.mention}")
        
        await inter.response.send_message("Done!", ephemeral = True)

    @Cog.listener()
    async def on_ready(self):
        self.tortoRemind.start()
        self.wacaRemind.start()
        return
def setup(bot: Bot):
    bot.add_cog(BumpPings(bot))
