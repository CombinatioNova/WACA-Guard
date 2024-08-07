import disnake
from disnake.ext.commands import Bot, Cog, Param, slash_command
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from disnake.utils import get
from datetime import datetime
import unicodedata
from core import statbed

class on_verification(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        role = disnake.utils.get(member.guild.roles, name="Unverified")
        await member.add_roles(role)

    @Cog.listener()
    async def on_member_update(self, before, after):
        bot = self.bot
        
        if "Wick Verified" in [r.name for r in after.roles] and "Wick Verified" not in [r.name for r in before.roles] or "Verified" in [r.name for r in after.roles] and "Verified" not in [r.name for r in before.roles]:
            role = disnake.utils.get(after.guild.channels, name="🏠│general")# replace channel_id with the actual ID of the channel you want to send the message in
            joinChan = disnake.utils.get(after.guild.channels, name="✅│how-to-join")
            if after.guild.id == 826107409906008085:
                role = disnake.utils.get(after.guild.roles, name="Welcomers")
            else:
                role = disnake.utils.get(after.guild.roles, name="Greeter")
            channel = disnake.utils.get(after.guild.channels, name="🏠│general")
            await channel.send(f"""{role.mention} Please welcome {after.mention} to {after.guild.name}!
            

Check out {joinChan.mention} for information on how to join the minecraft server! If you have trouble joining, feel free to reach out!""")
    
            role = disnake.utils.get(after.guild.roles, name="Unverified")
            await after.remove_roles(role)

    @slash_command(description="Assign Unverified to normal users")
    async def vericheck(self, inter: disnake.ApplicationCommandInteraction) -> None:
        await inter.response.defer(with_message=True, ephemeral=True)
        unverified_role = disnake.utils.get(inter.guild.roles, name="Unverified")
        wick_verified_role = disnake.utils.get(inter.guild.roles, name="Wick Verified")
        verified_role = disnake.utils.get(inter.guild.roles, name="Verified")
        
        checked_members = 0
        changed_members = 0
        for member in inter.guild.members:
            if checked_members == 0:
                print("Starting!")
            checked_members += 1
            if wick_verified_role not in member.roles and verified_role not in member.roles:
                await member.add_roles(unverified_role)
                changed_members += 1
            if checked_members % 10 == 0:
                print("Still alive")

        embed = await statbed.create_alert_embed(
            title="Checked for Unverified Members!",
            description=f"Members checked: {checked_members}\nMembers changed: {changed_members}",
            footer=f"Run by {inter.author.name}"
        )
        embed.timestamp = datetime.now()
        embed.set_author(
            name="WACA-Guard Audit",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )
        embed.set_footer(
            text=f"Run by {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )
        
        channel = disnake.utils.get(inter.guild.channels, name="waca-guard-audit")

        success_embed = await statbed.create_success_embed(
            title=f"Verified {checked_members} members!",
            footer="WACA-Guard"
        )
        success_embed.timestamp = datetime.now()
        
        success_embed.set_footer(
            text="WACA-Guard",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )
        await channel.send(embed=embed)
        await inter.edit_original_response(embed=success_embed)

    @slash_command(name="verify", description="Verify a user in NETWACA", guild_ids=[1117508209884799026])
    async def verify(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, server: str = Param(choices=["Character SMP", "Tortopia", "Parabellum", "SMPWACA"]), position: str = Param(choices=["Network Oversight Council", "Network Director", "Network Advisor", "Server Owner", "Server Management", "Server Staff"])):
        await inter.response.defer(with_message=True, ephemeral=False)
        unverified_role = disnake.utils.get(inter.guild.roles, name="Unverified")
        wick_verified_role = disnake.utils.get(inter.guild.roles, name="Wick Verified")
        verified_role = disnake.utils.get(inter.guild.roles, name="Verified")
        if wick_verified_role not in user.roles and verified_role not in user.roles:
            await user.add_roles(verified_role)
            server_role = disnake.utils.get(inter.guild.roles, name=server)
            position_role = disnake.utils.get(inter.guild.roles, name=position)
            await user.add_roles(server_role)
            await user.add_roles(position_role)
            success_embed = await statbed.create_success_embed(
                title="User Verified",
                description=f"Successfully verified {user.mention}.",
                footer="WACA-Guard"
            )
            await inter.edit_original_response(embed=success_embed)

    def sanitize_username(self, username):
        normalized = unicodedata.normalize('NFKD', username)
        sanitized = ''.join(c for c in normalized if not unicodedata.combining(c))
        return sanitized

    @slash_command(description="Normalize a username")
    async def sanitize(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        await inter.response.defer(with_message=True, ephemeral=False)
        sanitized_username = self.sanitize_username(user.display_name)
        await user.edit(nick=sanitized_username)
        success_embed = await statbed.create_success_embed(
            title="Username Sanitized",
            description=f"Successfully sanitized {user.mention}'s username.",
            footer="WACA-Guard"
        )
        await inter.edit_original_response(embed=success_embed)

def setup(bot: Bot) -> None:
    bot.add_cog(on_verification(bot))
