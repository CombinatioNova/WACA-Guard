import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.ext import tasks
from disnake.ui import View, Select, Button
from disnake.utils import get
from datetime import datetime
import numba
checkVer = "1.3"

class Protect(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_results = {}  # To store check results for each guild
        

    @Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as {self.bot.user}")

        for guild in self.bot.guilds:
            self.check_results[guild.id] = None  # Initialize check results as None for each guild
##    @slash_command(name="freshstart", description="Wipe the server clean")
##    async def freshstart(self, inter):
##        if inter.author.id == 458023820129992716:
##            for channel in inter.guild.channels:
##                await channel.delete()
##            for category in inter.guild.categories:
##                await category.delete()
##            for role in inter.guild.roles:
##                if role.name == "@everyone":
##                    continue
##                await role.delete()
##        else:
##            inter.response.send_message("What are you doing?")
        
    @slash_command(name="checkup", description="Perform a health scan!")
    async def checkup(self, inter):
         
        # Add the guild ID to the dropdown options
        dropdown = SecurityCheckView(self.bot.guilds[:25], self.bot)
        brief_embed = disnake.Embed(title="<:vitals:1128679029797556274> | WACA-Guard Health Check-Up", description="Welcome to Check-Up, NETWACA's own security analysis tool. While this tool cannot detect all vulnerabilities, it's a solid start to getting you on your way to a safer server!")
        brief_embed.color = 4143049
        brief_embed.set_footer( # Show the moderator
                text=f"Department of Institutional Security | Health Check-Up v.{checkVer}"
            )
        brief_embed.set_author( # Narcissism
                name="WACA-Guard",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
            )
        message = await inter.channel.send(embed=brief_embed)
        dropdown = SecurityCheckView(self.bot.guilds, self.bot)
        dropdown.on_select.options = [
            disnake.SelectOption(label=guild.name, value=str(guild.id)) for guild in self.bot.guilds
        ]
        dropdown.message = message
        await message.edit(view=dropdown)
        await inter.response.send_message("Dashboard Made!", ephemeral = True)

    
    @Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id
        if custom_id.startswith("fixDupe"):
            await inter.response.defer(with_message=True, ephemeral=True)
            
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            embed = inter.message.embeds[0]
            ogThing = set()
            deleteRoles = set()
            for role in guild.roles:
                for other_role in guild.roles:
                    if role == other_role:
                        continue
                    elif role.name == other_role.name and role.name != "@everyone" and role != other_role and other_role not in ogThing:
                        if role.position > other_role.position:
                            deleteRoles.add(other_role)
                        else:
                            deleteRoles.add(role)
                    else:
                        ogThing.add(role)
                
            for role in deleteRoles:
                try:
                    await role.delete()
                except:
                    continue
            await inter.edit_original_response("Done!")
                
        if custom_id.startswith("fixRole"):
            await inter.response.defer(with_message=True, ephemeral=True)
            
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            embed = inter.message.embeds[0]
            # Check if specified roles exist
            roles_to_check = [
                "Staff", "Trial Moderator", "Moderator", "Admin", "Senior Admin", "Server Owner", "Bump Pings", "Greeter:Welcomers","Verified:Wick Verified", "Unverified" 
            ]
            
            for preprocess in roles_to_check:
                role_name = preprocess.split(":")
                role = get(guild.roles, name=role_name[0])
                try:
                    role2 = get(guild.roles, name=role_name[1])
                    if not role and not role2:
                        await guild.create_role(name=role_name[0])
                except IndexError:
                    if not role:
                        await guild.create_role(name=role_name[0])
                except disnake.NotFound:
                    if not role:
                        await guild.create_role(name=role_name[0])
            
            await inter.edit_original_response("Done!")
            
        if custom_id.startswith("migrationUtil"):
            await inter.response.defer(with_message=True, ephemeral=True)
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            
            pass
        if custom_id.startswith("fixVeri"):
            await inter.response.defer(with_message=True, ephemeral=True)
            
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            verifiedRole = get(guild.roles, name="Verified")
            wickVerifiedRole = get(guild.roles, name="Wick Verified")
            staffRole = get(guild.roles, name="Staff")
            # Check if each channel denies view permission for quarantine or muted role
            channels_without_verified_role = []
            blacklisted_channels = ["📁wick-logs","📁wick-moderation-logs","💬│staff-chat","📂moderation","📂dms","📂reports","📂transcripts","📂appeals","waca-guard-audit"]
            for channel in guild.channels:
                
                if verifiedRole is None and wickVerifiedRole is None or channel.name in blacklisted_channels:
                    continue

                view_permission = disnake.Permissions(read_messages=True)
                try:
                    if verifiedRole in channel.overwrites or wickVerifiedRole in channel.overwrites or channel.category.name == "📬 | Support tickets":
                        continue
                    else:
                        if staffRole in channel.overwrites:
                            continue
                        else:
                            overwrites = channel.overwrites_for(verifiedRole)
                            overwrites.read_messages = True
                            await channel.set_permissions(verifiedRole, overwrite=overwrites)
                            
                except Exception as e:
                    if verifiedRole in channel.overwrites:
                        continue
                    else:
                        overwrites = channel.overwrites_for(wickVerifiedRole)
                        overwrites.read_messages = True
                        await channel.set_permissions(wickVerifiedRole, overwrite=overwrites)
            await inter.edit_original_response("Done!")
            
            
        if custom_id.startswith("fixProb"):
            await inter.response.defer(with_message=True, ephemeral=True)
            
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            embed = inter.message.embeds[0]
            quarantine_role = get(guild.roles, name="quarantined")
            muted_role = get(guild.roles, name="Muted")
            if quarantine_role:
                for channel in guild.channels:
                        
                    if quarantine_role is None:
                        pass

                    view_permission = disnake.Permissions(read_messages=False)
                    try:
                        if quarantine_role in channel.overwrites or channel.category.name == "📬 | Support tickets":
                            pass
                        else:
                            overwrites = channel.overwrites_for(quarantine_role)
                            overwrites.read_messages = False
                            await channel.set_permissions(quarantine_role, overwrite=overwrites)
                            await inter.edit_original_response("Done!")
                    except:
                        if quarantine_role in channel.overwrites:
                            pass
                        else:
                            overwrites = channel.overwrites_for(quarantine_role)
                            overwrites.read_messages = False
                            await channel.set_permissions(quarantine_role, overwrite=overwrites)
                            await inter.edit_original_response("Done!")
            elif muted_role:
                quarantine_role=muted_role
                for channel in guild.channels:
                        
                    if quarantine_role is None:
                        pass

                    view_permission = disnake.Permissions(read_messages=False)
                    try:
                        if quarantine_role in channel.overwrites or channel.category.name == "📬 | Support tickets":
                            pass
                        else:
                            overwrites = channel.overwrites_for(quarantine_role)
                            overwrites.read_messages = True
                            await channel.set_permissions(quarantine_role, overwrite=overwrites)
                            await inter.edit_original_response("Done!")
                    except:
                        if quarantine_role in channel.overwrites:
                            pass
                        else:
                            overwrites = channel.overwrites_for(quarantine_role)
                            overwrites.read_messages = True
                            await channel.set_permissions(quarantine_role, overwrite=overwrites)
                            await inter.edit_original_response("Done!")
            else:
                role = await guild.create_role(name="quarantined")
                await inter.edit_original_response("Quarantine role has been made, re-running fix...")
                view_permission = disnake.Permissions(read_messages=False)
                try:
                    for channel in guild.channels:
                        if role in channel.overwrites or channel.category.name == "📬 | Support tickets":
                            pass
                        else:
                            overwrites = channel.overwrites_for(role)
                            overwrites.read_messages = True
                            await channel.set_permissions(role, overwrite=overwrites)
                            await inter.edit_original_response("Done!")
                except:
                    for channel in guild.channels:
                        if role in channel.overwrites:
                            pass
                        else:
                            overwrites = channel.overwrites_for(role)
                            overwrites.read_messages = True
                            await channel.set_permissions(role, overwrite=overwrites)
                            await inter.edit_original_response("Done!")
        
        if custom_id.startswith("checkSpammer"):
            await inter.response.defer(with_message=True, ephemeral=True)
            
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            spammer_count = sum(1 for member in guild.members if member.public_flags.spammer)
            await inter.edit_original_response(f"Number of spammers: {spammer_count}")





def setup(bot):
    bot.add_cog(Protect(bot))

