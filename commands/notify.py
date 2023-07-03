import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import get
from disnake.ui import Button
from datetime import datetime
class notify(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    @slash_command(description="Notify someone")
    async def notify(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, notification: str):
        
        await inter.response.defer(with_message = True,ephemeral=False)
        bot=self.bot
        embed = disnake.Embed(
            title=f"Notification",
            color=5639085,
            description = notification)
        embed.set_author(
            name="WACA-Guard Notice",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
        embed.set_footer(
            text=f"Sent to {user}",
            icon_url=user.display_avatar
            )

        
        acknowledge = Button(label="Acknowledge", custom_id=f"acknowledge",style=disnake.ButtonStyle.success)
        try:
            await user.send(embed=embed)
            guilds = [
                guild
                for guild in bot.guilds
                if disnake.utils.get(guild.channels, name="📂dms") is not None
            ]

            # Send the message to all of the guilds
            for guild in guilds:
                channel = disnake.utils.get(guild.channels, name="📂dms")
                if channel is not None:
                    await channel.send(f"Sent a notification message to {user}")
                
            embed2 = disnake.Embed(
                title=f"Notification Log",
                color=5639085,
                description = notification)
            embed2.set_author(
                name="WACA-Guard Notice Log",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
                )
            embed2.set_footer(
                text=f"Sent to {user}",
                icon_url=user.display_avatar
                )
            guilds = [
                guild
                for guild in bot.guilds
                if disnake.utils.get(guild.channels, name="📂dms") is not None
            ]

            # Send the message to all of the guilds
            for guild in guilds:
                channel = disnake.utils.get(guild.channels, name="📂dms")
                if channel is not None:
                    await channel.send(embed=embed2)
            
            await inter.edit_original_message(content = f"Sent a notification message to {user.display_name} and logged the message!")
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
            log.add_field(name="Remedy:", value="Convince the user to turn on DMs or manually DM them by sending a friend request.")
            await inter.edit_original_message(embed=log)
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
          
            await inter.edit_original_message(embed=log)
            pass
    @Cog.listener()
    async def on_button_click(self, inter):
        bot=self.bot
        if inter.component.custom_id.startswith(f"acknowledge"):
            
            
            embed = disnake.Embed(title="Notice Acknowledged",color=5639085,)
            embed.set_author(
                name="WACA-Guard Notice Log",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
                )
            embed.set_footer(
                text=f"Sent to {inter.user.display_name}",
                icon_url=inter.user.display_avatar
                )
            guilds = [
                guild
                for guild in bot.guilds
                if disnake.utils.get(guild.channels, name="📂dms") is not None
            ]

            # Send the message to all of the guilds
            for guild in guilds:
                channel = disnake.utils.get(guild.channels, name="📂dms")
                if channel is not None:
                    await channel.send(embed=embed)
            await inter.send("Notification has been sent to the staff team. Thank you for notifying us that you've recieved this message.")
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))            
