from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button
from disnake import TextInputStyle
import youtube_dl 
from datetime import datetime

global av
global players
players = {}
class Player(Cog):
    def __init__(self,bot: Bot) -> None:
        self.bot = bot
        

    def check_queue(id):
        if players[id]["queue"]:
            player = players[id]["queue"].pop(0)
            players[id]["player"] = player
            player.start()
    
    @slash_command(description="Play a YouTube audio")
    async def play(self,inter, url : str):
        bot = self.bot
        channel = inter.author.voice.channel

        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        players[channel.guild.id] = player

        source = disnake.FFmpegPCMAudio(player.url)
        source = disnake.PCMVolumeTransformer(source)
        source.volume = 0.5

        inter.voice_client = await channel.connect()
        inter.voice_client.play(source, after=lambda e: check_queue(channel.guild.id))

        response_embed = disnake.Embed(
            title="Playing Audio",
            description=f"Now playing: {player.title}",
            color=0x00FF00
        )
        await inter.send(embed=response_embed)

    @slash_command(description="Pause the current audio")
    async def pause(self,inter):
        bot = self.bot
        id = inter.guild.id
        players[id]["player"].pause()

        response_embed = disnake.Embed(
            title="Paused Audio",
            description="Audio has been paused.",
            color=0x00FF00
        )
        await inter.send(embed=response_embed)

    @slash_command(description="Skip the current audio")
    async def skip(self,inter):
        bot = self.bot
        id = inter.guild.id
        player = players.get(id)
        if player is not None:
            player.source.stop()
            check_queue(id)

            response_embed = disnake.Embed(
                title="Skipped Audio",
                description="Audio has been skipped.",
                color=0x00FF00
            )
            await inter.send(embed=response_embed)
        else:
            response_embed = disnake.Embed(
                title="Error",
                description="No audio is currently playing.",
                color=0xFF0000
            )
            await inter.send(embed=response_embed)

    @slash_command(description="Reverse the current audio")
    async def reverse(self,inter):
        bot = self.bot
        id = inter.guild.id
        player = players[id]["player"]
        player.pause()
        player.seek(0)

        response_embed = disnake.Embed(
            title="Reversed Audio",
            description="Audio has been reversed.",
            color=0x00FF00
        )
        await inter.send(embed=response_embed)

    @slash_command(description="Add an audio to the queue")
    async def queue(self,inter, url : str):
        bot = self.bot
        id = inter.guild.id
        player = await YTDLSource.from_url(url, loop=bot.loop)
        players[id]["queue"].append(player)

        response_embed = disnake.Embed(
            title="Queued Audio",
            description=f"{player.title} has been added to the queue.",
           color=0x00FF00
            )
        await inter.send(embed=response_embed)
    @slash_command(description="Disconnect the bot from the voice channel")
    async def disconnect(self,inter):
        bot = self.bot
        server = inter.guild.voice_clients
        await server.disconnect()
        response_embed = disnake.Embed(
        title="Disconnected",
        description="Bot has been disconnected from the voice channel.",
        color=0x00FF00
        )
        
        await inter.send(embed=response_embed)

        
class YTDLSource(disnake.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download=not stream))

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"]
        return cls(disnake.FFmpegPCMAudio(filename), data=data)
