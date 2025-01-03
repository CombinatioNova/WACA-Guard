import disnake
from disnake.ext import commands, tasks
import asyncio
import aiosqlite
from core import statbed

class PrivateVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.inactivity_tasks = {}
        self.db_path = "databases/private_vc.db"
        self.bot.loop.create_task(self.init_database())  # Call init_database asynchronously

    async def init_database(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS active_channels (
                    text_channel_id INTEGER PRIMARY KEY,
                    voice_channel_id INTEGER,
                    owner_id INTEGER,
                    is_public INTEGER DEFAULT 0
                )
            ''')
            await db.commit()

    async def add_active_channel(self, text_channel_id, voice_channel_id, owner_id, is_public=0):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR REPLACE INTO active_channels (text_channel_id, voice_channel_id, owner_id, is_public)
                VALUES (?, ?, ?, ?)
            ''', (text_channel_id, voice_channel_id, owner_id, is_public))
            await db.commit()

    async def remove_active_channel(self, text_channel_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM active_channels WHERE text_channel_id = ?', (text_channel_id,))
            await db.commit()

    async def get_owner_and_voice_channel(self, text_channel_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT owner_id, voice_channel_id, is_public FROM active_channels WHERE text_channel_id = ?', (text_channel_id,))
            result = await cursor.fetchone()
            await cursor.close()
            return result if result else (None, None, None)

    async def user_has_active_channel(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT COUNT(*) FROM active_channels WHERE owner_id = ?', (user_id,))
            result = await cursor.fetchone()
            await cursor.close()
            return result[0] > 0 if result else False

    async def clear_database(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM active_channels')
            await db.commit()

    @commands.slash_command(name="private_vc", description="Create a private voice and text channel")
    async def private_vc(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        
        # Check if the user already has an active private VC
        if await self.user_has_active_channel(inter.author.id):
            embed = await statbed.create_error_embed(
                title="Private Channel Already Exists",
                description="You already have an active private voice channel. Please close it before creating a new one."
            )
            await inter.followup.send(embed=embed, ephemeral=True)
            return
        
        category = disnake.utils.get(inter.guild.categories, name="private")
        if not category:
            category = await inter.guild.create_category("private")
        else:
            # Check if the category has no channels
            if not category.channels:
                await self.clear_database()

        text_channel_name = f"🔒│private-{inter.author.display_name}"
        voice_channel_name = f"🎤│{inter.author.display_name}'s VC"
        
        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False, connect=False),
            inter.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True),
            inter.guild.me: disnake.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
        }
        
        text_channel = await inter.guild.create_text_channel(text_channel_name, category=category, overwrites=overwrites)
        voice_channel = await inter.guild.create_voice_channel(voice_channel_name, category=category, overwrites=overwrites)

        await self.add_active_channel(text_channel.id, voice_channel.id, inter.author.id)
        
        dashboard_embed = self.create_dashboard_embed(voice_channel)
        dashboard_components = self.create_dashboard_components()
        
        await text_channel.send(embed=dashboard_embed, components=dashboard_components)
        await self.update_dashboard(text_channel, voice_channel)
        if text_channel.id not in self.inactivity_tasks:
            task = self.bot.loop.create_task(self.check_inactivity(text_channel.id))
            self.inactivity_tasks[text_channel.id] = task

        embed = await statbed.create_success_embed(
            title="Private Channels Created",
            description=f"Your private channels have been created:\n{text_channel.mention}\n{voice_channel.mention}"
        )
        await inter.followup.send(embed=embed, ephemeral=True)

    def create_dashboard_embed(self, voice_channel, status_message=None):
        user_limit = voice_channel.user_limit
        limit_text = str(user_limit) if user_limit > 0 else "Unlimited"
        
        embed = disnake.Embed(
            title="🔒 Private Voice Channel Dashboard",
            description=f"Control your private voice channel: **{voice_channel.name}**",
            color=disnake.Color.purple()
        )
        
        embed.add_field(name="👥 Current User Limit", value=f"**{limit_text}**", inline=True)
        
        if status_message:
            embed.add_field(name="📢 Status", value=f"**{status_message}**", inline=False)
        
        embed.set_footer(text="Use the buttons below to manage your private voice channel")
        embed.set_author(name="WACA-Guard", icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png")
        
        return embed

    def create_dashboard_components(self, is_limited=False, is_public=False):
        components = [
            disnake.ui.Button(style=disnake.ButtonStyle.success, label="Invite", custom_id="invite_user", emoji="<:PersonAdd:1262796621402603541>"),
            disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Remove", custom_id="remove_user", emoji="<:PersonRemove:1262796620450238606>"),
        ]
        if is_limited:
            components.extend([
                disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Allow All", custom_id="allow_everyone", emoji="<:group:1264084798947721338>")
            ])
        else:
            components.append(disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Limit", custom_id="limit_users", emoji="<:grouprem:1264084796800241744>"))
        
        public_private_button = disnake.ui.Button(
            style=disnake.ButtonStyle.red if is_public else disnake.ButtonStyle.green,
            label="Private" if is_public else "Public",
            custom_id="toggle_public",
            emoji="<:closelock:1264084009902673940>" if is_public else "<:openlock:1264084990161981510>"
        )
        components.append(public_private_button)
        
        return components

    async def delete_channel(self, text_channel):
        owner_id, voice_channel_id, _ = await self.get_owner_and_voice_channel(text_channel.id)
        if owner_id:
            voice_channel = self.bot.get_channel(voice_channel_id)
            if voice_channel:
                await voice_channel.delete()
            await text_channel.delete()
            await self.remove_active_channel(text_channel.id)
            if text_channel.id in self.inactivity_tasks:
                del self.inactivity_tasks[text_channel.id]

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        custom_id = inter.component.custom_id
        if custom_id in ["invite_user", "remove_user", "limit_users", "allow_everyone", "toggle_public", "close_channel"]:
            owner_id, voice_channel_id, is_public = await self.get_owner_and_voice_channel(inter.channel.id)
            if inter.author.id != owner_id:
                await inter.response.send_message("You don't have permission to control this channel.", ephemeral=True)
                return

            voice_channel = self.bot.get_channel(voice_channel_id)
            if not voice_channel:
                await inter.response.send_message("The voice channel no longer exists.", ephemeral=True)
                return

            if custom_id == "toggle_public":
                is_public = not is_public
                await voice_channel.set_permissions(inter.guild.default_role, connect=is_public)
                status = "public" if is_public else "private"
                await self.add_active_channel(inter.channel.id, voice_channel.id, owner_id, is_public)
                embed = self.create_dashboard_embed(voice_channel, f"Channel is now {status}")
                await inter.response.edit_message(embed=embed, components=self.create_dashboard_components(is_limited=voice_channel.user_limit > 0, is_public=is_public))

            elif custom_id == "invite_user":
                modal = disnake.ui.Modal(
                    title="Invite User",
                    custom_id="invite_user_modal",
                    components=[
                        disnake.ui.TextInput(
                            label="User ID",
                            custom_id="user_id",
                            placeholder="Enter the user ID"
                        )
                    ]
                )
                await inter.response.send_modal(modal)

            elif custom_id == "remove_user":
                modal = disnake.ui.Modal(
                    title="Remove User",
                    custom_id="remove_user_modal",
                    components=[
                        disnake.ui.TextInput(
                            label="User ID",
                            custom_id="user_id",
                            placeholder="Enter the user ID"
                        )
                    ]
                )
                await inter.response.send_modal(modal)

            elif custom_id == "limit_users":
                modal = disnake.ui.Modal(
                    title="Limit Users",
                    custom_id="limit_users_modal",
                    components=[disnake.ui.TextInput(label="User Limit", custom_id="user_limit", placeholder="Enter a number between 1-99")]
                )
                await inter.response.send_modal(modal)

            elif custom_id == "allow_everyone":
                await voice_channel.edit(user_limit=0)
                await asyncio.sleep(1)
                await self.update_dashboard(inter.channel, voice_channel, "User limit removed")
                embed = self.create_dashboard_embed(voice_channel, f"User limit removed")
                await inter.response.edit_message(embed=embed, components=self.create_dashboard_components(is_limited=voice_channel.user_limit > 0, is_public=is_public))

            elif custom_id == "close_channel":
                await self.delete_channel(inter.channel)
                return
            elif custom_id == "still_active2":
                await inter.response.defer()
                message = inter.message  # Define the message variable
                await message.delete()
            elif custom_id == "not_active2":
                await inter.response.defer()
                await self.delete_channel(inter.channel)
            await inter.message.edit(components=self.create_dashboard_components(is_limited=voice_channel.user_limit > 0, is_public=is_public))

    @commands.Cog.listener()
    async def on_modal_submit(self, inter: disnake.ModalInteraction):
        custom_id = inter.custom_id
        if custom_id in ["invite_user_modal", "remove_user_modal", "limit_users_modal"]:
            owner_id, voice_channel_id, is_public = await self.get_owner_and_voice_channel(inter.channel.id)
            if inter.author.id != owner_id:
                await inter.response.send_message("You don't have permission to control this channel.", ephemeral=True)
                return

            voice_channel = self.bot.get_channel(voice_channel_id)
            if not voice_channel:
                await inter.response.send_message("The voice channel no longer exists.", ephemeral=True)
                return

            if custom_id == "invite_user_modal":
                user_id = inter.text_values["user_id"]
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    await voice_channel.set_permissions(user, connect=True)
                    await self.update_dashboard(inter.channel, voice_channel, f"{user.name} has been invited to the channel")
                    
                except:
                    await inter.response.send_message("Invalid user ID or unable to invite user.", ephemeral=True)

            elif custom_id == "remove_user_modal":
                user_id = inter.text_values["user_id"]
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    await voice_channel.set_permissions(user, connect=False)
                    await self.update_dashboard(inter.channel, voice_channel, f"{user.name} has been removed from the channel")
                except:
                    await inter.response.send_message("Invalid user ID or unable to remove user.", ephemeral=True)

            elif custom_id == "limit_users_modal":
                user_limit = inter.text_values["user_limit"]
                try:
                    limit = int(user_limit)
                    if 1 <= limit <= 99:
                        await voice_channel.edit(user_limit=limit)
                        await asyncio.sleep(1)
                        await self.update_dashboard(inter.channel, voice_channel, f"User limit set to {limit}")
                    else:
                        await inter.response.send_message("Please enter a number between 1 and 99.", ephemeral=True)
                except:
                    await inter.response.send_message("Invalid input. Please enter a number between 1 and 99.", ephemeral=True)

            
            await inter.response.edit_message(components=self.create_dashboard_components(is_limited=voice_channel.user_limit > 0, is_public=is_public))

    async def update_dashboard(self, text_channel, voice_channel, status_message=None):
        dashboard_embed = self.create_dashboard_embed(voice_channel, status_message)
        dashboard_components = self.create_dashboard_components(is_limited=voice_channel.user_limit > 0, is_public=voice_channel.permissions_for(text_channel.guild.default_role).connect)
        
        async for message in text_channel.history(limit=1):
            await message.edit(embed=dashboard_embed, components=dashboard_components)
            break

    async def check_inactivity(self, channel_id):
        while True:
            await asyncio.sleep(600)  # Wait for 10 minutes
            text_channel = self.bot.get_channel(channel_id)
            if not text_channel:
                break

            owner_id, voice_channel_id, _ = await self.get_owner_and_voice_channel(channel_id)
            voice_channel = self.bot.get_channel(voice_channel_id)
            if not voice_channel or not voice_channel.members:
                embed = disnake.Embed(
                    title="Inactivity Check",
                    description="Are you still using this channel?",
                    color=disnake.Color.yellow()
                )
                components = [
                    disnake.ui.Button(style=disnake.ButtonStyle.green, label="Yes", custom_id="still_active2"),
                    disnake.ui.Button(style=disnake.ButtonStyle.red, label="No", custom_id="not_active2")
                ]
                message = await text_channel.send(embed=embed, components=components)

                try:
                    inter = await self.bot.wait_for(
                        "button_click",
                        check=lambda i: i.message.id == message.id and i.user.id == owner_id,
                        timeout=180  # 3 minutes
                    )
                    if inter.component.custom_id == "still_active2":
                        await inter.response.defer()
                        await message.delete()
                    elif inter.component.custom_id == "not_active2":
                        await inter.response.defer()
                        await self.delete_channel(text_channel)
                        break
                except asyncio.TimeoutError:
                    await self.delete_channel(text_channel)
                    break

    async def on_voice_state_update(self, member, before, after):
        if before.channel:
            owner_id, _, _ = await self.get_owner_and_voice_channel(before.channel.id)
            if owner_id == member.id and len(before.channel.members) == 0:
                text_channel_id = next((k for k, v in self.inactivity_tasks.items() if v.done()), None)
                if text_channel_id:
                    del self.inactivity_tasks[text_channel_id]
                    text_channel = self.bot.get_channel(text_channel_id)
                    await text_channel.send("The owner has left the private voice channel. It will be deleted in 5 minutes if inactive.")
                    await asyncio.sleep(300)  # Wait for 5 minutes before deletion
                    if len(before.channel.members) == 0:
                        await before.channel.delete()
                        await text_channel.delete()
                        await self.remove_active_channel(text_channel_id)

def setup(bot):
    bot.add_cog(PrivateVC(bot))