import disnake
from disnake.ext import commands
from disnake.ui import Button
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
            title=f"Server Suggestion #{suggestion_id}:",
            color=4143049,
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
        view_button = Button(style=disnake.ButtonStyle.gray, label="View Votes", custom_id=f"suggView_{suggestion_id}")
        
        channel = None
        
        for guild_channel in inter.guild.channels:
            if guild_channel.name.endswith("suggestions"):
                channel = guild_channel
                break
        
        
        if channel:
            message = await channel.send(embed=embed, components=[[upvote_button, downvote_button, view_button]])
            suggestion_message_id = message.id
            
            cursor.execute("UPDATE suggestions SET message_id = ? WHERE id = ?", (suggestion_message_id, suggestion_id))
            conn.commit()
            
            await inter.edit_original_response(content="Suggestion Sent!")
        else:
            await inter.edit_original_response(content="I don't see a suggestions channel...")

    
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id
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
            
            # Check if the user has already upvoted
            cursor.execute("SELECT upvoters FROM suggestions WHERE id = ?", (suggestion_id,))
            result = cursor.fetchone()
            
            if result:
                upvoters = result[0] or ""
                if user_id in upvoters:
                    await inter.response.send_message("You may only vote once!", ephemeral=True)
                    return  # User has already upvoted, do nothing
                
                # Check if the user has already downvoted
                cursor.execute("SELECT downvoters FROM suggestions WHERE id = ?", (suggestion_id,))
                result = cursor.fetchone()
                
                if result:
                    downvoters = result[0] or ""
                    if user_id in downvoters:
                        # Switch from downvote to upvote
                        downvoters = downvoters.replace(user_id, "")
                        cursor.execute("UPDATE suggestions SET downvoters = ? WHERE id = ?", (downvoters, suggestion_id))
                        cursor.execute("UPDATE suggestions SET upvoters = upvoters || ? WHERE id = ?", (f",{user_id}", suggestion_id))
                        cursor.execute("UPDATE suggestions SET upvotes = upvotes + 1, downvotes = downvotes - 1 WHERE id = ?", (suggestion_id,))
                        conn.commit()
                        
                        # Fetch the updated suggestion from the database
                        cursor.execute("SELECT upvotes, downvotes FROM suggestions WHERE id = ?", (suggestion_id,))
                        result = cursor.fetchone()
                        
                        if result:
                            upvotes = result[0]
                            downvotes = result[1]
                            
                            # Update the suggestion's embed with the new number of likes and dislikes
                            embed = inter.message.embeds[0]
                            embed.set_field_at(0, name="Likes", value=upvotes, inline=True)
                            embed.set_field_at(1, name="Dislikes", value=downvotes, inline=True)
                            
                            await inter.response.edit_message(embed=embed)
                            
                        return
            
                # Update the upvoters list in the database
                upvoters += f",{user_id}"
                cursor.execute("UPDATE suggestions SET upvoters = ? WHERE id = ?", (upvoters, suggestion_id))
                conn.commit()
                
                # Increment the upvotes count
                cursor.execute("UPDATE suggestions SET upvotes = upvotes + 1 WHERE id = ?", (suggestion_id,))
                conn.commit()
                
                # Fetch the updated suggestion from the database
                cursor.execute("SELECT upvotes, downvotes FROM suggestions WHERE id = ?", (suggestion_id,))
                result = cursor.fetchone()
                
                if result:
                    upvotes = result[0]
                    downvotes = result[1]
                    
                    # Update the suggestion's embed with the new number of likes and dislikes
                    embed = inter.message.embeds[0]
                    embed.set_field_at(0, name="Likes", value=upvotes, inline=True)
                    embed.set_field_at(1, name="Dislikes", value=downvotes, inline=True)
                    
                    await inter.response.edit_message(embed=embed)
                
        elif custom_id.startswith("suggDownvote"):
            suggestion_id = int(custom_id.split("_")[1])
            user_id = str(inter.author.id)

            # Check if the user has already downvoted
            cursor.execute("SELECT downvoters FROM suggestions WHERE id = ?", (suggestion_id,))
            result = cursor.fetchone()

            if result:
                downvoters = result[0] or ""
                if user_id in downvoters:
                    await inter.response.send_message("You may only vote once!", ephemeral=True)
                    return  # User has already downvoted, do nothing

                # Check if the user has already upvoted
                cursor.execute("SELECT upvoters FROM suggestions WHERE id = ?", (suggestion_id,))
                result = cursor.fetchone()

                if result:
                    upvoters = result[0] or ""
                    if user_id in upvoters:
                        # Switch from upvote to downvote
                        upvoters = upvoters.replace(user_id, "")
                        cursor.execute("UPDATE suggestions SET upvoters = ? WHERE id = ?", (upvoters, suggestion_id))
                        cursor.execute("UPDATE suggestions SET downvoters = downvoters || ? WHERE id = ?",
                                       (f",{user_id}", suggestion_id))
                        cursor.execute("UPDATE suggestions SET upvotes = upvotes - 1, downvotes = downvotes + 1 WHERE id = ?",
                                       (suggestion_id,))
                        conn.commit()

                        # Fetch the updated suggestion from the database
                        cursor.execute("SELECT upvotes, downvotes FROM suggestions WHERE id = ?", (suggestion_id,))
                        result = cursor.fetchone()

                        if result:
                            upvotes = result[0]
                            downvotes = result[1]

                            # Update the suggestion's embed with the new number of likes and dislikes
                            embed = inter.message.embeds[0]
                            embed.set_field_at(0, name="Likes", value=upvotes, inline=True)
                            embed.set_field_at(1, name="Dislikes", value=downvotes, inline=True)

                            await inter.response.edit_message(embed=embed)

                        return

            # Update the downvoters list in the database
            downvoters += f",{user_id}"
            cursor.execute("UPDATE suggestions SET downvoters = ? WHERE id = ?", (downvoters, suggestion_id))
            conn.commit()

            # Check if the user has already upvoted and adjust the counts accordingly
            if result and user_id in upvoters:
                upvoters = upvoters.replace(user_id, "")
                cursor.execute("UPDATE suggestions SET upvoters = ? WHERE id = ?", (upvoters, suggestion_id))
                cursor.execute("UPDATE suggestions SET upvotes = upvotes - 1 WHERE id = ?", (suggestion_id,))
                conn.commit()

            # Fetch the updated suggestion from the database
            cursor.execute("SELECT upvotes, downvotes FROM suggestions WHERE id = ?", (suggestion_id,))
            result = cursor.fetchone()

            if result:
                upvotes = result[0]
                downvotes = result[1]

                # Update the suggestion's embed with the new number of likes and dislikes
                embed = inter.message.embeds[0]
                embed.set_field_at(0, name="Likes", value=upvotes, inline=True)
                embed.set_field_at(1, name="Dislikes", value=downvotes, inline=True)

                await inter.response.edit_message(embed=embed)



def setup(bot: commands.Bot) -> None:
    bot.add_cog(Suggestions(bot))
