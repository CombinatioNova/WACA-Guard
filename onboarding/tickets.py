from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button
from disnake import TextInputStyle
import chat_exporter
import io
import aiofiles
import aiohttp
from datetime import datetime

global av
class Ticket(Cog):
    def __init__(self,bot: Bot) -> None:
        self.bot = bot

    @slash_command(description="Make A Ticket Button")
    async def makebutton(self, inter: disnake.ApplicationCommandInteraction):
        av="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png"
        yes1 = Button(label="Open a Ticket",custom_id=f"open",style=disnake.ButtonStyle.success)
        appeal_url = 'https://smpwa.ca/appeal'
        appeal = Button(label='Submit a Ban Appeal!', url=appeal_url, style=disnake.ButtonStyle.link)
        embed = disnake.Embed(title='Need some help?', description=f'''Open a support ticket using the **button below** to get help from our friendly staff team!
        
Our staff team is here to help with any issue you might have! From theft, to petty disagreements, we're here to help you solve any problem you might face!''', color=0xffa500)
        embed.set_thumbnail(av)
        embed.set_author( # Narcissism
            name="WACA-Support",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )
        # Send the embed to the channel
        await inter.channel.send(embed=embed, components = [yes1, appeal])
        await inter.response.send_message(f"Done!", ephemeral = True)
    @Cog.listener()
    async def on_button_click(self, inter):
        if inter.guild.id == 826107409906008085:
            role = disnake.utils.get(inter.user.guild.roles, name="Moderation Team")
        else:
            role = disnake.utils.get(inter.user.guild.roles, name="Staff")
        
        if inter.component.custom_id.startswith("open"):
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
            await inter.response.send_message(f"Head on over to {channel.mention} to get some help!", ephemeral = True)


      

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
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
Thank you for reaching out! We know that having trouble joining can be *really* frustrating, and we hope your problem will be resolved!

As we wait for our helpful staff to be with you, __**please describe your issue to us:**__""",
                    
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
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
While you wait for help from our {role.mention}, please let us know the following:

**Where was it? Please give exact F3 screen coordinates.**

**If you know who did it, who did?**

**What did they grief?**""",
                    
                    color=disnake.Colour.brand_green())
            await inter.response.send_message(embed = log)                                 

        elif inter.component.custom_id.startswith("theft"):
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary)
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary)
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary)
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary)
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary,row=1)
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger,row=1)

            joinProb.disabled = True
            exploit.disabled = True
            grief.disabled = True
            theft.disabled = True
            other.disabled = True
            await inter.message.edit(components=[joinProb,exploit,grief,theft,other,close])
            await inter.channel.edit(name=f"theft-{inter.author.display_name}")
            log = disnake.Embed(
                    title=f"Thanks, {inter.author.name}!", # Smart or smoothbrain?????
                    description=f"""
While you wait for help from our {role.mention}, please let us know the following:

**Where was it? Please give exact F3 screen coordinates.**

**If you know who did it, who did?**

**What did they take?**""",
                    
                    color=disnake.Colour.brand_green())
            await inter.response.send_message(embed = log)

        elif inter.component.custom_id.startswith("other"):
            joinProb = Button(label="Trouble Joining", custom_id=f"joinProb",style=disnake.ButtonStyle.primary)
            exploit = Button(label="Hacking", custom_id=f"exploit",style=disnake.ButtonStyle.primary)
            grief = Button(label="Griefer", custom_id=f"grief",style=disnake.ButtonStyle.primary)
            theft = Button(label="Theft", custom_id=f"theft",style=disnake.ButtonStyle.primary)
            other = Button(label="Something Else", custom_id=f"other",style=disnake.ButtonStyle.primary,row=1)
            close = Button(label="Close Ticket", custom_id=f"close",style=disnake.ButtonStyle.danger,row=1)

            joinProb.disabled = True
            exploit.disabled = True
            grief.disabled = True
            theft.disabled = True
            other.disabled = True
            await inter.message.edit(components=[joinProb,exploit,grief,theft,other,close])
            await inter.channel.edit(name=f"other-{inter.author.display_name}")
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
    bot.add_cog(Ticket(bot)) 
