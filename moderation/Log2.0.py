import disnake
from disnake.ext import commands
import sqlite3
from datetime import datetime
from disnake.ext.commands import Param

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('logs.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                lusername TEXT,
                                luserid INTEGER,
                                lchannelid INTEGER,
                                musername TEXT,
                                muserid INTEGER,
                                removed INTEGER
                            )''')
        self.conn.commit()

    @commands.slash_command(description="Log a moderation action")
    async def log(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.User,
        reason: str,
        notes: str = "N/A",
        punishment: str = Param(
            choices=[
                "Verbal Warning",
                "1 Hour Ban",
                "3 Hour Ban",
                "6 Hour Ban",
                "1 Day Ban",
                "3 Day Ban",
                "5 Day Ban",
                "7 Day Ban",
                "14 Day Ban",
                "Permanent Ban",
                "Permanent Ban Without Appeal"
            ]
        )
    ):
        await inter.response.defer(with_message=True, ephemeral=True)
        log_id = self.get_next_log_id()

        channel = disnake.utils.get(inter.guild.channels, name="moderation-logs")

        log_embed = self.create_log_embed(log_id, user, reason, inter.author.name, notes)

        # Add Edit button
        edit_button = Button(
            style=ButtonStyle.primary,
            label="Edit",
            custom_id=f"edit_log:{log_id}",
        )
        log_embed.set_footer(
            text=f"Logged by {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )

        # Add Remove button
        remove_button = Button(
            style=ButtonStyle.danger,
            label="Remove",
            custom_id=f"remove_log:{log_id}",
        )

        # Add Reinstate button
        reinstate_button = Button(
            style=ButtonStyle.primary,
            label="Reinstate",
            custom_id=f"reinstate_log:{log_id}",
            disabled=True,  # Initially disabled
        )

        action_row = disnake.ActionRow(edit_button, remove_button, reinstate_button)

        message = await channel.send(embed=log_embed, components=action_row)

        # Log the moderation action in the database
        self.cursor.execute(
            '''INSERT INTO logs
            (log_id, user_id, reason, moderator, notes, removed)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (log_id, user.id, reason, inter.author.name, notes, 0)
        )
        self.conn.commit()

        await inter.followup.send(
            f"{user.display_name} has been logged and a support ticket has been created.",
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        custom_id = inter.custom_id
        log_id = int(custom_id.split(":")[1])

        if custom_id.startswith("edit_log"):
            await self.handle_edit_button(inter, log_id)
        elif custom_id.startswith("remove_log"):
            await self.handle_remove_button(inter, log_id)
        elif custom_id.startswith("reinstate_log"):
            await self.handle_reinstate_button(inter, log_id)

    async def handle_edit_button(self, inter: disnake.MessageInteraction, log_id: int):
        # Retrieve the log entry from the database
        log = self.get_log(log_id)

        if log:
            # Check if the log is already removed
            if log[6] == 1:
                await inter.followup.send(
                    f"Log {log_id} has been removed and cannot be edited.",
                    ephemeral=True
                )
                return

            # TODO: Handle the logic for editing the log entry

            await inter.followup.send(
                f"Editing log {log_id}...",
                ephemeral=True
            )
        else:
            await inter.followup.send(
                f"No log found with ID {log_id}.",
                ephemeral=True
            )

    async def handle_remove_button(self, inter: disnake.MessageInteraction, log_id: int):
        # Retrieve the log entry from the database
        log = self.get_log(log_id)

        if log:
            # Update the 'removed' field in the database
            self.cursor.execute(
                'UPDATE logs SET removed = ? WHERE log_id = ?',
                (1, log_id)
            )
            self.conn.commit()

            await inter.followup.send(
                f"Log {log_id} has been removed.",
                ephemeral=True
            )
        else:
            await inter.followup.send(
                f"No log found with ID {log_id}.",
                ephemeral=True
            )

    async def handle_reinstate_button(self, inter: disnake.MessageInteraction, log_id: int):
        # Retrieve the log entry from the database
        log = self.get_log(log_id)

        if log:
            # Update the 'removed' field in the database
            self.cursor.execute(
                'UPDATE logs SET removed = ? WHERE log_id = ?',
                (0, log_id)
            )
            self.conn.commit()

            await inter.followup.send(
                f"Log {log_id} has been reinstated.",
                ephemeral=True
            )
        else:
            await inter.followup.send(
                f"No log found with ID {log_id}.",
                ephemeral=True
            )

    def get_next_log_id(self):
        self.cursor.execute('SELECT MAX(log_id) FROM logs')
        result = self.cursor.fetchone()[0]
        if result:
            return result + 1
        return 1

    def get_log(self, log_id):
        self.cursor.execute('SELECT * FROM logs WHERE log_id = ?', (log_id,))
        return self.cursor.fetchone()

def setup(bot):
    bot.add_cog(Log(bot))
