import disnake
import datetime
import fuzzywuzzy
import logging
import aiofiles
import aiohttp
import json
import re
import numpy as np

from disnake.ext.commands import Bot, Cog,Param,slash_command
from disnake.ui import Button
from disnake.utils import get
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sklearn.model_selection import cross_val_score
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
from sklearn.datasets import load_iris

import chat_exporter
start_time = datetime.now()
logging.getLogger().setLevel(logging.ERROR)
X = np.array(["Can I get some help?",
              "could someone help me in dms",
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
         "im stuck joining",
              "i can't join",
              "this is bugged",
              
              "i found a bug",#
               "how do i balance work and school",
               "how do i build",
               'how do i do this',
               'how should someone get help',
               'how can i do this stuff honestly',
               'how can you possibly be okay with this',
               'i am so shocked at this',
              
              'the staff are cool',
              'i like the staff team',
              'i hate the staff team',
              'i am indifferent to the staff team',
              'to be a staff is to be nice',
              'i like helping the staff',
              'the staff are helping me',
              'what is the server ip',
               'whats the server ip',
               "whats the ip",
               "!ip",
               "the ip of the server is",
               "i enjoy that ip",
               "quite honestly i dont get that ip's hype",
               "hm, i wonder what it could be used for",
               "what is the server it",
               "what is it doing",
               "why is the server ip like that?",
               "what is the server ip doing?",
               'how do i join', 'how do i join the server', 'how do i get on', "how to join","1ip","dip","rip","skip","I don't get why the ip is like that","I get the ip",#
            'I found a griefer',
               "Someone stole",
               "Someone took my stuff",
               "OMG SOMEONE TOOK EVERYTHING",
               "THEY TOOK EVERYTHING",
               "My house is blown up ;-;",

               "SOMEONE DESTROYED EVERYTHING",
               "NOOO ALL MY PROGRESS",

              "I need a staff member to help me",
              "I do not need a staff member to help me",
              "I need lots of help doing this",
              "I don't need lots of help doing this",
              "I am fine",
              "I am not fine",
              "SOMEONE TOOK EVERYTHING",
              "SOMEONE DIDNT TAKE EVERYTHING",
              "THEY DIDNT TAKE ANYTHING",
              "THEY TOOK TOO MUCH", #10 1010001001
              
              "I love them for that",
              "I hate them for that",
              "Please help me",
              "Please help me staff",
              "Is there a mod online",
              "Can a mod help me",
              "Are mods unable to help?",
              "I've been waiting for a while and no one has come to help", # 8
                    "The tutorial on redstone circuits will help you create complex contraptions.",
    "I always offer assistance to new players who are unfamiliar with the game mechanics.",
    "The wiki is a great source of information and can help you navigate through various crafting recipes.",
    "A well-designed farm can help sustain a player's food supply.",
    "Automating processes with redstone can help improve efficiency in your Minecraft world.",
    "Teaming up with other players can provide valuable assistance when taking on challenging tasks.",
    "Enchanting your tools and weapons can help make them more effective in combat and resource gathering.",
    "The addition of beacons can help provide useful buffs to players within its range.",
    "Creating a well-organized storage system will help you manage your resources effectively.",
    "Constructing a mob grinder can help you gather valuable resources and experience.",
    "A little assistance with building techniques can significantly improve your architectural designs.",
    "Regular backups of your Minecraft world can help prevent data loss in case of corruption.",
    "Crafting a map will help you keep track of explored areas and avoid getting lost.",
    "Efficient strip mining techniques can help maximize your yield of valuable ores.",
    "Sleeping through the night can help avoid hostile mobs and make exploration safer.",
    "Potions can provide temporary buffs to help with various tasks and combat situations.",
    "Learning to navigate the Nether can help you travel long distances quickly in the Overworld.",
    "Constructing a perimeter around your base can help deter griefers and protect your creations.",
    "Creating an Ender Chest can help secure valuable items and make them accessible from anywhere.",
    "Finding a village and trading with villagers can help you acquire rare and useful items.",
    "A well-lit area can help prevent mob spawning and keep your base safe from unexpected attacks.",
    "Knowing how to breed animals can help maintain a steady food source and valuable resources.",
    "Crafting a shield can provide additional protection in combat and help block incoming projectiles.",
    "Enlisting the help of a skilled player can improve your gameplay and teach you new strategies.",
    "Exploring together can help make discovering new biomes and structures more enjoyable.",
    "Sharing resources and working together can help complete large-scale projects more efficiently.",
    "Crafting and placing signs can help provide directions and prevent players from getting lost.",
    "Setting a spawn point near your base can help you return quickly after death or exploration.",
    "Learning to use redstone effectively can help create secret entrances and hidden traps.",
    "Using a fishing rod can help you catch fish and other valuable items from bodies of water.",
    "Crafting a boat can help you traverse large bodies of water quickly and efficiently.",
    "Taming and riding a horse can help you cover vast distances in a short amount of time.",
    "Constructing a safe and secure Nether portal room can help prevent accidents and unwanted visitors.",
    "Building a watchtower can help you spot potential threats and monitor your surroundings.",
    "Planting trees and creating a sustainable forest can help provide a steady supply of wood.",
    "Setting up a rail system can help facilitate transportation between distant locations.",
    "Constructing an XP farm can help players quickly gain experience for enchanting and repairing items.",
    "Using a compass can help you navigate and find your way back to your original spawn point.",
    "Taking screenshots of important coordinates can help you remember important locations.",
    "Creating a community message board can help players communicate and share information.",
                  "A staff member helped me understand the server rules and guidelines.",
    "If you're unsure about a specific command, ask a staff member for assistance.",
    "I was stuck in a glitch, but a staff member teleported me to safety.",
    "When I reported a griefer, a staff member came to help resolve the issue.",
    "A staff member was available to help me claim land for my base.",
    "I reached out to a staff member when my items disappeared after a server rollback.",
    "The staff member kindly assisted me in recovering my lost pet after an update.",
    "A staff member helped me understand the process for reporting inappropriate behavior.",
    "I was having trouble with a plugin, and a staff member provided support.",
    "When I encountered a bug, the staff member advised me on how to submit a bug report.",
    "A staff member helped me navigate the server's economy and trading system.",
    "When I was unsure about a particular rule, the staff member clarified it for me.",
    "The staff member assisted me in setting up a shop to sell my items.",
    "A staff member helped me figure out the proper permissions for my player group",
                      "Is a staff member online? I need help understanding the server rules.",
    "Can a staff member assist me with using a specific command?",
    "I'm stuck in a glitch, could a staff member please teleport me to safety?",
    "I'd like to report a griefer, is there a staff member available to help?",
    "Can a staff member help me claim some land for my base?",
    "My items disappeared after a server rollback, can a staff member help me recover them?",
    "I lost my pet after an update, can a staff member assist me in finding it?",
    "I need help reporting inappropriate behavior, is there a staff member who can guide me?",
    "I'm having trouble with a plugin, can a staff member provide some support?",
    "I encountered a bug, can a staff member advise me on how to submit a bug report?",
    "Is a staff member available to help me understand the server's economy and trading system?",
    "I'm unsure about a rule, can a staff member please clarify it for me?",
    "Can a staff member help me set up a shop to sell my items?",
    "I need assistance with player group permissions, is there a staff member who can help?",
    "Is a staff member online? I need help understanding the teleportation system.",
              "Can someone help me figure out this redstone contraption?",

    "I'm new here, can anyone help me find a good place to build my base?",
    "Can someone show me how to use the server's custom crafting recipes?",
    "I'm looking for a specific biome, can anyone help me find it?",
    "Does anyone know how to build an efficient mob farm? I need some help.",
    "I'm having trouble enchanting my gear, can someone assist me?",
    "Can someone help me with ideas for my base's design?",
    "I need some assistance gathering resources, is anyone willing to help?",
    "I'm lost in the Nether, can someone help guide me back to the portal?",
    "Does anyone know how to breed villagers? I could use some help.",
    "I'm having trouble with my farm, can someone assist me in optimizing it?",
    "Can anyone help me find some rare ores? I'm struggling to locate them.",
    "I need help understanding the server's transportation system, can someone explain it to me?",
    "I want to explore an ocean monument, can someone help me prepare for the journey?",
    "Does anyone have experience building custom trees? I need help with landscaping.",

                  "I'm having an issue in-game, but I'm not sure where to find the support tickets.",
    "I need help with a problem on the Minecraft SMP, can someone point me to the ticket system?",
    "I've encountered a bug on the server, but I don't know how to create a support ticket.",
    "Is there a specific channel on Discord for submitting support tickets? I'm not sure where to go.",
    "I'm having trouble understanding the ticket system, can anyone help me with this?",
    "I need assistance with a plugin issue, but I don't know how to reach the staff through support tickets.",
    "I've been experiencing some issues on the server, but I'm not familiar with the support ticket process.",
    "I've run into a problem with another player, and I'm not sure how to get help using the ticket system.",
    "I have a question about the Minecraft SMP, but I don't know where to submit a support ticket.",
    "I need to report a griefer, but I'm having trouble navigating the support ticket system.",
    "I've encountered a glitch that's affecting my gameplay, but I can't seem to find the support tickets.",
    "I want to suggest a new feature for the server, but I'm unsure about how to create a support ticket.",
    "I'd like to request help from the staff, but I can't find the Discord channel for support tickets.",
    "I need to report a bug, but I'm having difficulty understanding how to use the support ticket system.",
    "I'm experiencing some performance issues on the server, but I don't know where to go for support tickets.",
              "I bought carnival tickets for the whole family.", "Please submit your support ticket through the online portal.", "I have concert tickets for the upcoming show.", "The technical support ticket was resolved quickly.", "The raffle tickets were sold out within a few hours.", "She purchased movie tickets for the premiere.", "The theme park tickets include access to all the rides.", "Our customer support team is processing your ticket.", "He won free airline tickets through a contest.", "The software bug was reported in a support ticket.", "I can't wait to use my tickets for the state fair.", "The help desk resolved my issue with a support ticket.", "I need to buy train tickets for our weekend trip.", "The IT department closed the support ticket after fixing the issue.", "She gifted me theater tickets for my birthday.", "The support ticket contained useful troubleshooting information.", "We found discount tickets for the amusement park.", "A customer submitted a support ticket with a feature request.", "We have season tickets to our favorite sports team.", "The support ticket was escalated to a senior technician.", "I used my tickets for the zoo on a sunny day.", "The support ticket indicated a common user error.", "I bought advance tickets for the art exhibition.", "The maintenance request was submitted as a support ticket.", "We got tickets for the charity gala.", "The support ticket was labeled as low priority.", "I managed to snag last-minute tickets for the musical.", "The support ticket contained an error log.", "I surprised my partner with opera tickets.", "The support ticket system helps track customer issues.", "We got tickets to the comedy club for a night of laughs.", "The support ticket included a detailed explanation of the problem.", "I reserved parking tickets for the big event.", "The support ticket was merged with a related issue.", "We scored backstage passes and concert tickets for our favorite band.", "The support ticket was resolved by updating the software.", "I'm saving my arcade tickets to get a big prize.", "The support ticket's status was updated to 'in progress'.", "We purchased lift tickets for a day of skiing.", "The support ticket was closed after the user confirmed the issue was resolved.",
              "I NEED STAFF ASSISTANCE",
              "I need to make a ticket",
              
               "I can't connect to the server",
              
              "someone had killed me and trapped my stuff in obsidian",
              "how do you think ill get anywhere near to Imperium or any of those other towns",
              
              "How do i fix i0k ping",
              "yknow considering that you took it from my chest it whould be stealing",
              "so i killed bit and his grave is gone",
              "yeah server has been crashing a bit",
                "what the heck is happened to the server",
              "also server crashed",
              "what happen to the server",
              "Server Died",
              "YOU ARE SPAWN KILLING",
              "i have no clue m new to the server",
              "how do i get animals out the nether",
              "How did he get into the end",
              
              "I need help",
              "Can a staff member help me?",
              "I don't know what I'm doing",
              "I'm new here, what do I do?",
              "How do I register?",

              "How do I register-",
              "Uhh... How do I verify my account",
              "guys how do i claim my house",
              "how the tables have turned",
              "help me! I'm lagging",
              "I'm seriously lagging too much to play-",
              "Sorry I was lagging too much on the server",
              "YAY INTERNET BLESSED ME ITS LAGGING BUT IT BLESSED ME",
              "is called lag",
              "I need staff",
              "I could use some staff",

              """:Notice: **CONNECTION ISSUES? WE CAN HELP!** :Notice: 

Hello all!

Many people may have a slower connection on SMPWACA than they'd like, or possibly have trouble joining at all! We can help you diagnose the issue with the proper tools and a bit of help from you!

Download WinMTR, the hosting industry's standard for route tracing, and open a ticket with us to help you diagnose the problem:
https://sourceforge.net/projects/winmtr/

We can use our connections to our hosting provider to give you blazing fast speeds! 

Just put in the IP of the server, and run! Send us a screenshot of the output and we can help route your connection to faster nodes!

@General Pings""",
              """COMMUNITY SURVEY 📊 

Hello @everyone!

It's time again for the SMPWACA community survey, where you can show us what we are doing well and need to do better!

Your answers will be carefully considered for future decisions in the SMP. Thank you for participating!

https://forms.gle/Jc1M93P1i1EhbHkQ9

@General Pings @Community Pings @Events Pings""",
"how do i join the server",
              
              
             
              
              ])
X2 = np.array(['what is the server ip',
               'whats the server ip',
               "whats the ip",
               "!ip",
               "the ip of the server is",
               "i enjoy that ip",
               "quite honestly i dont get that ip's hype",
               "hm, i wonder what it could be used for",
               "what is the server it",
               "what is it doing",
               "why is the server ip like that?",
               "what is the server ip doing?",
               'how do i join', 'how do i join the server', 'how do i get on', "how to join","1ip","dip","rip","skip","I don't get why the ip is like that","I get the ip",#
               "how do i balance work and school",
               "how do i build",
               'how do i do this',
               'how should someone get help',
               'how can i do this stuff honestly',
               'how can you possibly be okay with this',
               'i am so shocked at this',
               "rip",
               "crip",
               "Rassx how much do i need to make a town",
               "What is the IP of the server?",
               "What is the age of the server?",

               'Someone once told me "Hey what\'s the IP?" i told them back AGHHHH UP YOURS BUDDY',
               "Yknow why would an IP be an IP",
               "Now that's a good IP right there",
               "Who's an IP?",
               "Who needs an IP?",
               "rip",
               "ippie",
               "yip",
               "ip",
               "yippie",
               "tip",
               "snip",
               "parsnip",
               "peas and kips",
               
               ##TIME TIME
               
               "Yeah the ip is play.smpwaca.com",
               "This is the ip",
               'find the ip in announcements',
               'find the ip in information',
               "Yeah the videogame IP's these days are interesting",
               
               "IP addresses are crucial for devices to communicate on the internet.",
"The IPv4 address space is limited, which is why IPv6 was developed.",
"When it comes to IP, the abbreviation can refer to either Internet Protocol or Intellectual Property.",
"To protect your IP, it's essential to register for trademarks, copyrights, and patents.",
"Dynamic IP addresses change periodically, while static IPs remain the same.",
"Intellectual Property rights are designed to protect creators and their inventions.",
"An IP packet is the basic unit of information transmitted over the internet.",
"Patents grant exclusive rights to inventors for a limited period of time.",
"Copyrights protect original works of authorship, including books, music, and software.",
"Trademarks protect brand names, logos, and symbols that distinguish products and services.",
"A subnet mask is used to divide an IP address into network and host parts.",
"Intellectual Property law is complex and often requires the expertise of a specialized attorney.",
"NAT, or Network Address Translation, allows multiple devices to share a single public IP address.",
"Licensing agreements are a common way for IP owners to generate revenue from their creations.",
"IPv4 uses 32-bit addresses, while IPv6 uses 128-bit addresses for increased capacity.",
"Infringement of IP rights can result in costly lawsuits and damage to a company's reputation.",
"An IP header contains information about the source and destination of a packet.",
"An IP header contains information about the source and destination of a packet.",
"Trade secrets are a type of Intellectual Property that protect valuable business information.",
"A router is responsible for forwarding IP packets between networks.",
"Non-disclosure agreements can help protect sensitive IP during business negotiations.",
"A public IP address is accessible from the internet, while a private IP is used within local networks.",
"The World Intellectual Property Organization (WIPO) promotes the protection of IP rights globally.",
"DHCP, or Dynamic Host Configuration Protocol, is used to assign IP addresses dynamically.",
"The patent application process can be time-consuming and costly, but it's essential for protecting IP.",
"Internet Protocol consists of two main versions: IPv4 and IPv6.",
"IP licensing can enable companies to expand their product offerings without significant investment.",
"The IP stack is a set of protocols that enable network communication.",
"Fair use is a legal doctrine that allows limited use of copyrighted IP without permission.",
"An IP conflict occurs when two devices on a network have the same IP address.",
"Protecting your IP assets is a critical aspect of business strategy.",
"Domain Name System (DNS) translates domain names into IP addresses.",
"To maintain a competitive edge, companies must vigilantly guard their IP.",
"An IP blacklist is a list of IP addresses known for sending spam or engaging in malicious activities.",
"Piracy is a significant concern for IP owners in the digital age.",
"An IP tunnel is a method of encapsulating one IP packet within another for secure transmission.",
"Registering your IP can provide legal recourse in the event of infringement.",
"Internet Protocol Security (IPSec) is a suite of protocols used to secure IP communication.",
"Counterfeit goods are a major issue for IP owners, as they can damage brand reputation.",
"The Internet Protocol (IP) is responsible for addressing and routing data packets across networks.",
"When licensing IP, it's essential to establish clear terms and conditions to protect your rights.",
               "I can't connect to the server",
               "how do you think ill get anywhere near to Imperium or any of those other towns",
               "how do I join",
               "I don't know how to join",
               "How do you get the IP",
               "Where is the IP",
               "What's the server version?",
               "What is the IP of the minecraft server?",

               "We know the server hosters so we can see if we can adjust the routing",
               "Sorry I was lagging too much on the server",
               "Well it was the day i rejoined the server",

               "You mean you're going to improve the server by getting input from users...",
               "I litteraly dont know how he can do it too Nova cuz he snet me to jail and could use the cams to check on me ;-;",

               "how do i join the server",
               """:Notice: **CONNECTION ISSUES? WE CAN HELP!** :Notice: 

Hello all!

Many people may have a slower connection on SMPWACA than they'd like, or possibly have trouble joining at all! We can help you diagnose the issue with the proper tools and a bit of help from you!

Download WinMTR, the hosting industry's standard for route tracing, and open a ticket with us to help you diagnose the problem:
https://sourceforge.net/projects/winmtr/

We can use our connections to our hosting provider to give you blazing fast speeds! 

Just put in the IP of the server, and run! Send us a screenshot of the output and we can help route your connection to faster nodes!

@General Pings""",
              """COMMUNITY SURVEY 📊 

Hello @everyone!

It's time again for the SMPWACA community survey, where you can show us what we are doing well and need to do better!

Your answers will be carefully considered for future decisions in the SMP. Thank you for participating!

https://forms.gle/Jc1M93P1i1EhbHkQ9

@General Pings @Community Pings @Events Pings""",
               
               ])
Y = np.array([0,1,1,1,1,0,1,0,1,
0,1,0,0,1,
1,1,1,1,1,
1,0,0,0,1,0,0,0,

0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,

1,1,1,1,1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,1,
              0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
               1,1,1,0,1,1,1,1,1,1,1,0,0,1
              ])
Y2 = np.array([1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,
              0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,0,0,0,0,1,0,0

               
               ])
iris = load_iris()

#vectorizing dataset
vectorizer = CountVectorizer()
vectorizer2 = TfidfVectorizer()
#instantiate SVM classifier

polyGrid ={
    'C': [0.1,0.01,0.04,1,5,10,18,15,20],
    'kernel': ['poly'],
    'degree': [2,4,6,7,8],
    'coef0': [0, 1,2 ,5, 10,15]}
optionPoly = GridSearchCV(SVC(), polyGrid, n_jobs = -1)
# Train the classifier
X2_train = vectorizer.fit_transform(X2)
X_train_vectors = vectorizer2.fit_transform(X)

classifier = MultinomialNB()
classifier.fit(X_train_vectors, Y)
# Use the SVM classifier to train the model
optionPoly.fit(X2_train, Y2)
polyScore= cross_val_score(classifier, X_train_vectors, Y, cv=5)
print("Accuracy of Help analysis: %0.2f (+/- %0.2f)" % (polyScore.mean(), polyScore.std() * 2))
polyScore2= cross_val_score(optionPoly, X2_train, Y2, cv=5)
print("Accuracy of IP analysis: %0.2f (+/- %0.2f)" % (polyScore2.mean(), polyScore2.std() * 2))
accuracyPoly="%0.2f (+/- %0.2f)" % (polyScore2.mean(), polyScore2.std() * 2)
###Crosstrain using each other's dataset
##polyScore= cross_val_score(optionPoly, X_train, Y2, cv=5)
##print("Accuracy of Help analysis crossed with IP Dataset: %0.2f (+/- %0.2f)" % (polyScore.mean(), polyScore.std() * 2))
##polyScore2= cross_val_score(optionPoly2, X2_train, Y, cv=5)
##print("Accuracy of IP analysis crossed with Help Dataset: %0.2f (+/- %0.2f)" % (polyScore2.mean(), polyScore2.std() * 2))
##accuracyPoly="%0.2f (+/- %0.2f)" % (polyScore2.mean(), polyScore2.std() * 2)

async def preprocess_text(self, text):
    text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"[@]+", "a", text)
    text = re.sub(r"[1]+", "i", text)
    text = re.sub(r"[3]+", "e", text)
    return text

TRIGGER_WORDS = ["help","assist","how do","how to" "how can", "staff",'grief','steal','stole','killed','destroyed',"ticket","stealing","don't know","dont know",]
IP_WORDS = ['ip','server','how']

class Support(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    
    @Cog.listener()
    async def on_ready(self):
        accuracyPoly2="%0.2f (+/- %0.2f)" % (polyScore2.mean(), polyScore2.std() * 2)
        accuracyPoly="%0.2f (+/- %0.2f)" % (polyScore.mean(), polyScore.std() * 2)
        bot = self.bot
        end_time = datetime.now()
        delta = end_time - start_time
        print(f"Bot took {delta.total_seconds()} seconds to start.")
        channel = bot.get_channel(1062470547327426682)
        embed = disnake.Embed(title='Automated Help Analysis', description=f"""

    

    **IP Accuracy:{accuracyPoly}**

    Best Parameters: {optionPoly.best_params_}

    Best Estimators: {optionPoly.best_estimator_}

    **Points of IP Data: {len(Y2)}**

    **Help Accuracy:{accuracyPoly2}**

    **Points of Help Data: {len(Y)}**
    """, color=0x00ff00,timestamp=datetime.now())
        embed.set_footer(text=f"Bot ready in {delta.total_seconds()} seconds")
        await channel.send(embed=embed)

    

    @Cog.listener()
    async def on_message(self, message):
        crashed_patterns = [
        "server crashed","the server room is on fire","did the server crash","i think the server crashed","idk about you but the server clearly crashed","the server just crashed", "it just crashed"
            ]
        if message.author == self.bot.user:
            return
        with open("users.txt", "r") as file:
                # Read the contents of the file
                try:
                    users = json.loads(file.read())
                except json.decoder.JSONDecodeError:
                    users = []
        if message.author == self.bot.user:
            return
        
        crashed_response = process.extractOne(message.content, crashed_patterns, scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=70)
        if crashed_response:
            yesCrash = Button(label="Yes",custom_id=f"yesCrash",style=disnake.ButtonStyle.success)
            noCrash = Button(label="No",custom_id=f"noCrash",style=disnake.ButtonStyle.danger)
            embed = disnake.Embed(title='Did the server crash?', description=f'I heard some people talking about a crash. Is this true? Please use the buttons below to answer.', color=0xffa500)

            # Send the embed to the channel
            await message.channel.send(embed=embed, components = [yesCrash, noCrash])
            # Check if the user ID is already in the list
        if message.author.id not in users:
            # Apply pre-processing to the message
            message_content = await preprocess_text(self,message.content)
            if any(word in message_content.lower() for word in TRIGGER_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in TRIGGER_WORDS) or bool(re.search(r'\b(' + '|'.join(TRIGGER_WORDS) + r')\b', message_content.lower())):
            # Classify the message as NSFW or safe
                X_test = vectorizer2.transform([message_content])
                polyPrediction = classifier.predict(X_test)[0]
                print(message_content + " FLAGGED IN HELP WORDS")
                print(f"POLY {polyPrediction}")
                if polyPrediction == 1:
                    channel = self.bot.get_channel(913208895017717810)
                    yes1 = Button(label="Yes",custom_id=f"yes1",style=disnake.ButtonStyle.success)
                    no1 = Button(label="No",custom_id=f"no1",style=disnake.ButtonStyle.danger)
                    embed = disnake.Embed(title='Do you need help?', description=f'Use the {channel.mention} channel  to open a support ticket to get help! \nWould you like me to open a ticket for you now?', color=0xffa500)

                    # Send the embed to the channel
                    await message.channel.send(embed=embed, components = [yes1, no1])
        if message.author.id not in users:
            # Apply pre-processing to the message
            message_content = await preprocess_text(self,message.content)
            if any(word in message_content.lower() for word in IP_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in IP_WORDS) or bool(re.search(r'\b(' + '|'.join(IP_WORDS) + r')\b', message_content.lower())):
            # Classify the message as NSFW or safe
                X2_test = vectorizer.transform([message_content])
                polyPrediction2 = optionPoly.predict(X2_test)[0]
                print(message_content + " FLAGGED IN IP WORDS")
                print(f"POLY {polyPrediction2}")
                if polyPrediction2 == 1:
                # Create the embed
                    embed = disnake.Embed(title='Join the server!', description='Join through play.smpwaca.com! The server is in 1.19.3. Make sure to send the code to the Server Information bot!', color=0x00ff00)

                # Send the embed to the channel
                    await message.channel.send(embed=embed)
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
    bot.add_cog(AHS(bot))