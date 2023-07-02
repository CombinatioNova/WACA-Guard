import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import get
from disnake.ui import Button
from datetime import datetime
class deny(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    @slash_command(description="Deny an Application")
    async def deny(self,inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        bot = self.bot
        await inter.response.defer(with_message = True,ephemeral=False)
        embed = disnake.Embed(
            title=f"Your application has been denied",
            description = f"""
    **Dear, {user}**

    Thank you for your interest in the Network Staff Training Program at NETWACA. After careful consideration, we regret to inform you that we are unable to offer you a position in the program at this time. The selection process was highly competitive, and we had to make difficult decisions based on specific program requirements.

We encourage you to continue pursuing your professional development goals and exploring other training opportunities in the field. While you were not selected for this program, we believe in your potential and encourage you to consider reapplying in the future.

We appreciate your time and effort in the application process and wish you the best in your future endeavors.

    **Regards,**
    **NETWACA Management**
    """,
            color=disnake.Colour.brand_red(),
            timestamp=datetime.now()
            )
        embed.set_author(
            name="NETWACA Management",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
        embed.set_footer(
            text=f"Sent to {user}",
            icon_url=user.display_avatar
            )
        
        try:
            await user.send(embed=embed)
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
    
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
