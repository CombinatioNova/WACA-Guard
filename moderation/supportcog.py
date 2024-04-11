import disnake
from disnake.ext import commands, tasks
import sqlite3
from datetime import datetime
from disnake.ui import Button
from disnake import TextInputStyle, ButtonStyle

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_tickets.start()

    def cog_unload(self):
        self.check_tickets.cancel()

    @commands.slash_command(description="ManualRun")
    async def manrun(self,
        inter: disnake.ApplicationCommandInteraction,):
        await inter.response.defer()
        guilds = self.bot.guilds
        for guild in guilds:
            support_channel = disnake.utils.get(guild.categories, name="📬 | Support tickets")
            print(support_channel.channels)
            if support_channel:
                unresolved_tickets = 0
                for channel in support_channel.channels:
                    unresolved_tickets += 1
                    print(f"Found {unresolved_tickets}!")
            try:
                if unresolved_tickets != 0:
                    channel = disnake.utils.get(guild.channels, name="💬│staff-chat")
                    await channel.send(f"Total unresolved tickets in {guild.name}: {unresolved_tickets}")
                else: 
                    print("stopped mods' fury")
            except Exception as e:   
                print(e)                 
                continue
        await inter.edit_original_response("Done")
    @tasks.loop(hours=24)
    async def check_tickets(self):
        guilds = self.bot.guilds
        for guild in guilds:
            support_channel = disnake.utils.get(guild.categories, name="📬 | Support tickets")
            print(support_channel.channels)
            if support_channel:
                unresolved_tickets = 0
                for channel in support_channel.channels:
                    unresolved_tickets += 1
                    print(f"Found {unresolved_tickets}!")
            try:
                if unresolved_tickets != 0:
                    channel = disnake.utils.get(guild.channels, name="💬│staff-chat")
                    await channel.send(f"Total unresolved tickets in {guild.name}: {unresolved_tickets}")
                else: 
                    print("stopped mods' fury")
            except Exception as e:   
                print(e)                 
                continue

    @check_tickets.before_loop
    async def before_check_tickets(self):
        await self.bot.wait_until_ready()
def setup(bot):
    bot.add_cog(SupportCog(bot))
