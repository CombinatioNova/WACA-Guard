
from socialscan.util import Platforms, execute_queries
from socialscan.platforms import Platforms
from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button
from disnake import TextInputStyle
import discord
from datetime import datetime
import io
import asyncio
import calendar
class WHOIS(Cog):
    def __init__(self,bot: Bot) -> None:
        self.bot = bot
    async def lookup(self, inter, user: disnake.User):
        queriedList = []
        try:
            name1 = user.name.replace(' ', '')
            queriedList.append(name1.lower())
        except:
            pass
        try:
            name2 = user.display_name.replace(' ', '')
            queriedList.append(name2.lower())
        except:
            pass
        try:
            name3 = user.global_name.replace(' ', '')
            queriedList.append(name3.lower())
        except:
            pass
        queries = list(set(queriedList))
        platforms = [p for p in Platforms]
        results = await execute_queries(queries, platforms)
        knownAcc = []
        for result in results:
            print(f"{result.query} on {result.platform}: {"Taken" if not result.available and result.success else "Available"})")
            if not result.available and result.success:
                knownAcc.append(f"{result.query} found on {result.platform}")
        return knownAcc

    @slash_command(description="Perform a lookup on a user")
    async def whois(self, inter, user: disnake.User):
        await inter.response.defer(with_message=True, ephemeral=False)
        knownAcc = await self.lookup(inter, user)
        
    
        interaction = inter
        member = user

        # 1. Joined at
        joined_at = calendar.timegm(member.joined_at.utctimetuple())

        # 2. Created on
        createdon = calendar.timegm(member.created_at.utctimetuple())

        # 3. Profile picture
        avatar_url = member.avatar.url

        # 4. Display name
        display_name = member.display_name

        # 5. Username
        username = member.name

        # 6. Global Name (Nickname on other servers) - Not accessible through API
        global_name = user.global_name

        found_servers = []
        for guild in self.bot.guilds:
            try:
                member = guild.get_member(user.id)
                if member:
                    found_servers.append(guild.name)
            except disnake.HTTPException:
            # Handle potential HTTP errors during member fetching
                pass

        if found_servers:
            response = '\n'.join(found_servers)
        else:
            response = "User not found in any shared servers."

        # 7. Last message sent (requires message intents)
        guild = inter.guild
        if not guild:
            last_message = None

        # Use text channel iterator to efficiently search through channels
        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=None):
                    if message.author.id == user.id:
                        last_message = calendar.timegm(message.created_at.utctimetuple())
                        break
            except discord.HTTPException:
            # Handle potential HTTP errors during message fetching
                pass
        

        # 8. Total messages sent (requires message intents)
        #  - Can be inefficient for large servers
        total_messages = 0
        for message in interaction.guild.text_channels:
            async for message in message.history(limit=None):
                if message.author == member:
                    total_messages += 1

        # 9. Total attachments sent (requires message intents)
        #  - Can be inefficient for large servers
        total_attachments = 0
        for message in interaction.guild.text_channels:
            async for message in message.history(limit=None):
                if message.author == member and message.attachments:
                    total_attachments += len(message.attachments)

        # 10. Dangerous roles (subjective)
        #  - Define your own criteria for dangerous roles based on permission names
        dangerous_roles = [
            role.name for role in member.roles if any(perm in role.permissions for perm in ["Overseer", "Overseer Council", "Server Owner", "Senior Admin", "Admin", "Owner", "Robotic Overlord"])
        ]

        # 11. Dangerous permissions (requires fetching member object)
        #  - Consider using member.guild_permissions instead for efficiency
        dangerous_permissions = [
  perm for perm in interaction.guild.get_member(member.id).guild_permissions
  if perm and perm in ["administrator", "manage_server", "manage_channels"]
]


        

        # Embed message with information
        embed = disnake.Embed(title=f"Whois: {member}", color=member.color)
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Account Created", value=f"<t:{createdon}:R>", inline = True)
        embed.add_field(name="Joined Server", value=f"<t:{joined_at}:R>", inline=True)
        embed.add_field(name="Server Display Name", value=display_name, inline=True)
        embed.add_field(name="Global Display Name", value=global_name, inline=True)
        embed.add_field(name="Username", value=username, inline=True)
        if last_message:
            embed.add_field(name="Last Message", value=f"<t:{last_message}:R>", inline=False)
        embed.add_field(name="Total Messages", value=total_messages, inline=True)
        embed.add_field(name="Total Attachments", value=total_attachments, inline=True)
        if dangerous_roles:
            embed.add_field(name="Dangerous Roles", value=", ".join(dangerous_roles), inline=False)
        if dangerous_permissions:
            embed.add_field(name="Dangerous Permissions", value=", ".join(dangerous_permissions), inline=False)
        if response:
            embed.add_field(name="Belongs To:", value=response, inline = False)
        await inter.edit_original_response(embed = embed, content = ", ".join(knownAcc))
        
