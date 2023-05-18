import disnake
from disnake.ext.commands import Bot, Cog,slash_command

from disnake.utils import get
class SetupCommand(Cog):
    """A command that sets up the server."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="setup")
    async def setup(self, interaction: disnake.ApplicationCommandInteraction):
        """Sets up the server."""
        # Check if the roles exist
        server_admin_role = disnake.utils.get(interaction.guild.roles, name="Server Admin")
        senior_admin_role = disnake.utils.get(interaction.guild.roles, name="Senior Admin")
        moderator_role = disnake.utils.get(interaction.guild.roles, name="Moderator")
        trial_moderator_role = disnake.utils.get(interaction.guild.roles, name="Trial Moderator")

        # If the roles don't exist, create them
        if not server_admin_role:
            server_admin_role = await interaction.guild.create_role(name="Server Admin")
        if not senior_admin_role:
            senior_admin_role = await interaction.guild.create_role(name="Senior Admin")
        if not moderator_role:
            moderator_role = await interaction.guild.create_role(name="Moderator")
        if not trial_moderator_role:
            trial_moderator_role = await interaction.guild.create_role(name="Trial Moderator")

        # Check if the channels exist
        # Check if the channels exist
        moderation_channel = disnake.utils.get(interaction.guild.channels, name="📂moderation")
        dms_channel = disnake.utils.get(interaction.guild.channels, name="📂dms")
        reports_channel = disnake.utils.get(interaction.guild.channels, name="📂reports")
        transcripts_channel = disnake.utils.get(interaction.guild.channels, name="📂transcripts")
        waca_guard_audit_channel = disnake.utils.get(interaction.guild.channels, name="waca-guard-audit")

         # If the channels don't exist, create them
        if not moderation_channel:
            moderation_channel = await interaction.guild.create_text_channel(name="📂moderation")
        if not dms_channel:
            dms_channel = await interaction.guild.create_text_channel(name="📂dms")
        if not reports_channel:
            reports_channel = await interaction.guild.create_text_channel(name="📂reports")
        if not transcripts_channel:
            transcripts_channel = await interaction.guild.create_text_channel(name="📂transcripts")
        if not waca_guard_audit_channel:
            waca_guard_audit_channel = await interaction.guild.create_voice_channel(name="waca-guard-audit")

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
            await interaction.send(embed=success_embed)
            failure_embed.add_field(name="Roles", value=", ".join([role.name for role in [server_admin_role, senior_admin_role, moderator_role, trial_moderator_role] if role]))
            failure_embed.add_field(name="Channels", value=", ".join([channel.name for channel in [moderation_channel, dms_channel, reports_channel, transcripts_channel, waca_guard_audit_channel] if channel]))
            failure_embed.add_field(name="Roles", value=", ".join([category.name for category in [tickets] if category]))
        else:
            failure_embed.add_field(name="Roles", value=", ".join([role.name for role in [server_admin_role, senior_admin_role, moderator_role, trial_moderator_role] if not role]))
            failure_embed.add_field(name="Channels", value=", ".join([channel.name for channel in [moderation_channel, dms_channel, reports_channel, transcripts_channel, waca_guard_audit_channel] if not channel]))
            failure_embed.add_field(name="Roles", value=", ".join([category.name for category in [tickets] if not category]))
            
            await interaction.send(embed=failure_embed)


def setup(bot: Bot):
    bot.add_cog(SetupCommand(bot))
