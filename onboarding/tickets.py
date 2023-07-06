from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button, View
from disnake import TextInputStyle
import chat_exporter
import io
import aiofiles
import aiohttp
from datetime import datetime
suppVer = 2.1
dashVer = 1.1
designVer = 1.2
global av
class MoreOptions(View):
    def __init__(self):
        super().__init__()
        
        
        self.about_button = Button(style=disnake.ButtonStyle.secondary, label="About", custom_id=f"aboutTicket", emoji = "<:About:1124497314346700920>")
        self.bug_button = Button(style=disnake.ButtonStyle.danger, label="Report Bug", custom_id=f"bugReport", emoji = "🐞")
                            
        
        self.add_item(self.about_button)
        self.add_item(self.bug_button)

class StdRow(View):
    def __init__(self, user_id, author_id):
        super().__init__()
        self.close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
        self.menu = Button(custom_id=f"menu: {author_id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")

        self.add_item(self.menu)
        self.add_item(self.close)

class HomeRow(View):
    def __init__(self, user_id):
        super().__init__()
        self.joinProb = Button(label="Issue Joining", custom_id=f"joinProb: {user_id}",style=disnake.ButtonStyle.primary, emoji="<:Join:1124143628135186533>")
        self.report = Button(label="Report Violation", custom_id=f"report: {user_id}",style=disnake.ButtonStyle.primary, emoji = "<:Report:1124146580442857502>")
        self.other = Button(label="Other", custom_id=f"other: {user_id}",style=disnake.ButtonStyle.primary, emoji = "<:More:1124143631243169842>")

        self.add_item(self.joinProb)
        self.add_item(self.report)
        self.add_item(self.other)

class MoreStaffOptions(View):
    def __init__(self,ticket_id):
        super().__init__()
        
        self.claim_button = Button(style=disnake.ButtonStyle.green, label="Claim Ticket", custom_id=f"claim: {ticket_id}", emoji = "<:Claim:1124497312190828635>")
        self.about_button = Button(style=disnake.ButtonStyle.secondary, label="About", custom_id=f"aboutTicket", emoji = "<:About:1124497314346700920>")
        self.bug_button = Button(style=disnake.ButtonStyle.danger, label="Report Bug", custom_id=f"bugReport", emoji = "🐞")
        
        self.add_item(self.claim_button)
        self.add_item(self.about_button)
        self.add_item(self.bug_button)
        
        
class Ticket(Cog):
    def __init__(self,bot: Bot) -> None:
        self.bot = bot

    @slash_command(description="Make A Ticket Button")
    async def makebutton(self, inter: disnake.ApplicationCommandInteraction):
        av="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png"
        yes1 = Button(label="Contact Support",custom_id=f"open: {inter.author.id}",style=disnake.ButtonStyle.success, emoji = "<:Support:1124143632589520906>")
        appeal_url = 'https://smpwa.ca/appeal'
        appeal = Button(label='Appeal Ban', url=appeal_url, style=disnake.ButtonStyle.link, emoji = "<:Appeal:1124143624783941632> ")
        embed = disnake.Embed(title='Need help?', description=f'''
If you're having trouble in any way, shape, or form, feel free to reach out to us!

Click **Contact Support** below to get help dealing with join issues, griefing, theft, or any number of problems!
''', color=0xffa500)
        embed.set_thumbnail(av)
        embed.set_author( # Narcissism
            name="WACA-Support",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )
        # Send the embed to the channel
        await inter.channel.send(embed=embed, components = [yes1, appeal])
        await inter.response.send_message(f"<:wacayes:1109510617401917540> | Done!", ephemeral = True)
        
    @Cog.listener()
    async def on_button_click(self, inter):
        try:
            role = disnake.utils.get(inter.guild.roles, name="Staff")
        except:
            pass
        try:
            if inter.guild.id == 826107409906008085:
                role = disnake.utils.get(inter.user.guild.roles, name="Moderation Team")
            else:
                role = disnake.utils.get(inter.user.guild.roles, name="Staff")
        except:
            pass
        if inter.component.custom_id.startswith("back"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            await inter.channel.edit(name=f"🟢│ticket-{inter.author.display_name}")
            welcome_embed = disnake.Embed(
            title="Welcome to Your Help Dashboard!",
            description="""
Thank you for reaching out!

Please select a category from the buttons below:
""",
            timestamp=datetime.now(),
            color=0xFFFF00
            )
            
            welcome_embed.set_author(
                name="Support Dashboard",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
            
            welcome_embed.set_footer(
                text=f"{inter.author.name}'s Ticket",
                icon_url=inter.author.display_avatar
                )
            #welcome_embed.set_thumbnail(user.display_avatar)
            
            welcome_embed.add_field(name="<:Low:1124512597111214110> Priority", value="Low")
            welcome_embed.add_field(name="<:Status:1124145577312145509> Status", value="Choosing Problem Category...")
            welcome_embed.add_field(name="<:SupportAgent:1124145579321204746>  Support Agent", value="Unspecified")
            
            joinProb = Button(label="Issue Joining", custom_id=f"joinProb: {user_id}",style=disnake.ButtonStyle.primary, emoji="<:Join:1124143628135186533>")
            report = Button(label="Report Violation", custom_id=f"report: {user_id}",style=disnake.ButtonStyle.primary, emoji = "<:Report:1124146580442857502>")
            other = Button(label="Other", custom_id=f"other: {user_id}",style=disnake.ButtonStyle.primary, emoji = "<:More:1124143631243169842>")
            
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            
            await inter.response.edit_message(embed=welcome_embed,components=[menu,joinProb,report,other,close])
        if inter.component.custom_id.startswith("open"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            await inter.response.defer(with_message = True, ephemeral = True)
            bot = self.bot
            global name
            user = inter.user
            member = user
            name = user.display_name
            av=user.display_avatar
            overwrites = {
                member.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                get(member.guild.roles, name="Staff"): disnake.PermissionOverwrite(read_messages = True),
                inter.user: disnake.PermissionOverwrite(read_messages = True)}
            category = disnake.utils.get(member.guild.categories, name = "📬 | Support tickets")
            channel = await inter.user.guild.create_text_channel(f"🟢│ticket-{member.display_name}", overwrites=overwrites, category=category)
            welcome_embed = disnake.Embed(
            title="Welcome to Your Help Dashboard!",
            description="""
Thank you for reaching out!

Please select a category from the buttons below:
""",
            timestamp=datetime.now(),
            color=0xFFFF00
            )
            
            welcome_embed.set_author(
                name="Support Dashboard",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
            
            welcome_embed.set_footer(
                text=f"{inter.author.name}'s Ticket",
                icon_url=inter.author.display_avatar
                )
            #welcome_embed.set_thumbnail(user.display_avatar)
            
            welcome_embed.add_field(name="<:Low:1124512597111214110> Priority", value="Low")
            welcome_embed.add_field(name="<:Status:1124145577312145509> Status", value="Choosing Problem Category...")
            welcome_embed.add_field(name="<:SupportAgent:1124145579321204746>  Support Agent", value="Unspecified")
            
            joinProb = Button(label="Issue Joining", custom_id=f"joinProb: {user_id}",style=disnake.ButtonStyle.primary, emoji="<:Join:1124143628135186533>")
            report = Button(label="Report Violation", custom_id=f"report: {user_id}",style=disnake.ButtonStyle.primary, emoji = "<:Report:1124146580442857502>")
            other = Button(label="Other", custom_id=f"other: {user_id}",style=disnake.ButtonStyle.primary, emoji = "<:More:1124143631243169842>")
            
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            
            message = await channel.send(inter.user.mention, embed=welcome_embed)
            await message.edit(content="", embed=welcome_embed,components=[menu,joinProb,report,other,close])
            await inter.edit_original_response(f"<:wacayes:1109510617401917540> **TICKET CREATED:** Head on over to {channel.mention} to get some help!")
############################################ -- REPORT THING -- #####################################################



        elif inter.component.custom_id.startswith("report"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            theft = Button(label="Theft", custom_id=f"theft: {user_id}",style=disnake.ButtonStyle.primary, emoji="<:Theft:1124143633835233340>")
            grief = Button(label="Grief", custom_id=f"grief: {user_id}",style=disnake.ButtonStyle.primary, emoji="<:Grief:1126089989332144229>")
            hack = Button(label="Hacker", custom_id=f"hack: {user_id}",style=disnake.ButtonStyle.primary, emoji="<:Hack:1126090342157013042>")
            back = Button(label="Back", custom_id=f"back: {user_id}",style=disnake.ButtonStyle.success, emoji="<:Back:1126089988187107380>")
            await inter.channel.edit(name=f"🟡│report-{inter.author.display_name}")
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            embed = inter.message.embeds[0]
            embed.set_author(
                name="Support Dashboard",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
            
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Waiting for Selection...")
            embed.title = "Choose What to Report"
            embed.description = """
Please choose what incident you would like to report with using the buttons below!
"""
            
            await inter.response.edit_message(embed = embed, components=[menu,theft,grief,hack,close])

        elif inter.component.custom_id.startswith("theft"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            
            await inter.channel.edit(name=f"🟡│theft-{inter.author.display_name}")
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            embed = inter.message.embeds[0]
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Waiting for Staff Response...")
            embed.set_field_at(0,name="<:Priority:1124145576074805268> Priority", value="Medium")
             
            embed.title = "Please tell us..."
            embed.description = """

<:arrow5:1023715845748305961> **What** was stolen?

<:arrow5:1023715845748305961> What are the X and Z **coordinates** where the items were stolen? (Use F3 if you're on Java. If you're on bedrock, just tell us roughly where it is!)

<:arrow5:1023715845748305961> Do you know **who** might have stolen it?

We understand that getting your stuff stolen can be really frustrating. We're here to make sure your stuff gets back safe and sound!



"""
            
            await inter.response.edit_message(embed = embed, components=[menu,close])
            message = await inter.channel.send(role.mention)
            await message.delete()


        elif inter.component.custom_id.startswith("grief"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            await inter.channel.edit(name=f"🟡│grief-{inter.author.display_name}")
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            embed = inter.message.embeds[0]
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Waiting for Staff Response...")
            embed.set_field_at(0,name="<:Priority:1124145576074805268> Priority", value="Medium")
             
            embed.title = "Please tell us..."
            embed.description = """

<:arrow5:1023715845748305961> **What** was griefed?

<:arrow5:1023715845748305961> What are the X and Z **coordinates** where the grief happened? (Use F3 if you're on Java. If you're on bedrock, just tell us roughly where it is!)

<:arrow5:1023715845748305961> Do you know **who** might have griefed?

We understand that getting griefed can be really frustrating. We're here to make sure your stuff is restored!


"""
            
            await inter.response.edit_message(embed = embed, components=[menu,close])
            message = await inter.channel.send(role.mention)
            await message.delete()
        elif inter.component.custom_id.startswith("hack"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            await inter.channel.edit(name=f"🔴│hack-{inter.author.display_name}")
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            embed = inter.message.embeds[0]
            embed.color=disnake.Color.red()
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Waiting for Staff Response...")
            embed.set_field_at(0,name="<:High:1124512819895877693> Priority", value="High")
             
            embed.title = "Please tell us..."
            embed.description = """

<:arrow5:1023715845748305961> **Who** was hacking?

<:arrow5:1023715845748305961> **What** was the hack?

<:arrow5:1023715845748305961> **When** did this happen?

**We will get back to you shortly about this issue! Thank you for your patience!**


"""
            
            await inter.response.edit_message(embed = embed, components=[menu,close])
            await inter.channel.send(f"**HIGH PRIORITY!** {role.mention}")
        
            
        elif inter.component.custom_id.startswith("joinProb"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            await inter.channel.edit(name=f"🟡│join-{inter.author.display_name}")
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            
            embed = inter.message.embeds[0]
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Waiting for Staff Response...")
            embed.set_field_at(0,name="<:Priority:1124145576074805268> Priority", value="Medium")

            match inter.guild.id:
                
############################################################################################################################################################################################################

                case 912725322166829116: #SMPWACA
                    embed.title = "Please write what your join issue is:"
                    embed.description = """

        **Before we begin, have you tried...**

        <:arrow5:1023715845748305961> Making sure to enable Direct Messages from server members?

        <:arrow5:1023715845748305961> (If on Console, Mobile, Switch, or Windows 10 Edition) Using the Bedrock port 19132?

        <:arrow5:1023715845748305961> Using the IP play.smpwaca.com?

        """
                    user = await self.bot.fetch_user(1032680296396636191)
                    embed.add_field(name=f":link: Send the Code to:", value = user.mention)
                    embed.add_field(name=f":computer: Server Version:", value = "1.19.3")
                    embed.add_field(name=f":closed_lock_with_key: Registration Command:", value = "/register (Password)")
                    
############################################################################################################################################################################################################

                case 826107409906008085: #Tortopia
                    embed.title = "Please write what your join issue is:"
                    embed.description = """

        **Before we begin, have you tried...**

        <:arrow5:1023715845748305961> Making sure the Modpack is up to date?

        <:arrow5:1023715845748305961> Checking announcements for downtime?

        <:arrow5:1023715845748305961> Using the IP tortopia.netwaca.com:25096?

        """
                    
                    
############################################################################################################################################################################################################

                case 1069398385758580757: #Parabellum
                    embed.title = "Please write what your join issue is:"
                    embed.description = """

        **Before we begin, have you tried...**

        <:arrow5:1023715845748305961> Making sure to enable Direct Messages from server members?

        <:arrow5:1023715845748305961> (If on Console, Mobile, Switch, or Windows 10 Edition) Using the Bedrock port 19132?

        <:arrow5:1023715845748305961> Using the IP parabellum.netwaca.com?

        """
                    user = await self.bot.fetch_user(1032680296396636191)
                    embed.add_field(name=f":link: Send the Code to:", value = user.mention)
                    embed.add_field(name=f":computer: Server Version:", value = "1.19.2")
                    embed.add_field(name=f":closed_lock_with_key: Registration Command:", value = "/register (Password)")
                    
############################################################################################################################################################################################################

                case 854938852599005196: #Character SMP
                    embed.title = "Please write what your join issue is:"
                    embed.description = """

        **Before we begin, have you tried...**

        <:arrow5:1023715845748305961> Making sure to enable Direct Messages from server members?

        <:arrow5:1023715845748305961> (If on Console, Mobile, Switch, or Windows 10 Edition) Using the Bedrock port 19132?

        <:arrow5:1023715845748305961> Using the IP character.netwaca.com?

        """
                    user = await self.bot.fetch_user(1047760428115173419)
                    embed.add_field(name=f":link: Send the Code to:", value = user.mention)
                    embed.add_field(name=f":computer: Server Version:", value = "1.19.2")
                    embed.add_field(name=f":closed_lock_with_key: Registration Command:", value = "/register (Password)")

                case _:                

                    embed.title = "Please write what your join issue is:"
                    embed.description = """
Feel free to write about whatever problems you have 
        """
            
            reset = Button(label="Reset Password", custom_id=f"PasswordReset: {inter.author.id}",style=disnake.ButtonStyle.danger, emoji = "<:PasswordReset:1126089980985483274>")
            if inter.guild.id == 912725322166829116:
                
                await inter.response.edit_message(embed = embed, components=[menu, reset, close])
            else:
                await inter.response.edit_message(embed = embed, components=[menu, close])
            message = await inter.channel.send(role.mention)
            await message.delete()
############################################ -- TICKET CLAIMING -- #####################################################
        elif inter.component.custom_id.startswith("PasswordReset"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            await inter.channel.edit(name=f"🟡│reset-{inter.author.display_name}")
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            
            embed = inter.message.embeds[0]
            embed.title = "Please wait for our staff team to assist you..."
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Waiting for Reset...")
            embed.remove_field(3)
            embed.remove_field(4)
            embed.remove_field(5)
            embed.description = """
**Thank you for reaching out!**

We'll make sure to have your password reset ASAP! Please be ready to join the Minecraft Server when we're ready! 
"""
            
            await inter.channel.send(f"**Password Reset Requested!** {role.mention}")
            await inter.response.edit_message(embed = embed, components=[menu, close])
                






                
        elif inter.component.custom_id.startswith("aboutTicket"):
            embed = disnake.Embed(title="About Tickets:",
                                  color=disnake.Color.green(),
                                  timestamp = datetime.now())
            embed.add_field(name="<:Support:1124143632589520906> Network Support System Ver.",value=suppVer, inline = False)
            embed.add_field(name="<:SupportAgent:1124145579321204746> Support Dashboard Ver.",value=dashVer, inline = False)
            embed.add_field(name="<:DesignTeam:1079422156397621309> WACA-Design Ver.",value=designVer, inline = False)
            await inter.response.send_message(embed=embed, ephemeral = True)


        elif inter.component.custom_id.startswith("bugReport"):
            # Reason input field
            reason_input = disnake.ui.TextInput(
                label="Reason:",
                placeholder="Enter the new reason...",
                min_length=1,
                max_length=256,
                custom_id=f"bug_reason"
            )
            modal = disnake.ui.Modal(title="Bug Report",custom_id=f"bugReportModal", components=[reason_input])
            await inter.response.send_modal(modal)
            
        elif inter.component.custom_id.startswith("menu"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            user = await self.bot.fetch_user(user_id)
            
            if "Staff" in [r.name for r in inter.author.roles]:
                more_options = MoreStaffOptions(inter.message.id)
                await inter.response.send_message("Staff Options:", view=more_options, ephemeral=True)
            else:
                more_options = MoreOptions()
                await inter.response.send_message("Options:", view=more_options, ephemeral=True)

            
        elif inter.component.custom_id.startswith("claim"):
            message_id = int(inter.component.custom_id.split(": ")[1])
            message = await inter.channel.fetch_message(message_id)
            
            embed = message.embeds[0]
            embed.color=disnake.Color.green()
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Ticket Claimed by Staff!")
            embed.set_field_at(2,name="<:SupportAgent_1:1124512599850111118>  Support Agent", value=inter.author.display_name)

            await message.edit(embed = embed)
            await inter.response.edit_message("Ticket Claimed!")

            
############################################ -- OTHER -- #####################################################






            
        elif inter.component.custom_id.startswith("other"):
            user_id = int(inter.component.custom_id.split(": ")[1])
            close = Button(label="Close Ticket", custom_id=f"close: {user_id}",style=disnake.ButtonStyle.danger)
            menu = Button(custom_id=f"menu: {inter.author.id}",style=disnake.ButtonStyle.secondary, emoji = "<:menu:1124096544606531635>")
            await inter.channel.edit(name=f"🟢│other-{inter.author.display_name}")


            embed = inter.message.embeds[0]
            embed.title = "Please tell us how we can help you..."
            embed.set_author(
                name="Support Dashboard",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
            embed.set_field_at(0,name="<:Low:1124512597111214110> Priority", value="Low")
            embed.set_field_at(1,name="<:Status:1124145577312145509> Status", value="Waiting for Staff Response...")
            embed.description = """
As you wait for our friendly staff to assist you, please give us as much information as you can on why you are here!
"""
            
            await inter.response.edit_message(embed = embed, components=[menu, close])
            message = await inter.channel.send(role.mention)
            await message.delete()
            
        elif inter.component.custom_id.startswith("close"):
            await inter.response.defer(with_message = True, ephemeral = True)
            bot = self.bot
            user_id = int(inter.component.custom_id.split(": ")[1])
            user = await self.bot.fetch_user(user_id)
            if inter.channel.category.name.startswith("📬 | Support tickets"):
                
                transcript = await chat_exporter.export(
                    inter.channel,
                    limit=10000,
                    tz_info="UTC",
                    military_time=False,
                    bot=bot,
                )

                if transcript is None:
                    return

                transcript_file = disnake.File(
                    io.BytesIO(transcript.encode()),
                    filename=f"transcript-{inter.channel.name}-{datetime.now()}.html",
                )

                
                channel = disnake.utils.get(inter.guild.channels, name="📂transcripts")
                
                
                log = disnake.Embed(
                    title=f"{user.display_name}, Your Case is Closed!", # Smart or smoothbrain?????
                    color=disnake.Colour.brand_green(), # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
                    timestamp=datetime.now(), #Get the datetime... now...
                    description=f"The transcript of **#{inter.channel.name}** (**{inter.channel.id}**) has been saved! View below:")
                log.set_author(name="WACA-Support Log",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
                log.set_footer( # Show the moderator
                text=f"Closed by: {inter.author.name}",
                icon_url=inter.author.display_avatar)

                toSend = disnake.Embed(
                    title=f"{user.display_name}, Your case is closed!", # Smart or smoothbrain?????
                    color=disnake.Colour.brand_green(), # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
                    timestamp=datetime.now(), #Get the datetime... now...
                    description=f"""The transcript of **#{inter.channel.name}** (**{inter.channel.id}**) has been saved!

**Please rate your support experience:**""",
                )
                toSend.set_author(
                name="WACA-Support Notification",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
                )
                toSend.set_footer( # Show the moderator
                text=f"Closed by: {inter.author.name}",
                icon_url=inter.author.display_avatar,
                )


                veryUnhappy = Button(custom_id=f"veryUnhappy_{inter.guild.id}",style=disnake.ButtonStyle.danger, emoji = "<:VeryDissatisfied:1123679089149087885>")
                unhappy = Button(custom_id=f"unhappy_{inter.guild.id}",style=disnake.ButtonStyle.secondary, emoji = "<:Dissatisfied:1123679077816090705>")
                neutral = Button(custom_id=f"neutral_{inter.guild.id}",style=disnake.ButtonStyle.secondary, emoji = "<:Neutral:1123679079158251603> ")
                happy = Button(custom_id=f"happy_{inter.guild.id}",style=disnake.ButtonStyle.secondary, emoji = "<:Satisfied:1123679081423196260>")
                veryHappy = Button(custom_id=f"veryHappy_{inter.guild.id}",style=disnake.ButtonStyle.success, emoji = "<:VerySatisfied:1123679086737358889>")



                
                try:
                    await channel.send(embed=log) #Send the shit
                    await channel.send(file=transcript_file)
                except:
                    pass
                
                if user_id == inter.author.id:
                    await inter.author.send(embed=toSend, components = [veryHappy,happy,neutral,unhappy,veryUnhappy])
                    await inter.author.send(file=transcript_file)
                else:
                    await user.send(embed=toSend,components = [veryHappy,happy,neutral,unhappy,veryUnhappy])
                    await user.send(file=transcript_file)
                await inter.channel.delete()
                await inter.edit_original_response("Sent to Transcripts!")
                
            else:
                await inter.edit_original_response("No.")

############################################ -- REACTION THINGS -- #####################################################
        elif inter.component.custom_id.startswith("veryHappy"):
            guild_id = int(inter.component.custom_id.split("_")[1])
            guild = self.bot.get_guild(guild_id)
            channel = disnake.utils.get(guild.channels, name="📂transcripts")
            ogEmbed = inter.message.embeds[0]
            embed = disnake.Embed(title=f"{inter.author.display_name} feels Very Happy with their service! Great work!",
                                  color=disnake.Color.green(),
                                  timestamp = datetime.now())
            await channel.send(embed=embed)
            veryUnhappy = Button(custom_id=f"veryUnhappy",style=disnake.ButtonStyle.danger, emoji = "<:VeryDissatisfied:1123679089149087885>",disabled=True)
            unhappy = Button(custom_id=f"unhappy",style=disnake.ButtonStyle.secondary, emoji = "<:Dissatisfied:1123679077816090705>",disabled=True)
            neutral = Button(custom_id=f"neutral",style=disnake.ButtonStyle.secondary, emoji = "<:Neutral:1123679079158251603> ",disabled=True)
            happy = Button(custom_id=f"happy",style=disnake.ButtonStyle.secondary, emoji = "<:Satisfied:1123679081423196260>",disabled=True)
            veryHappy = Button(custom_id=f"veryHappy",style=disnake.ButtonStyle.success, emoji = "<:VerySatisfied:1123679086737358889>",disabled=True)
            await inter.response.edit_message(embed=ogEmbed, components = [veryHappy,happy,neutral,unhappy,veryUnhappy])
        elif inter.component.custom_id.startswith("happy"):
            guild_id = int(inter.component.custom_id.split("_")[1])
            guild = self.bot.get_guild(guild_id)
            channel = disnake.utils.get(guild.channels, name="📂transcripts")
            ogEmbed = inter.message.embeds[0]
            embed = disnake.Embed(title=f"{inter.author.display_name} feels Happy with their service! Good job!",
                                  color=disnake.Color.green(),
                                  timestamp = datetime.now())
            await channel.send(embed=embed)
            veryUnhappy = Button(custom_id=f"veryUnhappy",style=disnake.ButtonStyle.danger, emoji = "<:VeryDissatisfied:1123679089149087885>",disabled=True)
            unhappy = Button(custom_id=f"unhappy",style=disnake.ButtonStyle.secondary, emoji = "<:Dissatisfied:1123679077816090705>",disabled=True)
            neutral = Button(custom_id=f"neutral",style=disnake.ButtonStyle.secondary, emoji = "<:Neutral:1123679079158251603> ",disabled=True)
            happy = Button(custom_id=f"happy",style=disnake.ButtonStyle.secondary, emoji = "<:Satisfied:1123679081423196260>",disabled=True)
            veryHappy = Button(custom_id=f"veryHappy",style=disnake.ButtonStyle.success, emoji = "<:VerySatisfied:1123679086737358889>",disabled=True)
            await inter.response.edit_message(embed=ogEmbed, components = [veryHappy,happy,neutral,unhappy,veryUnhappy])
        elif inter.component.custom_id.startswith("neutral"):
            guild_id = int(inter.component.custom_id.split("_")[1])
            guild = self.bot.get_guild(guild_id)
            channel = disnake.utils.get(guild.channels, name="📂transcripts")
            ogEmbed = inter.message.embeds[0]
            embed = disnake.Embed(title=f"{inter.author.display_name} feels Neutral with their service. Let's see if we can get that higher!",
                                  color=16742431,
                                  timestamp = datetime.now())
            await channel.send(embed=embed)
            veryUnhappy = Button(custom_id=f"veryUnhappy",style=disnake.ButtonStyle.danger, emoji = "<:VeryDissatisfied:1123679089149087885>",disabled=True)
            unhappy = Button(custom_id=f"unhappy",style=disnake.ButtonStyle.secondary, emoji = "<:Dissatisfied:1123679077816090705>",disabled=True)
            neutral = Button(custom_id=f"neutral",style=disnake.ButtonStyle.secondary, emoji = "<:Neutral:1123679079158251603> ",disabled=True)
            happy = Button(custom_id=f"happy",style=disnake.ButtonStyle.secondary, emoji = "<:Satisfied:1123679081423196260>",disabled=True)
            veryHappy = Button(custom_id=f"veryHappy",style=disnake.ButtonStyle.success, emoji = "<:VerySatisfied:1123679086737358889>",disabled=True)
            await inter.response.edit_message(embed=ogEmbed, components = [veryHappy,happy,neutral,unhappy,veryUnhappy])
        elif inter.component.custom_id.startswith("unhappy"):
            guild_id = int(inter.component.custom_id.split("_")[1])
            guild = self.bot.get_guild(guild_id)
            channel = disnake.utils.get(guild.channels, name="📂transcripts")
            ogEmbed = inter.message.embeds[0]
            embed = disnake.Embed(title=f"{inter.author.display_name} feels Unhappy with their service. Make sure we keep those ratings up!",
                                  color=disnake.Color.red(),
                                  timestamp = datetime.now())
            await channel.send(embed=embed)
            veryUnhappy = Button(custom_id=f"veryUnhappy",style=disnake.ButtonStyle.danger, emoji = "<:VeryDissatisfied:1123679089149087885>",disabled=True)
            unhappy = Button(custom_id=f"unhappy",style=disnake.ButtonStyle.secondary, emoji = "<:Dissatisfied:1123679077816090705>",disabled=True)
            neutral = Button(custom_id=f"neutral",style=disnake.ButtonStyle.secondary, emoji = "<:Neutral:1123679079158251603> ",disabled=True)
            happy = Button(custom_id=f"happy",style=disnake.ButtonStyle.secondary, emoji = "<:Satisfied:1123679081423196260>",disabled=True)
            veryHappy = Button(custom_id=f"veryHappy",style=disnake.ButtonStyle.success, emoji = "<:VerySatisfied:1123679086737358889>",disabled=True)
            await inter.response.edit_message(embed=ogEmbed, components = [veryHappy,happy,neutral,unhappy,veryUnhappy])
        elif inter.component.custom_id.startswith("veryUnhappy"):
            guild_id = int(inter.component.custom_id.split("_")[1])
            guild = self.bot.get_guild(guild_id)
            channel = disnake.utils.get(guild.channels, name="📂transcripts")
            ogEmbed = inter.message.embeds[0]
            embed = disnake.Embed(title=f"{inter.author.display_name} feels Very Unhappy with their service. Make sure we keep those ratings up!",
                                  color=disnake.Color.red(),
                                  timestamp = datetime.now())
            await channel.send(embed=embed)
            veryUnhappy = Button(custom_id=f"veryUnhappy",style=disnake.ButtonStyle.danger, emoji = "<:VeryDissatisfied:1123679089149087885>",disabled=True)
            unhappy = Button(custom_id=f"unhappy",style=disnake.ButtonStyle.secondary, emoji = "<:Dissatisfied:1123679077816090705>",disabled=True)
            neutral = Button(custom_id=f"neutral",style=disnake.ButtonStyle.secondary, emoji = "<:Neutral:1123679079158251603> ",disabled=True)
            happy = Button(custom_id=f"happy",style=disnake.ButtonStyle.secondary, emoji = "<:Satisfied:1123679081423196260>",disabled=True)
            veryHappy = Button(custom_id=f"veryHappy",style=disnake.ButtonStyle.success, emoji = "<:VerySatisfied:1123679086737358889>",disabled=True)
            await inter.response.edit_message(embed=ogEmbed, components = [veryHappy,happy,neutral,unhappy,veryUnhappy])
            
    @Cog.listener()
    async def on_modal_submit(self, inter: disnake.ModalInteraction):

        if inter.custom_id.startswith("bugReportModal"):
            dic=inter.text_values
            reason=dic[f"bug_reason"]
            
            embed = disnake.Embed(title = "Bug Reported!",
                                  color = 4143049,
                                  timestamp=datetime.now())
            
            embed.add_field(name="<:Note:1124096605944037438> Bug Reported:",value=reason, inline = True)
            embed.add_field(name="<:Staff:1124124862487732255> Reported By:",value=inter.author.display_name, inline = True)
            channel = disnake.utils.get(inter.guild.channels, name="🐛│bug-reports")
            await channel.send(embed=embed)
            await inter.response.send_message("Bug reported! Thank you!", ephemeral = True)







   

    @Cog.listener()
    async def on_guild_channel_create(self, channel):
        # Check if the created channel is within the "Support tickets" category
        if isinstance(channel.category, disnake.CategoryChannel) and channel.category.name == "📬 | Support tickets":
            await self.organize_channels(channel.guild, channel.category)

    @Cog.listener()
    async def on_guild_channel_update(self, before, after):
        # Check if the updated channels are within the "Support tickets" category and have different names
        if (
            isinstance(before.category, disnake.CategoryChannel)
            and isinstance(after.category, disnake.CategoryChannel)
            and before.category.name == "📬 | Support tickets"
            and after.category.name == "📬 | Support tickets"
            and before.name != after.name
        ):
            await self.organize_channels(after.guild, after.category)

    async def organize_channels(self, guild, category):
        # Fetch all channels within the category
        channels = category.text_channels

        # Define a custom comparison function for sorting
        def channel_sort_key(channel):
            priority_emojis = {
                "🔴": 0,
                "🟡": 1,
                "🟢": 2,
                "📝": 3
            }
            priority = priority_emojis.get(channel.name.split("│")[0], 3)  # Default to 3 if no priority emoji found
            return (priority, channel.name.lower())

        channels = category.text_channels
        sorted_channels = sorted(channels, key=channel_sort_key, reverse=False)
        positions = {channel: index for index, channel in enumerate(sorted_channels)}

        # Find the channel that is farthest from its initial spot
        farthest_channel = max(channels, key=lambda c: abs(c.position - positions[c]))

        # Move the farthest channel to its correct position
        if farthest_channel.position != positions[farthest_channel]:
            try:
                await farthest_channel.edit(position=positions[farthest_channel])
                print(f"Edited channel {farthest_channel.name} in guild {guild.name} at position {positions[farthest_channel]}.")
            except disnake.HTTPException as e:
                print(f"Failed to edit channel {farthest_channel.name} in guild {guild.name}: {e}")

        # Recheck if everything else is in the right spot
        for channel in channels:
            if channel.position != positions[channel]:
                try:
                    await channel.edit(position=positions[channel])
                    print(f"Edited channel {channel.name} in guild {guild.name} at position {positions[channel]}.")
                except disnake.HTTPException as e:
                    print(f"Failed to edit channel {channel.name} in guild {guild.name}: {e}")
            
def setup(bot: Bot) -> None:
    bot.add_cog(Ticket(bot)) 
