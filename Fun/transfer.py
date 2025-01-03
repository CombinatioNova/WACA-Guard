import disnake
from disnake.ext import commands
import sqlite3
import os

class Transfer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(os.path.join('databases', 'gambling.db'))
        self.cursor = self.conn.cursor()

    def cog_unload(self):
        self.conn.close()

    async def ensure_user_exists(self, user_id, guild_id):
        self.cursor.execute('INSERT OR IGNORE INTO gambling (user_id, guild_id, money) VALUES (?, ?, 0)', (user_id, guild_id))
        self.conn.commit()

    @commands.slash_command()
    async def pay(self, inter: disnake.ApplicationCommandInteraction, recipient: disnake.User, amount: int):
        """
        Pay another player WACA-Bucks.

        Parameters
        ----------
        recipient: The user to pay
        amount: The amount of WACA-Bucks to pay
        """
        if amount <= 0:
            return await inter.response.send_message("You must pay a positive amount.", ephemeral=True)

        sender_id = inter.author.id
        recipient_id = recipient.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(sender_id, guild_id)
        await self.ensure_user_exists(recipient_id, guild_id)

        # Check if sender has enough money
        self.cursor.execute('SELECT money FROM gambling WHERE user_id = ? AND guild_id = ?', (sender_id, guild_id))
        sender_money = self.cursor.fetchone()[0]

        if sender_money < amount:
            return await inter.response.send_message("You don't have enough WACA-Bucks to make this payment.", ephemeral=True)

        # Perform the transaction
        self.cursor.execute('UPDATE gambling SET money = money - ? WHERE user_id = ? AND guild_id = ?', (amount, sender_id, guild_id))
        self.cursor.execute('UPDATE gambling SET money = money + ? WHERE user_id = ? AND guild_id = ?', (amount, recipient_id, guild_id))
        self.conn.commit()

        # Create and send confirmation embed
        embed = disnake.Embed(
            title="Payment Successful",
            description=f"{inter.author.mention} has paid {recipient.mention} {amount} WACA-Bucks.",
            color=disnake.Color.green()
        )
        embed.set_footer(text="WACA-Bank Transfer Service")

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Transfer(bot))
