import time
from disnake.ext.commands import Bot, Cog, slash_command
import disnake
import json
class Mitochondria(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    @Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user:
            return
        elif message.content.lower().startswith("the mitochondria is the powerhouse of the cell") or message.content.lower().endswith("the mitochondria is the powerhouse of the cell"):
            await message.channel.send('''
You freaking disgusting piece of single brain celled level of intellect creature.
The word Mitochondria refers to multiple mitochondrion.
The scientifically correct statement is not "The Mitochondria is the powerhouse of the cell."
The correct statement is infact "The Mitochondria are the powerhouse of the cell."
Your education has failed you. Years of schooling, wasted.''')
def setup(bot: Bot) -> None:
    bot.add_cog(Mitochondria(bot))
