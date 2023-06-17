import disnake
from disnake.ext.commands import Bot, Cog
from disnake.utils import get
from datetime import datetime
import unicodedata
class JoinAndLeave(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    def sanitize_username(self,username):
        normalized = unicodedata.normalize('NFKD', username)
        sanitized = ''.join(c for c in normalized if not unicodedata.combining(c))
        return sanitized
    
    @Cog.listener()
    async def on_member_join(self, member):
        # Find the joins-and-leaves channel in the guild
        channel = await self.find_joins_and_leaves_channel(member.guild)
        sanitized_username = self.sanitize_username(member.display_name)
        await member.edit(nick=sanitized_username)
        if channel:
            member_count = len(member.guild.members)
            # Create and send a welcome embed
            embed = disnake.Embed(
                title="Welcome!",
                description=f"""Welcome to the server, {member.mention}!

You are member #{member_count}!""",
                color=disnake.Color.green(),
                    timestamp=datetime.now()
            )
            embed.set_thumbnail(url=member.avatar.url)
            await channel.send(embed=embed)
        

    @Cog.listener()
    async def on_member_remove(self, member):
        # Find the joins-and-leaves channel in the guild
        channel = await self.find_joins_and_leaves_channel(member.guild)

        if channel:
            member_count = len(member.guild.members)
            # Check if the member was banned
            try:
                ban_entry = await member.guild.fetch_ban(member)
                # Create and send a banned embed
                embed = disnake.Embed(
                    title="Banned!",
                    description=f"""{member.display_name} was banned from the server.

They were member #{member_count}.""",
                    color=disnake.Color.red(),
                    timestamp=datetime.now()
                )
            except disnake.NotFound:
                # Create and send a goodbye embed
                embed = disnake.Embed(
                    title="Goodbye!",
                    description=f"""Goodbye, {member.display_name}! We'll miss you.

They were member #{member_count}.""",
                    color=0xffa500,
                    timestamp=datetime.now()
                )
            embed.set_thumbnail(url=member.avatar.url)
            await channel.send(embed=embed)


    async def find_joins_and_leaves_channel(self, guild):
        # List of possible channel names to search for
        channel_names = ["joins-and-leaves", "welcomes", "welcome", "joins"]

        # Find the channel that ends with any of the specified names
        for channel in guild.channels:
            if any(channel.name.endswith(name) for name in channel_names):
                return channel

        return None
    

def setup(bot: Bot) -> None:
    bot.add_cog(JoinAndLeave(bot))
