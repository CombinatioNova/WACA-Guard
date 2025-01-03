import disnake
from disnake.ext import commands
import sqlite3
import os
from datetime import datetime
import asyncio

class Vouching(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join('databases', 'vouches.db')
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vouches
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER,
                           voucher_id INTEGER,
                           timestamp TEXT,
                           status TEXT,
                           is_vetted_voucher BOOLEAN,
                           comment TEXT)''')
        conn.commit()
        conn.close()

    @commands.slash_command()
    async def vouch(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, comment: str):
        """Vouch for a member to become a Vetted SMP Member"""
        await inter.response.defer(ephemeral=True)

        if member.id == inter.author.id:
            return await inter.followup.send("You can't vouch for yourself!", ephemeral=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if the user has already been vouched for by this member
        cursor.execute("SELECT * FROM vouches WHERE user_id = ? AND voucher_id = ?", (member.id, inter.author.id))
        if cursor.fetchone():
            conn.close()
            return await inter.followup.send("You have already vouched for this member!", ephemeral=True)

        # Check if the voucher is a Vetted SMP Member
        vetted_role = disnake.utils.get(inter.guild.roles, name="Vetted SMP Member")
        is_vetted_voucher = vetted_role in inter.author.roles

        # Add the vouch to the database
        timestamp = datetime.now().isoformat()
        cursor.execute("INSERT INTO vouches (user_id, voucher_id, timestamp, status, is_vetted_voucher, comment) VALUES (?, ?, ?, ?, ?, ?)",
                       (member.id, inter.author.id, timestamp, 'pending', is_vetted_voucher, comment))
        conn.commit()
        conn.close()

        # Update or create the vouch record in the vouches channel
        vouches_channel = disnake.utils.get(inter.guild.channels, name="📂vouches")
        if not vouches_channel:
            staff_role = disnake.utils.get(inter.guild.roles, name="Staff")
            if not staff_role:
                return await inter.followup.send("Staff role not found. Please create a role named 'Staff' and try again.", ephemeral=True)
            
            overwrites = {
                inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                staff_role: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                inter.guild.me: disnake.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            vouches_channel = await inter.guild.create_text_channel("📂vouches", overwrites=overwrites)

        embed = await self.create_vouch_embed(member)
        message = await self.find_vouch_message(vouches_channel, member)

        if message:
            await message.edit(embed=embed, components=self.get_vouch_buttons())
        else:
            await vouches_channel.send(embed=embed, components=self.get_vouch_buttons())

        await inter.followup.send(f"You have successfully vouched for {member.mention}!", ephemeral=True)

    async def create_vouch_embed(self, member):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vouches WHERE user_id = ? AND is_vetted_voucher = 1", (member.id,))
        vetted_vouch_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM vouches WHERE user_id = ? AND is_vetted_voucher = 0", (member.id,))
        regular_vouch_count = cursor.fetchone()[0]
        cursor.execute("SELECT voucher_id, is_vetted_voucher, status FROM vouches WHERE user_id = ?", (member.id,))
        vouchers = cursor.fetchall()
        conn.close()

        embed = disnake.Embed(title=f"Vouches for {member.display_name}", color=disnake.Color.blue())
        embed.set_thumbnail(url=member.display_avatar.url)  # Add the vouched user's pfp as the thumbnail
        embed.add_field(name="Vetted Member Vouches", value=str(vetted_vouch_count), inline=True)
        embed.add_field(name="Regular Member Vouches", value=str(regular_vouch_count), inline=True)
        
        vetted_vouchers = [f"{self.bot.get_user(row[0]).mention}" for row in vouchers if row[1]]
        regular_vouchers = [f"{self.bot.get_user(row[0]).mention}" for row in vouchers if not row[1]]
        
        embed.add_field(name="Vouched by Vetted Members", value="\n".join(vetted_vouchers) or "None", inline=False)
        embed.add_field(name="Vouched by Regular Members", value="\n".join(regular_vouchers) or "None", inline=False)
        embed.set_footer(text=f"User ID: {member.id}")
        return embed

    async def find_vouch_message(self, channel, member):
        async for message in channel.history(limit=None):
            if message.embeds and message.embeds[0].footer.text == f"User ID: {member.id}":
                return message
        return None

    def get_vouch_buttons(self):
        return [
            disnake.ui.Button(style=disnake.ButtonStyle.green, label="Approve", custom_id="approve_vouch", emoji="<:PersonAdd:1262796621402603541>"),
            disnake.ui.Button(style=disnake.ButtonStyle.red, label="Deny", custom_id="deny_vouch", emoji="<:PersonCancel:1262798492984672398>"),
            disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Show Comments", custom_id="show_comments", emoji="<:Comment:1262796617942040697>")
        ]

    def get_comment_buttons(self, current_index, total_comments):
        return [
            disnake.ui.Button(style=disnake.ButtonStyle.primary, custom_id="first_comment", emoji="<:firstpage:1262797966528352266>", disabled=current_index == 0),
            disnake.ui.Button(style=disnake.ButtonStyle.primary, custom_id="prev_comment", emoji="<:back:1262797968545943643>", disabled=current_index == 0),
            disnake.ui.Button(style=disnake.ButtonStyle.primary, custom_id="next_comment", emoji="<:next:1262797963223371807>", disabled=current_index == total_comments - 1),
            disnake.ui.Button(style=disnake.ButtonStyle.primary, custom_id="last_comment", emoji="<:lastpage:1262797965655806022>", disabled=current_index == total_comments - 1),
            disnake.ui.Button(style=disnake.ButtonStyle.red, label="Back", custom_id="back_to_vouch", emoji="<:Return:1262796614591057990>")
        ]

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id in ["approve_vouch", "deny_vouch"]:
            if not inter.author.guild_permissions.administrator:
                return await inter.response.send_message("Only administrators can approve or deny vouches.", ephemeral=True)

            user_id = self.extract_user_id(inter.message.embeds[0].footer.text)
            member = inter.guild.get_member(user_id)

            if not member:
                return await inter.response.send_message("The user is no longer in the server.", ephemeral=True)

            if inter.component.custom_id == "approve_vouch":
                vetted_role = disnake.utils.get(inter.guild.roles, name="Vetted SMP Member")
                if not vetted_role:
                    vetted_role = await inter.guild.create_role(name="Vetted SMP Member")

                await inter.response.send_message(f"{member.mention} has been approved as a Vetted SMP Member!", ephemeral=True)

                # Send approval embed to the user
                approval_embed = disnake.Embed(
                    title="Access Approved!",
                    description="You have been approved as a Vetted SMP Member. This gives you access to our SMP server.",
                    color=disnake.Color.green()
                )
                approval_embed.add_field(name="Server", value=inter.guild.name)
                approval_embed.add_field(name="Next Steps", value="Please click the 'Accept' button below to receive your role and access.")

                try:
                    msg = await member.send(embed=approval_embed, components=[
                        disnake.ui.Button(style=disnake.ButtonStyle.green, label="Accept", custom_id="accept_vouch"),
                        disnake.ui.Button(style=disnake.ButtonStyle.red, label="Decline", custom_id="decline_vouch")
                    ])

                    # Update the database to 'pending'
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE vouches SET status = 'pending' WHERE user_id = ?", (user_id,))
                    conn.commit()
                    conn.close()

                    # Update the embed to show 'pending' status
                    embed = await self.create_vouch_embed(member)
                    embed.color = disnake.Color.orange()
                    embed.title = f"{member.display_name}'s vouch is pending acceptance"
                    embed.add_field(name="Status", value="Pending User Acceptance", inline=False)
                    components = [
                        disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Show Comments", custom_id="show_comments", emoji="<:Comment:1262796617942040697>")
                    ]
                    await inter.message.edit(embed=embed, components=components)

                    def check(i):
                        return i.message.id == msg.id and i.user.id == member.id

                    interaction = await self.bot.wait_for("button_click", check=check, timeout=86400)  # 24 hour timeout

                    if interaction.component.custom_id == "accept_vouch":
                        await member.add_roles(vetted_role)
                        await interaction.response.send_message("You have accepted the Vetted SMP Member role. Welcome to the SMP!", ephemeral=True)
                        status = "approved_accepted"
                    else:
                        await interaction.response.send_message("You have declined the Vetted SMP Member role. If you change your mind, please contact an administrator.", ephemeral=True)
                        status = "approved_declined"

                    # Update the database with the final status
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE vouches SET status = ? WHERE user_id = ?", (status, user_id))
                    conn.commit()
                    conn.close()

                    # Update the embed with the final status
                    embed = await self.create_vouch_embed(member)
                    embed.color = disnake.Color.green() if status == "approved_accepted" else disnake.Color.red()
                    embed.title = f"{member.display_name} has {'accepted' if status == 'approved_accepted' else 'declined'} the vouch"
                    embed.add_field(name="Status", value=status.replace("_", " ").title(), inline=False)
                    components = [
                        disnake.ui.Button(style=disnake.ButtonStyle.red, label="Remove Access", custom_id="remove_role", emoji="<:PersonRemove:1262796620450238606>"),
                        disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Show Comments", custom_id="show_comments", emoji="<:Comment:1262796617942040697>")
                    ]
                    await inter.message.edit(embed=embed, components=components)

                except disnake.HTTPException:
                    await inter.followup.send(f"Unable to send DM to {member.mention}. They have been approved, but not given the role.", ephemeral=True)
                    status = "approved_nodm"
                except asyncio.TimeoutError:
                    await member.send("Your approval has expired. Please contact an administrator if you still wish to join the SMP.")
                    status = "approved_expired"

                    # Update the database and embed for timeout case
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE vouches SET status = ? WHERE user_id = ?", (status, user_id))
                    conn.commit()
                    conn.close()

                    embed = await self.create_vouch_embed(member)
                    embed.color = disnake.Color.orange()
                    embed.title = f"{member.display_name}'s vouch approval has expired"
                    embed.add_field(name="Status", value=status.replace("_", " ").title(), inline=False)
                    components = [
                        disnake.ui.Button(style=disnake.ButtonStyle.green, label="Approve", custom_id="approve_vouch", emoji="<:PersonAdd:1262796621402603541>"),
                        disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Show Comments", custom_id="show_comments", emoji="<:Comment:1262796617942040697>")
                    ]
                    await inter.message.edit(embed=embed, components=components)

            elif inter.component.custom_id == "deny_vouch":
                await inter.response.send_message(f"{member.mention}'s vouch has been denied.", ephemeral=True)

                # Send denial embed to the user
                denial_embed = disnake.Embed(
                    title="Access Denied",
                    description="We're sorry, but you will not be granted access to the SMP at this time.",
                    color=disnake.Color.red()
                )
                denial_embed.add_field(name="Server", value=inter.guild.name)
                denial_embed.add_field(name="Next Steps", value="If you believe this was a mistake, please contact a server administrator.")

                try:
                    await member.send(embed=denial_embed)
                except disnake.HTTPException:
                    await inter.followup.send(f"Unable to send DM to {member.mention}.", ephemeral=True)

                # Update the database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("UPDATE vouches SET status = 'denied' WHERE user_id = ?", (user_id,))
                conn.commit()
                conn.close()

                # Update the embed
                embed = await self.create_vouch_embed(member)
                embed.color = disnake.Color.red()
                embed.title = f"{member.display_name}'s vouch has been denied"
                embed.add_field(name="Status", value="Denied", inline=False)
                components = [
                    disnake.ui.Button(style=disnake.ButtonStyle.green, label="Approve", custom_id="approve_vouch", emoji="<:PersonAdd:1262796621402603541>"),
                    disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Show Comments", custom_id="show_comments", emoji="<:Comment:1262796617942040697>")
                ]
                await inter.message.edit(embed=embed, components=components)

        elif inter.component.custom_id == "remove_role":
            user_id = self.extract_user_id(inter.message.embeds[0].footer.text)
            member = inter.guild.get_member(user_id)
            vetted_role = disnake.utils.get(inter.guild.roles, name="Vetted SMP Member")

            if member and vetted_role in member.roles:
                await member.remove_roles(vetted_role)
                await inter.response.send_message(f"Removed Vetted SMP Member role from {member.mention}", ephemeral=True)

                # Update the database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("UPDATE vouches SET status = 'role_removed' WHERE user_id = ?", (user_id,))
                conn.commit()
                conn.close()

                # Update the embed
                embed = await self.create_vouch_embed(member)
                embed.color = disnake.Color.orange()
                embed.title = f"{member.display_name}'s Vetted SMP Member role has been removed"
                embed.add_field(name="Status", value="Role Removed", inline=False)
                await inter.message.edit(embed=embed, components=self.get_vouch_buttons())
            else:
                await inter.response.send_message("Unable to remove role. The user may no longer be in the server or doesn't have the role.", ephemeral=True)

        elif inter.component.custom_id == "show_comments":
            user_id = self.extract_user_id(inter.message.embeds[0].footer.text)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT voucher_id, comment FROM vouches WHERE user_id = ? AND comment IS NOT NULL", (user_id,))
            comments = cursor.fetchall()
            conn.close()

            if not comments:
                return await inter.response.send_message("No comments available for this vouch.", ephemeral=True)

            await self.show_comment(inter, comments, 0)

        elif inter.component.custom_id in ["prev_comment", "next_comment", "first_comment", "last_comment"]:
            await self.navigate_comments(inter)

        elif inter.component.custom_id == "back_to_vouch":
            user_id = self.extract_user_id(inter.message.embeds[0].footer.text)
            member = inter.guild.get_member(user_id)
            embed = await self.create_vouch_embed(member)
            
            # Determine the current state of the vouch
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM vouches WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
            status = cursor.fetchone()[0]
            conn.close()

            if status.startswith('approved'):
                embed.color = disnake.Color.green()
                embed.title = f"{member.display_name} has been approved!"
                embed.add_field(name="Status", value=status.replace("_", " ").title(), inline=False)
                components = [
                    disnake.ui.Button(style=disnake.ButtonStyle.red, label="Remove Role", custom_id="remove_role"),
                    disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Show Comments", custom_id="show_comments", emoji="<:Comment:1262796617942040697>")
                ]
            elif status == 'denied':
                embed.color = disnake.Color.red()
                embed.title = f"{member.display_name}'s vouch has been denied"
                embed.add_field(name="Status", value="Denied", inline=False)
                components = [
                    disnake.ui.Button(style=disnake.ButtonStyle.green, label="Approve", custom_id="approve_vouch", emoji="<:PersonAdd:1262796621402603541>"),
                    disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Show Comments", custom_id="show_comments", emoji="<:Comment:1262796617942040697>")
                ]
            else:
                components = self.get_vouch_buttons()

            await inter.response.edit_message(embed=embed, components=components)

    def extract_user_id(self, footer_text):
        # Extract user ID from both formats of footer text
        if '|' in footer_text:
            return int(footer_text.split("User ID: ")[1].split(" |")[0])
        else:
            return int(footer_text.split(": ")[1])

    async def show_comment(self, inter, comments, index):
        total = len(comments)
        voucher_id, comment = comments[index]
        voucher = self.bot.get_user(voucher_id)
        
        embed = inter.message.embeds[0]
        embed.clear_fields()
        embed.add_field(name=f"Comment {index + 1}/{total}", value=comment, inline=False)
        embed.set_author(name=f"Comment by {voucher.name}", icon_url=voucher.avatar.url)
        embed.set_footer(text=f"User ID: {embed.footer.text.split('User ID: ')[1].split(' |')[0]} | Comment Index: {index}")

        await inter.response.edit_message(embed=embed, components=self.get_comment_buttons(index, total))

    async def navigate_comments(self, inter):
        embed = inter.message.embeds[0]
        current_index = int(embed.footer.text.split("Comment Index: ")[1])
        user_id = int(embed.footer.text.split("User ID: ")[1].split(" |")[0])

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT voucher_id, comment FROM vouches WHERE user_id = ? AND comment IS NOT NULL", (user_id,))
        comments = cursor.fetchall()
        conn.close()

        total_comments = len(comments)
        if total_comments == 0:
            return await inter.response.send_message("No comments available.", ephemeral=True)

        if inter.component.custom_id == "next_comment":
            new_index = min(current_index + 1, total_comments - 1)
        elif inter.component.custom_id == "prev_comment":
            new_index = max(current_index - 1, 0)
        elif inter.component.custom_id == "first_comment":
            new_index = 0
        elif inter.component.custom_id == "last_comment":
            new_index = total_comments - 1

        await self.show_comment(inter, comments, new_index)

def setup(bot):
    bot.add_cog(Vouching(bot))