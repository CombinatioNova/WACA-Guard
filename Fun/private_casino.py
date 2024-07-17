import disnake
from disnake.ext import commands, tasks
import asyncio
import sqlite3
import os

class PrivateCasino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.inactivity_tasks = {}  # Dictionary to track tasks
        self.db_path = os.path.join('databases', 'private_casino.db')
        self.init_database()

    def init_database(self):
        os.makedirs('databases', exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_channels (
                channel_id INTEGER PRIMARY KEY,
                user_id INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def add_active_channel(self, channel_id, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO active_channels (channel_id, user_id) VALUES (?, ?)', (channel_id, user_id))
        conn.commit()
        conn.close()

    def remove_active_channel(self, channel_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM active_channels WHERE channel_id = ?', (channel_id,))
        conn.commit()
        conn.close()

    def get_user_id(self, channel_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM active_channels WHERE channel_id = ?', (channel_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    @commands.slash_command(name="private_casino", description="Create a private casino channel")
    async def private_casino(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        
        # Check if the category exists, if not create it
        category = disnake.utils.get(inter.guild.categories, name="Cova's Casino")
        if not category:
            category = await inter.guild.create_category("Cova's Casino")

        # Create the private channel
        channel_name = f"🎰│private-{inter.author.name}"
        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            inter.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
            inter.guild.me: disnake.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await inter.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        # Send welcome message
        welcome_embed = disnake.Embed(
            title="Welcome to Your Private Casino!",
            description="This channel is only accessible to you and staff. Enjoy your private gaming experience!",
            color=disnake.Color.gold()
        )
        await channel.send(embed=welcome_embed)

        # Start the inactivity check
        self.add_active_channel(channel.id, inter.author.id)
        if channel.id not in self.inactivity_tasks:
            task = self.bot.loop.create_task(self.check_inactivity(channel.id))
            self.inactivity_tasks[channel.id] = task

        await inter.followup.send(f"Your private casino channel has been created: {channel.mention}", ephemeral=True)

    async def check_inactivity(self, channel_id):
        while True:
            await asyncio.sleep(300)  # Wait for 5 minutes
            channel = self.bot.get_channel(channel_id)
            if not channel:
                break

            embed = disnake.Embed(
                title="Inactivity Check",
                description="Are you still using this channel?",
                color=disnake.Color.yellow()
            )
            components = [
                disnake.ui.Button(style=disnake.ButtonStyle.green, label="Yes", custom_id="still_active"),
                disnake.ui.Button(style=disnake.ButtonStyle.red, label="No", custom_id="not_active")
            ]
            message = await channel.send(embed=embed, components=components)

            try:
                inter = await self.bot.wait_for(
                    "button_click",
                    check=lambda i: i.message.id == message.id and i.user.id == self.get_user_id(channel_id),
                    timeout=180  # 3 minutes
                )

                if inter.component.custom_id == "still_active":
                    await inter.response.defer()
                    await message.delete()
                else:
                    await self.delete_channel(channel)

            except asyncio.TimeoutError:
                await self.delete_channel(channel)

    async def delete_channel(self, channel):
        await channel.delete()
        self.remove_active_channel(channel.id)
        if channel.id in self.inactivity_tasks:
            self.inactivity_tasks[channel.id].cancel()
            del self.inactivity_tasks[channel.id]

def setup(bot):
    bot.add_cog(PrivateCasino(bot))