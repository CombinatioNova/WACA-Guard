import disnake
from disnake.ext.commands import Bot, Cog,Param,slash_command
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from disnake.utils import get


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
            channel = bot.get_channel(913207064136925254)# replace channel_id with the actual ID of the channel you want to send the message in
            joinChan = bot.get_channel(912727464768307240)
            role = disnake.utils.get(after.guild.roles, name="Greeter")
            await channel.send(f"""{role.mention} Please welcome {after.mention} to SMPWACA!
            

Check out {joinChan.mention} for information on how to join the minecraft server! If you have trouble joining, feel free to reach out!""")
    
            role = disnake.utils.get(after.guild.roles, name="Unverified")
            await after.remove_roles(role)
    @slash_command(description="Assign Unverified to normal users")
    async def vericheck(self, inter: disnake.ApplicationCommandInteraction) -> None:
        role = disnake.utils.get(inter.guild.roles, name = "Unverified")
        for member in inter.guild.members:
                if len(member.roles) == 1:
                    await member.add_roles(role)

        await inter.response.send_message("Done!", ephemeral = True)
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
