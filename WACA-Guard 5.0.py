### THIS IS A BETA BUILD. NOT FOR PUBLIC RELEASE. ###

import os

global testingMode
global testingToken
# CONFIGURATION GUIDE:
#
# If you want to test WACA-Guard, please supply it with a "Testing Token" in the tokens.env file.
# Then, set testingMode to True.
#
# WACA-Guard will automatically deal with the rest of the logic.
testingMode = True

# --- BEGIN CONFIGURATION --- #

# Should WACA-Guard use AI? Defaults to TRUE (NOTE: USES HEAVY CPU ON STARTUP, MAY TAKE A FEW MINUTES TO LOAD.)
global useAI
useAI = False

# Should WACA-Guard be Verbose?
global verbose
verbose = True

# Should WACA-Guard launch in terminal mode?
terminalMode = True
# Should WACA-Guard ask if you would like to use the terminal on startup?
terminalAsk = True
#Is this a beta config?
betaMode = False

# --- END CONFIGURATION --- #

def wacaSign(testing):
    wacaGuardLogo = r"""
                                                                   
                                                               
                          ...........                          
                     .....................                     
                ...............................                
            .......................................            
          .................... ......................          
        .................      ........................        
        ...........            ........................        
        ........               ........................        
        ........               ........................        
        ........               ........................        
        ........               ........................        
        ........               ........................        
        ........               ........................        
        ........               ........................        
        ........               ........................        
        ........................               ........        
        ........................              .........        
         .......................              ........         
         .......................             .........         
          ......................            .........          
           .....................            ........           
            ....................          .........            
            ....................         ..........            
              ..................       ..........              
               .................     ...........               
                :...............  .............                
                  ...........................                  
                    .......................                    
                       .................                       
                           .........                           
                                                               
                                                               
    
    """
    if not testing:
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


                                                                                                             
#Setting Global Variables

global pingOn, veriOn, owoOn, logOn, supportOn, reminderOn, notifyOn, acceptOn, insanityOn, mitoOn, MDSOn, hostOn, botVer, DMListen, blessOn, banSync, closeSystem , statusSystem, serverSetup, bumpReminder, ticketsSystem, levelsOn
def setup():
    import subprocess
    from pathlib import Path

    def install_pip_if_needed():
      try:
        subprocess.run(["pip", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      except:
        # Install pip if not found
        print("Installing pip...")
        subprocess.run(["curl", "https://bootstrap.pypa.io/get-pip.py", "-o", "get-pip.py"], check=True)
        subprocess.run(["python3", "get-pip.py"], check=True)

    def install_dependencies():
      path = Path("./requirements.txt").resolve()
      command = ["pip", "install", "-r", str(path)]
      result = subprocess.run(command, check=True)
      if result.returncode == 0:
        print("Setup Complete! Welcome to WACA-Guard...")
      else:
        print("Error installing dependencies. Please check the logs.")

    # Check and install pip if needed
    install_pip_if_needed()

    # Install dependencies from requirements.txt
    install_dependencies()

    # Check if dotenv is loadable, if not run setup again
    

    # Load environment variables from tokens.env file
    

def terminal():
    
    try:
        import os
        import disnake
        from pathlib import Path
        import datetime
        import re
        import webbrowser
        import requests
        import json
        from dotenv import load_dotenv
        load_dotenv('tokens.env')

    
    except:
        
        setup()
        import webbrowser
        import requests
        import json
        from dotenv import load_dotenv
        load_dotenv('tokens.env')
    global testingToken
    testingToken = os.getenv('TESTING_TOKEN')

    # WACA-Guard's Token
    global token
    token = os.getenv('WACA_GUARD_TOKEN')    
    choosing = True
    while choosing:
        command = input("WACA-Guard: ")
        match command.lower():
            case "": pass
            case " " : pass
            case f if f.startswith("whatis"):
                args = command.split(" ")
                query = " ".join(args[1: ])

                url = "https://www.googleapis.com/customsearch/v1/search?key=AIzaSyBqoXqD51lRSh_V_5spz1cwrsreL_NK5cs&cx=f578d2388baaa4ec8&q=" + query
                response = requests.get(url)
                data = json.loads(response.content)

                if data["items"]:
                    answer = data["items"][0]["snippet"]
                    return answer
                else:
                    return "Sorry, I couldn't find an answer to your question."
            case g if g.startswith("google"):
                args = command.split(" ")
                try:
                    webbrowser.open(f"https://www.google.com/search?q={' '.join(args[1:])}")
                except IndexError:
                    print("""---GOOGLE HELP---
ABOUT:
Searches Google for a query.
                          
USAGE:
* - Required Argument
google [query*]
                          
ARGUMENTS:
[query] - Query to search""")
            case y if y.startswith("youtube"):
                args = command.split(" ")
                try:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={' '.join(args[1:])}")
                except IndexError:
                    print("""---YOUTUBE HELP---
ABOUT:
Searches YouTube for a query.
                          
USAGE:
* - Required Argument
youtube [query*]
                          
ARGUMENTS:
[query] - Query to search""")
            
            case o if o.startswith("open"):
                args = command.split(" ")
                try:
                    webbrowser.open(args[1])
                except IndexError:
                    print("""---OPEN HELP---
ABOUT:
Opens a URL in your default browser.
                          
USAGE:
* - Required Argument
open [url*]
                          
ARGUMENTS:
[url] - URL to open""")
                except webbrowser.Error:
                    print("Invalid URL")
                
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
                useAI = True
                barebones = False
                for arg in args:
                    match arg:
                        case "-b":
                            barebones = True
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
    -b: Bare-Bones Mode
""")
                        
                startup(testingMode, testStart, useAI, verbose, barebones)
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
                    address = "NONE"
                    for arg in args:
                        if not arg.startswith("-") and arg == args[1]:
                            address = arg
                        elif arg.startswith("-") and arg == args[1] and arg == "-h" or arg == "--help":
                            print("""---PING HELP---
                                      
ABOUT:
Pings an IP or Domain with one packet of data to quickly determine uptime.
                                      
USAGE:
* - Required Argument
ping [address*] [options]
                                      
ARGUMENTS:
[address] - Domain or IP address to ping
                                      
OPTIONS:
-c | --count - Number of times to ping""")
                            break

                          
                        match arg:
                            case "-c" | "--count":
                                count = arg[arg.index("=")+1:]
                            case "-h" | "--help":
                                print("""---PING HELP---
                                      
ABOUT:
Pings an IP or Domain with one packet of data to quickly determine uptime.
                                      
USAGE:
* - Required Argument
ping [address*] [options]
                                      
ARGUMENTS:
[address] - Domain or IP address to ping
                                      
OPTIONS:
-c | --count - Number of times to ping""")
                            
                                

                                    
                                
                    if address == "NONE":
                        print("Please provide an address to ping.")
                    else:
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
                
                args = s.split(" ")
                for arg in args:
                   match arg:
                          case "-h" | "--help":
                                print("""---SETUP HELP---
ABOUT:
Sets up WACA-Guard.
                                      
USAGE:
* - Required Argument
setup [options]
                                      
ARGUMENTS:
-h - Displays this help menu
""")
                if len(args) == 1:
                    setup()
                
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
                try:
                    if os.name != 'nt':
                        os.system(f"python3 {args[1]}")
                    else:
                        os.system(f"python {args[1]}")
                except IndexError:
                    print("""---RUN HELP---
ABOUT:
Runs a python file.
                          
USAGE:
* - Required Argument
run [file*]
                          
ARGUMENTS:
[file] - File to run""")
                    
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
                        
            
            case p if p.startswith("pshell") or p.startswith("ps"):
                args = command.split(" ")
                if len(args) == 1:

                    try:
                        if os.name != 'nt':
                            os.system(f"python3")
                        else:
                            os.system(f"python")
                    except IndexError:
                        print("""---PSHELL HELP---
    ABOUT:
    Opens a python shell.
                            
    USAGE:
    * - Required Argument
    pshell
                            
    ARGUMENTS:
    None""")
                else:
                    match args:
                        case "-h" | "--help":
                            print("""---PSHELL HELP---
    ABOUT:
    Opens a python shell.
                                  
    USAGE:
    * - Required Argument
    pshell
                                  
    ARGUMENTS:
    None""")
                    


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
                
def startup(testingMode: False, testingStart: False, useAI: True, verbose: True, barebones: False):
    def vprint(text):
        if verbose:
            print(text)
    if barebones:
        useAI = False
    print("Importing Modules...")
    vprint("VERBOSE MODE: ON")
    vprint("Importing disnake")
    import disnake
    from disnake.ui import Button
    from disnake.ext import commands, tasks
    
    from commands.ping import Ping
    vprint("Completed!")
    vprint("Importing Intelligence Modules")
    from moderation import Intel
    vprint("Done!")
    if useAI:
        vprint("Importing RVDS")
        from RVDS.MDS import MDS
        vprint("Completed!")
        vprint("Importing AI Support")
        from AHS import AISupport

        vprint("Completed!")
    else:
        vprint("Skipping AI Imports")
    vprint("Importing owo, suggestion, and notify commands")
    if not barebones:
        from commands import owo,notify,suggestions
    else:
        from commands import suggestions
    vprint("Completed!")
    vprint("Importing training acceptance comamnds")
    if not barebones:
        from training import accept, deny
    vprint("Completed!")
    vprint("Importing Moderation Logs")

    from moderation.Log import Log
    vprint("Completed!")
    from moderation import supportcog
    vprint("Importing DM Listener, BanSync, Close, and Protect")
    if not barebones:
        from moderation import DMListener, BanSync, Protect, Close
    vprint("Completed!")
    vprint("Importing Verification")
    if not barebones:
        from onboarding.verified import on_verification

    vprint("Completed!")
    if not barebones:
        from Fun import Quotes, EightBall, Emojify, GeneralFun, counting
    import asyncio
    if not barebones:
        from eastereggs import insanity
        from eastereggs import Mitochondria
        from eastereggs import bless
    
        from ServerStats import Status
        from onboarding import ServerSetup,JoinsAndLeaves, vouching
        vprint("Addicting Children to Gambling...")
        from Fun import Gambling
        vprint("Completed!")
    from onboarding import tickets
    from Fun import levels
    import os
    

    vprint("Setting variables as global...")
    
    vprint("Setting online states...")
    counts = "Online :green_circle:"
    gfun = "Online :green_circle:"
    emojif = "Online :green_circle:"
    eightb = "Online :green_circle:"
    quotesys = "Online :green_circle:"
    protectsys = "Online :green_circle:"
    denysys = "Online :green_circle:"
    joinsleaves = "Online :green_circle:"
    suggestionss = "Online :green_circle:"
    supportc = "Online :green_circle:"
    ticketsSystem = "Online :green_circle:"
    bumpReminder = "Online :green_circle:"
    serverSetup = "Online :green_circle:"
    statusSystem = "Online :green_circle:"
    closeSystem = "Online :green_circle:"
    banSync = "Online :green_circle:"
    DMListen = "Online :green_circle:"
    pingOn = "Online :green_circle:"
    veriOn = "Online :green_circle:"
    MDSOn = "Online :green_circle:"
    owoOn = "Online :green_circle:"
    logOn = "Online :green_circle:"
    supportOn = "Online :green_circle:"
    notifyOn = "Online :green_circle:"
    acceptOn = "Online :green_circle:"
    insanityOn = "Online :green_circle:"
    blessOn = "Online :green_circle:"
    mitoOn = "Online :green_circle:"
    whoisSys = "Online :green_circle:"
    gamblingOn = "Online :green_circle"
    levelsOn = "Online :green_circle"
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
    @tasks.loop(seconds=90)
    async def change_status_noAI():
        total_users = sum(guild.member_count for guild in bot.guilds)
        await bot.change_presence(status=disnake.Status.idle,activity=disnake.Activity(name='over NETWACA', type=disnake.ActivityType.watching))
        await asyncio.sleep(30)
        await bot.change_presence(status=disnake.Status.idle,activity=disnake.Activity(name=f'at half capacity!'))
        await asyncio.sleep(30)
        await bot.change_presence(status=disnake.Status.idle,activity=disnake.Activity(name=f'{len(bot.guilds)} servers!', type=disnake.ActivityType.watching))
        await asyncio.sleep(30)
        await bot.change_presence(status=disnake.Status.idle,activity=disnake.Activity(name=f'{total_users} users!', type=disnake.ActivityType.watching))
        await asyncio.sleep(30)
        await bot.change_presence(status=disnake.Status.idle,activity=disnake.Activity(name=f'in NON-AI mode!'))
        await asyncio.sleep(30)
    @bot.event
    async def on_ready():
        
        print(wacaSign(testingMode))
        vprint("Starting Status Loop")
        if not barebones and not betaMode and useAI:
            change_status.start()
        elif not useAI and not betaMode and not barebones:
            change_status_noAI.start()
        elif betaMode:
            await bot.change_presence(status=disnake.Status.idle,activity=disnake.Activity(name='BETA Mode | UNSTABLE BUILD')) 
        else:
            await bot.change_presence(status=disnake.Status.dnd,activity=disnake.Activity(name='Maintenance Mode | Essential Commands Only')) 
        vprint("Started Status Loop")
        
        print("All systems online! WACA-Guard is now running in...\n")
        for guild in bot.guilds:
            print(guild)

        print('\nWelcome to WACA-Guard! Run /setup in any servers you wish for WACA-Guard to have full functionality in.')

    ## ADD COGS

    vprint("Adding Cogs")
    try:
        bot.add_cog(counting.CountingCog(bot))
    except:
        counts = "Offline :red_circle:"
    try:
        bot.add_cog(GeneralFun.FunCog(bot))
    except:
        gfun = "Offline :red_circle:"
    try:
        bot.add_cog(Emojify.EmojifyCog(bot))
    except:
        emojif = "Offline :red_circle:"
    try:
        bot.add_cog(EightBall.EightBall(bot))
    except:
        eightb = "Offline :red_circle:"
    try:
        bot.add_cog(Quotes.QuotesCog(bot))
    except:
        quotesys = "Offline :red_circle:"
    try:
        bot.add_cog(Protect.Protect(bot))
    except:
        protectsys = "Offline :red_circle:"
    try:
        bot.add_cog(deny.deny(bot))
    except:
        denysys = "Offline :red_circle:"
    try:
        bot.add_cog(JoinsAndLeaves.JoinAndLeave(bot))
    except:
        joinsleaves = "Offline :red_circle:"
    try:
        bot.add_cog(suggestions.Suggestions(bot))
    except:
        suggestionss = "Offline :red_circle:"
    try:
        bot.add_cog(supportcog.SupportCog(bot))
    except:
        supportc = "Offline :red_circle:"
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
        bot.add_cog(Intel.WHOIS(bot))
    except:
        whoisSys = "Offline :red_circle:"
    try:
        bot.add_cog(Gambling.Roulette(bot))
    except:
        gamblingOn = "Offline :red_circle:"
    try:
        bot.add_cog(levels.LevelCog(bot))
    except:
        levelsOn = "Offline :red_circle:"
    try:
        bot.add_cog(vouching.Vouching(bot))
        vouchingOn = "Online :green_circle:"
    except:
        vouchingOn = "Offline :red_circle:"

    


    @bot.slash_command(description="WACA-Guard Information")
    async def about(inter):
        botVer = "BETA 5.0.0"
        depDate = "April 14th, 2024"
        embed = disnake.Embed(title=f"About WACA-Guard v. {botVer}", description=f"""

    Deployed on: **{depDate}**

    Bot latency is {bot.latency * 1000:.2f}ms.

    --------------------------------------------

    **TEST MODE?** {testingMode}

    --------------------------------------------

    **COMMAND CENTER:**

    """, color = disnake.Colour.brand_green())
        embed.add_field(name="Ping", value=f"{pingOn}")
        embed.add_field(name="OwO", value=f"{owoOn}")
        embed.add_field(name="Moderation Logs", value=f"{logOn}")
        embed.add_field(name="Support Detection", value=f"{supportOn}")
        embed.add_field(name="Notifications", value=f"{notifyOn}")
        embed.add_field(name="Training Commands", value=f"{acceptOn}")
        embed.add_field(name="Insanity Easter Egg", value=f"{insanityOn}")
        embed.add_field(name="Mitochondria Easter Egg", value=f"{mitoOn}")
        embed.add_field(name="Server Setup", value=f"{serverSetup}")
        embed.add_field(name="Bump Reminder", value=f"{bumpReminder}")
        embed.add_field(name="Mean Detection System", value=f"{MDSOn}")
        embed.add_field(name="DM Listener", value=f"{DMListen}")
        embed.add_field(name="Counting", value=f"{counts}")
        embed.add_field(name="General Fun", value=f"{gfun}")
        embed.add_field(name="Emojify", value=f"{emojif}")
        embed.add_field(name="Eight Ball", value=f"{eightb}")
        embed.add_field(name="Quotes", value=f"{quotesys}")
        embed.add_field(name="Protection", value=f"{protectsys}")
        embed.add_field(name="Deny", value=f"{denysys}")
        embed.add_field(name="Joins & Leaves", value=f"{joinsleaves}")
        embed.add_field(name="Suggestions", value=f"{suggestionss}")
        embed.add_field(name="Support", value=f"{supportc}")
        embed.add_field(name="Tickets", value=f"{ticketsSystem}")
        embed.add_field(name="Status", value=f"{statusSystem}")
        embed.add_field(name="Close", value=f"{closeSystem}")
        
        
        e = disnake.Embed(title=f"About WACA-Guard v. {botVer} - Continued", color = disnake.Colour.brand_green())
        e.add_field(name="Ban Sync", value=f"{banSync}")
        e.add_field(name="Verification", value=f"{veriOn}")
        e.add_field(name="WHOIS", value=f"{whoisSys}")
        e.add_field(name="Gambling", value=f"{gamblingOn}")
        e.add_field(name="Levels", value=f"{levelsOn}")
        e.add_field(name="Vouching", value=f"{vouchingOn}")
        appeal = Button(label='Appeals Link', url="https://smpwa.ca/appeal", style=disnake.ButtonStyle.link, emoji = "<:Appeal:1124143624783941632> ")
        
        await inter.response.send_message(embeds=[embed, e], components = [appeal])

                
        

    if testingMode:
        bot.run(testingToken)
        print("Completed! All tasks have completed. Beginning WACA-Guard...")
    elif testingStart == False:
        bot.run(token)
        print("Completed! All tasks have completed. Beginning WACA-Guard...")
    

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





