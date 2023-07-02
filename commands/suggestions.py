import disnake
from disnake import Embed, ButtonStyle, TextInputStyle
from disnake.ext import commands
from disnake.ui import View, Button, Select
import sqlite3
from datetime import datetime

# Create a database connection
conn = sqlite3.connect('suggestions.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suggestion TEXT,
        status TEXT,
        upvotes INTEGER,
        downvotes INTEGER,
        upvoters TEXT,
        downvoters TEXT,
        reason TEXT,
        message_id INTEGER
    )
''')
conn.commit()
class AcceptModal(disnake.ui.Modal):
    
    def __init__(self,message_id,suggestion_id,bot: commands.Bot):
        self.message_id = message_id
        self.suggestion_id = suggestion_id
        self.bot = bot
        title = "Accept Suggestion",
        custom_id="acceptModal",
        components = [
            
            disnake.ui.TextInput(
                label="Reason",
                
                custom_id=f"reason",
                style=TextInputStyle.short,
                required=True,\
                max_length=500,),
            
            ]

        
        super().__init__(title="Accept Suggestion",custom_id="acceptModal",components=components)
    async def callback(self, inter: disnake.ApplicationCommandInteraction):
        # Get the suggestion message
        
        suggestion_message = await inter.channel.fetch_message(self.message_id)
        
        bot = self.bot
        global ava
        print(inter.text_values.items())
        dic=inter.text_values
        reason=dic["reason"]
        print("Sending embed")
        upvote_button = Button(style=disnake.ButtonStyle.green, emoji="👍", custom_id=f"suggUpvote_{self.suggestion_id}")
        downvote_button = Button(style=disnake.ButtonStyle.red, emoji="👎", custom_id=f"suggDownvote_{self.suggestion_id}")
        more_button = Button(style=disnake.ButtonStyle.gray, emoji="<:menu:1124096544606531635>", custom_id=f"suggMore_{self.suggestion_id}")
        # Disable the upvote and downvote buttons
        upvote_button.disabled = True
        downvote_button.disabled = True

        print("Editing message")
        embed = suggestion_message.embeds[0]
        embed.color = 65280  # Green color
        embed.title = f"Suggestion #{self.suggestion_id} Accepted!"
        ##############
        reason_index = None
        for index, field in enumerate(embed.fields):
            if field.name == "Reason":
                reason_index = index
                break
        if reason_index is not None:
            # Update the value of the "Reason" field
            embed.set_field_at(reason_index, name="Reason", value=reason, inline=False)
        else:
            # Add a new field if "Reason" field is not found
            embed.add_field(name="Reason", value=reason, inline=False)

        #######################

        userIndex = None
        for index, field in enumerate(embed.fields):
            if field.name == "Accepted By" or field.name == "Denied By" or field.name == "Reopened By":
                userIndex = index
                break
        if userIndex is not None:
            # Update the value of the "Reason" field
            embed.set_field_at(userIndex, name="Accepted By", value=f"{inter.author.display_name}", inline=False)
        else:
            # Add a new field if "Reason" field is not found
            embed.add_field(name="Accepted By", value=f"{inter.author.display_name}", inline=False)
            
        await suggestion_message.edit(embed=embed, components=[upvote_button,downvote_button,more_button])
        await inter.response.edit_message("Suggestion Accepted!")










class DenyModal(disnake.ui.Modal):
    
    def __init__(self,message_id,suggestion_id,bot: commands.Bot):
        self.message_id = message_id
        self.suggestion_id = suggestion_id
        self.bot = bot
        title = "Deny Suggestion",
        custom_id="denyModal",
        components = [
            
            disnake.ui.TextInput(
                label="Reason",
                
                custom_id=f"reason",
                style=TextInputStyle.short,
                required=True,\
                max_length=500,),
            
            ]

        
        super().__init__(title="Deny Suggestion",custom_id="denyModal",components=components)
    async def callback(self, inter: disnake.ApplicationCommandInteraction):
        # Get the suggestion message
        
        suggestion_message = await inter.channel.fetch_message(self.message_id)
        
        bot = self.bot
        global ava
        print(inter.text_values.items())
        dic=inter.text_values
        reason=dic["reason"]
        print("Sending embed")
        upvote_button = Button(style=disnake.ButtonStyle.green, emoji="👍", custom_id=f"suggUpvote_{self.suggestion_id}")
        downvote_button = Button(style=disnake.ButtonStyle.red, emoji="👎", custom_id=f"suggDownvote_{self.suggestion_id}")
        more_button = Button(style=disnake.ButtonStyle.gray, label="More", custom_id=f"suggMore_{self.suggestion_id}")
        # Disable the upvote and downvote buttons
        upvote_button.disabled = True
        downvote_button.disabled = True

        print("Editing message")
        embed = suggestion_message.embeds[0]
        embed.color = disnake.Color.red()  # Red color
        embed.title = f"Suggestion #{self.suggestion_id} Denied!"
        ##############
        reason_index = None
        for index, field in enumerate(embed.fields):
            if field.name == "Reason":
                reason_index = index
                break
        if reason_index is not None:
            # Update the value of the "Reason" field
            embed.set_field_at(reason_index, name="Reason", value=reason, inline=False)
        else:
            # Add a new field if "Reason" field is not found
            embed.add_field(name="Reason", value=reason, inline=False)

        #######################

        userIndex = None
        for index, field in enumerate(embed.fields):
            if field.name == "Accepted By" or field.name == "Denied By" or field.name == "Reopened By":
                userIndex = index
                break
        if userIndex is not None:
            # Update the value of the "Reason" field
            embed.set_field_at(userIndex, name="Denied By", value=f"{inter.author.display_name}", inline=False)
        else:
            # Add a new field if "Reason" field is not found
            embed.add_field(name="Denied By", value=f"{inter.author.display_name}", inline=False)
            
        await suggestion_message.edit(embed=embed, components=[upvote_button,downvote_button,more_button])
        await inter.response.edit_message("Suggestion Denied!")













class OpenModal(disnake.ui.Modal):
    
    def __init__(self,message_id,suggestion_id,bot: commands.Bot):
        self.message_id = message_id
        self.suggestion_id = suggestion_id
        self.bot = bot
        title = "Reopen Suggestion",
        custom_id="opemModal",
        components = [
            
            disnake.ui.TextInput(
                label="Reason",
                
                custom_id=f"reason",
                style=TextInputStyle.short,
                required=True,\
                max_length=500,),
            
            ]

        
        super().__init__(title="Reopen Suggestion",custom_id="opemModal",components=components)
    async def callback(self, inter: disnake.ApplicationCommandInteraction):
        # Get the suggestion message
        
        suggestion_message = await inter.channel.fetch_message(self.message_id)
        
        bot = self.bot
        global ava
        print(inter.text_values.items())
        dic=inter.text_values
        reason=dic["reason"]
        print("Sending embed")
        upvote_button = Button(style=disnake.ButtonStyle.green, emoji="👍", custom_id=f"suggUpvote_{self.suggestion_id}")
        downvote_button = Button(style=disnake.ButtonStyle.red, emoji="👎", custom_id=f"suggDownvote_{self.suggestion_id}")
        more_button = Button(style=disnake.ButtonStyle.gray, label="More", custom_id=f"suggMore_{self.suggestion_id}")
        # Disable the upvote and downvote buttons
        upvote_button.disabled = False
        downvote_button.disabled = False

        print("Editing message")
        embed = suggestion_message.embeds[0]
        embed.color = 3106815  # Red color
        embed.title = f"Pending Suggestion #{self.suggestion_id}"
        ##############
        reason_index = None
        for index, field in enumerate(embed.fields):
            if field.name == "Reason":
                reason_index = index
                break
        if reason_index is not None:
            # Update the value of the "Reason" field
            embed.set_field_at(reason_index, name="Reason", value=reason, inline=False)
        else:
            # Add a new field if "Reason" field is not found
            embed.add_field(name="Reason", value=reason, inline=False)

        #######################

        userIndex = None
        for index, field in enumerate(embed.fields):
            if field.name == "Accepted By" or field.name == "Denied By" or field.name == "Reopened By":
                userIndex = index
                break
        if userIndex is not None:
            # Update the value of the "Reason" field
            embed.set_field_at(userIndex, name="Reopened By", value=f"{inter.author.display_name}", inline=False)
        else:
            # Add a new field if "Reason" field is not found
            embed.add_field(name="Reopened By", value=f"{inter.author.display_name}", inline=False)
            
        await suggestion_message.edit(embed=embed, components=[upvote_button,downvote_button,more_button])
        await inter.response.edit_message("Suggestion Reopened!")











        
        
class MoreOptions(View):
    def __init__(self, suggestion_id):
        super().__init__()
        self.suggestion_id = suggestion_id
        
        self.accept_button = Button(style=ButtonStyle.green, label="Accept", custom_id=f"suggAccept_{suggestion_id}")
        self.deny_button = Button(style=ButtonStyle.red, label="Deny", custom_id=f"suggDeny_{suggestion_id}")
        self.open_button = Button(style=ButtonStyle.gray, label="Open", custom_id=f"suggOpen_{suggestion_id}")
        self.view_button = Button(style=disnake.ButtonStyle.gray, label="View Votes", custom_id=f"suggView_{suggestion_id}")
        
        self.add_item(self.accept_button)
        self.add_item(self.deny_button)
        self.add_item(self.open_button)
        self.add_item(self.view_button)
        
# Cog class for suggestions
class Suggestions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # Slash command to suggest something
    @commands.slash_command(
        name='suggest',
        description='Suggest something',
        options=[
            disnake.Option(
                type=disnake.OptionType.string,
                name='suggestion',
                description='Your suggestion',
                required=True
            )
        ]
    )
    async def suggest(self, inter: disnake.ApplicationCommandInteraction, suggestion: str):
        await inter.response.defer(with_message=True, ephemeral=True)
        
        cursor.execute("INSERT INTO suggestions (suggestion, upvotes, downvotes) VALUES (?, 0, 0)", (suggestion,))
        suggestion_id = cursor.lastrowid
        conn.commit()
        
        embed = disnake.Embed(
            title=f"Pending Suggestion #{suggestion_id}:",
            color=3106815,
            timestamp=datetime.now(),
            description=suggestion
        )
        
        embed.add_field(name="Likes", value=0, inline=True)
        embed.add_field(name="Dislikes", value=0, inline=True)
        embed.set_thumbnail(inter.author.display_avatar)
        embed.set_footer(
            text=f"Sent by {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )
        
        upvote_button = Button(style=disnake.ButtonStyle.green, emoji="👍", custom_id=f"suggUpvote_{suggestion_id}")
        downvote_button = Button(style=disnake.ButtonStyle.red, emoji="👎", custom_id=f"suggDownvote_{suggestion_id}")
        more_button = Button(style=disnake.ButtonStyle.gray, label="More", custom_id=f"suggMore_{suggestion_id}")
        channel = None
        
        for guild_channel in inter.guild.channels:
            if guild_channel.name.endswith("suggestions"):
                channel = guild_channel
                break
        
        
        if channel:
            message = await channel.send(embed=embed, components=[[upvote_button, downvote_button, more_button]])
            suggestion_message_id = message.id
            
            cursor.execute("UPDATE suggestions SET message_id = ? WHERE id = ?", (suggestion_message_id, suggestion_id))
            conn.commit()
            
            await inter.edit_original_response(content="Suggestion Sent!")
        else:
            await inter.edit_original_response(content="I don't see a suggestions channel...")

    
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id
        if custom_id.startswith("suggMore"):
            suggestion_id = int(custom_id.split("_")[1])
            more_options = MoreOptions(suggestion_id)
            await inter.response.send_message("More options:", view=more_options, ephemeral=True)
            
        elif custom_id.startswith("suggAccept"):
            if disnake.utils.get(inter.author.roles, name="Server Owner") or disnake.utils.get(inter.author.roles, name="Owner"):
                suggestion_id = int(custom_id.split("_")[1])

                # Update the suggestion status to "Accepted" in the database
                cursor.execute("UPDATE suggestions SET status = 'Accepted' WHERE id = ?", (suggestion_id,))
                conn.commit()

                # Get the suggestion message ID from the database
                cursor.execute("SELECT message_id FROM suggestions WHERE id = ?", (suggestion_id,))
                result = cursor.fetchone()
                if not result:
                    await inter.response.send_message("The suggestion message does not exist.", ephemeral=True)
                    return

                suggestion_message_id = result[0]
    
                # Show a modal to enter the acceptance reason
                await inter.response.send_modal(AcceptModal(suggestion_message_id,suggestion_id,self.bot))
            else:
                await inter.response.edit_message("Only Server Owners do that!")
        
        elif custom_id.startswith("suggDeny"):
            if disnake.utils.get(inter.author.roles, name="Server Owner") or disnake.utils.get(inter.author.roles, name="Owner"):
                suggestion_id = int(custom_id.split("_")[1])

                # Update the suggestion status to "Accepted" in the database
                cursor.execute("UPDATE suggestions SET status = 'Accepted' WHERE id = ?", (suggestion_id,))
                conn.commit()

                # Get the suggestion message ID from the database
                cursor.execute("SELECT message_id FROM suggestions WHERE id = ?", (suggestion_id,))
                result = cursor.fetchone()
                if not result:
                    await inter.response.send_message("The suggestion message does not exist.", ephemeral=True)
                    return

                suggestion_message_id = result[0]

            
                # Show a modal to enter the acceptance reason
                await inter.response.send_modal(DenyModal(suggestion_message_id,suggestion_id,self.bot))
            else:
                await inter.response.edit_message("Only Server Owners do that!")
        elif custom_id.startswith("suggOpen"):
            if disnake.utils.get(inter.author.roles, name="Server Owner") or disnake.utils.get(inter.author.roles, name="Owner"):
                suggestion_id = int(custom_id.split("_")[1])

                # Update the suggestion status to "Accepted" in the database
                cursor.execute("UPDATE suggestions SET status = 'Accepted' WHERE id = ?", (suggestion_id,))
                conn.commit()

                # Get the suggestion message ID from the database
                cursor.execute("SELECT message_id FROM suggestions WHERE id = ?", (suggestion_id,))
                result = cursor.fetchone()
                if not result:
                    await inter.response.send_message("The suggestion message does not exist.", ephemeral=True)
                    return

                suggestion_message_id = result[0]

            
                # Show a modal to enter the acceptance reason
                await inter.response.send_modal(OpenModal(suggestion_message_id,suggestion_id,self.bot))
            else:
                await inter.response.edit_message("Only Server Owners do that!")
######################################
        if custom_id.startswith("suggView"):
            suggestion_id = int(custom_id.split("_")[1])
            
            # Fetch the upvoters and downvoters from the database
            cursor.execute("SELECT upvoters, downvoters FROM suggestions WHERE id = ?", (suggestion_id,))
            result = cursor.fetchone()
            
            if result:
                upvoters = result[0] or ""
                downvoters = result[1] or ""
                
                # Create a list of users who upvoted the suggestion
                upvoter_list = []
                for upvoter_id in upvoters.split(","):
                    if upvoter_id:
                        try:
                            user = await self.bot.fetch_user(int(upvoter_id))
                            upvoter_list.append(user.display_name)
                        except disnake.NotFound:
                            upvoter_list.append(f"User ID: {upvoter_id} (Left Server)")
                
                # Create a list of users who downvoted the suggestion
                downvoter_list = []
                for downvoter_id in downvoters.split(","):
                    if downvoter_id:
                        try:
                            user = await self.bot.fetch_user(int(downvoter_id))
                            downvoter_list.append(user.display_name)
                        except disnake.NotFound:
                            downvoter_list.append(f"User ID: {downvoter_id} (Left Server)")
                
                # Create an embed to display the upvoters and downvoters
                embed = disnake.Embed(
                    title="Votes",
                    color=4143049,
                    timestamp=datetime.now()
                )
                embed.add_field(name="Upvoters", value=", ".join(upvoter_list) if upvoter_list else "No upvotes", inline=False)
                embed.add_field(name="Downvoters", value=", ".join(downvoter_list) if downvoter_list else "No downvotes", inline=False)
                
                # Send a new ephemeral message with the upvoters and downvoters
                await inter.response.send_message(embed=embed, ephemeral=True)
       ############################################### 
        if custom_id.startswith("suggUpvote"):
            suggestion_id = int(custom_id.split("_")[1])
            user_id = str(inter.author.id)

            # Check if the user has already upvoted or downvoted
            cursor.execute("SELECT upvoters, downvoters FROM suggestions WHERE id = ?", (suggestion_id,))
            result = cursor.fetchall()

            if result:
                upvoters = result[0][0].split(",") if result[0][0] else []
                downvoters = result[0][1].split(",") if result[0][1] else []

                if user_id in upvoters:
                    await inter.response.send_message("You may only vote once!", ephemeral=True)
                    return  # User has already upvoted, do nothing

                if user_id in downvoters:
                    # Switch from downvote to upvote
                    downvoters.remove(user_id)
                    upvoters.append(user_id)
                else:
                    upvoters.append(user_id)

                # Update the upvoters and downvoters lists in the database
                cursor.execute("UPDATE suggestions SET upvoters = ?, downvoters = ? WHERE id = ?",
                               (",".join(upvoters), ",".join(downvoters), suggestion_id))
                conn.commit()

                # Update the suggestion's embed with the new number of likes and dislikes
                upvotes = len(upvoters)
                downvotes = len(downvoters)

                embed = inter.message.embeds[0]
                embed.set_field_at(0, name="Likes", value=upvotes, inline=True)
                embed.set_field_at(1, name="Dislikes", value=downvotes, inline=True)

                await inter.response.edit_message(embed=embed)

            return

        elif custom_id.startswith("suggDownvote"):
            suggestion_id = int(custom_id.split("_")[1])
            user_id = str(inter.author.id)

            # Check if the user has already downvoted or upvoted
            cursor.execute("SELECT upvoters, downvoters FROM suggestions WHERE id = ?", (suggestion_id,))
            result = cursor.fetchall()

            if result:
                upvoters = result[0][0].split(",") if result[0][0] else []
                downvoters = result[0][1].split(",") if result[0][1] else []

                if user_id in downvoters:
                    await inter.response.send_message("You may only vote once!", ephemeral=True)
                    return  # User has already downvoted, do nothing

                if user_id in upvoters:
                    # Switch from upvote to downvote
                    upvoters.remove(user_id)
                    downvoters.append(user_id)
                else:
                    downvoters.append(user_id)

                # Update the upvoters and downvoters lists in the database
                cursor.execute("UPDATE suggestions SET upvoters = ?, downvoters = ? WHERE id = ?",
                               (",".join(upvoters), ",".join(downvoters), suggestion_id))
                conn.commit()

                # Update the suggestion's embed with the new number of likes and dislikes
                upvotes = len(upvoters)
                downvotes = len(downvoters)

                embed = inter.message.embeds[0]
                embed.set_field_at(0, name="Likes", value=upvotes, inline=True)
                embed.set_field_at(1, name="Dislikes", value=downvotes, inline=True)

                await inter.response.edit_message(embed=embed)

            return




def setup(bot: commands.Bot) -> None:
    bot.add_cog(Suggestions(bot))
