import disnake
from disnake.ext import commands
import sqlite3
from datetime import datetime
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
                await quotes_channel.send(f"\"{reaction.message.content}\" -{reaction.message.author.display_name.capitalize()}, {datetime.now().year}")
                await reaction.message.add_reaction("📸")

    def is_message_reacted(self, message_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT message_id FROM reacted_messages WHERE message_id = ?", (message_id,))
        result = cursor.fetchone()
        return result is not None

    def add_reacted_message(self, message_id):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO reacted_messages (message_id) VALUES (?)", (message_id,))
        self.db_connection.commit()

def setup(bot):
    bot.add_cog(QuotesCog(bot))
