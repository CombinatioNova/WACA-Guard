import disnake
from disnake.ext import commands
import sqlite3
import os

class CountingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_folder = "countingData"
        self.db_connection = None
        self.db_cursor = None
        self.counters = {}
        self.last_authors = {}
        self.initialize_database()

    def initialize_database(self):
        os.makedirs(self.db_folder, exist_ok=True)
        db_file = os.path.join(self.db_folder, "counting.db")
        self.db_connection = sqlite3.connect(db_file)
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute("CREATE TABLE IF NOT EXISTS counting (guild_id INTEGER PRIMARY KEY, last_number INTEGER)")
        self.db_connection.commit()

        self.load_counters()

    def load_counters(self):
        self.db_cursor.execute("SELECT * FROM counting")
        results = self.db_cursor.fetchall()
        for guild_id, last_number in results:
            self.counters[guild_id] = last_number
            self.last_authors[guild_id] = None

    @commands.command()
    async def start_counting(self, ctx):
        guild_id = ctx.guild.id
        self.counters[guild_id] = 0
        self.db_cursor.execute("INSERT OR REPLACE INTO counting (guild_id, last_number) VALUES (?, ?)",
                               (guild_id, self.counters[guild_id]))
        self.db_connection.commit()
        await ctx.send(f"Let's start counting! I'll begin with {self.counters[guild_id] + 1}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.channel.name != "🔢│counting":
            return

        guild_id = message.guild.id

        if guild_id not in self.counters:
            self.counters[guild_id] = 0

        if guild_id not in self.last_authors:
            self.last_authors[guild_id] = None

        try:
            next_number = self.counters[guild_id] + 1
            if int(message.content) == next_number:
                self.counters[guild_id] = next_number
                self.last_authors[guild_id] = message.author
                self.db_cursor.execute("INSERT OR REPLACE INTO counting (guild_id, last_number) VALUES (?, ?)",
                                       (guild_id, self.counters[guild_id]))
                self.db_connection.commit()                    
                await message.add_reaction("<:WACACheck:1079146012934942773>")
            else:
                self.counters[guild_id] = 0
                await message.add_reaction("<:WACAx:1079146014969180340>")
                await message.channel.send(f"{message.author.mention}, that's the wrong number! Let's start over from {self.counters[guild_id]}")
                
        except ValueError:
            pass  # Ignore non-integer messages

    def cog_unload(self):
        self.db_connection.close()

def setup(bot):
    bot.add_cog(CountingCog(bot))
