import disnake
from disnake.ext.commands import Bot, Cog,slash_command

from disnake.utils import get
class SetupCommand(Cog):
    """A command that sets up the server."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="setup")
    async def setup(self, interaction: disnake.ApplicationCommandInteraction):
        roleExists = []
        roleCreated = []
        categoryExists = []
        categoryCreated = []
        channelExists = []
        channelCreated = []
        inter = interaction
        await inter.response.defer(with_message = True,ephemeral=False)
        """Sets up the server."""
        # Check if the roles exist
        server_admin_role = disnake.utils.get(interaction.guild.roles, name="Server Admin")
        senior_admin_role = disnake.utils.get(interaction.guild.roles, name="Senior Admin")
        moderator_role = disnake.utils.get(interaction.guild.roles, name="Moderator")
        trial_moderator_role = disnake.utils.get(interaction.guild.roles, name="Trial Moderator")
        unverified_role = disnake.utils.get(interaction.guild.roles, name="Unverified")
        verified_role = disnake.utils.get(interaction.guild.roles, name="Verified")
        wick_verified_role = disnake.utils.get(interaction.guild.roles, name="Wick Verified")
        staff_role = disnake.utils.get(interaction.guild.roles, name="Staff")
        greeter_role = disnake.utils.get(interaction.guild.roles, name="Greeter")
        owner_role = disnake.utils.get(interaction.guild.roles, name="Server Owner")


        # If the roles don't exist, create them
        if server_admin_role:
            roleExists.append("Server Admin")
        if senior_admin_role:
            roleExists.append("Senior Admin")
        if moderator_role:
            roleExists.append("Moderator")
        if trial_moderator_role:
            roleExists.append("Trial Moderator")
        if unverified_role:
            roleExists.append("Unverified ")
        if verified_role or wick_verified_role:
            roleExists.append("Verified")
        if staff_role:
            roleExists.append("Staff")
        if greeter_role:
            roleExists.append("Greeter")
        if owner_role:
            roleExists.append("Server Owner")

        if not owner_role:
            owner_role = await interaction.guild.create_role(name="Server Owner")
            roleCreated.append("Server Owner")    
        if not server_admin_role:
            server_admin_role = await interaction.guild.create_role(name="Server Admin")
            roleCreated.append("Server Admin")
            
        if not senior_admin_role:
            senior_admin_role = await interaction.guild.create_role(name="Senior Admin")
            roleCreated.append("Senior Admin")
        if not moderator_role:
            moderator_role = await interaction.guild.create_role(name="Moderator")
            roleCreated.append("Moderator")
        if not trial_moderator_role:
            trial_moderator_role = await interaction.guild.create_role(name="Trial Moderator")
            roleCreated.append("Trial Moderator")
        if not unverified_role:
            unverified_role = await interaction.guild.create_role(name="Unverified")
            roleCreated.append("Unverified")
        if not verified_role and not wick_verified_role:
            verified_role = await interaction.guild.create_role(name="Verified")
            roleCreated.append("Verified")
        if not staff_role:
            staff_role = await interaction.guild.create_role(name="Staff")
            roleCreated.append("Staff")
        if not greeter_role:
            greeter_role = await interaction.guild.create_role(name="Greeter")
            roleCreated.append("Greeter")
            
        # Check if the channels exist
        # Check if the channels exist
        moderation_channel = disnake.utils.get(interaction.guild.channels, name="📂moderation")
        dms_channel = disnake.utils.get(interaction.guild.channels, name="📂dms")
        reports_channel = disnake.utils.get(interaction.guild.channels, name="📂reports")
        transcripts_channel = disnake.utils.get(interaction.guild.channels, name="📂transcripts")
        waca_guard_audit_channel = disnake.utils.get(interaction.guild.channels, name="waca-guard-audit")
        joinInfo = disnake.utils.get(interaction.guild.channels, name="✅│how-to-join")
         # If the channels don't exist, create them
        newCat = disnake.utils.get(interaction.guild.categories, name="New Channels")

        if moderation_channel:
            channelExists.append("Moderation")
        if dms_channel:
            channelExists.append("DMs")
        if reports_channel:
            channelExists.append("Reports")
        if transcripts_channel:
            channelExists.append("Transcripts")
        if waca_guard_audit_channel:
            channelExists.append("WACA-Guard Audit")
        if joinInfo:
            channelExists.append("How-To-Join")

        if newCat:
            categoryExists.append("New Channels")
            
    
        if not newCat:
            newCat = await interaction.guild.create_category_channel(name="New Channels")
            categoryCreated.append("New Channels")
            
        if not moderation_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            moderation_channel = await interaction.guild.create_text_channel(name="📂moderation", overwrites=overwrites, category = newCat)
            channelCreated.append("Moderation")
            
        if not dms_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            dms_channel = await interaction.guild.create_text_channel(name="📂dms", overwrites=overwrites, category = newCat)
            channelCreated.append("DMs")
        if not reports_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            reports_channel = await interaction.guild.create_text_channel(name="📂reports", overwrites=overwrites, category = newCat)
            channelCreated.append("Reports")
        if not transcripts_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            transcripts_channel = await interaction.guild.create_text_channel(name="📂transcripts", overwrites=overwrites, category = newCat)
            channelCreated.append("Transcripts")
        if not waca_guard_audit_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            waca_guard_audit_channel = await interaction.guild.create_text_channel(name="waca-guard-audit", overwrites=overwrites, category = newCat)
            channelCreated.append("WACA-Guard Audit")
        if not joinInfo:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=True),
            inter.guild.default_role: disnake.PermissionOverwrite(send_messages=False),
            get(inter.guild.roles, name="Unverified"): disnake.PermissionOverwrite(read_messages = False),}
            joinInfo = await interaction.guild.create_text_channel(name="✅│how-to-join", overwrites=overwrites, category = newCat)
            channelCreated.append("How-To-Join")
            
        tickets = disnake.utils.get(interaction.guild.categories, name="📬 | Support tickets")
        if tickets:
            categoryExists.append("Tickets")
        if not tickets:
            tickets = await interaction.guild.create_category_channel(name="📬 | Support tickets")
            categoryCreated.append("Tickets")

        
        
        roleExistsMod = [s + '\n' for s in roleExists]
        roleExistsList = ''.join(roleExistsMod)

        roleCreatedMod = [s + '\n' for s in roleCreated]
        roleCreatedList = ''.join(roleCreatedMod)

        categoryExistsMod = [s + '\n' for s in categoryExists]
        categoryExistsList = ''.join(categoryExistsMod)

        categoryCreatedMod = [s + '\n' for s in categoryCreated]
        categoryCreatedList = ''.join(categoryCreatedMod)

        channelExistsMod = [s + '\n' for s in channelExists]
        channelExistsList = ''.join(channelExistsMod)

        channelCreatedMod = [s + '\n' for s in channelCreated]
        channelCreatedList = ''.join(channelCreatedMod)

        embed = disnake.Embed(
            title = "Server Setup Breakdown:",
            color = disnake.Color.green(),
            )

        embed.add_field(name= "Existing Roles", value = roleExistsList)
        embed.add_field(name= "Created Roles", value = roleCreatedList)
        embed.add_field(name= "Existing Categories", value = categoryExistsList)
        embed.add_field(name= "Created Categories", value = categoryCreatedList)
        embed.add_field(name= "Existing Channels", value = channelExistsList)
        embed.add_field(name= "Created Channels", value = channelCreatedList)



        
        await interaction.edit_original_response(embed=embed)


def setup(bot: Bot):
    bot.add_cog(SetupCommand(bot))
