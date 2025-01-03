import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import get
from disnake.ext import tasks
from datetime import datetime, time
import asyncio

class BumpPings(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
    tortopia_id = 826107409906008085
    smpwaca_id = 912725322166829116

    servers = [tortopia_id,smpwaca_id]
    
##    @Cog.listener()
##    async def on_message(self, message):
##        if message.author.id==115385224119975941:
##            if message.content.startswith("Your server has been"):
##                await message.channel.send("Thank you for bumping! I'll remind everyone in 12 hours to bump again!")
##                await asyncio.sleep(12 * 60 * 60) # Wait 12 hours
##                if message.guild.id == tortopia_id:
##                    bot = self.bot
##                    tortoGuild = disnake.utils.get(bot.guilds, id=tortopia_id)
##                    role = disnake.utils.get(tortoGuild.roles, name="Bump Pings")
##                    channel = disnake.utils.get(tortoGuild.channels, name="🤖│bot-commands")
##                    await channel.send(f"Run /bump in this channel! It boosts our listing on ad sites so we can get more members! {role.mention}")
##                    
##                elif message.guild.id == smpwaca_id:
##                    bot = self.bot
##                    smpwacaGuild = disnake.utils.get(bot.guilds, id=smpwaca_id)
##                    role = disnake.utils.get(smpwacaGuild.roles, name="Bump Pings")
##                    channel = disnake.utils.get(smpwacaGuild.channels, name="🤜│bump")
##                    await channel.send(f"Run /bump in this channel to help get our members up! {role.mention}")
##
##                
##        elif message.author.id==302050872383242240:
##            await message.channel.send("Thank you for bumping! I'll remind you in 2 hours to bump again!")
##            await asyncio.sleep(2 * 60 * 60) # Wait 2 hours
##            await message.channel.send(f"{message.author.mention}, it's time to bump again!")
##                
            
    @tasks.loop(hours=1)
    async def tortoRemind(self):
        now = datetime.now()
        current_hour = now.hour

        if current_hour in [5]:
            bot = self.bot
            
            tortoGuild = disnake.utils.get(bot.guilds, id=tortopia_id)
            role = disnake.utils.get(tortoGuild.roles, name="Bump Pings")
            channel = disnake.utils.get(tortoGuild.channels, name="🤖│bot-commands")
            await channel.send(f"Run /bump in this channel! It boosts our listing on ad sites so we can get more members! {role.mention}")

    @tasks.loop(hours=1)
    async def wacaRemind(self):
        now = datetime.now()
        current_hour = now.hour

        if current_hour in [12]:
            bot = self.bot
            
            smpwacaGuild = disnake.utils.get(bot.guilds, id=smpwaca_id)
            role = disnake.utils.get(smpwacaGuild.roles, name="Bump Pings")
            channel = disnake.utils.get(smpwacaGuild.channels, name="🤜│bump")
            await channel.send(f"Run /bump in this channel to help get our members up! {role.mention}")

    @slash_command(description="Remind all servers to bump!")
    async def bumpremind(self, inter: disnake.ApplicationCommandInteraction):
        bot = self.bot
        
        smpwaca_id = 912725322166829116
        smpwacaGuild = disnake.utils.get(bot.guilds, id=smpwaca_id)
        role = disnake.utils.get(smpwacaGuild.roles, name="Bump Pings")
        channel = disnake.utils.get(smpwacaGuild.channels, name="🤜│bump")
        await channel.send(f"Run /bump in this channel to help get our members up! {role.mention}")

        tortopia_id = 826107409906008085
        tortoGuild = disnake.utils.get(bot.guilds, id=tortopia_id)
        role = disnake.utils.get(tortoGuild.roles, name="Bump Pings")
        channel = disnake.utils.get(tortoGuild.channels, name="🤖│bot-commands")
        await channel.send(f"Run /bump in this channel to help get our members up! {role.mention}")
        
        await inter.response.send_message("Done!", ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        self.tortoRemind.start()
        self.wacaRemind.start()
        return
def setup(bot: Bot):
    bot.add_cog(BumpPings(bot))
