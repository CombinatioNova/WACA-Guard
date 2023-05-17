#Support Ticket Direction
from disnake.ext.commands import Bot, Cog, slash_command
import disnake
import json
from disnake.utils import get
import fuzzywuzzy
from fuzzywuzzy import fuzz,process
from disnake.ui import Button
import logging
from disnake import PartialEmoji

from datetime import datetime
import io
import asyncio

import chat_exporter
logging.getLogger().setLevel(logging.ERROR)
class Support(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    @Cog.listener()
    async def on_message(self,message):
        bot=self.bot
        server_ip_patterns = ['what is the server ip', 'whats the server ip',"whats the ip","!ip"]
        join_patterns = ['how do i join', 'how do i join the server', 'how do i get on', "how to join","where do i send the code"]
        help_patterns = [
        "Can I get some help?",
    "Is there a staff member available?",
    "I need assistance please",
    "Help needed",
    "I have a problem and I need help",
    "Can someone help me?",
    "I need a staff member",
    "Help me please",
    "I am stuck and I need help",
    "Can a staff member assist me?",
    "Can you point me in the right direction?",
    "I would appreciate some help with this.",
    "I need help joining",
    "are any staff online?",
    "Is there a staff member online?",
         "im stuck joining","i can't join","this is bugged","i found a bug"
                     ]
        crashed_patterns = [
        "server crashed","the server room is on fire","did the server crash","i think the server crashed","idk about you but the server clearly crashed","the server just crashed", "it just crashed"
            ]
        if message.author == self.bot.user:
            return
        server_ip_response = process.extractOne(message.content, server_ip_patterns, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=80)
        join_response = process.extractOne(message.content, join_patterns, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=70)
        help_response = process.extractOne(message.content, help_patterns, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=70)
        crashed_response = process.extractOne(message.content, crashed_patterns, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=70)
     
        if server_ip_response:
            # Create the embed
            embed = disnake.Embed(title='Join the server!', description='Join through play.smpwaca.com! The server is in 1.19.3. Make sure to send the code to the Server Information bot!', color=0x00ff00)

            # Send the embed to the channel
            await message.channel.send(embed=embed)
        if join_response:
            # Create the embed
            embed = disnake.Embed(title='Join the server!', description='Join through play.smpwaca.com! The server is in 1.19.3. Make sure to send the code to the Server Information bot!', color=0x00ff00)
        if help_response:
        # Create the embed
            channel = bot.get_channel(913208895017717810)
            yes1 = Button(label="Yes",custom_id=f"yes1",style=disnake.ButtonStyle.success)
            no1 = Button(label="No",custom_id=f"no1",style=disnake.ButtonStyle.danger)
            embed = disnake.Embed(title='Do you need help?', description=f'Use the channel  to open a support ticket to get help! \nWould you like me to open a ticket for you now?', color=0xffa500)

            # Send the embed to the channel
            await message.channel.send(embed=embed, components = [yes1, no1])
        if crashed_response:
            yesCrash = Button(label="Yes",custom_id=f"yesCrash",style=disnake.ButtonStyle.success)
            noCrash = Button(label="No",custom_id=f"noCrash",style=disnake.ButtonStyle.danger)
            embed = disnake.Embed(title='Did the server crash?', description=f'I heard some people talking about a crash. Is this true? Please use the buttons below to answer.', color=0xffa500)

            # Send the embed to the channel
            await message.channel.send(embed=embed, components = [yesCrash, noCrash])
    @Cog.listener()
    async def on_button_click(self, inter):
        
        role = disnake.utils.get(inter.user.guild.roles, name="Staff")
        if inter.component.custom_id.startswith("yesCrash"):
            yesCrash = Button(label="Yes",custom_id=f"yesCrash",style=disnake.ButtonStyle.success)
            noCrash = Button(label="No",custom_id=f"noCrash",style=disnake.ButtonStyle.danger)
            yesCrash.disabled = True
            noCrash.disabled = True
            await inter.message.edit(components=[yesCrash,noCrash])
            bug_report = disnake.Embed(
                title = "Server Crash!",
                description = f"WACA-Guard has detected a potential crashed server which hass been confirmed by {inter.user.display_name}.",
                timestamp=datetime.now(),
                color=0xFFFF00
                )
            bug_report.set_author(
                name="WACA-Guard",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
            channel = self.bot.get_channel(972240498603483277)
            await channel.send(embed=bug_report)
            
            await inter.response.send_message("Got it! Thank you for letting us know. The crash has been reported!")
        if inter.component.custom_id.startswith("noCrash"):
            yesCrash = Button(label="Yes",custom_id=f"yesCrash",style=disnake.ButtonStyle.success)
            noCrash = Button(label="No",custom_id=f"noCrash",style=disnake.ButtonStyle.danger)
            yesCrash.disabled = True
            noCrash.disabled = True
            await inter.message.edit(components=[yesCrash,noCrash])
            await inter.response.send_message("Got it! Thank you for letting us know!")
        if inter.component.custom_id.startswith("yes1"):
            bot = self.bot
            global name
            user = inter.user
            member = user
            name = user.display_name
            av=user.display_avatar
            overwrites = {
                member.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                get(member.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
                get(member.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
                get(member.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
                get(member.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),
                inter.user: disnake.PermissionOverwrite(read_messages = True)}
            category = disnake.utils.get(member.guild.categories, name = "📬 | Support tickets")
            channel = await inter.user.guild.create_text_channel(f"ticket-{member.display_name}", overwrites=overwrites, category=category)
            welcome_embed = disnake.Embed(
            title="Welcome to your support ticket!",
            description="""Hello there! Thank you for reaching out to us.

            We are here to help and will do our best to assist you with any questions or issues you may have. Thank you for your patience!

            Please pick out what problem you have today so we can better cater to you!""",
            timestamp=datetime.now(),
            color=0xFFFF00
            )
            welcome_embed.set_author(
                name="WACA-Support",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
            welcome_embed.set_footer(
                text=f"{inter.author.name}'s Ticket",
                icon_url=inter.author.display_avatar
                )
            welcome_embed.set_thumbnail(user.display_avatar)
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary)
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary)
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary)
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary)
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary)
            
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger)
            await channel.send(embed=welcome_embed,components=[joinProb,exploit,grief,theft,other,close])
            await channel.send(inter.user.mention)
            yes1 = Button(label="Yes",custom_id=f"yes1",style=disnake.ButtonStyle.success)
            no1 = Button(label="No",custom_id=f"no1",style=disnake.ButtonStyle.danger)
            yes1.disabled = True
            no1.disabled = True
            await inter.message.edit(components=[yes1,no1])
            await inter.response.send_message(f"Head on over to {channel.mention} to get some help!")


        elif inter.component.custom_id.startswith("no1"):
            yes1 = Button(label="Yes",custom_id=f"yes1",style=disnake.ButtonStyle.success)
            no1 = Button(label="No",custom_id=f"no1",style=disnake.ButtonStyle.danger)
            yes1.disabled = True
            no1.disabled = True
            await inter.message.edit(components=[yes1,no1])# Disable
            await inter.response.send_message(f"Alright, {inter.author.display_name}! I hope you've found everything you need. Feel free to reach out if you need help in the future!")


        elif inter.component.custom_id.startswith("joinProb"):
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary)
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary)
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary)
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary)
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary)
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger)

            joinProb.disabled = True
            exploit.disabled = True
            grief.disabled = True
            theft.disabled = True
            other.disabled = True
            await inter.message.edit(components=[joinProb,exploit,grief,theft,other,close])
            await inter.channel.edit(name=f"joining-{inter.author.display_name}")
            await inter.channel.send(role.mention)
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
While you wait for help from our {role.mention}, feel free to check out our wiki at https://wiki.smpwaca.com!

With that out of the way, **please describe your issue to us.**""",
                    
                    color=disnake.Colour.brand_green())
            await inter.response.send_message(embed = log)
            

        elif inter.component.custom_id.startswith("exploit"):
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary)
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary)
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary)
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary)
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary)
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger)

            joinProb.disabled = True
            exploit.disabled = True
            grief.disabled = True
            theft.disabled = True
            other.disabled = True
            await inter.message.edit(components=[joinProb,exploit,grief,theft,other,close])
            await inter.channel.edit(name=f"hack-{inter.author.display_name}")
            await inter.channel.send(role.mention)
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
While you wait for help from our {role.mention}, please give us the following information:

**Name of the exploiter/hacker**

**What they are doing**

**Any proof if you have it**

We'll get to you as soon as we can!""",
                    
                    color=disnake.Colour.brand_green())
            
            await inter.response.send_message(embed = log)

        elif inter.component.custom_id.startswith("grief"):
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary)
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary)
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary)
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary)
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary)
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger)

            joinProb.disabled = True
            exploit.disabled = True
            grief.disabled = True
            theft.disabled = True
            other.disabled = True
            await inter.message.edit(components=[joinProb,exploit,grief,theft,other,close])
            await inter.channel.edit(name=f"grief-{inter.author.display_name}")
            await inter.channel.send(role.mention)
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
While you wait for help from our {role.mention}, please let us know the following:

**Where was it? GIVE COORDINATES PLEASE**

**If you know who did it... Who did it?**

**What did they grief?**""",
                    
                    color=disnake.Colour.brand_green())
            await inter.response.send_message(embed = log)                                 

        elif inter.component.custom_id.startswith("theft"):
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":door:1079458385474363562"))
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":computer:1079458395762999306"))
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":firecracker:1079458406219382894"))
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":ninja:1079458415342010389"))
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary,row=1,emoji = PartialEmoji.from_str(":person_tipping_hand:1079458434732269568:"))
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger,row=1,emoji = PartialEmoji.from_str(":wave:1079458447461974127"))

            joinProb.disabled = True
            exploit.disabled = True
            grief.disabled = True
            theft.disabled = True
            other.disabled = True
            await inter.message.edit(components=[joinProb,exploit,grief,theft,other,close])
            await inter.channel.edit(name=f"theft-{inter.author.display_name}")
            await inter.channel.send(role.mention)
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
While you wait for help from our {role.mention}, please let us know the following:

**Where was it? GIVE COORDINATES PLEASE**

**If you know who did it... Who did it?**

**What did they take?**""",
                    
                    color=disnake.Colour.brand_green())
            await inter.response.send_message(embed = log)

        elif inter.component.custom_id.startswith("other"):
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":door:"))
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":computer:"))
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":firecracker:"))
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary,emoji = PartialEmoji.from_str(":ninja:"))
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary,row=1,emoji = PartialEmoji.from_str("a:person_tipping_hand::"))
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger,row=1,emoji = PartialEmoji.from_str(":wave:"))

            joinProb.disabled = True
            exploit.disabled = True
            grief.disabled = True
            theft.disabled = True
            other.disabled = True
            await inter.message.edit(components=[joinProb,exploit,grief,theft,other,close])
            await inter.channel.edit(name=f"other-{inter.author.display_name}")
            await inter.channel.send(role.mention)
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
While you wait for help from our {role.mention}, feel free to check out our wiki at https://wiki.smpwaca.com!

With that out of the way, **please describe your issue to us.**""",
                    
                    color=disnake.Colour.brand_green())
            await inter.response.send_message(embed = log)
        elif inter.component.custom_id.startswith("close"):
            bot = self.bot
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

                
                channel = bot.get_channel(913238399366885396)
                
                
                log = disnake.Embed(
                    title=f"{inter.channel.name} closed!", # Smart or smoothbrain?????
                    color=disnake.Colour.brand_green(), # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
                    timestamp=datetime.now(), #Get the datetime... now...
                    description=f"The transcript of **#{inter.channel.name}** (**{inter.channel.id}**) has been saved! View below:")
                log.set_author(name="WACA-Support Log",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
                log.set_footer( # Show the moderator
                text=f"Closed by: {inter.author.name}",
                icon_url=inter.author.display_avatar)

                toSend = disnake.Embed(
                    title=f"{inter.author.name}, Your case is closed!", # Smart or smoothbrain?????
                    color=disnake.Colour.brand_green(), # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
                    timestamp=datetime.now(), #Get the datetime... now...
                    description=f"The transcript of **#{inter.channel.name}** (**{inter.channel.id}**) has been saved! View below:",
                )
                toSend.set_author(
                name="WACA-Support Notification",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
                )
                toSend.set_footer( # Show the moderator
                text=f"Closed by: {inter.author.name}",
                icon_url=inter.author.display_avatar,
                )
                try:
                    await channel.send(embed=log) #Send the shit
                    await channel.send(file=transcript_file)
                except:
                    pass
                await inter.author.send(embed=toSend)
                await inter.author.send(file=transcript_file)
                await inter.channel.delete()
                await inter.response.send_message("Sent to Transcripts!", ephemeral=True)
            else:
                await inter.response.send_message("No.", ephemeral=True)
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))
