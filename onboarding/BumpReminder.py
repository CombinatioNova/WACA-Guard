import disnake
from disnake.ext.commands import Bot, Cog
from disnake.utils import get
import asyncio

class BumpPings(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        # Set the ID and name of the first server
        tortopia_id = 912725322166829116
        tortopia_name = "Tortopia"
        tortoGuild = disnake.utils.get(self.bot.guilds, id=tortopia_id)
        # Set the ID and name of the second server
        smpwaca_id = 826107409906008085
        smpwaca_name = "SMPWACA"
        smpwacaGuild = disnake.utils.get(self.bot.guilds, id=smpwaca_id)
        # Get the "Bump Pings" role in the first server
        tortopia_bump_pings_role = disnake.utils.get(tortoGuild.roles, name="Bump Pings")

        # Get the "Bump Pings" role in the second server
        smpwaca_bump_pings_role = disnake.utils.get(smpwacaGuild.roles, name="Bump Pings")

        # Create a task to ping the role every 12 hours in Tortopia
        tortopia_ping_task = self.bot.loop.create_task(self.ping_role(tortopia_bump_pings_role, 12,"🤜│bump"))

        # Create a task to ping the role every 2 hours in SMPWACA
        smpwaca_ping_task = self.bot.loop.create_task(self.ping_role(smpwaca_bump_pings_role, 2,"🤖│bot-commands"))

    async def ping_role(self, role, interval, channel):
        while True:
            await asyncio.sleep(interval * 3600)
            await role.mention()


def setup(bot: Bot):
    bot.add_cog(BumpPings(bot))
