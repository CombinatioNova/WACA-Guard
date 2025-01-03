import disnake
from disnake.ext import commands, tasks
import sqlite3
from datetime import datetime
from disnake.ui import Button
from disnake import TextInputStyle, ButtonStyle

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_tickets.start()

    def cog_unload(self):
        self.check_tickets.cancel()

    @commands.slash_command(description="ManualRun")
    async def manrun(self,
        inter: disnake.ApplicationCommandInteraction,):
        await inter.response.defer()
        guilds = self.bot.guilds
        for guild in guilds:
            support_channel = disnake.utils.get(guild.categories, name="📬 | Support tickets")
            
            if support_channel:
                unresolved_tickets = 0
                for channel in support_channel.channels:
                    unresolved_tickets += 1
                    
            try:
                if unresolved_tickets != 0:
                    channel = disnake.utils.get(guild.channels, name="💬│staff-chat")
                    embed = disnake.Embed(
                        title="Unresolved Tickets",
                        description=f"Total unresolved tickets in {guild.name}: {unresolved_tickets}",
                        color=disnake.Color.orange()
                    )
                    embed.set_author(
                        name="WACA-Guard Alert",
                        icon_url="https://cdn.discordapp.com/attachments/1125481298367094836/1261748715689873548/Warning4x.png?ex=6694168f&is=6692c50f&hm=c42b3a33842363358b8a96f7a7676e0cddbcbca236e45ed877d1dccade84b665&"
                    )
                    await channel.send(embed=embed)
                else: 
                    print("stopped mods' fury")
            except Exception as e:   
                print(e)                 
                continue
            success = disnake.Embed(
                title=f"Checked unresolved tickets",
                color=disnake.Colour.green(),
                timestamp=datetime.now())
            success.set_author(
                name="Operation Completed Successfully",
                icon_url="https://cdn.discordapp.com/attachments/1126547281081016482/1261812933642686565/check_circle_24dp_FFFFFF_FILL0_wght700_GRAD200_opsz48.png?ex=6694525e&is=669300de&hm=f3360b2b77301a628ec46b20bb1a4a58359becc04afa512e3f49f3386a2ae7ce&"
                )
            success.set_footer(
                text = f"WACA-Guard",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
            )
        await inter.edit_original_response(embed=success)
    @tasks.loop(hours=24)
    async def check_tickets(self):
        guilds = self.bot.guilds
        for guild in guilds:
            support_channel = disnake.utils.get(guild.categories, name="📬 | Support tickets")
            
            if support_channel:
                unresolved_tickets = 0
                for channel in support_channel.channels:
                    unresolved_tickets += 1
            try:
                if unresolved_tickets != 0:
                    channel = disnake.utils.get(guild.channels, name="💬│staff-chat")
                    embed = disnake.Embed(
                        title="Unresolved Tickets",
                        description=f"Total unresolved tickets in {guild.name}: {unresolved_tickets}",
                        color=disnake.Color.orange()
                    )
                    embed.set_author(
                        name="WACA-Guard Alert",
                        icon_url="https://cdn.discordapp.com/attachments/1125481298367094836/1261748715689873548/Warning4x.png?ex=6694168f&is=6692c50f&hm=c42b3a33842363358b8a96f7a7676e0cddbcbca236e45ed877d1dccade84b665&"
                    )
                    await channel.send(embed=embed)
                else: 
                    print("stopped mods' fury")
            except Exception as e:   
                print(e)                 
                continue

    @check_tickets.before_loop
    async def before_check_tickets(self):
        await self.bot.wait_until_ready()
def setup(bot):
    bot.add_cog(SupportCog(bot))
