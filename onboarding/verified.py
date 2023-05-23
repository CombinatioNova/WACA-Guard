import disnake
from disnake.ext.commands import Bot, Cog,Param,slash_command
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from disnake.utils import get
from datetime import datetime

class on_verification(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    @Cog.listener()
    async def on_member_join(self,member):
        role = disnake.utils.get(member.guild.roles, name="Unverified")
        await member.add_roles(role)
    @Cog.listener()
    async def on_member_update(self, before, after):
        bot = self.bot
        
        if "Wick Verified" in [r.name for r in after.roles] and "Wick Verified" not in [r.name for r in before.roles]:
            role = disnake.utils.get(after.guild.channels, name="🏠│general")# replace channel_id with the actual ID of the channel you want to send the message in
            joinChan = disnake.utils.get(after.guild.channels, name="✅│how-to-join")
            if after.guild.id == 912725322166829116:
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
        await inter.response.defer(with_message = True,ephemeral=False)
        unverified_role = disnake.utils.get(inter.guild.roles, name="Unverified")
        wick_verified_role = disnake.utils.get(inter.guild.roles, name="Wick Verified")

        checked_members = 0
        changed_members = 0
        for member in inter.guild.members:
            if checked_members == 0:
                print("Starting!")
            checked_members += 1
            if wick_verified_role not in member.roles:
                await member.add_roles(unverified_role)
                changed_members += 1
            if checked_members % 10 == 0:
                print("Still alive")

        embed = disnake.Embed(
            title="Checked for Unverified Members!",
            color=4143049,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="WACA-Guard Audit",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )

        embed.set_footer(
            text=f"Run by {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )
        embed.add_field(name="Members checked: ", value=checked_members, inline=False)
        embed.add_field(name="Members changed: ", value=changed_members, inline=False)
        
        channel = disnake.utils.get(inter.guild.channels, name = "waca-guard-audit")
        await channel.send(embed=embed)
        await inter.edit_original_response(f"Done! Verified {checked_members} members.")

def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
