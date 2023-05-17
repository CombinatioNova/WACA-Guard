##Automated Machine Learning for Help and IP Answering

from disnake.ext.commands import Bot, Cog, slash_command
import disnake
import json
from fuzzywuzzy import fuzz, process
import fuzzywuzzy
import logging
logging.getLogger().setLevel(logging.ERROR)
class Reminder(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self,message):
        bot = self.bot
        if message.author == self.bot.user:
            return
        playerlist = ["playerlist"]
        server_ip_response = process.extractOne(message.content, playerlist, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=80)
        
        if server_ip_response:
            channel = bot.get_channel(912731255165046814)
            embed = disnake.Embed(title='Check Announcements!', description=f'''We are currently switching providers from Bloom to Hybrid.

                                  Please check {channel.mention} for more information, or look at the sticky message below. Thanks!''', color=0xffa500)

            # Send the embed to the channel
            await message.reply(embed=embed)
