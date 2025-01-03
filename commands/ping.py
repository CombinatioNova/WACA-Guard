from disnake.ext.commands import Bot, Cog, slash_command
import disnake
import json


class Ping(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(name="ping", description="A simple ping command.")
    async def ping(self, inter: disnake.ApplicationCommandInteraction) -> None:
                # Open the text file
        with open("users.txt", "r") as file:
            # Read the contents of the file
            try:
                users = json.loads(file.read())
            except json.decoder.JSONDecodeError:
                users = []

        # Check if the user ID is already in the list
        if inter.author.id in users:
            embed = disnake.Embed(title="Bot watency", description=f"Bot watency iz {self.bot.latency * 1000:.2f}ms uwu")
            await inter.send(embed=embed)
        else:
            embed = disnake.Embed(title="Bot latency", description=f"Bot latency is {self.bot.latency * 1000:.2f}ms")
            await inter.send(embed=embed)
            
    
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
