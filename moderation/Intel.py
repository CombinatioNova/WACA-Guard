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
import sqlite3
from socialscan.util import Platforms, execute_queries
from socialscan.platforms import Platforms
from PIL import Image
import requests
from io import BytesIO

class WHOIS(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def lookup(self, inter, user: disnake.User):
        queried_list = {user.name.replace(' ', '').lower()}
        if user.display_name:
            queried_list.add(user.display_name.replace(' ', '').lower())
        if user.global_name:
            queried_list.add(user.global_name.replace(' ', '').lower())
        
        queries = list(queried_list)
        platforms = [p for p in Platforms]
        results = await execute_queries(queries, platforms)
        
        platform_dict = {}
        for result in results:
            if not result.available and result.success:
                if result.query in platform_dict:
                    platform_dict[result.query].append(result.platform)
                else:
                    platform_dict[result.query] = [result.platform]
        
        known_acc = [
            f"**{query}** found on: {', '.join([platform.name.title() for platform in platforms])}"
            for query, platforms in platform_dict.items()
        ]
        return known_acc

    @slash_command(description="Perform a lookup on a user")
    async def whois(self, inter, user: disnake.User):
        await inter.response.defer(with_message=True, ephemeral=False)
        
        member = inter.guild.get_member(user.id)
        if not member:
            member = user

        # 1. Joined at
        joined_at = calendar.timegm(member.joined_at.utctimetuple()) if isinstance(member, disnake.Member) and member.joined_at else None

        # 2. Created on
        created_on = calendar.timegm(member.created_at.utctimetuple())

        # 3. Profile picture
        avatar_url = member.avatar.url

        # Calculate average color of profile picture
        response = requests.get(avatar_url)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")  # Ensure image is in RGB mode
        img = img.resize((1, 1))
        avg_color = img.getpixel((0, 0))
        avg_color_hex = int('%02x%02x%02x' % avg_color, 16)

        # 4. Display name
        display_name = member.display_name

        # 5. Username
        username = member.name

        # 6. Global Name (Nickname on other servers) - Not accessible through API
        global_name = user.global_name

        found_servers = [guild.name for guild in self.bot.guilds if guild.get_member(user.id)]

        response = '\n'.join(found_servers) if found_servers else "User not found in any shared servers."

        # Fetch XP from level.db
        cursor = self.bot.get_cog('LevelCog').cursor
        cursor.execute('SELECT xp FROM levels WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        xp = row[0] if row else 0

        # 7. Dangerous roles (subjective)
        dangerous_roles = [role.name for role in member.roles if any(perm in role.permissions for perm in ["Overseer", "Overseer Council", "Server Owner", "Senior Admin", "Admin", "Owner", "Robotic Overlord"])] if hasattr(member, 'roles') else []

        # 8. Dangerous permissions (requires fetching member object)
        dangerous_permissions = [perm for perm in inter.guild.get_member(member.id).guild_permissions if perm and perm in ["administrator", "manage_server", "manage_channels"]] if hasattr(member, 'guild_permissions') else []

        # Embed message with information
        embed = disnake.Embed(
            title=f"Who is {display_name}?",
            color=avg_color_hex,
            description=f"Here is information WACA-Guard found about {member.mention}:"
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="🏷️ Server Display Name", value=display_name, inline=True)
        embed.add_field(name="🌐 Global Display Name", value=global_name, inline=True)
        embed.add_field(name="👤 Username", value=username, inline=True)
        embed.add_field(name="📅 Account Created", value=f"<t:{created_on}:R>", inline=False)
        if joined_at:
            embed.add_field(name="📥 Joined Server", value=f"<t:{joined_at}:R>", inline=True)
        embed.add_field(name="⭐ XP", value=xp, inline=True)
        if dangerous_roles:
            embed.add_field(name="⚠️ Dangerous Roles", value=", ".join(dangerous_roles), inline=False)
        if dangerous_permissions:
            embed.add_field(name="🔒 Dangerous Permissions", value=", ".join(dangerous_permissions), inline=False)
        if response:
            embed.add_field(name="🏠 Belongs To:", value=response, inline=False)
        # Check if the user has any public user flag
        user_alerts = []
        if user.public_flags.value:
            if user.public_flags.spammer:
                user_alerts.append("<:PersonAlert:1261797760605360148> User is a reported spammer")
            if user.public_flags.active_developer:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is an active developer")
            if user.public_flags.bug_hunter:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is a bug hunter")
            if user.public_flags.bug_hunter_level_2:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is a level 2 bug hunter")
            if user.public_flags.discord_certified_moderator:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is a Discord certified moderator")
            if user.public_flags.early_supporter:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is an early supporter")
            if user.public_flags.early_verified_bot_developer:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is an early verified bot developer")
            if user.public_flags.partner:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is a Discord partner")
            if user.public_flags.staff:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is a Discord staff member")
            if user.public_flags.system:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is a system user")
            if user.public_flags.moderator_programs_alumni:
                user_alerts.append("<:PersonCheck:1261797763939700897> User is a moderator programs alumni")
            
            user_alerts = "\n".join(user_alerts) if user_alerts else "No alerts"
        else:
            user_alerts = "No alerts"

        # Add the user alerts field to the embed
        embed.add_field(name="🚨 User Alerts", value=user_alerts, inline=False)
        # Check if the person running the command has the "[DIS] Department of Institutional Security" role
        dis_role = disnake.utils.get(inter.author.roles, name="[DIS] Department of Institutional Security") if hasattr(inter.author, 'roles') else None
        if dis_role:
            # Add "Deep Scan" button
            components = [
                disnake.ui.Button(
                    style=disnake.ButtonStyle.danger,
                    label="Deep Scan",
                    custom_id=f"deep_scan_{member.id}",
                    emoji="<:Search:1262184347016892530>"
                )
            ]
            action_row = disnake.ui.ActionRow(*components)
            await inter.edit_original_response(embed=embed, components=[action_row])
        else:
            await inter.edit_original_response(embed=embed)
        
        @self.bot.event
        async def on_button_click(interaction):
            if interaction.component.custom_id.startswith("deep_scan_"):
                dis_role = disnake.utils.get(interaction.user.roles, name="[DIS] Department of Institutional Security") if hasattr(interaction.user, 'roles') else None
                if dis_role:
                    user_id = int(interaction.component.custom_id.split("_")[2])
                    user = await self.bot.fetch_user(user_id)
                    # Call the lookup function and get extra results
                    extra_results = await self.lookup(interaction, user)
                    # Edit the embed with the extra results
                    embed.add_field(name="🔍 Deep Scan Results", value="\n".join(extra_results), inline=False)
                    await interaction.response.edit_message(embed=embed)
                else:
                    error_embed = disnake.Embed(
                        title="You do not have the required permissions to perform this action.",
                        color=0xffa500,
                        description="Only members of the Department of Institutional Security may perform a deep scan.",
                        timestamp=datetime.now()
                    )
                    error_embed.set_author(
                        name="Permission Denied!",
                        icon_url="https://cdn.discordapp.com/attachments/1125481298367094836/1261748715689873548/Warning4x.png?ex=6694168f&is=6692c50f&hm=c42b3a33842363358b8a96f7a7676e0cddbcbca236e45ed877d1dccade84b665&"
                        )
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)
        embed.set_footer(
            text="Department of Institutional Security",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png"
        )
        await inter.edit_original_response(embed=embed)