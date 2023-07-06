
from disnake.ui import Button
global testingMode
testingMode = True

if not testingMode:
    print(r'''
                                                                                                                                           
                                                                                                         ,,                      
`7MMF'     A     `7MF' db       .g8"""bgd     db            .g8"""bgd                                  `7MM                             
  `MA     ,MA     ,V  ;MM:    .dP'     `M    ;MM:         .dP'     `M                                    MM                             
   VM:   ,VVM:   ,V  ,V^MM.   dM'       `   ,V^MM.        dM'       ``7MM  `7MM   ,6"Yb.  `7Mb,od8  ,M""bMM       pd""b.      ,pP""Yq.  
    MM.  M' MM.  M' ,M  `MM   MM           ,M  `MM        MM           MM    MM  8)   MM    MM' "',AP    MM      (O)  `8b    6W'    `Wb 
    `MM A'  `MM A'  AbmmmqMA  MM.          AbmmmqMA mmmmm MM.    `7MMF'MM    MM   ,pm9MM    MM    8MI    MM           ,89    8M      M8 
     :MM;    :MM;  A'     VML `Mb.     ,' A'     VML      `Mb.     MM  MM    MM  8M   MM    MM    `Mb    MM         ""Yb. ,, YA.    ,A9 
      VF      VF .AMA.   .AMMA. `"bmmmd'.AMA.   .AMMA.      `"bmmmdPY  `Mbod"YML.`Moo9^Yo..JMML.   `Wbmd"MML.          88 db  `Ybmmd9'  
                                                                                                                 (O)  .M'               
                                                                                                                  bmmmd'                
                                                                                                                                        
                                                                                                             
                                                                                                             ''')
else:
    print(r'''
                                                                                                                                                                               
                                                                                                         ,,                                                                    
`7MMF'     A     `7MF' db       .g8"""bgd     db            .g8"""bgd                                  `7MM                                 `7MM"""Yp,           mm            
  `MA     ,MA     ,V  ;MM:    .dP'     `M    ;MM:         .dP'     `M                                    MM                                   MM    Yb           MM            
   VM:   ,VVM:   ,V  ,V^MM.   dM'       `   ,V^MM.        dM'       ``7MM  `7MM   ,6"Yb.  `7Mb,od8  ,M""bMM       pd""b.      ,pP""Yq.        MM    dP  .gP"Ya mmMMmm  ,6"Yb.  
    MM.  M' MM.  M' ,M  `MM   MM           ,M  `MM        MM           MM    MM  8)   MM    MM' "',AP    MM      (O)  `8b    6W'    `Wb       MM"""bg. ,M'   Yb  MM   8)   MM  
    `MM A'  `MM A'  AbmmmqMA  MM.          AbmmmqMA mmmmm MM.    `7MMF'MM    MM   ,pm9MM    MM    8MI    MM           ,89    8M      M8       MM    `Y 8M""""""  MM    ,pm9MM  
     :MM;    :MM;  A'     VML `Mb.     ,' A'     VML      `Mb.     MM  MM    MM  8M   MM    MM    `Mb    MM         ""Yb. ,, YA.    ,A9       MM    ,9 YM.    ,  MM   8M   MM  
      VF      VF .AMA.   .AMMA. `"bmmmd'.AMA.   .AMMA.      `"bmmmdPY  `Mbod"YML.`Moo9^Yo..JMML.   `Wbmd"MML.          88 db  `Ybmmd9'      .JMMmmmd9   `Mbmmd'  `Mbmo`Moo9^Yo.
                                                                                                                 (O)  .M'                                                      
                                                                                                                  bmmmd'

                                                                                                                  
                                                                                                             ''')
print('''
**WACA GUARD IS STARTING**

WACA-Guard is property of The Network Without A Cool Acronym and is used to progress the network's security and moderation logging capabilities.
Please wait for startup...

''')
print("Importing disnake")
import disnake
from disnake.ext import commands, tasks
from commands.ping import Ping
print("Importing RVDS")
#from RVDS.MDS import MDS
print("Completed!")
print("Importing AI Support")
#from AHS import AISupport#, Reminder

print("Completed!")
print("Importing owo, suggestion, and notify commands")
from commands import owo,notify,suggestions
print("Completed!")
print("Importing training acceptance comamnds")
from training import accept, deny
print("Completed!")
print("Importing Moderation Logs")

from moderation.Log2 import Log
print("Completed!")
print("Importing DM Listener")

from moderation import DMListener, BanSync, Protect
print("Completed!")
print("Importing Verification")

from onboarding.verified import on_verification

print("Completed!")
import asyncio
from eastereggs import insanity
from eastereggs import Mitochondria
from eastereggs import bless
from moderation import Close
#from commands import hostinfo
from ServerStats import Status
from onboarding import ServerSetup, BumpReminder, tickets,JoinsAndLeaves
import os


global pingOn
global veriOn
global owoOn
global logOn
global supportOn
global reminderOn
global notifyOn
global acceptOn
global insanityOn
global mitoOn
global MDSOn
global hostOn
global botVer
global DMListen
global blessOn
global banSync
global closeSystem
global statusSystem
global serverSetup
global bumpReminder
global ticketsSystem

print("Setting variables")


pingOn = "Online :green_circle:"
veriOn = "Online :green_circle:"
owoOn = "Online :green_circle:"
logOn = "Online :green_circle:"
supportOn = "Online :green_circle:"
reminderOn="Online :green_circle:"
notifyOn="Online :green_circle:"
acceptOn="Online :green_circle:"
insanityOn="Online :green_circle:"
mitoOn="Online :green_circle:"
MDSOn = "Online :green_circle:"
botVer = "2.0.2"
DMListen = "Online :green_circle:"
blessOn = "Online :green_circle:"
hostOn = "Online :green_circle:"

banSync = "Online :green_circle:"
closeSystem = "Online :green_circle:"
statusSystem = "Online :green_circle:"
serverSetup = "Online :green_circle:"
bumpReminder = "Online :green_circle:"
ticketsSystem = "Online :green_circle:"

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True
activity = disnake.Activity(name='over NETWACA', type=disnake.ActivityType.watching)
client = disnake.Client(activity=activity)
bot = commands.Bot(
    command_prefix='!',
    command_sync_flags=command_sync_flags,
    intents=disnake.Intents.all()
    )

@tasks.loop(seconds=90)
async def change_status():
    total_users = sum(guild.member_count for guild in bot.guilds)
    await bot.change_presence(activity=disnake.Activity(name='over NETWACA', type=disnake.ActivityType.watching))
    await asyncio.sleep(30)
    await bot.change_presence(activity=disnake.Activity(name=f'{len(bot.guilds)} servers!', type=disnake.ActivityType.watching))
    await asyncio.sleep(30)
    await bot.change_presence(activity=disnake.Activity(name=f'{total_users} users!', type=disnake.ActivityType.watching))
    await asyncio.sleep(30)
@bot.event
async def on_ready():
    print("Starting Status Loop")
    change_status.start() 
    print("Started Status Loop")
    
    print("All systems online! WACA-Guard 3.0 is now running in...\n")
    for guild in bot.guilds:
        print(guild)

    print('\nWelcome to WACA-Guard! Run /setup in any servers you wish for WACA-Guard to have full functionality in.')
## ADD COGS
    
print("Adding Cogs")
bot.add_cog(Protect.Protect(bot))
bot.add_cog(deny.deny(bot))
bot.add_cog(JoinsAndLeaves.JoinAndLeave(bot))
bot.add_cog(suggestions.Suggestions(bot))
try:
    bot.add_cog(tickets.Ticket(bot))
except:
    ticketsSystem = "Offline :red_circle:"
try:
    bot.add_cog(BumpReminder.BumpPings(bot))
except:
    bumpReminder = "Offline :red_circle:"
try:
    bot.add_cog(ServerSetup.SetupCommand(bot))
except:
    serverSetup = "Offline :red_circle:"
try:
    bot.add_cog(Status.Status(bot))
except:
    statusSystem = "Offline :red_circle:"
try:
    bot.add_cog(Close.Close(bot))
except:
    closeSystem = "Offline :red_circle:"
try:
    bot.add_cog(BanSync.BanUser(bot))
except:
    banSync = "Offline :red_circle:"
try:
    bot.add_cog(DMListener.DMListener(bot))
except:
    DMListen = "Offline :red_circle:"
try:
    bot.add_cog(Ping(bot))
except:
    pingOn="Offline :red_circle:"
try:
    bot.add_cog(on_verification(bot))
except:
    veriOn = "Offline :red_circle:"
try:
    bot.add_cog(MDS(bot))
except:
    MDSOn = "Offline :red_circle:"
try:    
    bot.add_cog(owo.OWO(bot))
except:
    owoOn = "Offline :red_circle:"
try:
    bot.add_cog(Log(bot))
except:
    logOn = "Offline :red_circle:"
try:
    bot.add_cog(AISupport.Support(bot))
except:
    supportOn = "Offline :red_circle:"
try:
    bot.add_cog(Reminder.Reminder(bot))
except:
    reminderOn="Offline :red_circle:"
try:
    bot.add_cog(notify.notify(bot))
except:
    notifyOn = "Offline :red_circle:"
try:
    bot.add_cog(accept.accept(bot))
except:
    acceptOn = "Offline :red_circle:"
try:
    bot.add_cog(insanity.EasterEggs(bot))
except:
    insanityOn = "Offline :red_circle:"
try:
    bot.add_cog(bless.Bless(bot))
except:
    blessOn = "Offline :red_circle:"
try:  
    bot.add_cog(Mitochondria.Mitochondria(bot))
except:
    mitoOn = "Offline :red_circle:"
try:  
    bot.add_cog(hostinfo.hoster(bot))
except:
    hostOn = "Offline :red_circle:"

print("Completed! All tasks have completed. Beginning WACA-Guard...")


@bot.slash_command(description="WACA-Guard Information")
async def about(inter):
    botVer = "4.0 Beta"
    depDate = "July 1st, 2023"
    embed = disnake.Embed(title=f"About WACA-Guard v. {botVer}", description=f"""

Deployed on: **{depDate}**

Bot latency is {bot.latency * 1000:.2f}ms.

--------------------------------------------

**TEST MODE?** {testingMode}

--------------------------------------------

**COMMAND CENTER:**

""", color = disnake.Colour.brand_green())
    embed.add_field(name="Ping",value=f"{pingOn}")
    embed.add_field(name="OwO",value=f"{owoOn}")
    embed.add_field(name="Moderation Logs",value=f"{logOn}")
    embed.add_field(name="Support Detection",value=f"{supportOn}")
    embed.add_field(name="Notifications",value=f"{notifyOn}")
    embed.add_field(name="Training Commands",value=f"{acceptOn}")
    embed.add_field(name="Insanity Easter Egg",value=f"{insanityOn}")
    embed.add_field(name="Mitochondria Easter Egg",value=f"{mitoOn}")
    embed.add_field(name="Server Setup",value=f"{serverSetup}")
    embed.add_field(name="Bump Reminder",value=f"{bumpReminder}")
    embed.add_field(name="Mean Detection System",value=f"{MDSOn}")
    embed.add_field(name="DM Listener",value=f"{DMListen}")
    embed.add_field(name="OWO Listener",value=f"{insanityOn}")
    embed.add_field(name="Easter Egg Listeners",value=f"{veriOn}")
    embed.add_field(name="Verification",value=f"{statusSystem}")
    embed.add_field(name="Friendly Reminders",value=f"{reminderOn}")
    
    appeal = Button(label='Appeals Link', url="https://smpwa.ca/appeal", style=disnake.ButtonStyle.link, emoji = "<:Appeal:1124143624783941632> ")
    
    await inter.response.send_message(embed=embed, components = [appeal])


    

if testingMode:
    bot.run(testToken)
else:
    bot.run(token)
