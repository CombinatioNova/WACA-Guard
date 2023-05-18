from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button
from disnake import TextInputStyle
import chat_exporter
from datetime import datetime
import io
import asyncio
class Close(Cog):
    def __init__(self,bot: Bot) -> None:
        self.bot = bot
    @slash_command(description="Close a notice")
    async def close(self, inter, reason: str = "No reason provided"):
        bot = self.bot
        if inter.channel.category.name.startswith("📬 | Support tickets"):
            
            transcript = await chat_exporter.export(
                inter.channel,
                limit=10000,
                tz_info="UTC",
                military_time=False,
                bot=bot,
            )

            if transcript is None:
                return

            transcript_file = disnake.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{inter.channel.name}-{datetime.now()}.html",
            )

            
            channel = disnake.utils.get(user.guild.channels, name = "📂transcripts")
                
            
            
            log = disnake.Embed(
                title=f"Case of {inter.channel.name.split('-')[1]} closed!", # Smart or smoothbrain?????
                color=disnake.Colour.brand_green(), # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
                timestamp=datetime.now(), #Get the datetime... now...
                description=f"The transcript of **#{inter.channel.name}** (**{inter.channel.id}**) has been saved! View below:",
            )
            log.set_author(
            name="WACA-Guard Log",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
            log.add_field(name="Reason: ", value=reason, inline=False)
            log.set_footer( # Show the moderator
            text=f"Closed by: {inter.author.name}",
            icon_url=inter.author.display_avatar,
            )
            await channel.send(embed=log) #Send the shit
            await channel.send(file=transcript_file)
            await inter.channel.delete()
            await inter.response.send_message("Sent to Transcripts!", ephemeral=True)
        else:
            await inter.response.send_message("No.", ephemeral=True)
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot)) 
