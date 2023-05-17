from disnake.ext.commands import Bot, Cog, slash_command, Param
import disnake
from disnake.utils import get
from disnake.ui import Button
from disnake import TextInputStyle

from datetime import datetime

global av
class Log(Cog):
    def __init__(self,bot: Bot) -> None:
        self.bot = bot

    @slash_command(description="Log a moderation action") #The actual command
    async def log(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str, notes: str = "N/A", punishment: str = Param(choices=["Verbal Warning", "1 Hour Ban", "3 Hour Ban", "6 Hour Ban","1 Day Ban", "3 Day Ban", "5 Day Ban", "7 Day Ban", "14 Day Ban", "Permanent Ban", "Permanent Ban Without Appeal"])):
        bot = self.bot
        global name
        name = user.display_name
        
        av=user.display_avatar
        log = disnake.Embed(
            title=f"{user.display_name}: {punishment}", # Smart or smoothbrain?????
            color=4143049, # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
            timestamp=datetime.now(), #Get the datetime... now...
        )
        
        log.set_author( # Narcissism
            name="SMPWACA Moderation",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )

        log.set_footer( # Show the moderator
            text=f"Logged by {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )

        log.set_thumbnail(user.display_avatar)

        log.add_field(name="Reason: ", value=reason, inline=False)
        log.add_field(name="Moderator Notes: ", value=notes, inline = False)

        
        channel = bot.get_channel(1046919714665922680)#Audit Log
        await channel.send(embed=log)
        #buttons
        edit = Button(label="Edit", custom_id=f"editLog",style=disnake.ButtonStyle.primary)
        channel = bot.get_channel(916707865073422376)#Actual Log Channel
        await channel.send(embed=log,components=[edit])
        
        
        member = user

        overwrites = {
            member.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            get(member.guild.roles, name="Server Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(member.guild.roles, name="Moderator"): disnake.PermissionOverwrite(read_messages = True),
            get(member.guild.roles, name="Senior Admin"): disnake.PermissionOverwrite(read_messages = True),
            get(member.guild.roles, name="Trial Moderator"): disnake.PermissionOverwrite(read_messages = True),
            member: disnake.PermissionOverwrite(read_messages = True)}
        category = disnake.utils.get(member.guild.categories, name = "📬 | Support tickets")
        channel = await member.guild.create_text_channel(f"notice-{member.display_name}", overwrites=overwrites, category=category)
        await channel.send(f"**Notify:** {inter.author.mention} {user.mention}")
        log = disnake.Embed(
            title=f"NOTICE FOR: {user.display_name}", # Smart or smoothbrain?????
            color=disnake.Colour.brand_red(), # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
            description=f'''
    **Dear {user},**

    We regret to inform you that after close investigation, we have concluded that you have by greater weight of the evidence violated SMPWACA Community Guidelines (The Rules).

    Due to this, our staff team has decided it is in the server's best interest to give you a **{punishment}.**

    You should be aware, however, that you have **rights** in this case. We believe everyone deserves to be heard, so if you so desire, you may appeal this action using this link for our records:
    https://forms.gle/Rar6La3p7D56szUe9

    You also have the right to your evidence. Below should be the evidence provided by your moderator as well as the pertinent information from your log. Note that this will not include any external notes the moderator may have made during extensive investigation.

    We hope this will be a learning experience for you.

    **Regards,**
    **SMPWACA Management**
    ''',
            timestamp=datetime.now(), #Get the datetime... now...
        )
        log.set_author( # Narcissism
            name="SMPWACA Moderation",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )
        log.set_footer( # Show the moderator
            text=f"Your moderator: {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )
        log.set_thumbnail("https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
        log.add_field(name="Reason: ", value=reason, inline=True)
        log.add_field(name="Your Moderator: ", value=inter.author.name, inline=True)
        log.add_field(name="Moderator Notes: ", value=notes, inline = True)
        
        embed = disnake.Embed(
            title=f"NOTICE FOR: {user.display_name}", # Smart or smoothbrain?????
            color=disnake.Colour.brand_red(), # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
            description=f'''
    **Dear {user},**

    We regret to inform you that after close investigation, we have concluded that you have by greater weight of the evidence violated SMPWACA Community Guidelines (The Rules).

    Due to this, our staff team has decided it is in the server's best interest to give you a **{punishment}.**

    You should be aware, however, that you have **rights** in this case. We believe everyone deserves to be heard, so if you so desire, you may appeal this action using this link for our records:
    https://forms.gle/Rar6La3p7D56szUe9

    You also have the right to your evidence. You are able to request the evidence provided by your moderator as well as the pertinent information from your log. Note that this will not include any external notes the moderator may have made during extensive investigation.

    We hope this will be a learning experience for you.

    **Regards,**
    **SMPWACA Management**8
    ''',
            timestamp=datetime.now(), #Get the datetime... now...
        )
        embed.set_author( # Narcissism
            name="SMPWACA Moderation",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )
        embed.set_footer( # Show the moderator
            text=f"Your moderator: {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )
        embed.set_thumbnail("https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png")
        embed.add_field(name="Reason: ", value=reason, inline=True)
        embed.add_field(name="Your Moderator: ", value=inter.author.name, inline=True)
        embed.add_field(name="Moderator Notes: ", value=notes, inline = True)

        await channel.send(embed=log)
        

        try:
            
            await user.send(embed=embed)
            await inter.response.send_message(content = f"Moderation case for **{user}** logged in {channel.mention}!", ephemeral = True)
        except disnake.Forbidden as error:
            log = disnake.Embed(
            title=f"Error dming {user}!", 
            color=disnake.Colour.brand_red(),
            timestamp=datetime.now(), 
        )
            log.set_author(
            name="WACA-Guard Notice",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
            log.add_field(name="Error Message", value=error, inline=False)
            log.add_field(name="Likely Cause:", value="User does not have DM's enabled!", inline=True)
            log.add_field(name="Remedy:", value="Convince the user to turn on DMs or manually DM them by sending a friend request.", inline=True)
            await inter.response.send_message(embed=log, ephemeral = True)
            pass
        except Exception as error:
            log = disnake.Embed(
            title=f"Error dming {user}!", 
            color=disnake.Colour.brand_red(),
            timestamp=datetime.now(), 
        )
            embed.set_author(
            name="WACA-Guard Notice",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1037813968502259833/Information_Type1.png"
            )
            log.add_field(name="Error Message", value=error, inline=False)
          
            await inter.response.send_message(embed=log, ephemeral = True)
            pass
        
    @Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id.startswith(f"editLog"):
            emDic = inter.message.embeds[0].to_dict()
            name = emDic["title"].split(":")[0]
            punish = emDic["title"].split(":")[1]
            reason = emDic["fields"][0]["value"]
            notes = emDic["fields"][1]["value"]
            av = emDic["thumbnail"]['url']
            print(emDic)
            print(reason)
            await inter.response.send_modal(MyModal(name, punish, reason, notes, av, self.bot))   
    
class MyModal(disnake.ui.Modal):
    
    def __init__(self,name, punish, reason, notes, av, bot: Bot):
        self.bot = bot
        global ava
        ava = av
        title = "Edit Log",
        custom_id="editLogModal",
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="Name",
                custom_id=f"Name",
                style=TextInputStyle.short,
                value=name,
                required=False,
                max_length=50,),
            disnake.ui.TextInput(
                label="Punishment",
                placeholder="Punishment",
                custom_id=f"punish",
                style=TextInputStyle.short,
                required=False,
                value=punish,
                max_length=50,),
            disnake.ui.TextInput(
                label="Reason",
                
                custom_id=f"reason",
                style=TextInputStyle.short,
                required=False,
                value=reason,
                max_length=500,),
            disnake.ui.TextInput(
                label="Notes",
                custom_id=f"notes",
                style=TextInputStyle.long,
                required=False,
                value=notes,
                max_length=1000,),
            ]

        
        super().__init__(title="Edit Log",custom_id="editLogModal",components=components)
    async def callback(self, inter: disnake.ApplicationCommandInteraction):
        bot = self.bot
        global ava
        print(inter.text_values.items())
        dic=inter.text_values
        name=dic["Name"]
        punish=dic["punish"]
        reason=dic["reason"]
        notes=dic["notes"]
        log = disnake.Embed(
            title=f"{name}: {punish}", # Smart or smoothbrain?????
            color=6370411, # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP
            timestamp=datetime.now(), #Get the datetime... now...
        )
        
        log.set_author( # Narcissism
            name="SMPWACA Moderation",
            icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
        )

        log.set_footer( # Show the moderator
            text=f"Edited by {inter.author.name}",
            icon_url=inter.author.display_avatar,
        )
        log.set_thumbnail(ava)
        log.add_field(name="Reason: ", value=reason, inline=False)
        log.add_field(name="Moderator Notes: ", value=notes, inline = False)

        channel = bot.get_channel(916707865073422376)
        
        
        channel = bot.get_channel(1046919714665922680)
    
        await channel.send(embed=log)
        print("Sending embed")
        edit = Button(label="Edit", custom_id=f"editLog", style=disnake.ButtonStyle.primary)
        channel = bot.get_channel(916707865073422376)
        print("Editing message")
        await inter.response.edit_message(embed=log, components=[edit])
        
    
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))        
