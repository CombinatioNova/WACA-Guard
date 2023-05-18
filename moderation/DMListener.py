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
        if message.channel.type == disnake.ChannelType.private:
            try:
                log = disnake.Embed(
                title=f"{message.author} has sent a dm!", # Smart or smoothbrain?????
                color=5639085, # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
                timestamp=datetime.now(), #Get the datetime... now...
            )
            
                log.set_author( # Narcissism
                name="SMPWACA Moderation",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
            )

                log.set_footer( # Show the moderator
                text=f"Sent by {message.author.name}",
                icon_url=message.author.display_avatar,
            )

                log.set_thumbnail(message.author.display_avatar)

                log.add_field(name="Message: ", value=message.content, inline=False)
                
                channel = disnake.utils.get(user.guild.channels, name = "📂dms")
                await channel.send(embed=log)
            except Exception as e:
                channel = disnake.utils.get(user.guild.channels, name = "📂dms")
                await channel.send(f"Error getting DM from {message.author}! {e}")
            else:
                return
def setup(bot: Bot) -> None:
    bot.add_cog(DMListener(bot))  
