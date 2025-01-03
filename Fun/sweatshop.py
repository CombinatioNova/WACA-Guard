import disnake
from disnake.ext import commands
import sqlite3
import os
import asyncio
import secrets

class Sweatshop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join('databases', 'sweatshop.db')
        self.init_database()
        self.high_stakes = {}  # Dictionary to store high stakes status for each user

    def init_database(self):
        os.makedirs('databases', exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_tokens (
                user_id INTEGER PRIMARY KEY,
                tokens INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def get_work_tokens(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT tokens FROM work_tokens WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def update_work_tokens(self, user_id, tokens):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO work_tokens (user_id, tokens) VALUES (?, ?)', (user_id, tokens))
        conn.commit()
        conn.close()

    @commands.slash_command(name="work", description="Work to earn Work Tokens!")
    async def work(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        
        # Get user level from levels database
        levels_conn = sqlite3.connect(os.path.join('databases', 'levels.db'))
        levels_cursor = levels_conn.cursor()
        levels_cursor.execute('SELECT level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, inter.guild.id))
        result = levels_cursor.fetchone()
        user_level = result[0] if result else 1
        levels_conn.close()

        tokens_per_click = max(1, (user_level + 5) // 5)  # 2 tokens at level 5, 3 at level 10, etc.
        current_tokens = self.get_work_tokens(user_id)

        # Check high stakes status
        is_high_stakes = self.high_stakes.get(user_id, False)
        high_stakes_style = disnake.ButtonStyle.secondary if is_high_stakes else disnake.ButtonStyle.danger

        embed = disnake.Embed(title="Sweatshop Work", color=disnake.Color.red() if is_high_stakes else disnake.Color.blue())
        embed.add_field(name="Work Tokens", value=str(current_tokens), inline=False)
        embed.add_field(name="Tokens per Click", value=f"{tokens_per_click} (High Stakes Mode)" if is_high_stakes else str(tokens_per_click), inline=False)
        embed.set_footer(text=f"User Level: {user_level}")

        components = [
            disnake.ui.Button(emoji="<:Construction:1263030921930477659>",style=disnake.ButtonStyle.primary, label="Work", custom_id="work_button"),
            disnake.ui.Button(emoji="<:CurrencyExchange:1262116791539335311>",style=disnake.ButtonStyle.success, label="Exchange all work tokens", custom_id="exchange_button"),
            disnake.ui.Button(emoji="<:Priority:1263030595295117312>",style=high_stakes_style, label="High Stakes", custom_id="high_stakes_button")
        ]

        await inter.response.send_message(embed=embed, components=components)

        exchange_rate = round(random.uniform(0.5, 5), 2)  # 0.5 to 5 WACA-Bucks per Work Token

        message = await inter.original_message()

        def check(i):
            return i.message.id == message.id and i.user.id == inter.author.id

        while True:
            try:
                button_inter = await self.bot.wait_for("button_click", check=check, timeout=30.0)

                if button_inter.component.custom_id == "work_button":
                    tokens_gained = tokens_per_click
                    current_tokens += tokens_gained
                    self.update_work_tokens(user_id, current_tokens)
                    
                    embed.set_field_at(0, name="Work Tokens", value=str(current_tokens), inline=False)
                    await button_inter.response.edit_message(embed=embed)

                elif button_inter.component.custom_id == "exchange_button":
                    if self.high_stakes.get(user_id, False):
                        exchange_rate = round(random.uniform(-5, 10), 2)
                    waca_bucks = round(current_tokens * exchange_rate)
                    quality = "high" if exchange_rate >= 3.5 else "medium" if exchange_rate >= 2 else "low"

                    result_embed = disnake.Embed(title="Token Exchange", color=disnake.Color.green())
                    result_embed.add_field(name="Work Tokens Exchanged", value=str(current_tokens), inline=False)
                    result_embed.add_field(name="WACA-Bucks Received", value=str(waca_bucks), inline=False)
                    result_embed.add_field(name="Exchange Rate", value=f"{exchange_rate:.2f} WACA-Bucks per Token", inline=False)
                    result_embed.add_field(name="Exchange Quality", value=quality.capitalize(), inline=False)
                    result_embed.add_field(name="High Stakes", value="Enabled" if self.high_stakes.get(user_id, False) else "Disabled", inline=False)

                    self.update_work_tokens(user_id, 0)  # Reset work tokens to 0

                    # Update WACA-Bucks in gambling database
                    gambling_conn = sqlite3.connect(os.path.join('databases', 'gambling.db'))
                    gambling_cursor = gambling_conn.cursor()
                    gambling_cursor.execute('UPDATE gambling SET money = money + ? WHERE user_id = ? AND guild_id = ?', 
                                            (waca_bucks, user_id, inter.guild.id))
                    gambling_conn.commit()
                    gambling_conn.close()

                    await button_inter.response.edit_message(embed=result_embed, components=[])
                    break  # End the loop after exchange

                elif button_inter.component.custom_id == "high_stakes_button":
                    self.high_stakes[user_id] = not self.high_stakes.get(user_id, False)
                    new_style = disnake.ButtonStyle.secondary if self.high_stakes[user_id] else disnake.ButtonStyle.danger
                    components[2] = disnake.ui.Button(emoji="<:Priority:1263030595295117312>",style=new_style, label="High Stakes", custom_id="high_stakes_button")
                    
                    embed.color = disnake.Color.red() if self.high_stakes[user_id] else disnake.Color.blue()
                    embed.set_field_at(1, name="Tokens per Click", value=f"{tokens_per_click} (High Stakes Mode)" if self.high_stakes[user_id] else str(tokens_per_click), inline=False)
                    
                    await button_inter.response.edit_message(embed=embed, components=components)

            except asyncio.TimeoutError:
                timeout_embed = disnake.Embed(title="Work Session Ended", description="30 seconds of inactivity has passed.", color=disnake.Color.red())
                await message.edit(embed=timeout_embed, components=[])
                break

def setup(bot):
    bot.add_cog(Sweatshop(bot))