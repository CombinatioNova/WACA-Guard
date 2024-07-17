import disnake
from disnake.ext import commands
import sqlite3
import asyncio
import math

class LevelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        import os
        from pathlib import Path

        # Create the 'databases' directory if it doesn't exist
        database_dir = Path('databases')
        database_dir.mkdir(exist_ok=True)

        # Connect to the database file in the 'databases' directory
        self.conn = sqlite3.connect(database_dir / 'levels.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS levels (
                                user_id INTEGER,
                                guild_id INTEGER,
                                xp INTEGER,
                                level INTEGER,
                                PRIMARY KEY (user_id, guild_id)
                              )''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        guild_id = message.guild.id

        self.cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        result = self.cursor.fetchone()

        if result:
            xp, level = result
            xp += 10
            new_level = int(xp ** (1/4))
            if new_level > level:
                embed = disnake.Embed(
                    title="Level Up!",
                    description=f"Congratulations {message.author.mention}, you have leveled up to level {new_level}!",
                    color=disnake.Color.green()
                )
                await message.channel.send(embed=embed, delete_after=10)
                level = new_level
            self.cursor.execute('UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?', (xp, level, user_id, guild_id))
        else:
            self.cursor.execute('INSERT INTO levels (user_id, guild_id, xp, level) VALUES (?, ?, ?, ?)', (user_id, guild_id, 10, 1))

        self.conn.commit()

    @commands.slash_command(
        name='level',
        description='Check your current level and XP'
    )
    async def level(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        self.cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        result = self.cursor.fetchone()

        if result:
            xp, level = result
            next_level_xp = (level + 1) ** 4
            xp_until_next_level = next_level_xp - xp
            embed = disnake.Embed(
                title="Your Level and XP",
                description=f"{inter.author.mention}, you are currently level {level} with {xp} XP.",
                color=disnake.Color.blue()
            )
            embed.add_field(name="XP Until Next Level", value=f"{xp_until_next_level} XP", inline=False)
        else:
            embed = disnake.Embed(
                title="No XP Yet",
                description=f"{inter.author.mention}, you have no XP yet. Start chatting to earn XP!",
                color=disnake.Color.red()
            )

        await inter.response.send_message(embed=embed)

