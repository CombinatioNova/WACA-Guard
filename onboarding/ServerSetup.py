import disnake
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import get

class SetupCommand(Cog):
    """A command that sets up the server."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="delete_all")
    async def delete_all(self, ctx):
        # Replace '1010578625814335588' with your server ID
        if ctx.guild.id != 1010578625814335588:
            await ctx.send("Sorry, this command can only be used in the specified server.")
            return

        for category in ctx.guild.categories:
            await category.delete()

        for channel in ctx.guild.channels:
            await channel.delete()

        await ctx.send("All channels and categories have been deleted.")

    @slash_command(name="setup")
    async def setup(self, interaction: disnake.ApplicationCommandInteraction):
        role_names = ["Server Admin", "Senior Admin", "Moderator", "Trial Moderator", "Unverified", "Verified", "Wick Verified", "Staff", "Greeter", "Server Owner"]
        channel_names = ["📂moderation", "📂dms", "📂reports", "📂transcripts", "waca-guard-audit", "✅│how-to-join", "🐛│bug-reports"]
        category_names = ["New Channels", "📬 | Support tickets"]

        roleExists, roleCreated, categoryExists, categoryCreated, channelExists, channelCreated = [], [], [], [], [], []

        await interaction.response.defer(with_message=True, ephemeral=False)

        # Check if the roles exist
        roles = {name: disnake.utils.get(interaction.guild.roles, name=name) for name in role_names}

        for name, role in roles.items():
            if role:
                roleExists.append(name)
            else:
                new_role = await interaction.guild.create_role(name=name)
                roleCreated.append(name)
                roles[name] = new_role

        # Check if the channels exist
        channels = {name: disnake.utils.get(interaction.guild.channels, name=name) for name in channel_names}
        categories = {name: disnake.utils.get(interaction.guild.categories, name=name) for name in category_names}

        for name, channel in channels.items():
            if channel:
                channelExists.append(name)

        for name, category in categories.items():
            if category:
                categoryExists.append(name)
            else:
                new_category = await interaction.guild.create_category_channel(name=name)
                categoryCreated.append(name)
                categories[name] = new_category

        newCat = categories["New Channels"]

        overwrites = {
            interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            roles["Verified"]: disnake.PermissionOverwrite(read_messages=True),
            roles["Moderator"]: disnake.PermissionOverwrite(read_messages=True),
            roles["Senior Admin"]: disnake.PermissionOverwrite(read_messages=True),
            roles["Trial Moderator"]: disnake.PermissionOverwrite(read_messages=True),
        }

        if not channels["🐛│bug-reports"]:
            bugReport = await interaction.guild.create_text_channel(name="🐛│bug-reports", overwrites=overwrites, category=newCat)
            channelCreated.append("Bug Reports")

        for name in ["📂moderation", "📂dms", "📂reports", "📂transcripts", "waca-guard-audit"]:
            if not channels[name]:
                new_channel = await interaction.guild.create_text_channel(name=name, overwrites=overwrites, category=newCat)
                channelCreated.append(name)

        if not channels["✅│how-to-join"]:
            joinInfo_overwrites = {
                interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=True, send_messages=False),
                roles["Unverified"]: disnake.PermissionOverwrite(read_messages=False),
            }
            joinInfo = await interaction.guild.create_text_channel(name="✅│how-to-join", overwrites=joinInfo_overwrites, category=newCat)
            channelCreated.append("How-To-Join")

        if not categories["📬 | Support tickets"]:
            tickets = await interaction.guild.create_category_channel(name="📬 | Support tickets")
            categoryCreated.append("Tickets")

        def format_list(items):
            return ''.join([f"{item}\n" for item in items])

        embed = disnake.Embed(
            title="Server Setup Breakdown:",
            color=disnake.Color.green(),
        )

        embed.add_field(name="Existing Roles", value=format_list(roleExists))
        embed.add_field(name="Created Roles", value=format_list(roleCreated))
        embed.add_field(name="Existing Categories", value=format_list(categoryExists))
        embed.add_field(name="Created Categories", value=format_list(categoryCreated))
        embed.add_field(name="Existing Channels", value=format_list(channelExists))
        embed.add_field(name="Created Channels", value=format_list(channelCreated))

        await interaction.edit_original_response(embed=embed)

def setup(bot: Bot):
    bot.add_cog(SetupCommand(bot))
