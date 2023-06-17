import disnake
from disnake.ext.commands import Bot, Cog,slash_command

from disnake.utils import get
class SetupCommand(Cog):
    """A command that sets up the server."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="setup")
    async def setup(self, interaction: disnake.ApplicationCommandInteraction):
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

        # If the roles don't exist, create them
        if not server_admin_role:
            server_admin_role = await interaction.guild.create_role(name="Server Admin")
        if not senior_admin_role:
            senior_admin_role = await interaction.guild.create_role(name="Senior Admin")
        if not moderator_role:
            moderator_role = await interaction.guild.create_role(name="Moderator")
        if not trial_moderator_role:
            trial_moderator_role = await interaction.guild.create_role(name="Trial Moderator")

        if not unverified_role:
            unverified_role = await interaction.guild.create_role(name="Unverified")
        if not verified_role or not wick_verified_role:
            verified_role = await interaction.guild.create_role(name="Verified")
        if not staff_role:
            staff_role = await interaction.guild.create_role(name="Staff")
        if not greeter_role:
            greeter_role = await interaction.guild.create_role(name="Greeter")
            
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

        if not newCat:
            newCat = await interaction.guild.create_category_channel(name="New Channels")
            
        if not moderation_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            moderation_channel = await interaction.guild.create_text_channel(name="📂moderation", overwrites=overwrites, category = newCat)
        if not dms_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            dms_channel = await interaction.guild.create_text_channel(name="📂dms", overwrites=overwrites, category = newCat)
        if not reports_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            reports_channel = await interaction.guild.create_text_channel(name="📂reports", overwrites=overwrites, category = newCat)
        if not transcripts_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            transcripts_channel = await interaction.guild.create_text_channel(name="📂transcripts", overwrites=overwrites, category = newCat)
        if not waca_guard_audit_channel:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(inter.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(inter.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),}
            waca_guard_audit_channel = await interaction.guild.create_text_channel(name="waca-guard-audit", overwrites=overwrites, category = newCat)
            
        if not joinInfo:
            overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=True),
            inter.guild.default_role: disnake.PermissionOverwrite(send_messages=False),
            get(inter.guild.roles, name="Unverified"): disnake.PermissionOverwrite(read_messages = False),}
            joinInfo = await interaction.guild.create_text_channel(name="✅│how-to-join", overwrites=overwrites, category = newCat)

        tickets = disnake.utils.get(interaction.guild.categories, name="📬 | Support tickets")

        if not tickets:
            tickets = await interaction.guild.create_category_channel(name="📬 | Support tickets")
            
        # Create an embed to display the results
        success_embed = disnake.Embed(
            title="Setup Complete",
            description="The server has been successfully set up. The following roles and channels were created:",
            color=0x00FF00,
        )
        failure_embed = disnake.Embed(
            title="Setup Failed",
            description="The server could not be set up. The following errors occurred:",
            color=0xFF0000,
        )

        # Check if all operations were successful
        success_roles = server_admin_role and senior_admin_role and moderator_role and trial_moderator_role
        success_channels = moderation_channel and dms_channel and reports_channel and transcripts_channel and waca_guard_audit_channel

        if success_roles and success_channels:
            
            success_embed.add_field(name="Roles", value=", \n".join([role.name for role in [server_admin_role, senior_admin_role, moderator_role, trial_moderator_role] if role]))
            success_embed.add_field(name="Channels", value=", \n".join([channel.name for channel in [moderation_channel, dms_channel, reports_channel, transcripts_channel, waca_guard_audit_channel] if channel]))
            success_embed.add_field(name="Categories", value=", \n".join([category.name for category in [tickets, newCat] if category]))
            await interaction.edit_original_response(embed=success_embed)
        else:
            failure_embed.add_field(name="Roles", value=", \n".join([role.name for role in [server_admin_role, senior_admin_role, moderator_role, trial_moderator_role] if not role]))
            failure_embed.add_field(name="Channels", value=", \n".join([channel.name for channel in [moderation_channel, dms_channel, reports_channel, transcripts_channel, waca_guard_audit_channel] if not channel]))
            failure_embed.add_field(name="Categories", value=", \n".join([category.name for category in [tickets, newCat] if not category]))
            
            await interaction.edit_original_response(embed=failure_embed)


def setup(bot: Bot):
    bot.add_cog(SetupCommand(bot))
