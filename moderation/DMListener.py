from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button
from disnake import TextInputStyle

from datetime import datetime

class DMListener(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        bot = self.bot
        if message.channel.type == disnake.ChannelType.private and not message.author.bot:
            try:
                log = disnake.Embed(
                    title=f"{message.author} has sent a dm!",
                    color=5639085,
                    timestamp=datetime.now(),
                )
            
                log.set_author(
                    name="SMPWACA Moderation",
                    icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
                )

                log.set_footer(
                    text=f"Sent by {message.author.name}",
                    icon_url=message.author.display_avatar,
                )

                log.set_thumbnail(message.author.display_avatar)

                log.add_field(name="Message: ", value=message.content, inline=False)
                
                # Get all guilds where the bot is in the "📂dms" channel
                guilds = [
                    guild
                    for guild in bot.guilds
                    if disnake.utils.get(guild.channels, name="📂dms") is not None
                ]

                # Send the message to all of the guilds
                for guild in guilds:
                    channel = disnake.utils.get(guild.channels, name="📂dms")
                    if channel is not None:
                        await channel.send(embed=log)
            except Exception as e:
                print(f"Error getting DM from {message.author}! {e}")
            else:
                return

def setup(bot: Bot) -> None:
    bot.add_cog(DMListener(bot))  
