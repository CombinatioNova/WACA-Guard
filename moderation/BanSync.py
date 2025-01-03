import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from datetime import datetime

class BanUser(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="bansync")
    async def ban(self, ctx, userid: str, reason: str):
        await ctx.response.defer(with_message = True,ephemeral=False)
        # Check if the user running the command has the correct permissions
        if ctx.author.id not in [458023820129992716, 362372093423255552]:
            await ctx.edit_original_response("You do not have permission to use this command.")
            return

        # Try to fetch the user from Discord
        try:
            user = await self.bot.fetch_user(int(userid))
        except disnake.NotFound:
            # The user does not exist
            embed = disnake.Embed(
                title="User Not Found",
                description=f"The user with ID {userid} does not exist.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        banned_servers = []
        unbanned_servers = []

        

        embed = disnake.Embed(
            title="🚫 NETWORK BAN NOTICE 🚫",
            description=(
                f"**User {user.mention} has been banned network-wide.**\n\n"
                "🔍 **User Information:**"
            ),
            color=0xff0000,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=user.display_avatar)
        
        # User Information
        embed.add_field(name="👤 Name:", value=user.name, inline=True)
        embed.add_field(name="🆔 ID:", value=user.id, inline=True)
        embed.add_field(name="📅 Created On:", value=f"<t:{int(user.created_at.timestamp())}:F>", inline=True)
        
        # Reason
        embed.add_field(name="❗ Reason:", value=reason, inline=False)
        
        embed.set_author(
            name="NETWACA Moderation",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png"
        )
        embed.set_footer(
            text=f"Sent by {ctx.user.display_name}",
            icon_url=ctx.user.display_avatar
        )
        # Ban the user outside the loop to ensure it happens after processing all servers
        if not banned_servers:
            try:
                for guild in self.bot.guilds:
                    await guild.ban(user, reason=reason)
                    moderation_channel = disnake.utils.get(guild.channels, name = "📂moderation")
                    banned_servers.append(guild.name)
                    if guild.name in unbanned_servers:
                        unbanned_servers.remove(guild.name)
                    if moderation_channel:
                        await moderation_channel.send(embed=embed)
            except disnake.Forbidden:
                await ctx.send(f"Missing permissions to ban in server: {ctx.guild.name}")
                return
            
        for guild in self.bot.guilds:
            try:
                member = guild.get_member(user.id)
                if member:
                    ban_entry = await guild.fetch_ban(member)
                    if ban_entry:
                        banned_servers.append(guild.name)
                    else:
                        await guild.ban(member, reason=reason)
                        banned_servers.append(guild.name)
                else:
                    unbanned_servers.append(guild.name)
            except disnake.Forbidden:
                if guild.name == "RareMC Lobby":
                    await guild.leave()
                else:
                    await ctx.send(f"Missing permissions to check/ban in server: {guild.name}")
                    return
            except:
                continue
           
        embed = disnake.Embed(
            title=f"🔨 Ban of {user.name} Synchronized!",
            description=f"**User Information**",
            color=0x00ff00 if banned_servers else 0xff0000,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=user.display_avatar)
        
        # User Information
        embed.add_field(name="👤 Name:", value=user.name, inline=True)
        embed.add_field(name="🆔 ID:", value=user.id, inline=True)
        embed.add_field(name="📅 Created On:", value=f"<t:{user.created_at.timestamp()}:F>", inline=False)
        
        # Reason
        embed.add_field(name="❗ Reason:", value=reason, inline=False)
        
        embed.set_author(
            name="NETWACA Moderation",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )
        embed.set_footer(
            text=f"Sent by {ctx.user.display_name}",
            icon_url=ctx.user.display_avatar
        )
        banned_servers = []
        unbanned_servers = []

        for guild in self.bot.guilds:
            try:
                ban_entry = await guild.fetch_ban(user)
                banned_servers.append(guild.name)
            except disnake.NotFound:
                unbanned_servers.append(guild.name)
            except disnake.Forbidden:
                if guild.name == "RareMC Lobby":
                    await guild.leave()
                else:
                    await ctx.send(f"Missing permissions to check bans in server: {guild.name}")
                    return
            except:
                continue
        if banned_servers:
            banned_servers_list = "\n".join([f"🔴 {server}" for server in banned_servers])
            embed.add_field(name="🚫 Banned Servers", value=banned_servers_list, inline=False)
        if unbanned_servers:
            unbanned_servers_list = "\n".join([f"🟢 {server}" for server in unbanned_servers])
            embed.add_field(name="✅ Unbanned Servers", value=unbanned_servers_list, inline=False)

        moderation_channel = self.bot.get_channel(1117508642351091763)
        if moderation_channel:
            await moderation_channel.send(embed=embed)

        await ctx.edit_original_response(content = f"User is logged")

    @slash_command(name="banstatus")
    async def ban_status(self, ctx, userid: str):
        # Check if the user running the command has the correct permissions
        if ctx.author.id not in [458023820129992716, 362372093423255552]:
            await ctx.send("You do not have permission to use this command.")
            return

        user = await self.bot.fetch_user(int(userid))
        banned_servers = []
        unbanned_servers = []

        for guild in self.bot.guilds:
            try:
                ban_entry = await guild.fetch_ban(user)
                banned_servers.append(guild.name)
            except disnake.NotFound:
                unbanned_servers.append(guild.name)
            except disnake.Forbidden:
                if guild.name == "RareMC Lobby":
                    await guild.leave()
                else:
                    await ctx.send(f"Missing permissions to check bans in server: {guild.name}")
                    return
            except:
                continue

        embed = disnake.Embed(
            title="🔨 Ban Status",
            description=f"**User ID:** {user.id}\n**User Name:** {user.name}\n**Account Creation Date:** <t:{user.created_at.timestamp()}:f>",
            color=0xff0000 if banned_servers else 0x00ff00
        )

        embed.set_author(
            name="WACA-Guard",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png"
        )

        embed.set_thumbnail(url=user.avatar.url)

        if banned_servers:
            embed.add_field(name="🚫 Banned Servers", value="\n".join(banned_servers), inline=False)
        if unbanned_servers:
            embed.add_field(name="✅ Unbanned Servers", value="\n".join(unbanned_servers), inline=False)

        embed.set_footer(
            text="WACA-Guard Ban Status",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BanUser(bot))
