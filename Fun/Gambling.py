import disnake
from disnake.ext import commands, tasks
import sqlite3
import random
import os
from disnake.ext.commands import Param

# Connect to (or create) the SQLite database in the databases folder
conn = sqlite3.connect(os.path.join('databases', 'gambling.db'))
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS gambling (
    user_id INTEGER,
    guild_id INTEGER,
    money INTEGER NOT NULL DEFAULT 100,
    xp INTEGER NOT NULL DEFAULT 0,
    times_played INTEGER NOT NULL DEFAULT 0,
    loan INTEGER NOT NULL DEFAULT 0,
    loan_interest REAL NOT NULL DEFAULT 0,
    wins INTEGER NOT NULL DEFAULT 0,
    losses INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, guild_id)
)
''')
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
        embed.add_field(name="Loan", value=f"{loan}", inline=True)
        embed.add_field(name="Interest", value=f"{loan_interest:.2f}", inline=True)
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
        levels_conn = sqlite3.connect('databases/levels.db')
        levels_cursor = levels_conn.cursor()

        # Fetch user XP and level from levels database
        levels_cursor.execute('SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        result = levels_cursor.fetchone()

        if result:
            user_xp, user_level = result
            embed = disnake.Embed(
                title="Exchange XP for WACA-Bucks",
                description=f"You currently have {user_xp} XP. The exchange rate is 10 XP for 1 WACA-Buck.",
                color=disnake.Color.blue()
            )
            embed.set_author(name="WACA-Bank Currency Exchange", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262126386060198079/CExchange.png?ex=6695764b&is=669424cb&hm=bc2167697ad828f04fe0265c93fb5fa1c20f5f390eac7a53712d02e4f16d7f63&")
            embed.add_field(name="Current XP", value=f"{user_xp}", inline=True)
            embed.add_field(name="Exchange Rate", value="10 XP = 1 WACA-Buck", inline=True)
            components = [
                disnake.ui.Button(label="Exchange", custom_id="exchange_xp_confirm", style=disnake.ButtonStyle.success),
                disnake.ui.Button(label="Cancel", custom_id="exchange_xp_cancel", style=disnake.ButtonStyle.danger)
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

    @commands.slash_command()
    async def loan(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        # Create the loan confirmation embed
        embed = disnake.Embed(title="Loan Confirmation", description="Are you sure you would like a loan?",color=0xffa500)
        embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
        
        embed.add_field(name="Loan Amount", value="100 WACA-Bucks", inline=False)
        embed.add_field(name="Interest Rate", value="20%", inline=False)
        embed.set_footer(text=f"{inter.author.display_name}'s Session", icon_url=inter.author.display_avatar.url)

        components = [
            disnake.ui.Button(label="Yes", custom_id="loan_yes",style=disnake.ButtonStyle.success),
            disnake.ui.Button(label="No", custom_id="loan_no",style=disnake.ButtonStyle.danger)
        ]

        await inter.response.send_message(embed=embed, components=[disnake.ui.ActionRow(*components)])

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ['loan_yes', 'loan_no', 'black', 'red', 'bet_10', 'bet_20', 'bet_50', 'bet_100', 'rps_wager_10', 'rps_wager_20', 'rps_wager_50', 'rps_wager_100', 'rps_rock', 'rps_paper', 'rps_scissors']:
            return

        user_id = inter.author.id
        guild_id = inter.guild.id

        await self.ensure_user_exists(user_id, guild_id)

        cursor.execute('SELECT money, loan, loan_interest, wins, losses FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        user = cursor.fetchone()
        if user is None:
            return await inter.send("You need to run the /roulette command first.", ephemeral=True)

        money, loan, loan_interest, wins, losses = user

        if inter.component.custom_id == 'loan_yes':
            # Give a loan of 100 WACA-Bucks
            cursor.execute('UPDATE gambling SET money = money + 100, loan = loan + 100 WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            conn.commit()

            # Fetch updated user data
            cursor.execute('SELECT money, loan, loan_interest FROM gambling WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            money, loan, loan_interest = cursor.fetchone()

            embed = disnake.Embed(title="Loan Granted", description="You have received a loan.", color = disnake.Colour.green())
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
        
            embed.add_field(name="New WACA-Bucks Amount", value=f"{money}", inline=False)
            embed.add_field(name="Loan", value=f"{loan}", inline=True)
            embed.add_field(name="Interest", value=f"{loan_interest:.2f}", inline=True)
            await inter.response.edit_message(embed=embed, components=[])

        elif inter.component.custom_id == 'loan_no':
            embed = disnake.Embed(title="Loan Canceled", description="You have canceled the loan request.", color = disnake.Colour.red())
            embed.set_author(name="WACA-Bank", icon_url="https://cdn.discordapp.com/attachments/1262100698204471408/1262128295865221170/AccountBalance.png?ex=66957812&is=66942692&hm=717439a90dd6f7275332146a19e2b119a1299a1cf090aba7c58254275036d060&")
        
            await inter.response.edit_message(embed=embed, components=[])

        elif inter.component.custom_id in ['black', 'red']:
            # Store the user's color choice
            self.user_choices[user_id] = inter.component.custom_id
            embed = disnake.Embed(title="Choose your bet", description=f"You have {money} WACA-Bucks.", color=disnake.Color.blue())
            embed.set_author(name="WACA-Casino", icon_url="https://cdn.discordapp.com/emojis/1262085399938076762.webp?size=128&quality=lossless")
            components = [
                disnake.ui.Button(label="10 WACA-Bucks", custom_id="bet_10",style=disnake.ButtonStyle.primary, emoji="💵"),
                disnake.ui.Button(label="20 WACA-Bucks", custom_id="bet_20",style=disnake.ButtonStyle.primary, emoji="💸"),
                disnake.ui.Button(label="50 WACA-Bucks", custom_id="bet_50",style=disnake.ButtonStyle.primary, emoji="💰"),
                disnake.ui.Button(label="100 WACA-Bucks", custom_id="bet_100",style=disnake.ButtonStyle.primary, emoji="🏦")
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

            random_color = random.choice(['black', 'red'])
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
                "XP"
            ]
        )):
        guild_id = inter.guild.id
        if category == "WACA-Bucks":
            cursor.execute('SELECT user_id, money FROM gambling WHERE guild_id = ? ORDER BY money DESC LIMIT 5', (guild_id,))
            top_users = cursor.fetchall()

            embed = disnake.Embed(title="Top 5 Players", description="Here are the top 5 players with the most WACA-Bucks:", color=disnake.Color.gold())
            embed.set_author(name="WACA-Casino", icon_url="https://cdn.discordapp.com/emojis/1262085399938076762.webp?size=128&quality=lossless")
            for i, (user_id, money) in enumerate(top_users, 1):
                user = await self.bot.fetch_user(user_id)
                embed.add_field(name=f"{i}. {user.name}", value=f"{money} WACA-Bucks", inline=False)

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

        else:
            embed = disnake.Embed(title="Invalid Category", description="Please choose a valid category: 'WACA-Bucks' or 'XP'.", color=disnake.Color.red())

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

        bot_choice = random.choice(["rock", "paper", "scissors"])
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