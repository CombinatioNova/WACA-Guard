import disnake
from disnake.ext.commands import Bot
from commands.ping import Ping
from AHS import Support
import Transcription
global testingMode
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
global botVer
global DMListen

testingMode = True
pingOn = "Online"
veriOn = "Online"
owoOn = "Online"
logOn = "Online"
supportOn = "Online"
reminderOn="Online"
notifyOn="Online"
acceptOn="Online"
insanityOn="Online"
mitoOn="Online"
MDSOn = "Online"
botVer = "2.0"
DMListen = "Online"

bot = Bot("!",sync_commands_debug=True,
          intents=disnake.Intents.all(),
          test_guilds=[1010578620135260160])

    
## ADD COGS
bot.add_cog(Support.Support(bot))
try:
    bot.add_cog(Close.Close(bot))
except:
    pass
try:
    bot.add_cog(Transcription.TranscriptionCog(bot))
except:
    pass
try:
    bot.add_cog(DMListener.DMListener(bot))
except:
    DMListen = "Offline"
try:
    bot.add_cog(Ping(bot))
except:
    pingOn="Offline"
try:
    bot.add_cog(on_verification(bot))
except:
    veriOn = "Offline"
try:
    bot.add_cog(MDS(bot))
except:
    MDSOn = "Offline"
try:    
    bot.add_cog(owo.OWO(bot))
except:
    owoOn = "Offline"
try:
    bot.add_cog(Log(bot))
except:
    logOn = "Offline"
try:
    bot.add_cog(Support.Support(bot))
except:
    supportOn = "Offline"
try:
    bot.add_cog(Reminder.Reminder(bot))
except:
    reminderOn="Offline"
try:
    bot.add_cog(notify.notify(bot))
except:
    notifyOn = "Offline"
try:
    bot.add_cog(accept.accept(bot))
except:
    acceptOn = "Offline"
try:
    bot.add_cog(insanity.EasterEggs(bot))
except:
    insanityOn = "Offline"
try:  
    bot.add_cog(Mitochondria.Mitochondria(bot))
except:
    mitoOn = "Offline"
@bot.slash_command(description="WACA-Guard Information")
async def about(inter):
    botVer = "2.0"
    depDate = "January 15th, 2023"
    embed = disnake.Embed(title=f"About WACA-Guard v. {botVer}", description=f"""

Deployed on: **{depDate}**

Bot latency is {bot.latency * 1000:.2f}ms.

--------------------------------------------

**TEST MODE?** {testingMode}

--------------------------------------------

**COG FUNCTIONALITY ANALYSIS:**

Ping: **{pingOn}**
Verification: **{veriOn}**
OWO Commands: **{owoOn}**
Moderation Logs: **{logOn}**
Support Detection: **{supportOn}**
Friendly Reminders: **{reminderOn}**
Notifications: **{notifyOn}**
Training Commands: **{acceptOn}**
Insanity Easter Egg:**{insanityOn}**
Mitochondria Easter Egg: **{mitoOn}**

**Machine Learning Algorithms:**

Mean Detection System: **{MDSOn}**
NSFW Detection System : **NOT IMPLEMENTED**

**Listeners:**

DM Listener: **{DMListen}**
OWO Listener: **{owoOn}**
Easter Egg Listeners: **{insanityOn}**

--------------------------------------------

**Notable Changes:**

- Completley restructured backend, taking the 2,700ish lines of code
  and moving it to multiple files like a sane programmer
- MDS Improvements and extra training data.
- Application acceptance improvements
- Added the "Ping" command
- Added a welcome upon user verification
- Added an easter egg (shhh!)
- Removed the edit button from Moderation Log cards
- Added acknowledgement buttons to the "notify" command
- Added answers to a few common questions
""", color = disnake.Colour.brand_green())
    await inter.response.send_message(embed=embed)




    
token = "OTIxMTAwMzUyMzAzMDMwMzU3.Gse5_e.qJz0DDAcw-2wEN-v7wWdvz-1NeiTPt9ggIN-Iw"
testToken = "MTAzOTE2NjMyODAzODIyODEyMA.GdnGsq.9pcFZAul1zW7Gf0_a6cvBM5aCrUgqTj__DENDM"

if testingMode:
    bot.run(testToken)
else:
    bot.run(token)
