import disnake
from disnake.ext import commands
import sqlite3
import os
from core import statbed

class RichestPoorEasterEgg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join('databases', 'gambling.db')

    def get_extreme_user(self, guild_id, order='DESC'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, money FROM gambling WHERE guild_id = ? ORDER BY money {order} LIMIT 1', (guild_id,))
        result = cursor.fetchone()
        conn.close()
        return result if result else (None, 0)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            if message.author.id == 1128180875654332466:
                embed = await statbed.create_alert_embed(
                    title="Hmm...",
                    description="I see how it is. Using another bot instead of WACA-Chan, are we?",
                    footer="Betrayal detected"
                )
                await message.channel.send(embed=embed)
            return

        richest_user_id, _ = self.get_extreme_user(message.guild.id, 'DESC')
        poorest_user_id, poorest_money = self.get_extreme_user(message.guild.id, 'ASC')
        
        if message.author.id == richest_user_id:
            poor_keywords = ['poor', 'broke', 'no money', 'cant afford', "can't afford"]
            if any(keyword in message.content.lower() for keyword in poor_keywords):
                embed = await statbed.create_alert_embed(
                    title="A Message for the Wealthy",
                    description=(
                        f"{message.author.mention}, as the wealthiest member of this server, "
                        "it might be beneficial for you to read this:\n"
                        "https://www.marxists.org/archive/marx/works/download/pdf/Manifesto.pdf"
                    ),
                    footer="The Communist Manifesto"
                )
                await message.channel.send(embed=embed)
        
        elif message.author.id == poorest_user_id and poorest_money < 0:
            bailout_keywords = ['bailout', 'need money', 'financial assistance']
            if any(keyword in message.content.lower() for keyword in bailout_keywords):
                embed = await statbed.create_alert_embed(
                    title="Career Opportunity",
                    description=(
                        f"{message.author.mention}, as the most indebted member of this server, "
                        "we thought you might find this helpful:\n"
                        "https://careers.mcdonalds.com/us-restaurants/jobs"
                    ),
                    footer="McDonald's Job Application"
                )
                await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(RichestPoorEasterEgg(bot))
