from disnake.ext.commands import Bot, Cog, slash_command
import disnake
from disnake.utils import get
class hoster(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(name="hostinfo", description="A simple command to update host stuff.", guild_ids=[912725322166829116])
    async def hostinfo(self, inter: disnake.ApplicationCommandInteraction) -> None:
         channel = self.bot.get_channel(912727464768307240)
         embed = disnake.Embed(title= "Server Specs", description = "Note: Out of transparency, we are sponsored by **Hybrid Hosting**, however the performance you feel in-game is the same performance Hybrid gives to other servers.", color = 0x00FF00)
         embed.add_field(name = "CPU", value = "Ryzen 5950X", inline = True)
         embed.add_field(name = "Cores", value = "10", inline = True)
         embed.add_field(name = "RAM", value = "32GB DDR4 @ 3600 MHz", inline = True)
         embed.add_field(name = "Location", value = "New York City", inline = True)
         embed.add_field(name = "Website", value = "https://www.hybridhosting.xyz/", inline = True)
         await channel.send(embed=embed)
    
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
