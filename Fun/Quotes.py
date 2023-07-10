import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
import sqlite3
from datetime import datetime
import re

class QuotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_connection = sqlite3.connect('reacted_messages.db')
        self.create_table()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS reacted_messages
                          (message_id INTEGER PRIMARY KEY)''')
        self.db_connection.commit()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        current_year = datetime.now().year
        quotes_channel_name = "💬│quotes"  # Default channel name
        guild = reaction.message.guild
        if guild:
            quotes_channel = disnake.utils.get(guild.channels, name=quotes_channel_name, type=disnake.ChannelType.text)
            if (
                quotes_channel
                and reaction.emoji == "📸"
                and reaction.message.channel != quotes_channel
                and user.id != self.bot.user.id
                and not self.is_message_reacted(reaction.message.id)
            ):
                self.add_reacted_message(reaction.message.id)
                quoted_content = self.remove_mentions(reaction.message.content, reaction.message.mentions)
                quoted_text = f"\"{quoted_content}\" - {reaction.message.author.display_name.capitalize()}, {datetime.now().year}"
                await quotes_channel.send(quoted_text)
                await reaction.message.add_reaction("📸")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return

    def is_message_reacted(self, message_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT message_id FROM reacted_messages WHERE message_id = ?", (message_id,))
        result = cursor.fetchone()
        return result is not None

    def add_reacted_message(self, message_id):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO reacted_messages (message_id) VALUES (?)", (message_id,))
        self.db_connection.commit()

    def remove_mentions(self, content, mentions):
        # Remove @everyone and @here mentions
        content = content.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")

        # Remove role mentions
        content = re.sub(r"<@&[0-9]+>", "", content)

        # Remove user mentions
        for mention in mentions:
            content = content.replace(mention.mention, mention.display_name)

        return content

    @commands.message_command(name="Snapshot")
    async def snapshot(self, inter, message):
        
        if message:
            current_year = datetime.now().year
            quotes_channel_name = "💬│quotes"  # Default channel name
            quotes_channel = disnake.utils.get(message.guild.channels, name=quotes_channel_name)
            if (
                quotes_channel
                and message.channel != quotes_channel
                and message.author != self.bot.user
                and not self.is_message_reacted(message.id)
            ):
                self.add_reacted_message(message.id)
                print("Add!")
                quoted_content = self.remove_mentions(message.content, message.mentions)
                print("Removed mentions!")
                quoted_text = f"\"{quoted_content}\" - {message.author.display_name.capitalize()}, {datetime.now().year}"
                await quotes_channel.send(quoted_text)
                print("Sent!")
                await message.add_reaction("📸")
                await inter.response.send_message("Done!", ephemeral=True)
            else:
                print("No...")

def setup(bot):
    bot.add_cog(QuotesCog(bot))
