import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import get
from disnake.ui import Button
from datetime import datetime
class accept(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    @slash_command(description="Accept an Application")
    async def accept(self,inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        bot = self.bot
        await inter.response.defer(with_message = True,ephemeral=False)
        embed = disnake.Embed(
            title=f"Your application has been accepted!",
            description = f"""
    **Dear, {user}**

    We have reviewed your application thoroughly and we have come to the conclusion that you meet the necessary qualifications to join the SMPWACA Staff TraIning Program!

    This program is designed to help you gain the skills, knowledge, and attitudes needed to become a staff member for N-WACA. There is no prior work that needs to be done on your end, so sit tight as we determine the date for your first day of training!

    Our team will be in contact with you in the near future to determine the details of the class and what times work for you.

    Please accept or deny this invitation to acknowledge you have seen this message and accept the offer.

    Thank you for applying!

    **Regards,**
    **N-WACA Management**
    """,
            color=disnake.Colour.brand_green(),
            timestamp=datetime.now()
            )
        embed.set_author(
            name="N-WACA Management",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
        embed.set_footer(
            text=f"Sent to {user}",
            icon_url=user.display_avatar
            )
        accept = Button(label="Accept", custom_id=f"1acc",style=disnake.ButtonStyle.success)
        deny = Button(label="Deny", custom_id=f"d",style=disnake.ButtonStyle.danger)
        try:
            await user.send(embed=embed,components=[accept,deny])
        except disnake.Forbidden as error:
            log = disnake.Embed(
            title=f"Error dming {user}!", 
            color=disnake.Colour.brand_red(),
            timestamp=datetime.now(), 
        )
            log.set_author(
            name="WACA-Guard Notice",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
            log.add_field(name="Error Message", value=error, inline=False)
            log.add_field(name="Likely Cause:", value="User does not have DM's enabled!", inline=True)
            log.add_field(name="Remedy:", value="Convince the user to turn on DMs or manually DM them by sending a friend request.", inline=True)
            await inter.edit_original_response(embed=log)
            pass
        except Exception as error:
            log = disnake.Embed(
            title=f"Error dming {user}!", 
            color=disnake.Colour.brand_red(),
            timestamp=datetime.now(), 
        )
            embed.set_author(
            name="WACA-Guard Notice",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
            log.add_field(name="Error Message", value=error, inline=False)
          
            await inter.response.send_message(embed=log, ephemeral = True)
            pass
        await inter.edit_original_response(f"Sent an acceptance message to {user}!")
        channel = disnake.utils.get(user.guild.channels, name = "training-resources")
        if inter.channel.id != channel:
            await channel.send(f"Sent an acceptance message to {user}")
        else:
            pass
    @Cog.listener()
    async def on_button_click(self, inter):
        bot=self.bot
        if inter.component.custom_id.startswith(f"1acc"):
            
            
            channel = disnake.utils.get(user.guild.channels, name = "training-resources")
            embed = disnake.Embed(title=f"{inter.user.display_name} has accepted!",description= f"{inter.user.display_name} has accepted their training program invitation. \n\n They may now be added to the list of official Trainees",color=disnake.Colour.brand_green())
            embed.set_author(
                name="Training Program Notice",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
                )
            embed.set_footer(
                text=f"Sent to {inter.user.display_name}",
                icon_url=inter.user.display_avatar
                )
            await channel.send(embed=embed)
            await inter.send("Thank you for accepting our invitation to the training program! We're glad to have you here.")
        if inter.component.custom_id.startswith(f"d"):
            
            
            channel = disnake.utils.get(user.guild.channels, name = "training-resources")
            embed = disnake.Embed(title=f"{inter.user.display_name} has DENIED their application",description= f"{inter.user.display_name} has deniedn their training program invitation. \n\n They are no longer a valid candidate for the training program",color=disnake.Colour.brand_red())
            embed.set_author(
                name="Training Program Notice",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
                )
            embed.set_footer(
                text=f"Sent to {inter.user.display_name}",
                icon_url=inter.user.display_avatar
                )
            await channel.send(embed=embed)
            await inter.send("Thank you for informing us of your decision. If you change your mind prior to the start date, please inform us. Feel free to apply again!")
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
