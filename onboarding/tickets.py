from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button
from disnake import TextInputStyle

from datetime import datetime

global av
class Ticket(Cog):
    def __init__(self,bot: Bot) -> None:
        self.bot = bot

    @slash_command(description="Open A Ticket")
    async def ticket(self, inter: disnake.ApplicationCommandInteraction):
        bot = self.bot
        global name
        user = inter.user
        member = user
        name = user.display_name
        av=user.display_avatar
        overwrites = {
            member.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(member.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(member.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(member.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(member.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),
            inter.user: disnake.PermissionOverwrite(read_messages = True)}
        category = disnake.utils.get(member.guild.categories, name = "📬 | Support tickets")
        channel = await inter.user.guild.create_text_channel(f"ticket-{member.display_name}", overwrites=overwrites, category=category)
        welcome_embed = disnake.Embed(
        title="Welcome to your support ticket!",
        description="""Hello there! Thank you for reaching out to us.

        We are here to help and will do our best to assist you with any questions or issues you may have. Thank you for your patience!""",
        color=0xFFFF00
        )
        joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary)
        exploit = Button(label="Exploiter", custom_id=f"exploit",style=disnake.ButtonStyle.primary)
        grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary)
        theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary)
        other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary)
        await channel.send(embed=welcome_embed,components=[joinProb,exploit,grief,theft,other])
        await inter.response.send_message("Test",ephemeral="True")
        
    @Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id.startswith(f"joinProb"):
            
            yes = Button(label="Yes",custom_id=f"yes1",style=disnake.ButtonStyle.success)
            no = Button(label="No",custom_id=f"no1",style=disnake.ButtonStyle.danger)
            await inter.response.send_message("wat problem?", components=[yes,no])
            
        elif inter.component.custom_id.startswith("yes1"):
            yes = Button(label="Yes",custom_id=f"yes2",style=disnake.ButtonStyle.success)
            no = Button(label="No",custom_id=f"no2",style=disnake.ButtonStyle.danger)
            await inter.response.send_message("okay, u do da ding???", components=[yes,no])
        elif inter.component.custom_id.startswith("no1"):
            await inter.response.send_message("dumbass")

        elif inter.component.custom_id.startswith("yes2"):
            await inter.response.send_message("okay, u do da ding???")
        elif inter.component.custom_id.startswith("no2"):
            await inter.response.send_message("dumbass")
        
        
def setup(bot: Bot) -> None:
    bot.add_cog(Ticket(bot)) 
