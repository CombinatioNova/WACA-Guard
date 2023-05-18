import disnake
from disnake.ext.commands import Bot, Cog, slash_command
import requests

class Status(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    @slash_command(name="status", description="Looks up a minecraft server to get information")
    async def lookup(self, inter: disnake.ApplicationCommandInteraction,ip: str) -> None:
        server_ip = message.content[7:]
        url = f'https://mcapi.us/server/status?ip={server_ip}'
        response = requests.get(url)
        server_status = response.json()
        player_count = server_status['players']['online']
        await inter.send(f'Player count for {server_ip}: {player_count}')

