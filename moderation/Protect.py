import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.ext import tasks
from disnake.ui import View, Select, Button
from disnake.utils import get
from datetime import datetime
import numba
checkVer = "1.2"

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
            await inter.response.defer(with_message=True, ephemeral = True)
            
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            embed = inter.message.embeds[0]
            ogThing = []
            deleteRoles = []
            for role in guild.roles:
                for other_role in guild.roles:
                    if role == other_role:
                        continue
                    elif role.name == other_role.name and role.name != "@everyone" and role != other_role and other_role not in ogThing:
                        if role.position > other_role.position:
                            print(f"{other_role.name} will be delete {role.id}")
                            deleteRoles.append(other_role)
                            print(f"\n\n\n##########################         Deleted {role.name}           #################################\n\n\n")
                            continue
                        else:
                            print(f"{role.name} will be delete {role.id}")
                            deleteRoles.append(role)
                            print(f"\n\n\n##########################         Deleted {role.name}           #################################\n\n\n")
                            continue
                    else:
                        ogThing.append(role)
                        continue
                
            for role in deleteRoles:
                try:
                    print("Deleted")
                    await role.delete()
                except:
                    continue
            print(ogThing)
            await inter.edit_original_response("Done!")
                
                        
                
        if custom_id.startswith("fixRole"):
            await inter.response.defer(with_message=True, ephemeral = True)
            
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
            await inter.response.defer(with_message=True, ephemeral = True)
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            
            pass
        if custom_id.startswith("fixVeri"):
            await inter.response.defer(with_message=True, ephemeral = True)
            
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
                    print("Exempted")
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
                    print(e)
                    if verifiedRole in channel.overwrites:
                        continue
                    else:
                        overwrites = channel.overwrites_for(wickVerifiedRole)
                        overwrites.read_messages = True
                        await channel.set_permissions(wickVerifiedRole, overwrite=overwrites)
                        continue
            await inter.edit_original_response("Done!")
            
            
        if custom_id.startswith("fixProb"):
            await inter.response.defer(with_message=True, ephemeral = True)
            
            guild_id = int(custom_id.split("_")[1])
            guild = disnake.utils.get(self.bot.guilds, id=guild_id)
            embed = inter.message.embeds[0]
##            components = embed.components
##            for component in components if custom_id.startswith("fixProb"):
##                component.disable = True
##            await inter.message.
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
                #try:
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
##                except Exception as e:
##                    print(e)
##                    await inter.edit_original_response("No permissions to make quarantine role!")
                                                

class SecurityCheckView(View):
    def __init__(self, guilds, bot):
        super().__init__()
        self.guilds = guilds
        self.bot = bot
        self.message = None
        self.check_results = {}  # To store check results for each guild

    @disnake.ui.select(placeholder="Select a Server", options=[])
    async def on_select(self, select: disnake.ui.Select, inter: disnake.ApplicationCommandInteraction):
        
        guild_id = int(select.values[0])
        message_id = self.message.id
        if message_id:
            message = inter.message

            # Get the selected guild based on the guild ID
            guild = disnake.utils.get(self.guilds, id=guild_id)

            if guild:
                print(guild)

                # Create and send the initial dashboard embed
                embed = disnake.Embed(title="<:SecurityCheckMed:1126171034886873198>│Checking your server...", description=f"WACA-Guard is now scanning {guild.name} for any potential issues...")
                await inter.response.edit_message(embed=embed)

                # Store the message ID for later reference
                self.check_results[guild.id] = message.id

                # Perform the security checks
                violations = []
                dupliVio = []
                missRoleVio = []
                qVio = []
                permVio = []
                danger = []
                features = []
                unseen = []

                default_notifications = guild.default_notifications
                is_mfa_enabled = guild.mfa_level
                missing_features = guild.features
                veriLevel = guild.verification_level
                nsfwLevel = guild.nsfw_level
                
                filterLevel = disnake.utils.get(self.guilds, id=guild_id).explicit_content_filter
                print(filterLevel)
                if filterLevel == disnake.ContentFilter.disabled:
                    features.append("<:SecurityBad:1126200375125483520>│Server has no NSFW filter!")
                elif filterLevel == disnake.ContentFilter.no_role:
                    features.append("<:SecurityWarn:1126200371572908153>│Server has low NSFW filter requirements")
                    
                if nsfwLevel == disnake.NSFWLevel.explicit:
                    features.append("<:SecurityBad:1126200375125483520>│Server contains NSFW content!")
                elif nsfwLevel == disnake.NSFWLevel.age_restricted:
                    features.append("<:SecurityWarn:1126200371572908153>│Server may contain NSFW content")
                

                
                
                
        
                if veriLevel == disnake.VerificationLevel.none:
                    features.append("<:SecurityBad:1126200375125483520>│Server has no discord verification requirements!")
                elif veriLevel == disnake.VerificationLevel.low:
                    features.append("<:SecurityWarn:1126200371572908153>│Server has low discord verification requirements")
                elif veriLevel == disnake.VerificationLevel.highest:
                    features.append("<:SecurityWarn:1126200371572908153>│Server has overkill discord verification requirements!")
                

                if default_notifications == disnake.NotificationLevel.only_mentions:
                    print("The guild's default notifications are set to @mention.")
                else:
                    features.append("<:SecurityWarn:1126200371572908153>│Default notifications are not set to @mention")

                if is_mfa_enabled == 1:
                    pass
                else:
                    features.append("<:SecurityBad:1126200375125483520>│Multi-Factor Authentication is NOT enabled!")

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
                            missRoleVio.append(f"<:SecurityWarn:1126200371572908153>│Role missing: {str(role_name[0])}")
                    except:
                        if not role:
                            missRoleVio.append(f"<:SecurityWarn:1126200371572908153>│Role missing: {str(role_name[0])}")

                # Check if quarantine role exists
                quarantine_role = get(guild.roles, name="quarantined")
                muted_role = get(guild.roles, name="Muted")
                if not quarantine_role and not muted_role:
                    missRoleVio.append("<:SecurityBad:1126200375125483520>│Quarantine role missing")
                    

                # Check if Wick role exists and is highest
                wick_role = get(guild.roles, name="Wick")
                wick_prem_role = get(guild.roles, name="Wick Premium")
                top_role = sorted(guild.roles, key=lambda role: role.position, reverse=True)[0]
                if not wick_role and not wick_prem_role:
                    features.append("<:SecurityBad:1126200375125483520>│Wick is **__missing__** or it's default role has changed names!")
                if wick_role != top_role and wick_prem_role != top_role:
                    qVio.append("<:SecurityBad:1126200375125483520>│Wick role is not highest!")
                
                    
                waca_guard = await guild.fetch_member(self.bot.user.id)
                waca_guard_roles = []
                for role in waca_guard.roles:
                    waca_guard_roles.append(role)
                print(waca_guard_roles)
                top_5_roles = sorted(guild.roles, key=lambda role: role.position, reverse=True)[:5]
                waca_guard_5 = []
                for waca_guard_role in waca_guard_roles:
                    if waca_guard_role in top_5_roles:
                        waca_guard_5.append(role)
                        print(f"One of WACA-Guard's roles is within the top 5: {waca_guard_role.name}")
                if len(waca_guard_5) == 0:
                    qVio.append("<:SecurityWarn:1126200371572908153>│None of WACA-Guard's roles is within the top 5! It might not manage things well...")
                        
                # Check if each channel denies view permission for quarantine or muted role
                channels_without_quarantine_role = []
                for channel in guild.channels:
                    
                    if quarantine_role is None and muted_role is None:
                        channels_without_quarantine_role.append(channel.name)
                        continue

                    view_permission = disnake.Permissions(read_messages=False)
                    try:
                        if quarantine_role in channel.overwrites or muted_role in channel.overwrites or channel.category.name == "📬 | Support tickets":
                            continue
                        else:
                            channels_without_quarantine_role.append(channel.name)
                            continue
                    except:
                        if quarantine_role in channel.overwrites:
                            continue
                        else:
                            channels_without_quarantine_role.append(channel.name)
                            continue

                if channels_without_quarantine_role:
                    violations.append("\n".join(channels_without_quarantine_role))
                    
                verifiedRole = get(guild.roles, name="Verified")
                wickVerifiedRole = get(guild.roles, name="Wick Verified")
                staffRole = get(guild.roles, name="Staff")
                blacklisted_channels = ["📁wick-logs","📁wick-moderation-logs","💬│staff-chat","📂moderation","📂dms","📂reports","📂transcripts","📂appeals","waca-guard-audit"]
                blacklisted_categories = ["📂 | action logs", "staff",]
                # Check if each channel denies view permission for quarantine or muted role
                channels_without_verified_role = []
                for channel in guild.channels:
                    
                    if verifiedRole is None and wickVerifiedRole is None:
                        channels_without_verified_role.append(channel.name)
                        continue

                    view_permission = disnake.Permissions(read_messages=True)
                    try:
                        if verifiedRole in channel.overwrites or wickVerifiedRole in channel.overwrites or channel.category.name == "📬 | Support tickets" or channel.name in blacklisted_channels or channel.category.name.lower() in blacklisted_categories:
                            continue
                        else:
                            channels_without_verified_role.append(channel.name)
                            continue
                    except:
                        if verifiedRole in channel.overwrites or wickVerifiedRole in channel.overwrites:
                            continue
                        else:
                            channels_without_verified_role.append(channel.name)
                            continue

                if channels_without_verified_role:
                    unseen.append("\n".join(channels_without_verified_role))

                # Check if the bot has proper permissions and role hierarchy
                bot_member = guild.me
                bot_permissions = bot_member.guild_permissions
                if not bot_permissions.manage_roles or not bot_permissions.administrator:
                    permVio.append("<:SecurityCheckMed:1126171034886873198>│Bot does not have 'Manage Roles' permission")
                if not bot_permissions.manage_channels or not bot_permissions.administrator:
                    permVio.append("<:SecurityCheckHigh:1126171038376534126>│Bot does not have 'Manage Channels' permission")
                if not bot_permissions.manage_messages or not bot_permissions.administrator:
                    permVio.append("<:SecurityCheckHigh:1126171038376534126>│Bot does not have 'Manage Messages' permission")
                if not bot_permissions.kick_members or not bot_permissions.administrator:
                    permVio.append("<:SecurityCheckHigh:1126171038376534126>│Bot does not have 'Kick Members' permission")
                if not bot_permissions.ban_members or not bot_permissions.administrator:
                    permVio.append("<:SecurityCheckHigh:1126171038376534126>│Bot does not have 'Ban Members' permission")


                for member in guild.members:
                    if member == self.bot.user:
                        continue
                    # Check if people have dangerous permissions
                    mem_permissions = member.guild_permissions
                    if mem_permissions.administrator:
                        danger.append(f"<:SecurityWarn:1126200371572908153>│**{member.display_name.capitalize()}** has Administrator permissions!")
                    elif mem_permissions.manage_roles:
                        danger.append(f"<:SecurityWarn:1126200371572908153>│**{member.display_name.capitalize()}** has dangerous permissions")
                    elif mem_permissions.manage_channels:
                        danger.append(f"<:SecurityWarn:1126200371572908153>│**{member.display_name.capitalize()}** has dangerous permissions")
                    elif mem_permissions.manage_messages:
                        danger.append(f"<:SecurityWarn:1126200371572908153>│**{member.display_name.capitalize()}** has dangerous permissions")
                    elif mem_permissions.kick_members:
                        danger.append(f"<:SecurityWarn:1126200371572908153>│**{member.display_name.capitalize()}** has dangerous permissions")
                    elif mem_permissions.ban_members:
                        danger.append(f"<:SecurityWarn:1126200371572908153>│**{member.display_name.capitalize()}** has dangerous permissions")
                duplicate_roles = []
                similar_roles = []    
                for role in guild.roles:
                    for other_role in guild.roles:
                        if role == other_role:
                            continue

                        if role.name == other_role.name:
                            duplicate_roles.append((role, other_role))
                        elif role.name.lower() == other_role.name.lower():
                            similar_roles.append((role, other_role))
                
                for role, other_role in duplicate_roles:
                    dupliVio.append(f"<:SecurityWarn:1126200371572908153>│**{role.name}** is a duplicate!")
                for role, other_role in similar_roles:
                    dupliVio.append(f"<:SecurityWarn:1126200371572908153>│**{role.name}** is similar to **{other_role.name}**")

                # Update the dashboard embed with the final summary
                embed.description = """

We checked your server for any potentially dangerous permissions, missing roles, or unquarantined channels! Here are your results:"""
                embed.title = f"<:SecurityCheckLow:1126171036208074772> | {guild.name} Check-Up Complete!"
                embed.color = disnake.Color.green()
                homeRow=[]
                if features:
                    violation_message = "\n".join(features)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    embed.add_field(name="General Issues:", value=truncated_message, inline=False)
                if danger:
                    violation_message = "\n".join(danger)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    embed.add_field(name="Dangerous Permissions", value=truncated_message, inline=False)
                if permVio:
                    violation_message = "\n".join(permVio)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    embed.add_field(name="Bot Permission Issues", value=truncated_message, inline=False)
                if missRoleVio:
                    violation_message = "\n".join(missRoleVio)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    embed.add_field(name="Missing Roles", value=truncated_message, inline=False)
                    fixRoles = Button(style=disnake.ButtonStyle.green,label="Fix Roles", emoji="<:Fix:1126241342922690714>", custom_id=f"fixRole_{guild.id}")
                    homeRow.append(fixRoles)
                if violations:
                    violation_message = "\n".join(violations)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    embed.add_field(name="Quarantine not set in:", value=truncated_message, inline=False)
                    fixButton = Button(style=disnake.ButtonStyle.green,label="Fix Quarantine", emoji="<:Fix:1126241342922690714>", custom_id=f"fixProb_{guild.id}")
                    homeRow.append(fixButton)
                if dupliVio:
                    violation_message = "\n".join(dupliVio)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    fixButton = Button(style=disnake.ButtonStyle.green,label="Fix Duplicates", emoji="<:Fix:1126241342922690714>", custom_id=f"fixDupe_{guild_id}")
                    homeRow.append(fixButton)
                    embed.add_field(name="Duplicated Roles:", value=truncated_message, inline=False)
                if qVio:
                    violation_message = "\n".join(qVio)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    embed.add_field(name="Role Position Violations:", value=truncated_message, inline=False)
                if unseen:
                    violation_message = "\n".join(unseen)
                    truncated_message = violation_message[:1019] + "`...`" if len(violation_message) > 1024 else violation_message
                    embed.add_field(name="Verified not set up in:", value=truncated_message, inline=False)
                    #fixButton = Button(style=disnake.ButtonStyle.green,label="Fix Verification", emoji="<:Fix:1126241342922690714>", custom_id=f"fixVeri_{guild_id}")
                    #homeRow.append(fixButton)


                
                if not features:
                    embed.add_field(name="General Issues:", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                if not violations:
                    embed.add_field(name="Quarantine", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                if not missRoleVio:
                    embed.add_field(name="Roles", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                if not permVio:
                    embed.add_field(name="Bot Permissions", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                if not danger:
                    embed.add_field(name="User Permissions", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                if not dupliVio:
                    embed.add_field(name="Duplicated Roles", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                if not qVio:
                    embed.add_field(name="Role Position Violations", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                if not unseen:
                    embed.add_field(name="Verified User Setup", value="<:SecurityGood:1126200372806029322>│No Issues", inline=False)
                
                    
                    
                await message.edit(embed=embed, components=homeRow)





def setup(bot):
    bot.add_cog(Protect(bot))

