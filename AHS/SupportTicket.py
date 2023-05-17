#Support Ticket Direction
from disnake.ext.commands import Bot, Cog, slash_command
import disnake
import json

class Support(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        server_ip_patterns = ['what is the server ip', 'whats the server ip', 'server ip', 'serverip', 'server_ip', 'ip server', 'ip_server', "whats the ip"]
        join_patterns = ['how do i join', 'how do i join the server', 'how do i get on', "how to join"]
    @Cog.listener()
    async def on_message(self,message):
        if message.author == bot.user:
            return
        server_ip_response = process.extractOne(message.content, server_ip_patterns, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=80)
        join_response = process.extractOne(message.content, join_patterns, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=70)
     
        if server_ip_response:
            # Create the embed
            embed = disnake.Embed(title='Join the server!', description='Join through play.smpwaca.com! The server is in 1.19.2', color=0x00ff00)

            # Send the embed to the channel
            await message.channel.send(embed=embed)
        if join_response:
            # Create the embed
            embed = disnake.Embed(title='Join the server!', description='Join through play.smpwaca.com! The server is in 1.19.2', color=0x00ff00)
 
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
