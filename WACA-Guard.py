
global testingMode
global testingToken
# CONFIGURATION GUIDE:
#
# If you want to test WACA-Guard, please supply it with a "Testing Token" or the token of the bot you want to use to test WACA-Guard.
# Then, set testingMode to True.
#
# WACA-Guard will automatically deal with the rest of the logic.
testingMode = False
testingToken = ""

# --- BEGIN CONFIGURATION --- #

# WACA-Guard's Token
global token
token = "" 

# Should WACA-Guard use AI? Defaults to TRUE (NOTE: USES HEAVY CPU ON STARTUP, MAY TAKE A FEW MINUTES TO LOAD.)
global useAI
useAI = True

# Should WACA-Guard be Verbose?
global verbose
verbose = True

# Should WACA-Guard launch in terminal mode?
terminalMode = True
# Should WACA-Guard ask if you would like to use the terminal on startup?
terminalAsk = True

# --- END CONFIGURATION --- #

def wacaSign():
    if not testingMode:
        wacaGuardSign = r'''                                                                                                                
                                                                                                         ,,                      
`7MMF'     A     `7MF' db       .g8"""bgd     db            .g8"""bgd                                  `7MM                             
  `MA     ,MA     ,V  ;MM:    .dP'     `M    ;MM:         .dP'     `M                                    MM                             
   VM:   ,VVM:   ,V  ,V^MM.   dM'       `   ,V^MM.        dM'       ``7MM  `7MM   ,6"Yb.  `7Mb,od8  ,M""bMM    
    MM.  M' MM.  M' ,M  `MM   MM           ,M  `MM        MM           MM    MM  8)   MM    MM' "',AP    MM     
    `MM A'  `MM A'  AbmmmqMA  MM.          AbmmmqMA mmmmm MM.    `7MMF'MM    MM   ,pm9MM    MM    8MI    MM
      MM;    :MM;  A'     VML `Mb.     ,' A'     VML      `Mb.     MM  MM    MM  8M   MM    MM    `Mb    MM      
      VF      VF .AMA.   .AMMA. `"bmmmd'.AMA.   .AMMA.      `"bmmmdPY  `Mbod"YML.`Moo9^Yo..JMML.   `Wbmd"MML.
      
                                                                                                            '''
    else:
        wacaGuardSign = r'''                                                                                                                                                
                                                                                                         ,,                                                                    
`7MMF'     A     `7MF' db       .g8"""bgd     db            .g8"""bgd                                  `7MM     `7MM"""Yp,           mm            
  `MA     ,MA     ,V  ;MM:    .dP'     `M    ;MM:         .dP'     `M                                    MM       MM    Yb           MM            
   VM:   ,VVM:   ,V  ,V^MM.   dM'       `   ,V^MM.        dM'       ``7MM  `7MM   ,6"Yb.  `7Mb,od8  ,M""bMM       MM    dP  .gP"Ya mmMMmm  ,6"Yb.  
    MM.  M' MM.  M' ,M  `MM   MM           ,M  `MM        MM           MM    MM  8)   MM    MM' "',AP    MM       MM"""bg. ,M'   Yb  MM   8)   MM  
    `MM A'  `MM A'  AbmmmqMA  MM.          AbmmmqMA mmmmm MM.    `7MMF'MM    MM   ,pm9MM    MM    8MI    MM       MM    `Y 8M""""""  MM    ,pm9MM  
     :MM;    :MM;  A'     VML `Mb.     ,' A'     VML      `Mb.     MM  MM    MM  8M   MM    MM    `Mb    MM       MM    ,9 YM.    ,  MM   8M   MM  
      VF      VF .AMA.   .AMMA. `"bmmmd'.AMA.   .AMMA.      `"bmmmdPY  `Mbod"YML.`Moo9^Yo..JMML.   `Wbmd"MML.   .JMMmmmd9   `Mbmmd'  `Mbmo`Moo9^Yo.
      
                                                                                                             '''
    return wacaGuardSign                                                                                                         

if not testingMode:
    wacaGuardSign = r'''                                                                                                                
                                                                                                         ,,                      
`7MMF'     A     `7MF' db       .g8"""bgd     db            .g8"""bgd                                  `7MM                             
  `MA     ,MA     ,V  ;MM:    .dP'     `M    ;MM:         .dP'     `M                                    MM                             
   VM:   ,VVM:   ,V  ,V^MM.   dM'       `   ,V^MM.        dM'       ``7MM  `7MM   ,6"Yb.  `7Mb,od8  ,M""bMM    
    MM.  M' MM.  M' ,M  `MM   MM           ,M  `MM        MM           MM    MM  8)   MM    MM' "',AP    MM     
    `MM A'  `MM A'  AbmmmqMA  MM.          AbmmmqMA mmmmm MM.    `7MMF'MM    MM   ,pm9MM    MM    8MI    MM
      MM;    :MM;  A'     VML `Mb.     ,' A'     VML      `Mb.     MM  MM    MM  8M   MM    MM    `Mb    MM      
      VF      VF .AMA.   .AMMA. `"bmmmd'.AMA.   .AMMA.      `"bmmmdPY  `Mbod"YML.`Moo9^Yo..JMML.   `Wbmd"MML.
      
                                                                                                             '''
else:
    wacaGuardSign = r'''                                                                                                                                                
                                                                                                         ,,                                                                    
`7MMF'     A     `7MF' db       .g8"""bgd     db            .g8"""bgd                                  `7MM     `7MM"""Yp,           mm            
  `MA     ,MA     ,V  ;MM:    .dP'     `M    ;MM:         .dP'     `M                                    MM       MM    Yb           MM            
   VM:   ,VVM:   ,V  ,V^MM.   dM'       `   ,V^MM.        dM'       ``7MM  `7MM   ,6"Yb.  `7Mb,od8  ,M""bMM       MM    dP  .gP"Ya mmMMmm  ,6"Yb.  
    MM.  M' MM.  M' ,M  `MM   MM           ,M  `MM        MM           MM    MM  8)   MM    MM' "',AP    MM       MM"""bg. ,M'   Yb  MM   8)   MM  
    `MM A'  `MM A'  AbmmmqMA  MM.          AbmmmqMA mmmmm MM.    `7MMF'MM    MM   ,pm9MM    MM    8MI    MM       MM    `Y 8M""""""  MM    ,pm9MM  
     :MM;    :MM;  A'     VML `Mb.     ,' A'     VML      `Mb.     MM  MM    MM  8M   MM    MM    `Mb    MM       MM    ,9 YM.    ,  MM   8M   MM  
      VF      VF .AMA.   .AMMA. `"bmmmd'.AMA.   .AMMA.      `"bmmmdPY  `Mbod"YML.`Moo9^Yo..JMML.   `Wbmd"MML.   .JMMmmmd9   `Mbmmd'  `Mbmo`Moo9^Yo.
      
                                                                                                             '''
#Setting Global Variables
global pingOn, veriOn, owoOn, logOn, supportOn, reminderOn, notifyOn, acceptOn, insanityOn, mitoOn, MDSOn, hostOn, botVer, DMListen, blessOn, banSync, closeSystem , statusSystem, serverSetup, bumpReminder, ticketsSystem

def terminal():
    try:
        import os
        import disnake
        from pathlib import Path
        import datetime
        import re
    except:
        import os
        from pathlib import Path
        import datetime
        import re
        print("Attempting First-Time Setup...")
        if os.name != 'nt' and os.getpid() != 0:
            print("First-Time Setup is only able to be completed automatically with sudo permissions. Please run \"sudo pip install -r requirements.txt\" or relaunch with sudo permissions to accomplish first-time setup requirements.")
        elif os.name != 'nt' and os.getpid() == 0:
            path = Path("requirements.txt").resolve()
            linuxPath = re.sub(" ","\ ", path)
            os.system(f"sudo pip install -r {linuxPath}")
            print("First-Time Setup Complete! Welcome to WACA-Guard")
        else:
            path = Path("./requirements.txt").resolve()
            os.system(f"python -m pip install -r \"{str(path)}\"")
            print("First-Time Setup Complete! Welcome to WACA-Guard")
        
    choosing = True
    while choosing:
        command = input("WACA-Guard: ")
        match command.lower():
            case "lc" | "listcommand" | "listc" | "commands" | "cmds":
                print("""---COMMANDS---
start
qping
about
time
exit | quit
setup
testimport | ti
testsystem | ts
backup | bk
delete | del
move | mv
run | r
find | f
help | h
cls
date
""")
            case s if s.startswith("start"):
                args = command.split(" ")
                # -n: No AI
                # -t: Use Testing Bot Token
                # -v: Verbose
                testingMode = False
                testStart = False
                verbose = False
                for arg in args:
                    match arg:
                        case "-n":
                            useAI = False
                        case "-t":
                            testingMode = True
                        case "-v":
                            verbose = True
                        case "-h" | "--help":
                            print("""---START HELP---
ABOUT:
Starts WACA-Guard.
                                  
USAGE:
* - Required Argument
start [options]
                                  
ARGUMENTS:
    -n: No AI
    -t: Use Testing Bot Token
    -v: Verbose
""")
                        
                startup(testingMode, testStart, useAI, verbose)
            case p if p.startswith("qping"):
                try:
                    args = command.split(" ")
                    if os.name != 'nt':
                        response = os.system("ping -c 1 " + args[1])
                    else:
                        response = os.system("ping /n 1 " + args[1])
                    if response == 0:
                      print(f"{args[1]} is UP")
                    else:
                      print(f"{args[1]} is DOWN")
                except IndexError:
                    print("""---PING HELP---

ABOUT:
Pings an IP or Domain with one packet of data to quickly determine uptime.

USAGE:
* - Required Argument
qping [address*]

ARGUMENTS:
[address] - Domain or IP address to ping""")
            case p if p.startswith("ping"):
                count = 5
                try:
                    args = command.split(" ")
                    for arg in args:
                        if arg == "-c":
                            count = args[args.index(arg)+1]
                    if os.name != 'nt':
                        response = os.system(f"ping -c {count} " + args[1])
                    else:
                        response = os.system(f"ping /n {count} " + args[1])
                    if response == 0:
                      print(f"{args[1]} is UP, Pinged {count} times")
                    else:
                      print(f"{args[1]} is DOWN, Pinged {count} times")
                except IndexError:
                    print("""---PING HELP---
                          
ABOUT:
Pings an IP or Domain with one packet of data to quickly determine uptime.

USAGE:
* - Required Argument
qping [address*]

ARGUMENTS:
[address] - Domain or IP address to ping""")

            case "about":
                print(wacaSign())
                print("WACA-Guard Ver. 4.0 | Created by CombinatioNova for NETWACA")
            case c if c.startswith("clear"):
                args = command.split(" ")
                if len(args) == 1:
                    os.system("clear")
                else:
                    match args:
                        case "-h" | "--help":
                            print("""---CLEAR HELP---
ABOUT:
Clears the terminal.
                                  
USAGE:
* - Required Argument
clear [options]
                                  
ARGUMENTS:
-h - Displays this help menu""")

            case f if f.startswith("find") or f.startswith("f"):
                args = command.split(" ")
                for arg in args:
                    match arg:
                        case "-h" | "--help":
                            print("""---FIND HELP---
ABOUT:
Finds a file.
                                  
USAGE:
* - Required Argument
find [file*]
                                  
ARGUMENTS:
[file] - File to find""")
                        case _:                        
                            if os.name != 'nt':
                                os.system(f"find {args[1]}")
                            else:
                                os.system(f"dir {args[1]}")  
                
            case "help":
                print("""---HELP---
                      Follow any command with -h or --help to get help on that command.""")
            case "cls":
                os.system("cls")
            case "date":
                print(datetime.datetime.now().strftime("Current Date: %m/%d/%Y"))
            
            case t if t.startswith("time"):
                args = command.split(" ")
                if len(args) == 1:
                    print(datetime.datetime.now().strftime("Current Time: %H:%M:%S"))
                else:
                    match args:
                        
                        case "-h" | "--help":
                            print("""---TIME HELP---
ABOUT:
Gets the current time.
                                  
USAGE:
* - Required Argument
time [options]
                                  
ARGUMENTS:
-h - Displays this help menu
""")
                        



            case "exit" | "quit":
                print("Quitting WACA-Guard...")
                choosing = False
            
            case s if s.startswith("setup"):
                forced = False
                args = s.split(" ")
                for arg in args:
                    match arg:
                        case "--force":
                            forced = True
                        case "-h" | "--help":
                            print("""---SETUP HELP---
ABOUT:
Sets up WACA-Guard for first-time use.
                                  
USAGE:
* - Required Argument
setup [--force]
                                  
ARGUMENTS:
[--force] - Forces setup to run, even if requirements are already installed""")
                if os.name != 'nt' and os.getpid() != 0 and not forced:
                    print("This program is not run as sudo. Please run this program as sudo to ensure all permissions are properly handled.")
                elif os.name != 'nt' and os.getpid() == 0 or forced:
                    path = Path("requirements.txt").resolve()
                    linuxPath = re.sub(" ","\ ", path)
                    os.system(f"sudo pip install -r {linuxPath}")
                    print("Setup Complete!")
                elif os.name == 'nt':
                    path = Path("./requirements.txt").resolve()
                    os.system(f"pip install -r \"{str(path)}\"")
                    print("Setup Complete!")

            case b if b.startswith("backup") or b.startswith("bk"):
                args = command.split(" ")
                if os.name != 'nt':
                    os.system(f"cp {args[1]} {args[2]}")
                else:
                    os.system(f"copy {args[1]} {args[2]}")
                for arg in args:
                    match arg:
                        case "-h" | "--help":
                            print("""---BACKUP HELP---
ABOUT:                            
Backs up a file.
                                  
USAGE:
* - Required Argument
backup [file*] [backup_as*]

ARGUMENTS:
[file] - File to backup
[backup_as] - Name of backup""")
                               
                                  
            case d if d.startswith("delete") or d.startswith("del"):
                args = command.split(" ")
                if os.name != 'nt':
                    os.system(f"rm {args[1]}")
                else:
                    os.system(f"del {args[1]}")
                for arg in args:
                    match arg:
                        case "-h" | "--help":
                            print("""---DELETE HELP---
ABOUT:
Deletes a file.
                                  
USAGE:
* - Required Argument
delete [file*]
                                  
ARGUMENTS:
[file] - File to delete""")
            case m if m.startswith("move") or m.startswith("mv"):
                args = command.split(" ")
                if os.name != 'nt':
                    os.system(f"mv {args[1]} {args[2]}")
                else:
                    os.system(f"move {args[1]} {args[2]}")
                for arg in args:
                    match arg:
                        case "-h" | "--help":
                            print("""---MOVE HELP---
ABOUT:
Moves a file.
                                  
USAGE:
* - Required Argument
move [file*] [destination*]
                                  
ARGUMENTS:
[file] - File to move
[destination] - Destination to move file to""")
            case r if r.startswith("run") or r.startswith("r"):
                args = command.split(" ")
                if os.name != 'nt':
                    os.system(f"python3 {args[1]}")
                else:
                    os.system(f"python {args[1]}")
                for arg in args:
                    match arg:
                        case "-h" | "--help":
                            print("""---RUN HELP---
ABOUT:
Runs a python file.
                                  
USAGE:
* - Required Argument
run [file*]
                                  
ARGUMENTS:
[file] - File to run""")
                        
            
             

            case t if t.startswith("testimport") | t.startswith("ti"):
                args = command.split(" ")
                try:
                    module = __import__(args[1])
                    print("Import Succesful!")
                except Exception as e:
                    print(f"Import Unsucessful:\n\n {e}")
                for arg in args:
                    match arg:
                        case "-h" | "--help":
                            print("""---TEST IMPORT HELP---
ABOUT:
Tests an import to ensure it is working properly.
                                  
USAGE:
* - Required Argument
testimport [module*]
                                  
ARGUMENTS:
[module] - Module to test""")
            case t if t.startswith("testsystem") or t.startswith("ts"):
                args = command.split(" ")
                # -n: No AI
                # -l: Login to Discord
                # -t: Use Testing Bot Token
                # -v: Verbose
                testingMode = False
                testStart = True
                useAI = True
                verbose = False
                for arg in args:
                    match arg:
                        case "-h" | "--help":
                            print("""---TEST SYSTEM HELP---
ABOUT:
Test System tests all components of WACA-Guard's imports by running the startup command without providing a token.

USAGE:
* - Required Argument
testsystem [options]

ARGUMENTS:
 -n: No AI
 -l: Login to Discord
 -t: Use Testing Bot Token
 -v: Verbose
""")
                        case "-n":
                            useAI = False
                        case "-l":
                            testStart = False
                        case "-t":
                            testingMode = True
                        case "-v":
                            verbose = True
                        
                startup(testingMode, testStart, useAI, verbose)
            case _:
                print("Unknown Command")
                
def startup(testingMode: False, testingStart: False, useAI: True, verbose: True):
    if verbose:
        print("Importing disnake")
        import disnake
        from disnake.ui import Button
        from disnake.ext import commands, tasks
        
        from commands.ping import Ping
        if useAI:
            print("Importing RVDS")
            from RVDS.MDS import MDS
            print("Completed!")
            print("Importing AI Support")
            from AHS import AISupport

            print("Completed!")
        else:
            print("Skipping AI Imports")
        print("Importing owo, suggestion, and notify commands")
        from commands import owo,notify,suggestions
        print("Completed!")
        print("Importing training acceptance comamnds")
        from training import accept, deny
        print("Completed!")
        print("Importing Moderation Logs")

        from moderation.Log2 import Log
        print("Completed!")
        print("Importing DM Listener, BanSync, Close, and Protect")

        from moderation import DMListener, BanSync, Protect, Close
        print("Completed!")
        print("Importing Verification")

        from onboarding.verified import on_verification

        print("Completed!")
        from Fun import Quotes, EightBall, Emojify, GeneralFun, counting
        import asyncio
        from eastereggs import insanity
        from eastereggs import Mitochondria
        from eastereggs import bless
        
        from ServerStats import Status
        from onboarding import ServerSetup, BumpReminder, tickets,JoinsAndLeaves
        import os

        print("Setting variables as global...")
       
        print("Setting online states...")
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
        botVer = "4.0.0"
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
            print(wacaGuardSign)
            print("Starting Status Loop")
            change_status.start() 
            print("Started Status Loop")
            
            print("All systems online! WACA-Guard is now running in...\n")
            for guild in bot.guilds:
                print(guild)

            print('\nWelcome to WACA-Guard! Run /setup in any servers you wish for WACA-Guard to have full functionality in.')

        ## ADD COGS
    
        print("Adding Cogs")
        bot.add_cog(counting.CountingCog(bot))
        bot.add_cog(GeneralFun.FunCog(bot))
        bot.add_cog(Emojify.EmojifyCog(bot))
        bot.add_cog(EightBall.EightBall(bot))
        bot.add_cog(Quotes.QuotesCog(bot))
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

        


        @bot.slash_command(description="WACA-Guard Information")
        async def about(inter):
            botVer = "4.0.0"
            depDate = "July 7th, 2023"
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
            bot.run(testingToken)
            print("Completed! All tasks have completed. Beginning WACA-Guard...")
        elif testingStart == False:
            bot.run(token)
            print("Completed! All tasks have completed. Beginning WACA-Guard...")
    else:
        print("Importing modules...")
        import disnake
        from disnake.ui import Button
        from disnake.ext import commands, tasks
        
        from commands.ping import Ping
        if useAI:
            
            from RVDS.MDS import MDS
            
           
            from AHS import AISupport

            
        else:
            pass
        from commands import owo,notify,suggestions
        
        from training import accept, deny
        

        from moderation.Log2 import Log
       

        from moderation import DMListener, BanSync, Protect, Close
        

        from onboarding.verified import on_verification

        
        from Fun import Quotes, EightBall, Emojify, GeneralFun, counting
        import asyncio
        from eastereggs import insanity
        from eastereggs import Mitochondria
        from eastereggs import bless
        
        from ServerStats import Status
        from onboarding import ServerSetup, BumpReminder, tickets,JoinsAndLeaves
        import os

        print("Setting variables as global...")
        # Set status variables
        
        print("Setting online states...")
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
        botVer = "4.0.0"
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
            print(wacaGuardSign)
            print("Starting Status Loop")
            change_status.start() 
            print("Started Status Loop")
            
            print("All systems online! WACA-Guard is now running in...\n")
            for guild in bot.guilds:
                print(guild)

            print('\nWelcome to WACA-Guard! Run /setup in any servers you wish for WACA-Guard to have full functionality in.')

        ## ADD COGS
    
        print("Adding Cogs")
        bot.add_cog(counting.CountingCog(bot))
        bot.add_cog(GeneralFun.FunCog(bot))
        bot.add_cog(Emojify.EmojifyCog(bot))
        bot.add_cog(EightBall.EightBall(bot))
        bot.add_cog(Quotes.QuotesCog(bot))
        #bot.add_cog(Backup.BackupCog(bot))
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

        


        @bot.slash_command(description="WACA-Guard Information")
        async def about(inter):
            botVer = "4.0.0"
            depDate = "July 7th, 2023"
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
            bot.run(testingToken)
            print("Starting WACA-Guard...")
        elif testingStart == False:
            bot.run(token)
            print("Starting WACA-Guard...")

if terminalMode and not terminalAsk:
    terminal()
elif terminalAsk:
    
    picking = True
    while picking:
        choice = input("Would you like to start WACA-Guard in Terminal mode? [y/n]: ")
        match choice:
            case "y":
                terminal()
                picking = False
            case "n":
                startup(testingMode, False, useAI, verbose)
                picking = False
            case _:
                print("Please answer with \"y\" or \"n\"")
    
else:
    startup(testingMode, False, useAI, verbose)





