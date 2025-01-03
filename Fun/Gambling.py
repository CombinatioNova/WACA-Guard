import disnake
from disnake.ext import commands, tasks
import sqlite3
import secrets
import os
import json
from disnake.ext.commands import Param
from core import statbed

# Connect to (or create) the SQLite database in the databases folder
conn = sqlite3.connect(os.path.join('databases', 'gambling.db'))
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS gambling (
    user_id INTEGER,
    guild_id INTEGER,
    money INTEGER NOT NULL DEFAULT 100,
    PRIMARY KEY (user_id, guild_id)
)
''')

# Add columns if they don't exist
columns_to_add = [
    ('xp', 'INTEGER NOT NULL DEFAULT 0'),
    ('times_played', 'INTEGER NOT NULL DEFAULT 0'),
    ('loan', 'INTEGER NOT NULL DEFAULT 0'),
    ('loan_interest', 'REAL NOT NULL DEFAULT 0'),
    ('wins', 'INTEGER NOT NULL DEFAULT 0'),
    ('losses', 'INTEGER NOT NULL DEFAULT 0'),
    ('payment_history', 'TEXT DEFAULT \'[]\'')
]

for column_name, column_type in columns_to_add:
    cursor.execute(f"PRAGMA table_info(gambling)")
    existing_columns = [column[1] for column in cursor.fetchall()]
    if column_name not in existing_columns:
        cursor.execute(f"ALTER TABLE gambling ADD COLUMN {column_name} {column_type}")

conn.commit()

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_choices = {}
        self.add_interest.start()

    def cog_unload(self):
        self.add_interest.cancel()

    @tasks.loop(hours=24)
    async def add_interest(self):
        cursor.execute('SELECT user_id, guild_id, loan, loan_interest FROM gambling WHERE loan > 0')
        users_with_loans = cursor.fetchall()
        for user_id, guild_id, loan, loan_interest in users_with_loans:
            new_interest = loan * 0.05  # 5% daily interest
            cursor.execute('UPDATE gambling SET loan_interest = loan_interest + ? WHERE user_id = ? AND guild_id = ?', (new_interest, user_id, guild_id))
        conn.commit()

    async def ensure_user_exists(self, user_id, guild_id):
        cursor.execute('SELECT * FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user = cursor.fetchone()
        if user is None:
            cursor.execute('INSERT INTO gambling (user_id, guild_id) VALUES (?, ?)', (user_id, guild_id))
            conn.commit()

    @commands.slash_command()
    async def roulette(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        # Fetch user data after ensuring the record exists
        cursor.execute('SELECT money, xp, times_played, loan, loan_interest, wins, losses FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user = cursor.fetchone()
        money, xp, times_played, loan, loan_interest, wins, losses = user

        embed = disnake.Embed(title="<:Cards:1262085399938076762> Roulette", color=disnake.Color.blue())
        embed.add_field(name="WACA-Bucks", value=f"{money}", inline=True)
        embed.add_field(name="Debt", value=f"{loan + loan_interest:.2f}", inline=True)
        embed.set_footer(text=f"{inter.author.display_name}'s Game", icon_url=inter.author.display_avatar.url)
        components = [
            disnake.ui.Button(emoji="⚫", custom_id="black"),
            disnake.ui.Button(emoji="🔴", custom_id="red")
        ]
        await inter.response.send_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

    @commands.slash_command(
        name='exchange_xp',
        description='Exchange your XP for WACA-Bucks'
    )
    async def exchange_xp(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        # Connect to the levels database
        levels_conn = sqlite3.connect(os.path.join('databases', 'levels.db'))
        levels_cursor = levels_conn.cursor()

        # Fetch user XP and level from levels database
        levels_cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        result = levels_cursor.fetchone()

        if result:
            user_xp, user_level = result
            embed = disnake.Embed(
                title="Exchange XP for WACA-Bucks",
                description="The exchange rate is 10 XP for 1 WACA-Buck.",
                color=disnake.Color.blue()
            )
            embed.set_author(name="WACA-Bank Currency Exchange", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262126386060198079/CExchange.png?ex=6695764b&is=669424cb&hm=bc2167697ad828f04fe0265c93fb5fa1c20f5f390eac7a53712d02e4f16d7f63&")
            embed.add_field(name="Current XP", value=f"{user_xp}", inline=True)
            embed.add_field(name="Exchange Rate", value="10 XP = 1 WACA-Buck", inline=True)
            components = [
                disnake.ui.Button(emoji="<:CurrencyExchange:1262116791539335311>",label="Exchange", custom_id="exchange_xp_confirm", style=disnake.ButtonStyle.success),
                disnake.ui.Button(emoji="<:whitex:1263028345721851924>",label="Cancel", custom_id="exchange_xp_cancel", style=disnake.ButtonStyle.danger)
            ]
            await inter.response.send_message(embed=embed, components=[disnake.ui.ActionRow(*components)])
        else:
            embed = disnake.Embed(
                title="No XP Yet",
                description="You do not have any XP to exchange. Start chatting to earn XP!",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed)
            levels_conn.close()

    @commands.Cog.listener()
    async def on_modal_submit(self, inter: disnake.ModalInteraction):
        if inter.custom_id == "exchange_xp_modal":
            xp_amount = int(inter.text_values["xp_amount"])
            user_id = inter.author.id
            guild_id = inter.guild.id

            await self.ensure_user_exists(user_id, guild_id)

            # Connect to the levels database
            levels_conn = sqlite3.connect('databases/levels.db')
            levels_cursor = levels_conn.cursor()

            # Fetch user XP and level from levels database
            levels_cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            result = levels_cursor.fetchone()

            if result:
                user_xp, user_level = result
                if user_xp < xp_amount:
                    embed = disnake.Embed(
                        title="Insufficient XP",
                        description=f"You do not have enough XP to exchange. You currently have {user_xp} XP.",
                        color=disnake.Color.red()
                    )
                    embed.add_field(name="Current XP", value=f"{user_xp}", inline=True)
                    embed.add_field(name="Requested XP", value=f"{xp_amount}", inline=True)
                    await inter.response.edit_message(embed=embed, components=[])
                    levels_conn.close()
                    return

                # Calculate WACA-Bucks to be given
                waca_bucks = xp_amount // 10
                remaining_xp = user_xp - xp_amount
                new_level = int(remaining_xp ** (1/4))

                # Update levels database
                levels_cursor.execute('UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?', (remaining_xp, new_level, user_id, guild_id))
                levels_conn.commit()
                levels_conn.close()

                # Update gambling database
                cursor.execute('SELECT money FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
                user = cursor.fetchone()
                if user is None:
                    cursor.execute('INSERT INTO gambling (user_id, guild_id, money) VALUES (?, ?, ?)', (user_id, guild_id, waca_bucks))
                else:
                    cursor.execute('UPDATE gambling SET money = money + ? WHERE user_id = ? AND guild_id = ?', (waca_bucks, user_id, guild_id))
                conn.commit()

                embed = disnake.Embed(
                    title="Exchange Successful",
                    description=f"You have successfully exchanged {xp_amount} XP for {waca_bucks} WACA-Bucks.",
                    color=disnake.Color.green()
                )
                embed.set_author(name="WACA-Bank Currency Exchange", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262126386060198079/CExchange.png?ex=6695764b&is=669424cb&hm=bc2167697ad828f04fe0265c93fb5fa1c20f5f390eac7a53712d02e4f16d7f63&")
                embed.add_field(name="Exchanged XP", value=f"{xp_amount}", inline=True)
                embed.add_field(name="WACA-Bucks Received", value=f"{waca_bucks}", inline=True)
                embed.add_field(name="Remaining XP", value=f"{remaining_xp}", inline=True)
                embed.add_field(name="New Level", value=f"{new_level}", inline=True)
                await inter.response.edit_message(embed=embed, components=[])
            else:
                embed = disnake.Embed(
                    title="No XP Yet",
                    description="You do not have any XP to exchange. Start chatting to earn XP!",
                    color=disnake.Color.red()
                )
                await inter.response.edit_message(embed=embed, components=[])
                levels_conn.close()
        elif inter.custom_id == "pay_loan_modal":
            user_id = inter.author.id
            guild_id = inter.guild.id
            cursor.execute('SELECT money, loan, loan_interest, wins, losses FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            user = cursor.fetchone()
            if user is None:
                return await inter.send("You need to run the /roulette command first.", ephemeral=True)

            money, loan, loan_interest, wins, losses = user
            try:
                payment_amount = float(inter.text_values["payment_amount"])
            except ValueError:
                return await inter.response.send_message("Please enter a valid number for the payment amount.", ephemeral=True)

            

            cursor.execute('SELECT money, loan, loan_interest, payment_history FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            user = cursor.fetchone()
            if user is None:
                return await inter.response.send_message("You don't have any loans.", ephemeral=True)

            money, loan, loan_interest, payment_history = user
            payment_history = json.loads(payment_history)
            total_debt = loan + loan_interest

            if payment_amount > money:
                return await inter.response.send_message("You don't have enough WACA-Bucks to make this payment.", ephemeral=True)

            if payment_amount > total_debt:
                payment_amount = total_debt

            # Pay off the loan
            money -= payment_amount
            on_time = payment_amount >= (total_debt * 0.1)  # Consider payment on time if it's at least 10% of total debt
            payment_history.append([payment_amount, on_time])

            if payment_amount > loan_interest:
                loan -= (payment_amount - loan_interest)
                loan_interest = 0
            else:
                loan_interest -= payment_amount

            cursor.execute('UPDATE gambling SET money = ?, loan = ?, loan_interest = ?, payment_history = ? WHERE user_id = ? AND guild_id = ?', 
                           (money, loan, loan_interest, json.dumps(payment_history), user_id, guild_id))
            conn.commit()

            credit_score = await self.calculate_credit_score(user_id, guild_id)

            embed = disnake.Embed(
                title="Loan Payment Successful",
                description=f"You have successfully paid {payment_amount:.2f} WACA-Bucks towards your loan.",
                color=disnake.Color.green()
            )
            embed.add_field(name="Remaining Loan", value=f"{loan:.2f}", inline=True)
            embed.add_field(name="Remaining Interest", value=f"{loan_interest:.2f}", inline=True)
            embed.add_field(name="Current WACA-Bucks", value=f"{money:.2f}", inline=True)
            embed.add_field(name="Credit Score", value=f"{credit_score}", inline=True)
            await inter.response.edit_message(embed=embed, components=[])
        # Handle the custom loan modal submission
        elif inter.custom_id == "custom_loan_modal":
            user_id = inter.author.id
            guild_id = inter.guild.id

            # Fetch current user data
            cursor.execute('SELECT money, loan FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            user_data = cursor.fetchone()
            if user_data is None:
                embed = await statbed.create_error_embed(
                    title="No Gambling Data",
                    description="You need to play some games first before taking a loan.",
                    footer="WACA-Bank Error"
                )
                return await inter.response.send_message(embed=embed, ephemeral=True)

            current_money, current_loan = user_data

            # Fetch user level from levels database
            levels_conn = sqlite3.connect(os.path.join('databases', 'levels.db'))
            levels_cursor = levels_conn.cursor()
            levels_cursor.execute('SELECT level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            level_result = levels_cursor.fetchone()
            levels_conn.close()

            user_level = level_result[0] if level_result else 1
            max_loan = user_level * 100  # Max loan is 100 times the user's level

            loan_amount = inter.text_values["loan_amount"]
            try:
                loan_amount = int(loan_amount)
                if loan_amount <= 0 or loan_amount > max_loan:
                    raise ValueError
            except ValueError:
                embed = await statbed.create_error_embed(
                    title="Invalid Loan Amount",
                    description=f"Please enter a valid loan amount between 1 and {max_loan}.",
                    footer="WACA-Bank Error"
                )
                await inter.response.send_message(embed=embed, ephemeral=True)
                return

            # Process the custom loan
            new_loan = current_loan + loan_amount
            new_money = current_money + loan_amount
            cursor.execute('UPDATE gambling SET loan = ?, money = ? WHERE user_id = ? AND guild_id = ?', (new_loan, new_money, user_id, guild_id))
            conn.commit()

            embed = disnake.Embed(
                title="Custom Loan Approved",
                description=f"You have been granted a loan of {loan_amount} WACA-Bucks.",
                color=disnake.Color.green()
            )
            embed.add_field(name="New Balance", value=f"{new_money:.2f} WACA-Bucks", inline=True)
            embed.add_field(name="Total Loan", value=f"{new_loan:.2f} WACA-Bucks", inline=True)
            await inter.response.edit_message(embed=embed, components=[])
    @commands.slash_command()
    async def loan(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        # Connect to the levels database
        levels_conn = sqlite3.connect(os.path.join('databases', 'levels.db'))
        levels_cursor = levels_conn.cursor()

        # Fetch user XP and level from levels database
        levels_cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        result = levels_cursor.fetchone()

        if result:
            user_xp, user_level = result
            max_loan = user_level * 100  # Max loan is 100 times the user's level
        else:
            user_level = 1
            max_loan = 100

        levels_conn.close()

        # Create the loan confirmation embed
        embed = disnake.Embed(title="Loan Options", description="Choose a loan amount or enter a custom amount.", color=0xffa500)
        embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
        
        embed.add_field(name="Default Loan Amount", value="100 WACA-Bucks", inline=False)
        embed.add_field(name="Maximum Loan Amount", value=f"{max_loan} WACA-Bucks", inline=False)
        embed.add_field(name="Interest Rate", value="20%", inline=False)
        embed.set_footer(text=f"{inter.author.display_name}'s Session | Level: {user_level}", icon_url=inter.author.display_avatar.url)

        components = [
            disnake.ui.Button(emoji="<:Credit:1263027887372636210>",label="100 WACA-Bucks", custom_id="loan_100", style=disnake.ButtonStyle.primary),
            disnake.ui.Button(emoji="<:CreditGear:1263029129696251947>",label="Custom Amount", custom_id="loan_custom", style=disnake.ButtonStyle.success),
            disnake.ui.Button(emoji="<:whitex:1263028345721851924>",label="Cancel", custom_id="loan_cancel", style=disnake.ButtonStyle.danger)
        ]

        await inter.response.send_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        

        if inter.component.custom_id not in ['confirm_all_in','cancel_all_in','bet_all','pay_loan_modal', 'loan_yes', 'loan_no', 'black', 'red', 'bet_10', 'bet_20', 'bet_50', 'bet_100', 'rps_wager_10', 'rps_wager_20', 'rps_wager_50', 'rps_wager_100', 'rps_rock', 'rps_paper', 'rps_scissors', 'exchange_xp_confirm', 'exchange_xp_cancel', 'bank_loan', 'bank_exchange', 'bank_back', 'loan_100', 'loan_custom', 'loan_cancel']:
            return
            # Check if the user who clicked the button is the same as the one who initiated the command
        elif inter.message.interaction and inter.message.interaction.user.id != inter.author.id:
            embed = await statbed.create_alert_embed(
                title="Unauthorized Interaction",
                description="You cannot interact with someone else's game.",
                footer="Access denied"
            )
            return await inter.response.send_message(embed=embed, ephemeral=True)
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        cursor.execute('SELECT money, loan, loan_interest, wins, losses FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user = cursor.fetchone()
        if user is None:
            return await inter.send("You need to run the /roulette command first.", ephemeral=True)

        money, loan, loan_interest, wins, losses = user
        if inter.component.custom_id == 'loan_cancel':
            embed = disnake.Embed(title="Loan Cancelled", description="You have cancelled the loan request.", color=0xff0000)
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
            embed.set_footer(text=f"{inter.author.display_name}'s Session", icon_url=inter.author.display_avatar.url)
            await inter.response.edit_message(embed=embed, components=[])
            return
        if inter.component.custom_id == 'loan_100':
            loan_amount = 100
            new_loan = loan + loan_amount
            new_money = money + loan_amount
            new_loan_interest = loan_interest + int(loan_amount * 0.2)  # 20% interest

            cursor.execute('UPDATE gambling SET money = ?, loan = ?, loan_interest = ? WHERE user_id = ? AND guild_id = ?',
                           (new_money, new_loan, new_loan_interest, user_id, guild_id))
            conn.commit()

            embed = disnake.Embed(title="Loan Approved", color=0x00ff00)
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
            embed.add_field(name="Loan Amount", value=f"{loan_amount} WACA-Bucks", inline=False)
            embed.add_field(name="New Balance", value=f"{new_money} WACA-Bucks", inline=False)
            embed.add_field(name="Total Loan", value=f"{new_loan} WACA-Bucks", inline=False)
            embed.add_field(name="Interest to Pay", value=f"{new_loan_interest} WACA-Bucks", inline=False)
            embed.set_footer(text=f"{inter.author.display_name}'s Loan | Remember to repay!", icon_url=inter.author.display_avatar.url)

            await inter.response.edit_message(embed=embed, components=[])
            return
        if inter.component.custom_id == 'loan_custom':
            # Create a modal for custom loan amount
            modal = disnake.ui.Modal(
                title="Custom Loan Amount",
                custom_id="custom_loan_modal",
                components=[
                    disnake.ui.TextInput(
                        label="Enter loan amount",
                        custom_id="loan_amount",
                        style=disnake.TextInputStyle.short,
                        placeholder="Enter amount",
                        max_length=4
                    )
                ]
            )
            await inter.response.send_modal(modal)
            return

        

        if inter.component.custom_id == 'bank_loan':
            user_id = inter.author.id
            guild_id = inter.guild.id

            await self.ensure_user_exists(user_id, guild_id)

            # Connect to the levels database
            levels_conn = sqlite3.connect(os.path.join('databases', 'levels.db'))
            levels_cursor = levels_conn.cursor()
            # Fetch user XP and level from levels database
            levels_cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            result = levels_cursor.fetchone()

            if result:
                user_xp, user_level = result
                max_loan = user_level * 100  # Max loan is 100 times the user's level
            else:
                user_level = 1
                max_loan = 100

            levels_conn.close()
            # Create the loan confirmation embed
            embed = disnake.Embed(title="Loan Options", description="Choose a loan amount or enter a custom amount.", color=0xffa500)
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
            
            embed.add_field(name="Default Loan Amount", value="100 WACA-Bucks", inline=False)
            embed.add_field(name="Maximum Loan Amount", value=f"{max_loan} WACA-Bucks", inline=False)
            embed.add_field(name="Interest Rate", value="20%", inline=False)
            embed.set_footer(text=f"{inter.author.display_name}'s Session | Level: {user_level}", icon_url=inter.author.display_avatar.url)

            components = [
                disnake.ui.Button(emoji="<:Credit:1263027887372636210>",label="100 WACA-Bucks", custom_id="loan_100", style=disnake.ButtonStyle.primary),
                disnake.ui.Button(emoji="<:CreditGear:1263029129696251947> ",label="Custom Amount", custom_id="loan_custom", style=disnake.ButtonStyle.success),
                disnake.ui.Button(emoji="<:whitex:1263028345721851924>",label="Cancel", custom_id="loan_cancel", style=disnake.ButtonStyle.danger)
            ]

            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

        elif inter.component.custom_id == 'bank_exchange':
            try:
                user_id = inter.author.id
                guild_id = inter.guild.id

                await self.ensure_user_exists(user_id, guild_id)

                # Connect to the levels database
                levels_conn = sqlite3.connect(os.path.join('databases', 'levels.db'))
                levels_cursor = levels_conn.cursor()

                try:
                    # Fetch user XP and level from levels database
                    levels_cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
                    result = levels_cursor.fetchone()

                    if result:
                        user_xp, user_level = result
                        embed = disnake.Embed(
                            title="XP Exchange",
                            description="Would you like to exchange your XP for WACA-Bucks?",
                            color=disnake.Color.blue()
                        )
                        embed.set_author(name="WACA-Bank Currency Exchange", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262126386060198079/CExchange.png?ex=6695764b&is=669424cb&hm=bc2167697ad828f04fe0265c93fb5fa1c20f5f390eac7a53712d02e4f16d7f63&")
                        embed.add_field(name="Current XP", value=f"{user_xp}", inline=True)
                        embed.add_field(name="Exchange Rate", value="10 XP = 1 WACA-Buck", inline=True)
                        components = [
                            disnake.ui.Button(emoji="<:check:1263028346938458142>",label="Confirm", custom_id="exchange_xp_confirm", style=disnake.ButtonStyle.success),
                            disnake.ui.Button(emoji="<:whitex:1263028345721851924>",label="Cancel", custom_id="exchange_xp_cancel", style=disnake.ButtonStyle.danger),
                            disnake.ui.Button(emoji="<:BackArrow:1261797643487805440>",label="Back", custom_id="bank_back", style=disnake.ButtonStyle.secondary)
                        ]

                        await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])
                    else:
                        await inter.response.send_message("You don't have any XP to exchange.", ephemeral=True)
                except sqlite3.Error as e:
                    await inter.response.send_message(f"An error occurred while fetching your XP: {str(e)}", ephemeral=True)
                finally:
                    levels_conn.close()
            except Exception as e:
                await inter.response.send_message(f"An unexpected error occurred: {str(e)}", ephemeral=True)
        elif inter.component.custom_id == 'pay_loan_modal':
            try:
                modal = disnake.ui.Modal(
                    title="Pay Loan",
                    custom_id="pay_loan_modal",
                    components=[
                        disnake.ui.TextInput(
                            label="Payment Amount",
                            custom_id="payment_amount",
                            style=disnake.TextInputStyle.short,
                            placeholder="Enter the amount to pay towards your loan",
                            required=True
                        )
                    ]
                )
                await inter.response.send_modal(modal)
            except Exception as e:
                error_embed = disnake.Embed(
                    title="Error",
                    description=f"An error occurred while processing your request: {str(e)}",
                    color=disnake.Color.red()
                )
                await inter.response.send_message(embed=error_embed, ephemeral=True)

        elif inter.component.custom_id == 'bank_back':
            embed = disnake.Embed(title="WACA-Bank", description="Welcome to WACA-Bank. What would you like to do?", color=disnake.Color.blue())
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
            
            components = [
                disnake.ui.Button(emoji="<:Credit:1263027887372636210>", label="Get a Loan", custom_id="bank_loan", style=disnake.ButtonStyle.primary),
                disnake.ui.Button(emoji="<:CurrencyExchange:1262116791539335311>", label="Exchange XP", custom_id="bank_exchange", style=disnake.ButtonStyle.primary),
                disnake.ui.Button(emoji="<:CreditCheck:1263027888186196050>", label="Pay Loan", custom_id="pay_loan_modal", style=disnake.ButtonStyle.success)
            ]

            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

        elif inter.component.custom_id == 'loan_yes':
            # Give a loan of 100 WACA-Bucks
            cursor.execute('UPDATE gambling SET money = money + 100, loan = loan + 100 WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            conn.commit()

            # Fetch updated user data
            cursor.execute('SELECT money, loan, loan_interest FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            money, loan, loan_interest = cursor.fetchone()

            embed = disnake.Embed(title="Loan Granted", description="You have received a loan.", color = disnake.Colour.green())
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
        
            embed.add_field(name="WACA-Bucks", value=f"{money}", inline=True)
            embed.add_field(name="Debt", value=f"{loan + loan_interest:.2f}", inline=True)
            
            components = [
                disnake.ui.Button(emoji="<:BackArrow:1261797643487805440>",label="Back", custom_id="bank_back", style=disnake.ButtonStyle.secondary)
            ]
            
            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

        elif inter.component.custom_id == 'loan_no':
            embed = disnake.Embed(title="Loan Canceled", description="You have canceled the loan request.", color = disnake.Colour.red())
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
        
            components = [
                disnake.ui.Button(emoji="<:BackArrow:1261797643487805440>",label="Back", custom_id="bank_back", style=disnake.ButtonStyle.secondary)
            ]
            
            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

        elif inter.component.custom_id == "exchange_xp_confirm":
            print("triggered")
            modal = disnake.ui.Modal(
                title="Exchange XP",
                custom_id="exchange_xp_modal",
                components=[
                    disnake.ui.TextInput(
                        label="XP Amount",
                        custom_id="xp_amount",
                        style=disnake.TextInputStyle.short,
                        placeholder="Enter the amount of XP to exchange",
                        required=True
                    )
                ]
            )
            await inter.response.send_modal(modal)
        elif inter.component.custom_id == "exchange_xp_cancel":
            embed = disnake.Embed(
                title="XP Exchange Cancelled",
                description="You have cancelled the XP exchange.",
                color=disnake.Color.red()
            )
            components = [
                disnake.ui.Button(emoji="<:BackArrow:1261797643487805440>",label="Back", custom_id="bank_back", style=disnake.ButtonStyle.secondary)
            ]
            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

        elif inter.component.custom_id in ['black', 'red']:
            # Store the user's color choice
            self.user_choices[user_id] = inter.component.custom_id
            embed = disnake.Embed(title="Choose your bet", color=disnake.Color.blue())
            embed.add_field(name="WACA-Bucks", value=f"{money}", inline=True)
            embed.set_author(name="WACA-Casino", icon_url="https://cdn.discordapp.com/emojis/1262085399938076762.webp?size=128&quality=lossless")
            components = [
                disnake.ui.Button(label="10 WACA-Bucks", custom_id="bet_10",style=disnake.ButtonStyle.primary, emoji="💵"),
                disnake.ui.Button(label="20 WACA-Bucks", custom_id="bet_20",style=disnake.ButtonStyle.primary, emoji="💸"),
                disnake.ui.Button(label="50 WACA-Bucks", custom_id="bet_50",style=disnake.ButtonStyle.primary, emoji="💰"),
                disnake.ui.Button(label="100 WACA-Bucks", custom_id="bet_100",style=disnake.ButtonStyle.primary, emoji="🏦"),
                disnake.ui.Button(label="All-In", custom_id="bet_all",style=disnake.ButtonStyle.danger, emoji="🎰")
            ]
            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

            

        elif inter.component.custom_id == "bet_all":
            embed = disnake.Embed(
                title="⚠️ ALL-IN CONFIRMATION",
                description=f"Are you sure you want to bet all your {money} WACA-Bucks?",
                color=disnake.Color.gold()
            )
            embed.set_footer(text="This action cannot be undone!")
            components = [
                disnake.ui.Button(emoji="<:check:1263028346938458142>",label="Confirm", custom_id="confirm_all_in", style=disnake.ButtonStyle.danger),
                disnake.ui.Button(emoji="<:whitex:1263028345721851924>",label="Cancel", custom_id="cancel_all_in", style=disnake.ButtonStyle.secondary)
            ]
            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])
        elif inter.component.custom_id == "confirm_all_in":
            bet_amount = money
            chosen_color = self.user_choices.get(user_id)
            if not chosen_color:
                return await inter.response.edit_message(content="An error occurred. Please start the game again.")

            random_color = secrets.choice(['black', 'red'])
            if chosen_color == random_color:
                winnings = bet_amount
                wins += 1
                if loan > 0:
                    repayment = min(int(winnings * 0.20), loan + loan_interest)
                    winnings -= repayment
                    if repayment >= loan:
                        loan_interest -= (repayment - loan)
                        loan = 0
                    else:
                        loan -= repayment
                money += winnings
                title = "🎉 ALL-IN WIN!"
                description = f"Congratulations! You've doubled your money to {money} WACA-Bucks!"
                if loan:
                    description += f"\n{repayment} WACA-Bucks were used to repay your loan and interest."
                color = disnake.Colour.green()
            else:
                losses += 1
                money = 0
                title = "💔 ALL-IN LOSS"
                description = "Oh no! You've lost all your WACA-Bucks."
                color = disnake.Colour.red()

            cursor.execute('''
                UPDATE gambling
                SET money = ?, loan = ?, loan_interest = ?, times_played = times_played + 1, wins = ?, losses = ?
                WHERE user_id = ? AND guild_id = ?
            ''', (money, loan, loan_interest, wins, losses, user_id, guild_id))
            conn.commit()

            embed = disnake.Embed(title=title, description=description, color=color)
            embed.set_author(name="WACA-Casino", icon_url="https://cdn.discordapp.com/emojis/1262085399938076762.webp?size=128&quality=lossless")
            embed.add_field(name="WACA-Bucks", value=f"{money}", inline=True)
            await inter.response.edit_message(embed=embed, components=[])

        elif inter.component.custom_id == "cancel_all_in":
            embed = disnake.Embed(title="All-In Cancelled", description="You've decided not to go all-in. Wise choice!", color=disnake.Color.blue())
            embed.set_author(name="WACA-Casino", icon_url="https://cdn.discordapp.com/emojis/1262085399938076762.webp?size=128&quality=lossless")
            embed.add_field(name="WACA-Bucks", value=f"{money}", inline=True)
            components = [
                disnake.ui.Button(emoji="<:Replay:1263030090917216276>",label="Play Again", custom_id="play_again", style=disnake.ButtonStyle.primary),
                disnake.ui.Button(emoji="<:whitex:1263028345721851924>",label="Quit", custom_id="quit_game", style=disnake.ButtonStyle.secondary)
            ]
            await inter.response.edit_message(embed=embed, components=[disnake.ui.ActionRow(*components)])
        elif "bet_" in inter.component.custom_id:
            bet_amount = int(inter.component.custom_id.split('_')[1])
            if bet_amount > money:
                return await inter.response.edit_message(content="You cannot bet more than you have.")

            # Retrieve the user's previous color choice
            chosen_color = self.user_choices.get(user_id)
            if not chosen_color:
                return await inter.response.edit_message(content="An error occurred. Please start the game again.")

            random_color = secrets.choice(['black', 'red'])
            title = "<:Report:1124146580442857502> ERROR"
            description = f"An unknown error has occured!"
            color = disnake.Colour.red()
            if chosen_color == random_color:
                winnings = bet_amount
                wins += 1
                if loan > 0:
                    # Deduct 20% of winnings towards loan repayment
                    repayment = min(int(winnings * 0.20), loan + loan_interest)
                    winnings -= repayment
                    if repayment >= loan:
                        loan_interest -= (repayment - loan)
                        loan = 0
                    else:
                        loan -= repayment
                money += winnings
                title = "You won!"
                if loan:
                    description = f"You now have {money} WACA-Bucks. {repayment} WACA-Bucks were used to repay your loan and interest."
                else:
                    description=f"You now have {money} WACA-Bucks."
                color = disnake.Colour.green()
            else:
                losses += 1
                money -= bet_amount
                title = "You lost!"
                description = f"You now have {money} WACA-Bucks."
                color = disnake.Colour.red()
             # Update database
            cursor.execute('''
                UPDATE gambling
                SET money = ?, loan = ?, loan_interest = ?, times_played = times_played + 1, wins = ?, losses = ?
                WHERE user_id = ? AND guild_id = ?
            ''', (money, loan, loan_interest, wins, losses, user_id, guild_id))
            conn.commit()

            embed = disnake.Embed(title=title, description=description, color=color)
            embed.set_author(name="WACA-Casino", icon_url="https://cdn.discordapp.com/emojis/1262085399938076762.webp?size=128&quality=lossless")
            embed.add_field(name="WACA-Bucks", value=f"{money}", inline=True)
            embed.add_field(name="Loan", value=f"{loan}", inline=True)
            embed.add_field(name="Interest", value=f"{loan_interest:.2f}", inline=True)
            await inter.response.edit_message(embed=embed, components=[])
        if inter.component.custom_id == "exchange_xp_confirm":
            print("triggered")
            modal = disnake.ui.Modal(
                title="Exchange XP",
                custom_id="exchange_xp_modal",
                components=[
                    disnake.ui.TextInput(
                        label="XP Amount",
                        custom_id="xp_amount",
                        style=disnake.TextInputStyle.short,
                        placeholder="Enter the amount of XP to exchange",
                        required=True
                    )
                ]
            )
            await inter.response.send_modal(modal)
        elif inter.component.custom_id == "exchange_xp_cancel":
            embed = disnake.Embed(
                title="XP Exchange Cancelled",
                description="You have cancelled the XP exchange.",
                color=disnake.Color.red()
            )
            await inter.response.edit_message(embed=embed, components=[])
        elif inter.component.custom_id == "pay_loan_modal":
            modal = disnake.ui.Modal(
                title="Pay Loan",
                custom_id="pay_loan_modal",
                components=[
                    disnake.ui.TextInput(
                        label="Payment Amount",
                        custom_id="payment_amount",
                        style=disnake.TextInputStyle.short,
                        placeholder="Enter the amount to pay towards your loan",
                        required=True
                    )
                ]
            )
            await inter.response.send_modal(modal)

    @commands.slash_command()
    async def bank(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        cursor.execute('SELECT money, loan, loan_interest FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user_data = cursor.fetchone()
        if user_data:
            money, loan, loan_interest = user_data
            total_debt = loan + loan_interest
            credit_score = await self.calculate_credit_score(user_id, guild_id)
        else:
            money, total_debt, credit_score = 0, 0, 0

        # Check if the user is eligible to pay
        is_eligible = await self.is_eligible_to_pay(user_id, user_id, guild_id, 1)  # We use 1 as a dummy amount

        embed = disnake.Embed(title="WACA-Bank", description="Welcome to WACA-Bank. What would you like to do?", color=disnake.Color.blue())
        embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
        embed.add_field(name="Current WACA-Bucks", value=f"{money:,}", inline=True)
        embed.add_field(name="Current Debt", value=f"{total_debt:,.2f}", inline=True)
        embed.add_field(name="Credit Score", value=f"{credit_score}", inline=True)
        embed.add_field(name="Eligible to Pay?", value="**Yes**" if is_eligible else "**No**", inline=True)
        
        components = [
            disnake.ui.Button(emoji="<:Credit:1263027887372636210>",label="Get a Loan", custom_id="bank_loan", style=disnake.ButtonStyle.primary),
            disnake.ui.Button(emoji="<:CurrencyExchange:1262116791539335311>",label="Exchange XP", custom_id="bank_exchange", style=disnake.ButtonStyle.primary),
            disnake.ui.Button(emoji="<:CreditCheck:1263027888186196050>",label="Pay Loan", custom_id="pay_loan_modal", style=disnake.ButtonStyle.success)
        ]

        await inter.response.send_message(embed=embed, components=[disnake.ui.ActionRow(*components)])
    @commands.slash_command()
    async def balance(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        cursor.execute('SELECT user_id, money FROM gambling WHERE guild_id = ? ORDER BY money DESC', (guild_id,))
        all_users = cursor.fetchall()
        user_position = next((i for i, (uid, _) in enumerate(all_users, 1) if uid == user_id), None)

        cursor.execute('SELECT money, times_played, wins, losses, loan FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user = cursor.fetchone()
        if user is None:
            return await inter.send("You need to run the /roulette command first.", ephemeral=True)

        money, times_played, wins, losses, loan = user

        embed = disnake.Embed(title="<:Payment:1262085400978128937> Your Balance", description=f"You have {money} WACA-Bucks.", color=disnake.Color.blue())
        embed.add_field(name="Position", value=f"{user_position}", inline=True)
        embed.add_field(name="Times Played", value=f"{times_played}", inline=True)
        embed.add_field(name="Wins", value=f"{wins}", inline=True)
        embed.add_field(name="Losses", value=f"{losses}", inline=True)
        embed.add_field(name="Loan", value=f"{loan}", inline=True)
        embed.set_footer(text=f"{inter.author.display_name}'s Balance", icon_url=inter.author.display_avatar.url)
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.slash_command()
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction, category: str = Param(
            choices=[
                "WACA-Bucks",
                "XP",
                "Debt"
            ]
        )):
        guild_id = inter.guild.id
        if category == "WACA-Bucks":
            cursor.execute('SELECT user_id, money, loan FROM gambling WHERE guild_id = ? ORDER BY (money - loan) DESC LIMIT 5', (guild_id,))
            top_users = cursor.fetchall()

            embed = disnake.Embed(title="Top 5 Players", description="Here are the top 5 players with the highest net worth (WACA-Bucks - Debt):", color=disnake.Color.gold())
            embed.set_author(name="WACA-Casino", icon_url="https://cdn.discordapp.com/emojis/1262085399938076762.webp?size=128&quality=lossless")
            for i, (user_id, money, loan) in enumerate(top_users, 1):
                user = await self.bot.fetch_user(user_id)
                net_worth = money - loan
                embed.add_field(name=f"{i}. {user.name}", value=f"Net Worth: {net_worth} WACA-Bucks", inline=False)

        elif category == "XP":
            levels_conn = sqlite3.connect('databases/levels.db')
            levels_cursor = levels_conn.cursor()
            levels_cursor.execute('SELECT user_id, xp FROM levels WHERE guild_id = ? ORDER BY xp DESC LIMIT 5', (guild_id,))
            top_users = levels_cursor.fetchall()
            levels_conn.close()

            embed = disnake.Embed(title="Top 5 Chatters", description="Here are the top 5 players with the most XP in this server:", color=disnake.Color.blue())
            embed.set_author(name="Server XP Leaderboard", icon_url="https://cdn.discordapp.com/emojis/1262149503381930065.webp?size=128&quality=lossless")
            for i, (user_id, xp) in enumerate(top_users, 1):
                user = await self.bot.fetch_user(user_id)
                embed.add_field(name=f"{i}. {user.name}", value=f"{xp} XP", inline=False)

        elif category == "Debt":
            cursor.execute('SELECT user_id, loan, loan_interest FROM gambling WHERE guild_id = ? ORDER BY (loan + loan_interest) DESC LIMIT 5', (guild_id,))
            top_debtors = cursor.fetchall()

            embed = disnake.Embed(title="Top 5 Debtors", description="Here are the top 5 players with the highest debt (Loan + Interest):", color=disnake.Color.red())
            embed.set_author(name="WACA-Casino Debt Leaderboard", icon_url="https://cdn.discordapp.com/emojis/1262085400978128937.webp?size=128&quality=lossless")
            for i, (user_id, loan, loan_interest) in enumerate(top_debtors, 1):
                user = await self.bot.fetch_user(user_id)
                total_debt = loan + loan_interest
                embed.add_field(name=f"{i}. {user.name}", value=f"Total Debt: {total_debt:.2f} WACA-Bucks", inline=False)

        else:
            embed = disnake.Embed(title="Invalid Category", description="Please choose a valid category: 'WACA-Bucks', 'XP', or 'Debt'.", color=disnake.Color.red())

        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.user_command(name="Check Balance")
    async def check_balance(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        user_id = user.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        # Check if user exists in database, if not, create a new record
        cursor.execute('SELECT * FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user_record = cursor.fetchone()
        if user_record is None:
            cursor.execute('INSERT INTO gambling (user_id, guild_id) VALUES (?, ?)', (user_id, guild_id))
            conn.commit()
            cursor.execute('SELECT * FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            user_record = cursor.fetchone()

        money, xp, times_played, loan, loan_interest, wins, losses = user_record[2:]

        embed = disnake.Embed(title="<:Payment:1262085400978128937> User Balance", description=f"{user.display_name} has {money} WACA-Bucks.", color=disnake.Color.blue())
        embed.add_field(name="Times Played", value=f"{times_played}", inline=True)
        embed.add_field(name="Wins", value=f"{wins}", inline=True)
        embed.add_field(name="Losses", value=f"{losses}", inline=True)
        embed.add_field(name="Loan", value=f"{loan}", inline=True)
        embed.add_field(name="Interest", value=f"{loan_interest:.2f}", inline=True)
        embed.set_footer(text=f"{user.display_name}'s Balance", icon_url=user.display_avatar.url)
        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.user_command(name="Check XP")
    async def check_xp(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        user_id = user.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        # Connect to the levels database
        levels_conn = sqlite3.connect('databases/levels.db')
        levels_cursor = levels_conn.cursor()

        # Check if user exists in levels database for the current guild, if not, create a new record
        levels_cursor.execute('SELECT * FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user_record = levels_cursor.fetchone()
        if user_record is None:
            levels_cursor.execute('INSERT INTO levels (user_id, guild_id, xp, level) VALUES (?, ?, 0, 1)', (user_id, guild_id))
            levels_conn.commit()
            levels_cursor.execute('SELECT * FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            user_record = levels_cursor.fetchone()

        xp, level = user_record[2:]

        embed = disnake.Embed(title="<:XP:1262149503381930065> User XP", description=f"{user.display_name} has {xp} XP.", color=disnake.Color.blue())
        embed.add_field(name="Level", value=f"{level}", inline=True)
        embed.set_footer(text=f"{user.display_name}'s XP", icon_url=user.display_avatar.url)
        await inter.response.send_message(embed=embed, ephemeral=True)
        levels_conn.close()
    @commands.slash_command(
        name='rps',
        description='Play Rock Paper Scissors and wager your WACA-Bucks'
    )
    async def rps(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        cursor.execute('SELECT money, loan FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user_money, user_loan = cursor.fetchone()

        embed = disnake.Embed(title="<:Cards:1262085399938076762> Rock Paper Scissors", description=f"💰 You have **{user_money}** WACA-Bucks.\n\nChoose your bet:", color=disnake.Color.blue())
        
        class BetView(disnake.ui.View):
            def __init__(self, user_money):
                super().__init__()
                self.bet = None
                self.user_money = user_money

            async def handle_bet(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction, bet_amount: int):
                if self.user_money >= bet_amount:
                    await interaction.response.defer()
                    self.bet = bet_amount
                    self.stop()
                else:
                    await interaction.response.send_message("❌ You don't have enough WACA-Bucks!", ephemeral=True)

            @disnake.ui.button(label="10 WACA-Bucks", style=disnake.ButtonStyle.grey, emoji="💵")
            async def bet_10(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                await self.handle_bet(button, interaction, 10)

            @disnake.ui.button(label="20 WACA-Bucks", style=disnake.ButtonStyle.grey, emoji="💸")
            async def bet_20(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                await self.handle_bet(button, interaction, 20)

            @disnake.ui.button(label="50 WACA-Bucks", style=disnake.ButtonStyle.grey, emoji="💰")
            async def bet_50(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                await self.handle_bet(button, interaction, 50)

            @disnake.ui.button(label="100 WACA-Bucks", style=disnake.ButtonStyle.grey, emoji="🏦")
            async def bet_100(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                await self.handle_bet(button, interaction, 100)

        bet_view = BetView(user_money)
        await inter.response.send_message(embed=embed, view=bet_view)

        await bet_view.wait()

        if bet_view.bet is None:
            await inter.edit_original_message(content="❌ You didn't place a bet. The game has been cancelled.", embed=None, view=None)
            return

        bet = bet_view.bet

        embed = disnake.Embed(title="<:Cards:1262085399938076762> Rock Paper Scissors", description=f"💰 Bet: **{bet}** WACA-Bucks\n\nChoose your move:", color=disnake.Color.blue())
        
        class RPSView(disnake.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None

            @disnake.ui.button(label="Rock", style=disnake.ButtonStyle.grey, emoji="🪨")
            async def rock(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                self.value = "rock"
                self.stop()

            @disnake.ui.button(label="Paper", style=disnake.ButtonStyle.grey, emoji="📄")
            async def paper(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                self.value = "paper"
                self.stop()

            @disnake.ui.button(label="Scissors", style=disnake.ButtonStyle.grey, emoji="✂️")
            async def scissors(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                self.value = "scissors"
                self.stop()

        view = RPSView()
        await inter.edit_original_message(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            await inter.edit_original_message(content="❌ You didn't make a choice. The game has been cancelled.", embed=None, view=None)
            return

        bot_choice = secrets.choice(["rock", "paper", "scissors"])
        user_choice = view.value

        result_embed = disnake.Embed(title="<:Payment:1262085400978128937> Rock Paper Scissors Result", color=disnake.Color.blue())
        result_embed.add_field(name="Your Choice", value=f"{self.get_emoji(user_choice)} {user_choice.capitalize()}", inline=True)
        result_embed.add_field(name="Bot's Choice", value=f"{self.get_emoji(bot_choice)} {bot_choice.capitalize()}", inline=True)

        if user_choice == bot_choice:
            result = "🤝 It's a tie!"
            color = disnake.Color.yellow()
        elif (
            (user_choice == "rock" and bot_choice == "scissors") or
            (user_choice == "paper" and bot_choice == "rock") or
            (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = f"🎉 You win! You gained **{bet}** WACA-Bucks."
            color = disnake.Color.green()
            if user_loan > 0:
                loan_payment = min(bet * 0.2, user_loan)
                new_loan = user_loan - loan_payment
                new_money = user_money + bet - loan_payment
                cursor.execute('UPDATE gambling SET money = ?, loan = ?, wins = wins + 1, times_played = times_played + 1 WHERE user_id = ? AND guild_id = ?', (new_money, new_loan, user_id, guild_id))
                result += f"\n\n💼 20% of your earnings (**{loan_payment:.2f}** WACA-Bucks) was used to pay off your loan. Remaining loan: **{new_loan:.2f}** WACA-Bucks."
            else:
                cursor.execute('UPDATE gambling SET money = money + ?, wins = wins + 1, times_played = times_played + 1 WHERE user_id = ? AND guild_id = ?', (bet, user_id, guild_id))
        else:
            result = f"😔 You lose! You lost **{bet}** WACA-Bucks."
            color = disnake.Color.red()
            cursor.execute('UPDATE gambling SET money = money - ?, losses = losses + 1, times_played = times_played + 1 WHERE user_id = ? AND guild_id = ?', (bet, user_id, guild_id))

        conn.commit()

        result_embed.description = result
        result_embed.color = color

        await inter.edit_original_message(embed=result_embed, view=None)

    def get_emoji(self, choice):
        if choice == "rock":
            return "🪨"
        elif choice == "paper":
            return "📄"
        else:
            return "✂️"

    async def calculate_credit_score(self, user_id: int, guild_id: int):
        cursor.execute('SELECT loan, loan_interest, payment_history FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        result = cursor.fetchone()
        if not result:
            return 0

        loan, loan_interest, payment_history = result
        payment_history = json.loads(payment_history)

        if not payment_history:
            return 500  # Base score for new users

        total_payments = sum(payment for payment, _ in payment_history)
        on_time_payments = sum(1 for _, on_time in payment_history if on_time)
        payment_ratio = on_time_payments / len(payment_history)

        current_debt = loan + loan_interest
        debt_ratio = current_debt / (total_payments + 1)  # Add 1 to avoid division by zero

        credit_score = int(700 * payment_ratio - 100 * debt_ratio)
        return max(300, min(850, credit_score))  # Clamp score between 300 and 850

    async def is_eligible_to_pay(self, payer_id: int, recipient_id: int, guild_id: int, amount: int) -> bool:
        payer_score = await self.calculate_credit_score(payer_id, guild_id)
        
        cursor.execute('SELECT money, loan, loan_interest FROM gambling WHERE user_id = ? AND guild_id = ?', (payer_id, guild_id))
        payer_data = cursor.fetchone()
        
        if not payer_data:
            return False
        
        payer_money, payer_loan, payer_loan_interest = payer_data
        payer_debt = payer_loan + payer_loan_interest
        
        # Check if payer has enough money
        if payer_money < amount:
            return False
        
        # If payer has no debt, they're always eligible
        if payer_debt == 0:
            return True
        
        # Calculate debt-to-income ratio
        debt_to_income = payer_debt / (payer_money + 1)  # Add 1 to avoid division by zero
        
        # Define more forgiving eligibility criteria
        if payer_score >= 700 and debt_to_income <= 0.8:
            return True
        elif payer_score >= 600 and debt_to_income <= 0.6:
            return True
        elif payer_score >= 500 and debt_to_income <= 0.4:
            return True
        elif payer_score >= 400 and debt_to_income <= 0.2:
            return True
        else:
            return False

    @commands.slash_command(name="pay", description="Pay another user")
    async def pay_user(self, inter: disnake.ApplicationCommandInteraction, recipient: disnake.User, amount: int):
        payer_id = inter.author.id
        recipient_id = recipient.id
        guild_id = inter.guild.id

        if amount <= 0:
            embed = await statbed.create_error_embed(
                title="Invalid Amount",
                description="The amount must be positive.",
                footer="Payment Error"
            )
            return await inter.response.send_message(embed=embed, ephemeral=True)

        if payer_id == recipient_id:
            embed = await statbed.create_error_embed(
                title="Invalid Recipient",
                description="You can't pay yourself.",
                footer="Payment Error"
            )
            return await inter.response.send_message(embed=embed, ephemeral=True)

        await self.ensure_user_exists(payer_id, guild_id)
        await self.ensure_user_exists(recipient_id, guild_id)

        if await self.is_eligible_to_pay(payer_id, recipient_id, guild_id, amount):
            cursor.execute('UPDATE gambling SET money = money - ? WHERE user_id = ? AND guild_id = ?', (amount, payer_id, guild_id))
            cursor.execute('UPDATE gambling SET money = money + ? WHERE user_id = ? AND guild_id = ?', (amount, recipient_id, guild_id))
            conn.commit()

            embed = disnake.Embed(
                title="Payment Successful",
                description=f"You have successfully paid {amount} WACA-Bucks to {recipient.display_name}.",
                color=disnake.Color.green()
            )
            await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                title="Payment Failed",
                description="You are not eligible to make this payment. This could be due to insufficient funds, a low credit score, or a high debt-to-income ratio.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="credit_score", description="Check your credit score")
    async def credit_score(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        credit_score = await self.calculate_credit_score(user_id, guild_id)

        embed = disnake.Embed(
            title="Credit Score",
            description=f"Your current credit score is: **{credit_score}**",
            color=disnake.Color.blue()
        )
        embed.set_footer(text="Credit scores range from 300 to 850. Higher is better!")
        await inter.response.send_message(embed=embed)