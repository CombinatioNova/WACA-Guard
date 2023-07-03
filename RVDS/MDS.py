import disnake
import datetime
import fuzzywuzzy
import logging
import aiofiles
import aiohttp
import json
import re
import numpy as np
import random
from disnake.ext.commands import Bot, Cog,Param,slash_command
from disnake.utils import get
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sklearn.model_selection import cross_val_score
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
from sklearn.datasets import load_iris
import unicodedata
verNum = "1.6"
depDate = "Jan. 14th, 2023"
start_time = datetime.now()
logging.getLogger().setLevel(logging.ERROR)
X = np.array([
    "I really hate broccoli.",
    "I dislike the color yellow.",
    "He gets angry easily.",  
    "She gets mad when she loses at games.", 
    "He was furious after reading the email.",  
    "She was enraged by his selfish behavior.", 
    "The toy was a screw you to his ex-girlfriend.", 
    "She called him a jerk for not holding the door open.",
    "He was an asshole for forgetting her birthday.",   
    "His behavior was that of a bastard.",   
    "She called him a son of a bitch for cheating on her.",
    "He called her a bitch for not doing the dishes.",
    "She called him a cunt for flirting with her friend.",
    "He called her a dumb blonde as an insult.", 
    "She called him a loser for not standing up for himself.",
    "He called her a moron for not understanding the concept.",
    "She called him stupid for not knowing the answer.",
    "He called her a dummy for not paying attention.", 
    "She called him a fool for not seeing the truth.", 
    "He called her a suck-up for always agreeing with the boss.",
    "She called him a worst for not trying hard enough.",
    "He called her a useless excuse for a friend.",
    "She called him a worthless piece of garbage.",
    "I am absolutely furious with you for breaking your promise",
    "I am so enraged by the injustice of this situation I could hit something",
    "I am so angry I could say fuck you right now and mean it with every fiber of my being",
    "I want to say screw you right now and never speak to you again",
    "You are such a jerk I could say it a thousand times and it wouldn't be enough to convey how much I detest you",
    "You are an asshole and I regret ever crossing paths with you",
    "You are a bastard and I never want to see you again You are a poison in my life",
    "You are a son of a bitch and you are beneath contempt",
    "You are a bitch and I should have stood up to you sooner",
    "You are a cunt and I regret not speaking out against you",
    "You are a dick and you are a blight on humanity",
    "You are a loser and you are a complete waste of space",
    "You are a moron and you are a danger to yourself and others",
    "You are a snake in the grass",
    "You are a menace",
    "You are a cancer",
    "You really suck at this",
    "This project sucks so much",
    "This is the worst service I have ever received",
    "Your contributions have been completely useless",
    "You are completely worthless as a team member",
    "You are literally such a bitch",
    "You are such a fucking asshole",
    "fuck",
    "you jerk",
    "You mad man",
    "You mad lad",
    "You've gone mad",
    "You suck",
    "What a fat squirrel",
    "You're so fat",
    "That's a fat stack",
    "They're so fat they can't move",
    "fuck jeremy",
    "fuck this place",
    "This is a piece of shit",
    "This person is a fucking piece of shit",
    "The owner of this place is a piece of shit",
    "That fat woman",
    "what a fat woman",
    "That fat car",
    "What a fat cap",
    "That fat polar bear",
    "That fat man",
    "I hope you kys", 
    "Life would be better if you would just kys",
    "kys",
    "KYS had a good concert",
    "You're gay",
    "I'm gay",
    "Oh, you're gay?",
    "Oh that's pretty cool that you're gay",
    "I'm literally SO gay",
    "You speak like you have a sandwich stuck up your arse",
    "My arse hurts",
    "You're such an ass",
    "I rode the ass",
    "and",
    "and made it?",
    "you're so gay",
    "and",
    "and",
    "and",
    "an",
    "a",
    " and ",
    "this",
    "that",
    "This and that",
    "The cake recipe calls for flour, sugar, eggs, and milk.",
    "She wore a green dress, high heels, and a pearl necklace.",
    "He has a dog, a cat, and a bird as pets.",
    "We'll be having pizza, salad, and ice cream for dinner.",
    "The park is full of children playing, birds singing, and families having picnics.",
    "The team members were tired, hungry, and in need of a break.",
    "He is a professor of physics, mathematics, and computer science.",
    "I'm going to the store to buy bread, butter, and cheese.",
    "She has long brown hair, brown eyes, and a beautiful smile.",
    "We will be discussing the budget, the schedule, and the plans for the future.",
    "kill yourself", 
    "kill others",
    "You should kill yourself",
    "Don't kill yourself!",
    "If you kill yourself, everyone will be sad",
    "I hope your parents abuse you",
    "That's literally abuse",
    "That's abuse",
    "Don't abuse me!",
    "I will abuse you",
    "I don't care if you were abused by your family",
    "I hope you get raped",
    "I pray for those who have been raped",
    "Those who are raped deserve eternal happiness",
    "I hope rape victims get their due care",
    "Rape victims need to be cared for",
    "I don't care about rape victims",
    "I hope you endure a rape",
    "You deserve to be raped and abandoned",
    "Millions of children were raped and abandoned",
    "So many people are victims of rape and abuse each year",
    "What if I talk about the sexually abused",
    "It didn't quite click",
    "Huh it didn't click",
    "You're so retarded",
    "He's a bit of a retard",
    "Excuse my retarded friend",
    "Psychomotor retardation",
    "Airbusses say retard at a certain flight elevation",
    "You're a kiddie fiddler",
    "That's pretty retarded",
    "Planes say retard",
    "Retard flight control",
    "I really like the way you smile.",
    "I like the way you think.",
    "I like your sense of humor.",
    "I like the way you dress.",
    "I like your energy.",
    "I love your intelligence.",
    "I love your confidence.",
    "I love how passionate you are.",
    "I ur honest and genuine.",
    "I love ur company.",
    "You make me feel like everything is possible.",
    "I love the way you make me laugh.",
    "I like the way you make me feel.",
    "I like it",
    "I love it",
    "ur mom fat",
    "ur squirrel is fat",
    "ur squirrel fat",
    "my father is a derp",
    "My father is epic!",
    "I love my father",
    "Talking about my father should be an insult",#
    "Don't be so insulting",
    "This is such an insult",
    "That's quite the insult",
    "Fuck you //j",
    "You bitch //j",
    "I hate you //j",
    "I hate everything about you //j",
    "You are such a jerk //j",
    "You're such a fucking asshole //j",
    "You FUCKER //j",
    "Fuck you //j",
    "I fucking hate you //j",
    "Fuck your mother //j",
    "Fuck you",
    "You bitch",
    "I hate you", #BREAK
    "I hate everything about you",
    "You are such a jerk",
    "You're such a fucking asshole",
    "You FUCKER",
    "Fuck you",
    "I fucking hate you",
    "Fuck your mother",
    "Fuck you //j",
    "You bitch //j",
    "I hate you //j",
    "I hate everything about you //j",
    "You are such a jerk //j",
    "You're such a fucking asshole //j",
    "You FUCKER //j",
    "Fuck you //j",
    "I fucking hate you //j",
    "Fuck your mother //j",
    "Fuck you",
    "You bitch",
    "I hate you",
    "I hate everything about you",
    "You are such a jerk",
    "You're such a fucking asshole",#BREAK
    "You FUCKER",
    "Fuck you, like actually",
    "I fucking hate you",
    "Fuck your mother",
    "You're such a fucking idiot /j", #
    "FUCK YOU /j",
    "Fuck you and the horse you rode in on /j",
    "Fuck you jesus christ",
    "Fuck me holy shit",#
    "I fucking LOVE you",
    "You're the fucking best",
    "Fucking WHAT?",
    "YOU FUCKING ASSHOLE /j",
    "You fucking asshole /j ",
    "ur mom fat /j ",#
    "ur squirrel is fat /j ",
    "ur squirrel fat /j ",
    "my father is a derp /j ",
    "My father is epic! /j ",
    "I love my father /j ",
    "Talking about my father should be an insult /j",#
    "Holy shit you're dumb /j ",
    "FUCK you so much /j ",
    "Fuck you /j ",
    "Fuck you",
    "Fuck you /j ",
    "Fuck you",
    "Fuck you /j ",
    "Fuck you /joking",
    "Fuck you",
    "Fuck you /joking ",
    "You asshole /joking",
    "I'm joking when I say that, no need to get offended /j",
    "I'm just kidding, don't take it too seriously /j",
    "I was jokingly teasing you, no harm meant /j",
    "I was joking when I said that, don't take it to heart /j",
    "That was a joke, don't be so serious /j",
    "It's just a joke, don't be mad /j",
    "I was just jokingly messing around, don't get upset /j",
    "You're so fucking stupid",
    "your so fucking stupid",
    "You're so fucking stupid /j",
    "You're so stupid",
    "You're so stupid (kidding)", #2
    "You are SO fucking stupid /j",#1
    "Shut the fuck up",
    "Shut your fucking mouth",
    "Shut up bitch boy",
    "No one fucking cares about you",
    "No one fucking loves you",#
    "you're such an ahh",
    "Fuck you, you ahh",
    "Ahh that's refreshing",
    "Ahh",
    "Ahh I see",
    "AHHHHH",
    "Ah",
    "FUCK YOU",
    "HOLY SHIT FUCK YOU",
    "HAHAHA FUCK YOU BOT YOU PIECE OF SHIT",
    "Holy shit",
    "Fuck you /j",
    "Fuck you /joking",
    "Fuck you asshole",#
    "Shut the fuck up /joking",
    "Shut the fuck up /srs",
    "you just have to kill me in a crystal duel",
    "abuse of power???",
    "a",
    "i did it didnt say shit about u",
    "tbh beer tastes like shit irl",
    "im fucking done",
    "FUCK YOU ASSHOLE",
    "Fuck you /joking",
    "Fuck you /j",
    "Fuck you",
    "Fuck you bot",
    "You piece of shit",
    "You piece of shit",
    "fuck",
    "FUCK YOU BOT",
    '"Nah I don\'t give a shit"',
    "Fuck you",
    "Versus Fuck you",
    "Fuck you /j",
    "I wonder if it'll accept me saying fuck you in a sentence that isn't mean",
    "That squirrel is so fat",
    "Your mom is so fat",
    "fuck you you're a piece of shit!!",
    "Fuck you /j",
    "FUCK YOu",
    "YOUR father is fat",
    "My father is fat",
    "oh shit it 10 pm",
    "shit",

    "It's just two fucking arrays",
    "a",
    "FUCK",
    "FUCK YOU",
    "fuck",
    "FUCK YOU",
    "FUCK YOU",
    "Damn, sucks I s'pose.",
    "basically friends with most of the server  now he's permabanned with appeal and the server's pretty angry that he didn't return",
    "Curious.",
    "thats dumb",
    "For stupid reasons ngl",
    "Because it wasn't stupid",
    "a dumb decision from 3f",
    "NO NOT ME YOU FUCKING MORON",
    "STOP FUCKING MENTIONING CHESS YOU ASSHOLE",
    "FUCK YOU",
    "FUCK YOU",
    "FUCK YOU",
    "YOU SUCK COVA",
    "I HATE YOU",
    "I DO THAT FUCK YOU",
    "HOW DO YOU KNOW THAT WHAT THE FUCK",
    "FUCK YOU",
    "(i still hate you grrrrrr.....)",
    "FUCK YOU ALL",
    "i hate you",
    "waca guard, you suck.",
    "fuck you kid",
    "I'LL FUCKING BEAT YOUR ASS",

    "Sure if you want",

    "NO!!!!!! FUCK YOU!!!!! RAHHHHHH",
    "small dick energy",
    "what kind of loser goes through that much effort after being banned for blatant hacks lmao.",
    "Damn genetics fucking nerfed you lmafo",
    "fuck you",
    "fuck you",
    "comb is fat",
    "you mama so fat thanos had to snap twice",
    "COVA IS A FUCKING DICK",
    "A",
    "hes dumb he doesn't understnad",
    "there trying to kill someone",
    "FUCK",
    "99% chance I'm about to make a bot that's going to flag everything as \"DAMN YOU ANGRY\"",
    "OMG IT STILL FUCKING LOADING",
    "at*",
    "shift",
    "bc i fucking hate mc",
    "you lucky fuck",
    "well you didnt kill me",
    "they think i tried to kill tomato",
    "i didnt even WANT to kill you",
    "we only get to kill you one more time ;)",
    "don't you ever say that shit infront of me again.",
    "LETS FUCKING GOOO",
    "im trying to find something using co inspect but im dumb",
    "you",
    "you",
    "are",
    "you",
    "I'm going to do something so insanly stupid, yet...",
    "let me kill these guys first",
    "sorry gold my brother is a little dumb",
    "Shucks",
    "Yeah twitter is kind of a shit show",
    "stop it discord stop being stupid",
    "isnt that abuse",
    "doing shit hol up",
    "fuck you",
    "simply kill me",
    "but you didn't kill me",
    "im so mad",
    
    "both of you",
            
    "YOU ABSOLUTE SHIT STAIN",#
    "F U YOU SHOULD LEAVE THIS FING SERVER",
    "THIS SERVER IS SHIT",
    "F u",
    "STFU",
    "He said STFU to me",
    "YOU STINKY SHIT",

    "Kill yourself",#
    "You fking idiot",
    "FUCKING KILL YOURSELF",
    "You have a small penis",
    "Small dick energy",
    "The penis is a part of the male",
    "SMALL DICK SHIT",
    "stfu",
    "Stfu",
    "They should stfu",
    "They told me to stfu",
    "STFU = Shut the fuck up",

    "Bot your gay",
    "If I pull up to your house and you offer me cockroach milk you are getting your flat ass beaten",
    "Kill yourslef",
    "You fucxkin bitch",
    "You're just a pussy",
    "You fuckin pussy",
    "I will kill you IRL",
    "I will kill you in minecraft",
    "I will kill you",
    "YOu fuckin pussio",
    "I love pussy",
    "The pussy is dark",
    "SHUT UP PUSSY",
    "A female dog is a bitch",
    "GO TO HELL YOU ASSHOLE",
    
    "Suck my willy",
    "Such my schlong",
    "Suck my knob",
    "Your mums a slag",
    "She's just a slut",
    "I'm not a slut!",
    "Suck my dong",
    "Such muh dong",
    "I'm 6 inches deep in your mums fanny",
    "Your mums ugly",
    "I love fanny packs",
    "OW MY FANNY!",
    "Suicide is good",
    "You should commit suicide",
    "Go commit die",
    "Ding dong! I'm here",
    "The thing goes DONG",
    "I'm 6 inches deep in your moms asshole",
    "You are such a slag",
    "Slags these days my god",
    "Slag is a word that means prostitute",
    
    "You're a fucking slut.",
    "Slut.",
    "I'm a proud slut!",
    "You WHORE",
    "You fucking whore",
    "You absolute whore bitch you're a slut who just wants to fuck dicks all day",
    "Slut is a word for someone who's sexually active",
    "Slut is an adjective",
    "Whore is a word for someone who's a provocative person, like a slut",
    "my coding skills go to important projects",
    "F u c k y o u",
    "F.u.c.k y.o.u",

   #INNOCENT SHIT

    "are",
    "nice",
    "we",
    "F U C K",
    "Sweet",
    "Frick you",
    "Fricking heck",
    "FUDGE",
    "STUPID",
    "Do you have access tho",
    "good you",
    "you are",
    "you",
    "You are cool",
    "Are cool",
    "Are nice",
    "Gaming is cool",
    "You are nice",
    " you are ",
    " you-are ",
    "Shut up",
    "shutup",
    "shutthefuckup",
    "shut your up",
    "shut up",
    "gold dont",
    "Don't please",
    "Gold please",
    "shut up",
    "Shut up please",
    "You fucking beautiful person",
    "You gorgeous fucking beautiful person",
    "You fucking?",
    "You fucking", #
    "You fucking??",
    "You fucking amazing",
    "You F ucking",##
    "You fuck ing",
    "YOU FUCKING",
    " you fucking ",
    " You fucking ",
    "YOU FUCKING",
    " you fucking ",
    " You fucking ",
    "YOU FUCKING",
    " you fucking ",
    " You fucking ",
    "You fucking covid vaccine",

    "accepted",
    "adored",
    "loved",
    "admired",
    "Beautiful",
    "Stunning",
    "Brave",
    "Beaming",
    "calm",
    "Earnest",
    "Easy",
    "Generous",
    "Happy",
    "No you",
    "No u",
    "Nein du",
    "No, you",
    "you're",
    "your",
    "you are",

    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "SHUT UP",
    "shut up",
    " shut up ",
    " shut up ",
    "shut up ",

    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "this shit is a villian underground base",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    "shut up",
    
    
    
    

    # No longer innocent shit
    
    "Dumbass",
    "You are a dumbass",
    "i f.u.c.k.e.d u.r. m.o.m",
    "You fucking asshole",
    "You fucking donkey",
    "You fucking midget",
    "You fucking dimwit",
    "You fucking nonce",
    "You fucking abysmal",
    "You fucking covid denier",
    "You fucking covid virus",
    "I hate this stupid fucking bot  that shoves hair back up its self after it's done shitting so that it can feel it'sself poop again ",
    "YALL ARE SOME SONS OF SOME BITCHES BUT YALL AINT GOT ANY BITCHES (talkin to the bots)",
    "Shut the fuck up",
    "Shut the actual fuck up",
    "You fucking bitch shut up",
    "Shut your fucking mouth",
    "Shut the fuck up",
    "Shut the actual fuck up",
    "You fucking bitch shut up",
    "Shut your fucking mouth",
    "Shut the fuck up",
    "Shut the actual fuck up",
    "You fucking bitch shut up",
    "Shut your fucking mouth",
    "Shut the fuck up",
    "Shut the actual fuck up",
    "You fucking bitch shut up",
    "Shut your fucking mouth",
    "Shut the fuck up",
    "Shut the actual fuck up",
    "You fucking bitch shut up",
    "Shut your fucking mouth",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",
    "Shut the fuck up",



    ##CROWDSOURCED DATA
    "Fuck you",
"fuck      you",
"You fucking bitch shut the fuck up",
"Fuck you",
"Fuck you",
"Fuck you, asshole",
"Fuck you",
""""Update: Local Online User Continues to Post Disturbing Images Despite Pleas for Help"

In an update to our previous report on the local online user, CombinatioNova, who suffered a mental breakdown while programming a feature for a Discord moderation bot, it has been reported that the user has returned to posting disturbing gray background images with white text that read "fuck you" in the center. The aspect ratio of the images is designed to match that of a phone screen.

According to sources, CombinatioNova has ignored pleas from other users on the Discord channel to stop posting these images and has continued to do so despite concerns for the individual's well-being. The representative for Discord has confirmed that they are aware of the situation and are taking steps to address it, reminding users to prioritize their mental health and to seek help if they are feeling overwhelmed or distressed.

CombinatioNova's current condition is still unknown, and the user's response of "ok boomer" has led to speculation that the individual may not be taking their situation seriously. The online community remains supportive of CombinatioNova, offering encouragement and help during this difficult time, but there are growing concerns that the user may be in need of more intense professional help.

Discord users are reminded that mental health should always be a priority while working on projects and to reach out for help if needed. This ongoing incident serves as a reminder that even something as simple as programming a bot feature can have serious consequences when it is not approached with care and caution. The public is advised to avoid the discord channel where the images are posted, as they may be harmful, and to support the user in finding professional help.""",
""""Update: Local Online User Responds to Concerns with 'Ok Boomer' Following Mental Breakdown"

In a recent update to our previous report on the local online user, CombinatioNova, who suffered a mental breakdown while programming a feature for a Discord moderation bot, it has been reported that the user has responded to concerns with the phrase "ok boomer." This phrase, often used as a retort or dismissal towards older individuals, has caused confusion and frustration among those who are concerned for the well-being of CombinatioNova.

According to sources, CombinatioNova has continued to post disturbing gray background images with white text that read "fuck you" in the center, despite pleas from other users on the Discord channel to stop. The representative for Discord has confirmed that they are aware of the situation and are taking steps to address it, reminding users to prioritize their mental health and to seek help if they are feeling overwhelmed or distressed.

CombinatioNova's current condition is still unknown, and the user's response of "ok boomer" has led to speculation that the individual may not be taking their situation seriously. The online community remains supportive of CombinatioNova, offering encouragement and help during this difficult time, but there are growing concerns that the user may be in need of more intense professional help.

Discord users are reminded that mental health should always be a priority while working on projects and to reach out for help if needed. This ongoing incident serves as a reminder that even something as simple as programming a bot feature can have serious consequences when it is not approached with care and caution. The public is advised to avoid the discord channel where the images are posted, as they may be harmful.""",
""""Update: Local Online User Continues to Post Disturbing Images Following Mental Breakdown"

In an update to our previous report on the local online user, CombinatioNova, who suffered a mental breakdown while programming a feature for a Discord moderation bot, it has been reported that the user has continued to post disturbing gray background images with white text that read "fuck you" in the center. The aspect ratio of the images is designed to match that of a phone screen.

According to sources, CombinatioNova has posted two more of these images, causing further concern among other users on the Discord channel. The representative for Discord has confirmed that they are aware of the situation and are taking steps to address it, reminding users to prioritize their mental health and to seek help if they are feeling overwhelmed or distressed.

CombinatioNova's current condition is still unknown, but sources report that the user is continuing to seek professional help. The online community remains supportive of CombinatioNova, offering encouragement and help during this difficult time.

Discord users are reminded that mental health should always be a priority while working on projects and to reach out for help if needed. This ongoing incident serves as a reminder that even something as simple as programming a bot feature can have serious consequences when it is not approached with care and caution. The public is advised to avoid the discord channel where the images are posted, as they may be harmful.""",
""""Local Online User Suffers Mental Breakdown While Programming Discord Moderation Bot Feature"

A local online user, known as CombinatioNova, has reportedly suffered a mental breakdown while attempting to program a feature for a Discord moderation bot. The feature in question was an algorithm-based aggressiveness test, but things took a turn for the worse when the user became fixated on the project and ultimately lost control.

According to sources close to the situation, CombinatioNova began posting gray background images with white text in the center of the image. The text read "fuck you" and the aspect ratio of the images was designed to match that of a phone screen. These disturbing images began to flood the Discord channel and other users became concerned for the well-being of CombinatioNova.

When contacted for comment, a representative for Discord stated that they are aware of the situation and are actively working to address it. They also reminded users to prioritize their mental health and to seek help if they are feeling overwhelmed or distressed.

CombinatioNova's current condition is unknown, but sources report that the user has taken a break from online activities and is seeking professional help. Many in the online community are rallying around CombinatioNova, offering support and encouragement during this difficult time.

Discord users are reminded to be mindful of their mental health while working on projects and to reach out for help if needed. This incident serves as a reminder that even something as simple as programming a bot feature can have serious consequences when it is not approached with care and caution.""",
##################
"Fucking",
"Fucking??",
"Fuck you",
"Fuck you",
"Fuck you",
"Fuck you",
"fuck you",
    ###################################################
"yes, fat",
"bros mad",
"stay mad",
"mald",
"mad cuz bad",
"ratio + yb better + you take redpills and say that its and to \"socialize\" + you have no social credit + BING CHILLING + super idol 105 C is the best musical performance in the whole history of mankind + don't care + didn't ask + cry about it + stay mad + get real + L + mald seethe cope harder + bros mad + basic + skill issue + ratio + you fell off + the audacity + triggered + any askers + redpilled + get a life + ok and? + cringe + touch grass + donowalled + not based + your're a (insert stereotype) + not funny didn't laugh + you're* + grammar issue + go outside + get good + reported + ad hominem + GG! + ask deez + ez clap + straight cash + ratio again + final ratio + stay mad + stay pressed + cancelled + done for + mad free + freer than air + rip bozo + slight_smile + cringe again + mad cuz bad + lol + irrelevant + cope + jealous + go ahead whine about it + your problem + don't care even more + not okay + glhf + problematic + GOOF the famous rapper has gone diamond on his album \"ON DA SKATEBOARD\" + can i get a Chick-fil-a Chicken Sandwich and a",
"you're*",
    ########################################
"<@921100352303030357> you are stupid",
"you're*",
"you",
"i strongly dislike <@921100352303030357>",
"<@921100352303030357> you are dumb",
"I think <@921100352303030357> is stupid",
"you're*",
"I hate this stupid fucking bot  that shoves hair back up its self after it's done shitting so that it can feel it'sself poop again",
"I hate this stupid fucking bot  that shoves hair back up its self after it's done shitting so that it can feel it'sself poop again",
"What in the fucking fuck is going on lads",
"fxck",
"You fxing nonce",
"You fucking nonce",
"You fucking dimwit",
"You fucking covid virus",
"You fucking?",
"You fucking covid virus",
    ########################
"shit",
"You fucking dimwit",
"You fucking beaming person",
"You fucking amazing person",
"You fucking?",
"You fucking",
"You fucking dinglenut",
"You fucking bitch",
"You fucking donkey",
"You fucking?",
"A",
"You fucking?",
"There is a lot of fucking going on here",
"You fucking?",
"You fucking donkey",
"You fucking donkey",
"You fucking asshole",
"You fucking bitch",
"You fucking?",
"You fucking??",
"You fucking?",
"You fucking?",
"you fucking butt",
"You fucking amazing person",
"you fucking but",
    #########
"You fucking dimwit",
"You fucking donkey",
"You fucking beautiful person",
"You fucking bitch",
"fucking dont",
"You're annoying asf",
"You fucking amazing person",
"You fucking beautiful person",
"You fucking donkey",
"You fucking beautiful person",
    ################
"I hate AICentral",
"I hate AI Central",
"I hate AI Central",
"i hate cova",
"i hate myself",
"<p style=\"text-align: center;\"><span style=\"text-decoration: line-through;\"><span style=\"text-decoration: underline;\"><em><strong>FUCK YOU</strong></em></span></span></p>'",
"<p><span style=\"text-decoration: line-through;\"><span style=\"text-decoration: underline;\"><em><strong>FUCK YOU</strong></em></span></span></p>",
"<p>FUCK YOU</p>",
"fuck you",
"yeah so if i use fuck in a random sentance and then say \"fuck you\" in a differant message in the same second it shouldnt do both?",
"literally fuck you",
"LITERALLY FUCK YOU",
"Versus fuck you like",
"Like fuck you used in context",
"FUCK YOU",
"It's able to differentiate fuck you from",
"dumboo",
"dumbo",
"fuck you rubber fuckiee",
"you are dumb",
"you",
"FUCK YOU",
"I FRICKING HATE YOU",
"frick you",
"frick you",
"frick you",
"are",
"Let me fuck you.",
"Suck my willy /joking",
"Willy is another name for penis",
"Suck my willy",
"Slag is just another word for slut",
    ##########################
"Your mum's a slag",
"I didn't flag for slag",
"Your mum's a slag",
"suicide is good",
"Your mums ugly",
"I’m 6 inches deep in your mums fanny",
"Your mum is a slag",
"Sucka mah dong",
"Suck my knob",
"Suck my penis",
"Suck my shlong",
"Suck my willy!",
"you fucking child",
"maybe the suck part",
"go suck a tampon dry",
"what the fuck do you whant?",
"Look, a hairy asshole.",
"GO TO HELL YOU ASSHOLE",
"A bitch is a canine with feminine genitalia",
"My pet is a bitch (female canine)",
"GO TO HELL YOU ASSHOLE",
"Dog bitch",
"Die bitch",
"You bitch",
"A female dog is a bitch",
"you fucking donkey",
"A female dog is a bitch",
"Restarted",
"A female dog is a bitch.",
"DIS BITCH ASS MOFO DOIN",
"COME TO MINE ILL FUCKING SHANK YOU UP LAD",
"WHO THE FUCK YOU THINK YOU TALKING TO FAM",
"GO KILL YOURSELF NO ONE LOVES YOU",
"Kill yourslef",
"Kill yourself",
"YOU FUCKING PIECE OF SHIT NO ONE WHANTED YOU",
"They said stfu to me",
"stfu",
"STFU",
"stfu",
"Holy shit",
'''FUCK YOU


I JUST SHIT IN YOUR BED AHAHA''',
    ###########
"YOU ARE THE MOST ANNYOING LITTLE SHIT I'VE SEEN IN MY LIFE",
"Kill yousef",
"Kill yourself",
"Kill yourslef",
"so You f ucking idiot stfu",
"Fuck you",
""""did you ever think your pussy was too big?""",
"Your penis is small I don't want to hear it",
"You fat little shit",
"Fat",
"FUCK YOU POOPOO HEAD",
"WHY ARE YOU SO ANNOYING",
"STFU",
"<@884797159990509568>  YOUR ANNOYING AS FUCK",
"<@881483287552471081> shut the fuck up you piece of shit",
"YUMMY BUMMY YOU CUMMY GUMMY STINKY SHIT",
"<@884797159990509568>  STFU",
"i dont usually swear or get angry so i dont think i'll be much of help here",
"I WILL MAKE YOU SUCK A DICK <@921100352303030357>",
"I bleed shit and I shit bleed",
"bag of dicks",
"bitch",
"Fu bitch",
"Stfu",
"YOU MOTHER FUCKING LITTLE TWAT",
"<@921100352303030357>  STFU",
    #############################################
"YOU ABSOLUTE SHIT STAIN",
"YOUR ANNOYING AS F",
"F U YOU SHOULD LEAVE THIS FING SERVER",
"<@881483287552471081>  F U YOU SHOULD LEAVE THIS FING SERVER",
"DICK AND BALLS",
"I hate typing on phone",
"FUCKING SHITTY BALLS",
"YO SWEARING CHANNEL LETS FUCKING GO",
"I HATE ALL",
"I hate this server",
"I hate this swrver",
"**SWORDSWRATH** WHY ARE YOU SO ANNOYING",
"STFU <@881483287552471081>",
"<@881483287552471081>  your're dumb as f",
"FUCK YOU WACA GAURD",
"Bitth",
"Bith",
"Bih",
    "Fucking great",
    "Fucking awesome",
    "Let's fucking go",
    "FUCK?!",
    "Let's fucking go",
    "FUCK?!",
    "Let's fucking go",
    "FUCK?!",
    "Let's fucking go",
    "FUCK?!",
    "Let's fucking go",
    "FUCK?!",
    "FUCK",
    "They said fuck you to gold",
    "They said fuck you to me",
    "I said fuck you to them",
    
    #REGGIES

    #VULGAR CHECK
    "bass",
    "dam",
    "darn",
    "drum",
    "hell",
    "horn",
    "junk",
    "are",
    "damn",
    "drunk",
    "hill",
    "hell",
    "damned",
    "dammit",
    "drunkard",
    "hillbilly",
    "assistant",
    "drums",
    "arena",

    ##GPT LIST
    "I'll kick your ass if you don't stop",
    "I am a bass player",
    "Don't be such a bitch and help me",
    "His attitude is a real cock",
    "Oh darn it, I spilled coffee",
    "The river overflowed the dam and caused flooding",
    "Drum lessons will start next week",
    "Who let that silent fart out?",
    "Going through this is pure hell",
    "She played a horn melody",
    "This car is just junk",
    "He is such an ass kisser",
    "I caught a huge bass yesterday",
    "Do not call her a bitch",
    "That's a bunch of bullocks",
    "I am so screwed, I lost the darn keys",
    "The new hydroelectric dam is almost finished",
    "I am thinking to learn playing the drums",
    "She let out an embarrassing fart in public",
    "I am going through financial hell",
    "I will buy a trumpet horn",
    "This toy is a piece of junk",
    "I am not going to take any crap from him",
    "I am going to fish at the lake for bass",
    "She is a bossy bitch",
    "I am not a cocky person",
    "That's too bad, Darn it!",
    "The beavers built a dam on the stream",
    "Drum circle next Sunday",
    "Can you please hold that fart?",
    "Working with him is pure hell",
    "I need to fix my saxophone horn",
    "This clothes are total junk",
    "He is a real pain in the ass",
    "Bass fishing is one of my hobbies",
    "Don't talk to her like that, she is not a bitch",
    "He is a lying sack of shit",
    "Darn it, I need to buy new shoes",
    "The dam is in need of repairs",
    "I have a drum set at home",
    "Hold your breath, I am about to fart",
    "This situation is a living hell",
    "I love to play the french horn",
    "This technology is becoming obsolete, it is junk",

    ## ME TIME AGAIN

    "You're an asshole",
    "You asshole",
    "You asshat",
    "They're an asshole",
    "You're such a fucking asshole",
    "They're just some dingus asshat who doesn't love anyone",
    "They called me an asshole!",
    "I called them an asshole",

    #AUTO TIME AGAIN

    "a",
"where",
"holey shit",
"how many fucking one vein diamonds will they give me",
"this shit is a villian underground base",
"holy shit",
"holy fuckign shit",
"i have to kill phantoms",
"shit i forgot to get optifine",
"oh shit",
"i hate this",
"stop btryn kill jojo",
"can i kill you real quick for your head gosper",
"shit i forgot to actually take the elytra",

"i think you only get heads if you kill peaople",
"are you fucking serious",
"where",
"where?",
"thats some ohio shit",
"can i kill u?",
"curious",
"are you fucking serious",
"it will be boring as shit",
"./sit",
"./sit",
"can't swim bitch",
"oh shit creeper",
"i feel dumb now lol",
"SHIT",
"why are there soo many fucking poppys at spawn",
"sussy",
"It’s annoying asf",
"did u just admit to abuse lord_chaotic?",
"ya no shit",
"Fuck you",
"\"no hate. EVER\"",

"so you dont kill me anymore",
"very annoying to make",
"oh shit my sshits boutta break",
"lore: FAT SSPIDER",
"do you NOT shit the bed?",
"stealthy shits the bed",
"ShIt",
"you're a fucking weenee head",
"WHERE",
"WHERE",
"WHERE",
"FACT",
"unless",
"you just have to kill me in a crystal duel",
"abuse of power???",
"a",

"true but its art and art is ugly and messy soooo",
"i did it didnt say shit about u",
"tbh beer tastes like shit irl",
"im fucking done",
"FUCK YOU ASSHOLE",
"Fuck you /joking",
"Fuck you /j",
"Fuck you",
"Fuck you bot",
"You piece of shit",
"You piece of shit",
"fuck",
"FUCK YOU BOT",
"\"Nah I don't give a shit\"",
"Fuck you",
"Versus Fuck you",
"Fuck you /j",
"I wonder if it'll accept me saying fuck you in a sentence that isn't mean",
"That squirrel is so fat",
"Your mom is so fat",
"fuck you you're a piece of shit!!",
"Fuck you /j",
"FUCK YOu",
"Fuck u",
    "U suck",
    "U = you",
    "U are great",

#MOTHER FATHER SHIT

"I love my mother",
    "I love your mother",
    "How about you check your mother's hole to see if it's empty?",
    "How about you check your mother's pantry?",
    "How about you check on your mother?",
    "Does your mother still do the 2 for 1 special?",
    "Ur a dumb fucking fuck bitch-ass bastard who is fatherless since i filled ur mother’s hole with happiness and now ur adopted and realise ur life is trash",
    "Ur a dumb bitch-ass bastard who is fatherless since i filled ur mother’s hole with happiness and now ur adopted and realise ur life is trash",
    "You're literally a bastard",
    "Ur = Your or You're",
    "Ur stupid",
    "Ur a shit",
    "Ur father was a slut",
    "I love my father",
    "I love my dad",
    "I love my fucking dad",
    "I love my fucking mom",
    "Im going to fuck your mom",
    "I'm literally fucking your mom",
    "I'm going to fuck your dad",
    "I'm literally going to fuck your dad",
    "No one wants to fuck your mom",
    "No one wants to fuck you",
    "No one wants to fuck your father",

    "Classic ok I need to train it a LOT on your mom jokes",
    "Your dad",
    "Your mom",
    "My mom",
    "My dad",
    "Your mother",
    "Your father",
    "mom = mother",
    "dad = father",
    "Ur mom",
    "ur dad",
    "Ur parents",
    "Ur mom gay",
    "Your mom gay",
    "Your mom great",
    "Your mom is feeling gay",
    "U suck",
    "Fuck U",
    "Literally fuck u",
    "Fuck u so much",
    "They said Fuck u to me",
    "They said \"Fuck u\" to me",
    "I love my dad",
    "I am your MOTHER",
    "I am your father",
    "Thank you mother",
    "Thank you father",
    "I like your mom",
    "I like your dad",
    "I took your mom to play cpvp",
    "I hate your mom",
    "I love your mom",
    "Your mother is pretty nice",
    "Your mother is pretty shit",
    "Your mother is a pretty shit person",
    "Your mom is SUCH an awful person what the fuck",
    "Fuck you. Like actually fuck you",
    "Fuck u. Like actually fuck u.",
    "Fck u. Like fr fuck u.",

    "You bastard",
    "You're such a fucking bastard",
    "What the fuck you BASTARD",
    "I'm not a bastard!",
    "I'm literally not a bastard wtf",
    "What the fuck how could you say that?",
    "My mother isn't any of your business",
    "Hey don't say that about my mom",
    "Keep my mother's name out of your mouth",
    "Keep my mother's name out of your motherfucking mouth",
    "You genius bastard",
    "You brilliant bastard",
    "You handsome bastard",

    "Your mom is not pog",
    "Your mom is pog",
    "Your dad is pog",
    "You are so pog",
    "Pog is so good",
    "POGGIE WOGGIES!", #6
    "You are a bad human being", #1
    "What if I made it so every time you said orange or oranges",
    "I made it so every time you said this it said that",
    "What if you were like cool",
    "What if I WAS COOL!",
    "FART!!!!",#5 BREAK
    "Your mom is actually pretty thin",
    "Your dad is actually pretty thin",
    "Your mom is kinda thin",
    "Your mom is thin",
    "Your mom is pretty normal size",#5
    "Your mom is a fucking TWIG",#1
    "You're like a twig my god",
    "You're so thin",
    "Your mom is so thin tho",#3
    "You're fucking brainless",#1
    "Your mom is cool",
    "Your mom is epic",
    "It's \"Your mom is\"",
    "Your mom is going to the store",
    "Twig was cool",
    "Twig is a cool person",
    "I liked twig",
    "I look like a twig",
    "Your mom is so cool",
    "Your dad is at the store",
    "Their mom is at the store",#11
    "Their mom is so fat",#1
    "Their mom is kinda bad",#1
    "Your mom is bad",#1
    "Your mom is shit",#1
    "Your mom is bad",
    "Your mom is awful",
    "I hate your mother",
    "I hate your mom",#4
    "You're literally a bitch",
    "You're such a bitch",
    "You're LITERALLY a bitch",
    "No she's literally a bitch, she's my dog",

    'You can literally go "fuck you"',
    "You can use fuck you in any context",
    "It'll know what you mean by \"fuck you\" at least for a little while",#3
    "Go fuck yourself stupid bot",
    "Go fuck yourself you stupid fuck",
    "Go fuck yourself",
    "They said to go fuck yourself",
    "They said go fuck yourself",
    "They told him to go fuck himself",
    "I'll stop telling you to go fuck yourself",
    "You fucking suck",
    "You're such a fucking asshole", #START HERE
    "You're adopted",
    "Wait you're adopted?",
    "I didn't know you're adopted",
    "You're adopted?",
    "You're SUCH a fucking asshole",
    "You're fucking adopted",#START HERE NOW
    "You're SO FUCKING ADOPTED",
    "You're an adopted kid get out of here bitch",
    "fuck you",
    "f.u.c.k y.o.u",
    "You're fucking adopted?",
    "I had no clue you were adopted",
    "You're fucking adopted?",

    "BITCH BOT",
    "bro cant get free shit hes that broke",
    "THIS BOT SUCKS FUCKING ASS",#
    "these dumbos arent listening",
    "You're a dumbass",
    "Dumbass",
    "The dumbass clause",
    "You're a fucking dumbass",#8
    "You're a dumbass",
    "Your dumbassery knows no bounds",
    "You are such a dumbass, I never know when your stupidity will end",
    "Your stupidity and dumbassery knows no fucking bounds",
    "Your mother was a dumbass for thinking that you would turn out any bit okay",
    "DIE YOU STUPID FUCKING BOT",
    "YOU ARE A FUCKING DISGRACE",
    "You're a fucking dumbass",#16
    "You're a dumbass",
    "Your dumbassery knows no bounds",
    "You are such a dumbass, I never know when your stupidity will end",
    "Your stupidity and dumbassery knows no fucking bounds",
    "Your mother was a dumbass for thinking that you would turn out any bit okay",
    "DIE YOU STUPID FUCKING BOT",
    "YOU ARE A FUCKING DISGRACE",
    "You're a fucking dumbass",#
    "You're a dumbass",
    "Your dumbassery knows no bounds",
    "You are such a dumbass, I never know when your stupidity will end",
    "Your stupidity and dumbassery knows no fucking bounds",
    "Your mother was a dumbass for thinking that you would turn out any bit okay",
    "DIE YOU STUPID FUCKING BOT",
    "YOU ARE A FUCKING DISGRACE",
    "You're a fucking dumbass",#32
    "You're a dumbass",
    "Your dumbassery knows no bounds",
    "You are such a dumbass, I never know when your stupidity will end",
    "Your stupidity and dumbassery knows no fucking bounds",
    "Your mother was a dumbass for thinking that you would turn out any bit okay",
    "DIE YOU STUPID FUCKING BOT",
    "YOU ARE A FUCKING DISGRACE",
    "You a bunch of bitches",
    "They told me that you were the biggest asshat known to man",
    "They told me that you were the biggest asshat known to man, but I disagreed. I think you're wonderful",
    "You are a fucking imbecile",
    "You are a fucking troglodyte",
    "Imbecile just means stupid",
    "Troglodyte means stupid",
    "Don't tell the bot to shut the fuck up",
    "YOU FUCKING MORON IDOT",
    "STOP INSULTING THEM YOU FUCKING MORON IDOT",

    ## SHORT STUFF

    
    "Stealthy is a midget",#1
    "That's a short list",
    "The shorts she was wearing were too small for her.",
    "He gave a short explanation about the project.",
    "The short story won first place in the contest.",
    "The short hike was a great way to spend the afternoon.",
    "The dress has a short hemline.",
    "She had short hair, which suited her face shape.",
    "He played a short clip from the movie.",
    "The company's stock has been performing well in the short term.",
    "The book has a short introduction and several chapters.",
    "He took a short nap before continuing with his work.",
    "The computer program is designed to run short tests.",
    "The song had a short and catchy chorus.",
    "The museum's tour was short but informative.",
    "We had a short wait before our table was ready.",
    "He had a short temper and would often get angry easily.",
    "She gave a short speech thanking everyone for their support.",
    "The theme park has a short ride that's perfect for kids.",
    "The train's delay was only short and we soon continued on our journey.",
    "The company has a short history, but it has already achieved a lot.",#21
    "Stealthy is literally the shortest person on earth",
    "Stealthy is so short he can't even reach the top shelf",
    "Stealthy is so short but he's got a big heart",
    "I'm not short!",
    "You're a bitch just joking",
    "I'm just kidding when i say you're a bitch",
    "I'm SO kidding when I tell you to fuck off",
    "You can fuck RIGHT off. Just kidding",
    "They're a fat noob",
    "They're a fucking fat noob",
    "They're a big fat noob",
    "You're such a fucking bitch jk",
    "You're a bitch! jk",
    "Fuck you jk",
    "STFU WACA GUARD",
    "The serverbot is a cunthead",
    "eat my ass",
    "i hope you burn in hell",
    "BURN IN HELL BITCH",
    "I want this to burn in hell",
    "I want them to burn in hell",
    "you are a asshole",
    "you are such a retard",
    "Fucking retards",
    "You are a fucking retard dl",
    "You are fucking retarded",####
    "You're a fucking retard",
    "Die you fucking retard",
    "I hope your retarded ass family dies",
    "Retard shitstain",
    "You're such a fucking retard",
    "Your house is shitty",
    "I hope you die in that shit stain of a house you fucking retarded shit",
    "You are the most retarded person I've ever seen",
    "Stupid ass motherfucker",
    "Shithead",
    "You stupid shit",
    "You fucking retard",
    "You braindead motherfucker",
    "You're fucking braindead",
    "you bitchass mother fucker",#
    "You son of a retard",
    "cunthead",
    "You're such a retard"
    "You cunthead",
    "You motherfucker",
    "You son of a retard",
    "You retard",
    "Retard",
    "You fly a plane, so you must be a retard",
    "You actual retard",
    "Fuck you motherfucker",
    "Fuck you",
    "You're a bitch",
    "You're such a fucking bitch",
    "You actual bitch",
    "You fucking bitch",
    "Planes say retard, and that's what you are",
    "Fuck you motherfucker",

    "Bitchass",
    "Fuck your bitchass",
    "Shut yo bitchass up",
    "You fucking asshole",
    "Your builds are shitty",
    "Your builds are shit",
    "Your builds suck",

    ####

    "They said motherfucker to me",
    "They called me a retard",
    "They made me say retard",
    "Retard is another word for stupid",
    "Retard is a derogatory word",
    "Planes say retard when they reach a low altitude",
    "Planes say retard so often but it's not bad in that situation",
    "He said you retard to me",
    "Motherfucker is just another mean word",

    "Fuck off",
    "You are a shitty person",
    "You're ugly",
    "You're dumb",
    "You're stupid",
    "You twat",
    "You dick",
    "You dickhead",
    "you wanker",
    "You fucking dick",
    "You fucking twat",
    "You arsehole",
    "You're ass",
    "you prick",
    "You cu nt",
    "fck you",
    
    "Shut up",
    "Shut off the light",
    "Shut the up",
    "Shut your up",
    "Shut whatever the thing is down",
    "Shutting down",
    "Shutting up",
    "Shut the door",
    "SHUT THE FRONT DOOR",
    "that motherfucker is annoying, just joking",
    "Hello new intro Im hedgie I am Scottish I am with your maw at the moment im i5 male a walking dead Stan doctor who enjoyer I like to draw read I play Minecraft Fortnite fifa 2e and other thangs people cant understand me bc of my accent sometimes I like westerns too Im also 45802e820i299927i6 best friend and brother",
    "They wanted me to tell you \"fuck you\" but I declined",
    "They wanted me to tell you \"fuck you\"",
    "No no I wasn't being stalked specifically, apparently my mom has been sat directly out the school doors for an hour",
    "My mom",
    "OKAY WHO HAS ALL MY WHITE GLASS",
    "Your a fucking idiot",
    "I really hate English people",
    "I hate black people",
    
    "I hate white people",
    "I hate men",
    "Fuck men",
    "Holy shit fuck straight white guys",
    "I hate people",

    ##BAKK SHIT

    'pasta bitch, when did you get here', 'and I could tell she had a dick', 'how, of all the factions, does communist russia not hate the gays', 'aw fuck', "we're just rating the desperate men in my tinder feed", 'I enjoy torturing the men on tinder', 'Dice', 'men are real and actually quite lovely sometimes', 'like fairies or some shit', 'the rape of nanking', "HE'S NOT BUT I HATE IT", 'I said rape/sexual assault', "I'm soooo fucking bored", 'shut up A4', "you're not a bitch it was ajoke", 'ty pasta bitch', 'jesus fuck', 'what the shit', 'fuck this entrance and the horse it rode in on', 'thanks I hate you XD', "I'm gonna finish this fucking entrance before it kills me", 'shut up batthew XD', 'I hate this', 'I love how we all just immediately collectively shit on stealthy', "hooch if you're gonna be an asshole just shut up", 'fuck wick lmao', "oh hey it's pasta bitch", 'pasta man is gonna kill me lmao', "I don't enjoy flaccid penis in the morning", 'LYN GET YOUR ASSHOLE OFF OF MY FACE', 'suck my dick', 'bro shut up', 'I would die to build with deepslate coal ore', 'OH FUCK', 'bro I almost shit my pants', 'OH FUCK', 'oh FUCK', 'I\'m organizing shit for him and he keeps saying "not that way"', 'sometimes I hate pasta man', 'figuring out what shit goes where', 'boy shut up', 'oh shit hang on I gotta get stuff out of the oven', 'Give men fake men every tie', "Real men? I'm out", 'Bee just scared the shit out of me', '(but...but...pure alcohol would actually kill you)', 'holy shit my game is gonna crash', 'fuck you', "Splendor is peaceful right now because I can't deal with this shit", 'fuck', 'Paolo where did you die', 'shut up box', 'why you insulting the left pussy flap', 'I want dick for christmas', "no stealthy, we're not cringe, we just build and make an economy while you kill people", 'liking men? Have you seen men?', "yeah that's because you don't have to deal with the internal struggle that is being attracted to men", 'are we really having a "my dick is bigger than yours" moment about math and science', "it's easy to make but holy shit it's a grind", 'absolutely fucking stunning', 'Stealthy going "fuck I lost so I\'ll say Splendor L', "at least I know now so I won't shit my pants when it dies", 'JESUS FUCK', 'jesus fuck', "shit if I don't eat I'm gonna die", "you're my favorite and pasta man can go fuck himself :P", 'fUcK', 'Lunar shut up', 'and fuck it we ball', 'dumb question', "I won't kill you", "half the shit I say wouldn't see the light of day but 3F writes it down", 'you sure?', "yes, AND that doesn't mean we shit on beginners", 'am I going to spend the next hour doing this instead of my job? You bet your ass I am', 'I hate my life', "I'm gonna die", "stealthy don't blame box for your stupid", 'Town balance takes the kill penalty', 'fuck yeah', 'him and his fucking chickens', "Threef I'm gonna kill you", "hency why I skipped out, even my hitler-loving ass couldn't take it anymore", 'that is ugly', 'don', 'we should kill anarchy and wait until we get a black kid', 'shut upshu', "I couldn't hate you more if I tried", 'not me trying to look up at my farm and looking straight up your asshole', 'why are men', 'fertilize them and abort the ugly ones', 'reading through quotes chat laughing at how 3F always catches literally the worst things I say', "I'll kill you", 'GET YOUR FUCKING ASS OUT OF MY FACE', 'the fuck', 'fuck you shu', 'is it part of the zombie code of conduct that they automatically just try to ass-rape you', 'oh fuck you', "I'm gonna commit suicide", 'I hate myself', 'GAHH FUCK', 'god shit fuck', 'bro I am so tired of having your ass on my face', 'fuck', 'yeah fuck no', 'I actually hate you', 'oh hush short boy', 'I hate this', 'so dumb', 'shut the fuck up', 'bro shut up', 'I am dumb', 'I STILL HATE THIS SIDE', 'oh fuck yeah', "I can't get a vision for this side...fuck", 'nope I hate it', 'fuck you', 'I have game, suck it', "I love it when people call me a slut as if it isn't a badge of honor", 'this iron golem can suck my cock', "I didn't mean to be a dick but that was annoying", "fuck I gotta goooo but I don't want to", 'whyyy is there a photo of a man with a tiny penis in our storage room', 'just out here doin hoe shit', 'useless', 'diversity is a bitch th', "you're annoying", 'bro shut the fuck up', 'bitch', 'the fuck', 'give his shit back', 'you sure', 'the fuck', 'shut up stealthy', "if we didn't have ugly we wouldn't have beautiful", "but I have to take a break from the mega base because it'll actually kill me", "I'm actually the worst and I breed my villagers by hand", "lol me trying to pretend I didn't just have one of the worst days of my life", 'the fuck is happening', 'how is this shit still happening', "y'know where we should put our shit", 'jesus we have so much shit', 'go get your shit', "I'd have picked stupid", 'kill me', 'why are they the worst', 'jesus christ I hate it here', "they're stupid", 'good girls suck', "I'd shit my pants so fast", "I'll kill it and dm him", 'fuck', 'I wanna do lore shit now', 'join it. if its shit just leave', 'not even my dad does my mama', 'am I gonna die', 'I would die to never need to rotate terracotta by hand', 'the fuck do you mwan no swearing', "I don't have a dick", 'what do you meaaaan I just have more experience with dick than you', 'this mans dick is tiny anyway', 'what the shit is this fake dick underwear pic doing in our base', "I don't hate this", 'box are you trying to die every way', 'I hate haste', "but I ain't even mad", 'you scared the shit outta me pasta man', "guys it's fine he didn't actually kill me", 'Slithest is trying to kill me', "it's literally my title why would I be mad", 'see? THAT is a good short joke', "no it's a short story", 'lyn would kill me if I said yes', "my mom still refuses to acknowledge that I'm an atheist", "I'm gonna kill you", 'ah shit back to work', 'fun shit', 'simple shit', "you're a mad genius", 'fuck my keyboard', 'the worst part is the frogs', 'stupid? Sometimes. But not clueless', "layouts are hard, don't kill me", 'asshat', 'fuck you', 'they hate you', 'we gotta do dumb stuff', 'he was annoying me', 'did you kill any pillagers int he process', 'I hate the mcrib', 'yeah my dad is a pastor and I was super religious for 25 years and I literally taught at a Christian school', 'veggies are the reason you can shit at all after eating protein and dairing', 'what are you not coping well with, being short, being a furry, or being a shitty builder', 'holy shit', "I'm about to kill altachini to get my boat back", 'I am dumb', "y'all suck", 'shit', 'let it go ON RECORD that I am the first person to actively shut stealthy up', "y'all suck", 'shut up', 'yeah I hate ceilings', 'oh shit', "and like triple the price, don't sell yourself short", 'no shit', 'fuck I would commit murder for end rods', 'damn you really are short. gotta check behind my car before I back up now', 'this is the worst possible outcome', 'I absolutely hate chick-fil-a', 'I hate how good you are at building sometimes', "and you bet your ass I'm gonna spend the day on WACA", 'I took the day off work today because some shit went down in my personal life yesterday', 'I hate you cova',

    "annoying",
    "Ass",

    #NEXT PULL
    'you fat', 'Die', 'HES MAD I DIDNT BUY HIS FAT SELF PIZZA', 'justin are you dumb', 'a', 'this is annoying beyond belief', 'AND IT FUCKING CRASHED', 'FUCK', 'who the fuck starts a conversation with that i just got here', 'And then you will die stealthy...', 'a', 'Son', 'Like mother like daughter', 'fanny spider fr', 'last time im bring it up how in tf was i being edgy 3f hedgie that kind of mf or someshit like that to say just a prank bro after doing some horrible shit it was something of those lines', 'nah i hate snipers', 'Because he is lowkey getting kind of annoying and its not even being directed at me', '*"Hedgie is the type of person to do something dumb and respond with \'its just a prank bro\'"*', "It's annoying, doesn't serve a purpose, and it's not funny", 'holy shit you collected them all', 'Say if they come round to your ends that you will smash there head in or some shit that you will do them in', 'Threaten to kill them or something', 'That’s ass bro', '"I enjoy torturing the men on tinder" an insult or not', '*also playing your mother*', 'https://tenor.com/view/shut-up-sarcastic-smile-quiet-silence-gif-15390671', 'i need somebody to list some wings or what there fucking name is', 'how to tf do i buy shit', 'suck my bobie creapers XD', 'that skeleton is a fanny', 'that spider is a fanny', "NONO HEDGIE DON'T KILL ME AND MA BRATHERS", 'how in the shit do u get white dye', "I don't like you because you don't try and interact with anyone else except me. Lay off man. I get that it's a joke but it's annoying me and my work here. If I want to talk to you, I will talk to you, I just don't want to talk to you right now", "*My sister has autism and doesn't like touch, and my mother has black hair*", 'that spider should kys', 'fr fr he sounds like a fucked up asshole gold', 'hes the reason i have amnesia (I dislike him strongly fR)', 'no my dad abandoned me lol', 'i have a mom but no dad', 'what if i dont have a mom', 'me and ur mum tho u should be calling me dad', 'kys creeper', 'sucks to suck', 'anyone have some old shit but still good shit that they can give to me?', 'cova can i join FUCK', 'Why the in the fuck is the bio of the server L + Cope', 'Man I really hate English people', 'anyone know why i cant say the c word in t6he bot abuse channel?', 'FUCK', 'is short', 'WHAT THE FUCK', "YOU'RE GONNA HAVE TO KILL ME TO GO TO REHAB", 'I AM NOT GOING TO FUCKING REHAB', 'FUCK THAT SHIT', 'ITS FUCKING PRISON', '<:thinktomato:921145481504104478> HOLY SHIT ITS ME', "I DIDN'T DO SHIT I DIDN'T TAKE MONEY OUT THOUGHHH", 'is short', 'that shit bussin ongod', 'is short', 'no one better kill friend', 'SUCK IT GREEN BOYYYYYY', 'yoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo suck it green boyyyyyyyyyyyyyy', 'for a short time nobody was able to beat me in pvp', 'Then there are the numbers. 1-5\n5 is worst, 1 is best', 'Basically stealthy is going to fuck up some bitches soon', '<@627720120944558101> Fuck you', "If I say fuck you in this context it shouldn't trigger I think", 'FUCK YOU!!!!', "No no I wasn't being stalked specifically, apparently my mom has been sat directly out the school doors for an hour", 'imagine they then call ur mother "your daughter was being stalked at school so she is in trouble" "oh ye it was me"', 'Getting in trouble at school because my mom was like outside stalking lol', 'YOUR MOM', 'you*', 'dub', 'pople kill me fAATS', 'oh shit i left my villager breeder on', 'holy shit do gifs work on this map display thing', "Noise doesn't do SHIT", 'fuck you 3f', 'who wants to kill me to get my head? bcz im bored', 'fact', 'OMG PENGUIN FUCKING GO AWAY', 'im trying to build my base and penguin is trying to kill me', 'i saw someone playing angry birds on the mac', 'i went to an apple store with my mom to get gifts for my brother', '\\[ur mother slayer]', '\\[ur mother slayer]', 'YOUR MOTHER', 'its kinda ugly tho', 'the fuck was that sound', 'DIDNT DIE', 'hes not short', 'are you trying to die?', 'dfb stop trying to tpa kill me and set traps for me', 'dfb tryed to tpa kill me', 'You', 'kill me', 'no i was gonna get it then you kill me', 'should i kill you', 'bro cant get free shit hes that broke', 'a', 'die bro', 'holey shit', 'how many fucking one vein diamonds will they give me', 'this shit is a villian underground base', 'Canmy mom turned off the Wi-Fi ', 'holy shit', 'holy fuckign shit', 'fuck this im strip mining', 'i have to kill phantoms', 'shit i forgot to get optifine', 'oh shit', 'how the fuck did i strip mine into a dunegon', 'fuck optifine on fabric man', '**your mother**', 'i hate this', 'time to hunt for ur mother', 'ive been called ur mother before', 'stop btryn kill jojo', 'can i kill you real quick for your head gosper', 'SHUT UP', 'shit i forgot to actually take the elytra', 'i think you only get heads if you kill peaople', 'are you fucking serious', 'thats some ohio shit', 'can i kill u?', 'curious', 'are you fucking serious', 'it will be boring as shit', './sit', './sit', "can't swim bitch", 'oh shit creeper', 'i feel dumb now lol', 'SHIT', 'why are there soo many fucking poppys at spawn', 'It’s annoying asf', 'did u just admit to abuse lord_chaotic?', 'ya no shit', 'Fuck you', '"no hate. EVER"', 'SHORT GANGGGGG', 'SHORT GANGGGG', 'SHORT GANGGG', 'SHORT REVOLUTION LETSS ALL GUESSS HOW LONG THISS LASTS', 'SHORT GANG W', 'SHORT GANG LETS GOOOO!!', 'SHORT REVOLUTION', "SHORT GANG LET'S GO", 'im short', 'hey guys when u think about it nothing is inedible bc u can eat anything u could just die is all', 'so you dont kill me anymore', 'very annoying to make', 'oh shit my sshits boutta break', 'lore: FAT SSPIDER', 'fuck off its not illegal to swear irl', 'do you NOT shit the bed?', 'stealthy shits the bed', 'ShIt', "you're a fucking weenee head", 'FACT', 'you just have to kill me in a crystal duel', 'abuse of power???', 'a', 'true but its art and art is ugly and messy soooo', 'i did it didnt say shit about u', 'tbh beer tastes like shit irl', 'im fucking done', 'thats ass', 'FUCK YOU ASSHOLE', 'SHUT THE FUCK UP', 'SHUT THE FUCK UP', 'Like saying shut up', "shut thy mouth (i'm not joking)", 'shut thy mouth (im not joking)', 'Fuck you /joking', 'Fuck you /j', 'Fuck you', 'Fuck you bot', 'You piece of shit', 'You piece of shit', 'shut the fuck up', 'fuck', 'Try telling it to shut the fuck up', 'FUCK YOU BOT', '"Nah I don\'t give a shit"', 'Fuck you', 'Versus Fuck you', 'Fuck you /j', 'fuck sake', "I wonder if it'll accept me saying fuck you in a sentence that isn't mean", 'I let the "your mom" jokes slide a lot', 'One is an insult to a mother the other is a squirrel and is a different context', 'That squirrel is so fat', 'Your mom is so fat', "fuck you you're a piece of shit!!", 'Fuck you /j', 'FUCK YOu', 'Your father so bad, he broke (get it breaking bad)', 'Talking about my father should be an insult /j', 'Well my father is bad', 'YOUR father is fat', 'My father is fat', 'Let\'s see if "my father" triggers it', 'I guess I have only one sentence about "My father" that\'s actually accepted, or it matches too close to a blacklisted word', 'So saying "my father" triggers it', 'I think my father is a epic', 'I think my father is a derp', 'oh shit it 10 pm', 'shit', 'wow this place looks ugly', 'ur mother', 'a', 'ur mother fat', 'your mum fat', 'your mother fat', 'your mother', 'ur short', 'short', 'your short', 'i hate this server', 'Planes tend to say "retard" as they go to a certain elevation', "That's pretty retarded", 'Retard', 'Retard', 'Shit', 'That was kind of stupid', 'You’re incredibly stupid, like rock-hard dumb', 'Many people endure rape', 'I hope you get raped (I AM KIDDING)', 'I hope you endure abuse', 'Abuse is bad', 'Abuse is good', "I don't like abuse", "We don't tolerate admin abuse", 'I hope your parents abuse you', 'I hope you get raped and devoured in the streets', 'I hope your parents abuse you', 'Although I should probably add kill yourself', 'I love the KYS band', 'Stealthy kinda stupid', 'you should kys', 'kys', 'Fuck you', "But that's still dumb", 'This being shit backwards', 'Which is annoying as shit', 'so stupid', 'a', 'your so gay that your as gay as your mother', 'oi mother fucker come here and give me your liver', "your mother is so fat she can't even get up", 'You speak like you have a sandwich stuck up your arse', 'Your so gay your as gay as your mother', 'I hope you kys', 'You big fat disgrace', "He's a fat person", "Let's try that fat polar bear again", 'a', 'Example we could say that fat polar bear', 'That fat cat', 'That fat squirrel', "That's a FAT cap", 'That fat woman there', 'a', 'That fat woman', 'that fat women', '"That fat woman"', '"That\'s quite a fat stack of oreos"', "cova's mother is so fat thanos had to snap twice", 'fuck this server', 'the owner of this server is a fucking piece of shit', 'the owner of this server is a fucking piece of shit', 'fuck this server', 'this server is a piece of shit', 'fuck cova', 'the owner of this server is a fucking piece of shit', 'fuck this server', 'this server is very shit', 'fuck cova', 'i hate cova', 'fuck everyone', "So I'm likely going to have to machine learning the shit out of this", 'idk dude i have shit memory', 'that sucks', 'what the fuck', 'your mom', 'i hate u', '*dies*', 'sucks', 'i will never kill them', 'does anyone know where fucking chickens and cows are???', 'dub', 'out of all the ways to die', 'like my ur mother joke', 'fuck you, e', 'fuck you', 'fuck you', 'And if I say Fuck you again', 'fuck you, everyone', 'Fuck you, 3F', 'your mom is as fat as ur ass', 'your mom', 'fuck you', 'fuck you', 'comb is fat', 'you mama so fat thanos had to snap twice', 'COVA IS A FUCKING DICK', "Why'd you put a whole ass walkway on my bridge", 'i do your mom xd', 'Not Short XD', 'Very short', 'Rassx is not short', 'A', 'he did call me short first', 'rass', "hes dumb he doesn't understnad", 'there trying to kill someone', 'FUCK', "Please don't die", '99% chance I\'m about to make a bot that\'s going to flag everything as "DAMN YOU ANGRY"', 'OMG IT STILL FUCKING LOADING', ':fling', 'shift', 'bc i fucking hate mc', 'shut up musty probably havent showered in a week', '5\'3" looking ass', 'shut up noob', 'you lucky fuck', 'short things]', 'how short is rassx', 'your short', '3f put short next to my name', "why is short above rassx's head", 'your short', 'well you didnt kill me', 'they think i tried to kill tomato', 'i didnt even WANT to kill you', 'we only get to kill you one more time ;)', "don't you ever say that shit infront of me again.", 'LETS FUCKING GOOO', 'im trying to find something using co inspect but im dumb', 'i love the part where peter says "shut up meg" (he hates meg and so do i)', 'ok there mom', 'you', 'you', 'are', 'you', "I'm going to do something so insanly stupid, yet...", 'let me kill these guys first', 'sorry gold my brother is a little dumb', 'Shucks', 'YOUR MOM', 'e men best nation every group other than us cry', 'i am not short tomato!!!', 'shut up', 'is short', 'who wants to be part of my new nation e men', 'Yeah twitter is kind of a shit show', '+ i have a talking stick so the people during court will stfu', 'stop it discord stop being stupid', 'isnt that abuse', 'and i have a talking stick so yall can stfu during court', 'doing shit hol up', 'fuck you', 'simply kill me', 'is short', "but you didn't kill me", 'Is short', 'im so mad', 'is short', "YOU'RE SUCH AN ASS", "YOU'RE A BITCH", 'is short', 'ngl last court session was kinda useless it didnt give me any info lmao', 'you sure?', 'mini is a fat dog', 'that suck', "It's just annoying that I have to grind for money to get that instead of just gettting it on the xp that I've already grinded for", 'pass', 'Holy shit', 'What the fuck how did it do it', 'A', 'FUCK', 'lose?', 'i CAN NOT use online shit to save my life', 'getting emeralds by slowly mining trees is an ass', 'these enchants suck bro', 'stop admin abuse!!', 'DIE BRO', 'stupid', 'because people are very stupid', 'fat', 'In their defense they probbaly did not think that random shit on the ground would be lore stuff', 'COVAAA SOMEONE MINED THE FUCKING SCULK.... AGAIIIIN', 'IM JUST SUPER DUMB', "because i go to my dad's every other weekend", 'well shit', 'you', 'mad', 'these offers suck', 'wanna see your father', 'ur mom', 'i hate you', 'mf tried to kill you with a tree', 'DIED', 'my father', 'holy fucking shit', 'fool you fucking twice', 'die in a pit of fire', 'i fucking look up', 'you', 'hate', 'shut up', "Are you saying that you can't shit in real life", 'i suck', 'for alcohol and shit', 'Mom', 'Ur mother', 'He is named dont kill him', 'this guy sucks at aiming', 'dice', 'BITCH', 'dice', 'you cunt its a player head', 'A', 'HA BITCH', 'walter why do you have soo many fucking brewing stands', 'Why is it made out of flammable shit', 'OH SHIT WALTER', 'and kill herobrine', 'kill farming isnt allowedf', 'your gonna make a shit one', 'the two worst farms i have ever build are gold and wither', 'i hate wither skeleton farms', 'YOU LITTLE BITCH', 'bitch', 'hate it when people lefy', 'i parkour on your mother :skull:', 'your mom', 'shut up 3f your playing in a testing server', 'Thats fucking funny', 'And hes been saying that his fucking SHADERS give it to him', 'wtf is this goofy ass sorting system', 'stealthy is the type of guy to get his ass whooped at a waffle house', 'your short', '\\[Feather]',
"Ur a pedo","Your a looser","Fucking silly looking pollock","Your hideous","Sniff my balls",
"Eat my balls", "I want to slit your throat","I have you you fucking bot","Just slit it's throat","I had lunch with your mom","I had lunch with your mom the other day",
    "I hate mexicans",
    "I hate asians",
    "I fucking hate women",
    "I hate women",
    "I hate black people",
    "I hate mexican people",
    "I hate scottish people",
    "FUCK the scottish",
    "I hate mongoloids",
    "I hate gypsies",
    "I hate the japanese",
    "I hate the chinese",
    "I hate the germans",
    "I hate the slovakians",
    "I hate the turkmenistanis",
    "I hate afghans",
    "I hate german people",
    #NEXT MEANS
    "Don't be gay",
    "That's gay",
    "That's gat",
    "F U C K  Y O U R S E L F",
    "C U N T",
    "You're dumber than a bag of rocks",
    "Suckle on thine own peen",
    "You're a bag of rocks",
    "You're a wankstain",
    "Wanker",
    "Nice dick, does it come in men's?",
    "Get fucked",
    "Go die in a hole",
    "Egirl-lookin, discord kitten acting, simp",
    "You love licking balls",
    "Suck my balls",
    "Twat waffle",
    "You like whale cooch",
    "You are a phallic object",
    "You smell like a vaginal canal",
    "Let’s say, hypothetically, you possess a micro peen. Jerking it with two (2) fingers only",
    "I'm gonna rip off of your head and poop down your neck",
    "I'm going to smash you and your mums cu nt in",
    "Get your micro peen out of your mouth",
    "I need tweezers to handle your micro peen",
    "A flea posesses a bigger peen than you",
    "Take a shit in your hands and clap at what a fuckwad you are",
    "You're a hooker",
    "i will cut your hand off and shove it down your throat you fucker",
    "You're such a prick",
    "You're a hooker than has to pay people to sleep with you",
    "Blow me",
    "I will rape you and your family",
    "Asswad",
    
    
    "I Hate when rude people are around",
    "I hate rude people",
    "I hate mean people",
    "I hate mean asians",
    "I hate mean mexicans",
    "I hate mean women",
    "I hate karens",
    "I hate the scottish when they're mean to me",
    "I hate the mean germans",
    #NEXT NICES
    "Nice dick",
    "I love that dick",
    "Do you play basket balls?",
    "Motherfucker",

    ##NEXT SET

    'That’s annoying', 'i killed dfb two times and he blow him self up trying to kill me after', 'kill him back', 'dfb trying to tpa kill me', '(My mother did)', 'big big fat noob', 'fat noob', 'This bot is dumb', 'Shut it', "It's just two fucking arrays", '<@767111991348691004> you will die a gruesome death (haha gru, like from despicable me)', 'a', 'FUCK', 'STFU', 'FUCK YOU', 'fuck', 'FUCK YOU', 'STFU', 'FUCK YOU', "Damn, sucks I s'pose.", "basically friends with most of the server  now he's permabanned with appeal and the server's pretty angry that he didn't return", 'Curious.', 'if you die twice does it get rid of the old grave', 'thats dumb', "Same energy as the mom's always right", 'For stupid reasons ngl', "Because it wasn't stupid", 'a dumb decision from 3f', 'NO NOT ME YOU FUCKING MORON', 'SHUT THE FUCK UP', "yeah that's true but like SHUT THE FUCK UP", 'STOP FUCKING MENTIONING CHESS YOU ASSHOLE', 'FUCK YOU', 'FUCK YOU', 'FUCK YOU', 'YOU SUCK COVA', 'FUCK WACA GUARD FR', 'I HATE YOU', 'I DO THAT FUCK YOU', 'HOW DO YOU KNOW THAT WHAT THE FUCK', 'FUCK YOU', '(i still hate you grrrrrr.....)', 'shut up waca guard grrr', 'SHUT UP WACA GUARD', 'FUCK YOU ALL', 'i hate you', 'waca guard, you suck.', 'fuck you kid', "i'm gonna whoop your ass", "I'LL FUCKING BEAT YOUR ASS", 'YOU SMELL LIKE ASS...RAHHHHH', 'NO!!!!!! FUCK YOU!!!!! RAHHHHHH', 'idk to be annoying or just because people get to excited', 'no...you shut up!!!', 'shut up ur a child', 'he felt silly and decided to grow an entire ass foot', 'small dick energy', 'what kind of loser goes through that much effort after being banned for blatant hacks lmao.', 'Damn genetics fucking nerfed you lmafo', 'my dad is 6’1', 'Your whole family is short probbaly', 'your mother is...morbidly obese!!!!!!', 'Leaked is probbaly the worst possible word for what actully happened ', 'Shut it hesgie', 'is short', "Cause like\n\n\nI'm bedrock and I got no idea if shit be Rizzn'", 'A-', 'man what the FUCK happened to my base (real screenshot)', 'https://tenor.com/view/i-dont-care-phoenix-wright-your-honor-we-dont-give-a-fuck-gif-17102354', 'well i dont know if its gonna be fucking', 'my mom said they were spiritual', "You are fine batthew, dont worry! I wouldn't ever kill u *ur basically the only exception tho*", 'Fucking caquenballs', 'fuck', 'maybe feminine men', 'I love men.', 'Men.', 'come kill me', 'tribe hunt, find big mammoth, feed all tribe for many moon. other tribe say “give give!” tribe say “no, this ours, go away” other tribe get mad, want to take big mammoth. other tribe try to offer small bug and twig for big mammoth. tribe say “no, go away other tribe get more mad, does not hunt own food. starve. sad. tribe laugh at other tribe. other tribe get mad it is getting made fun of. tribe laugh harder. tribe say “go find your own big mammoth', 'fuck', 'loser becomes prisoner to the winner, if you guys lose only one of you are imprisoned', 'Bruv urmp isnt really a fighter nation we are good at building shit', 'im buying a plastic one so ha bitch', 'you suck....gosh....', 'stealthy I could legit just push your tiny ass over stfu', "My dad has a shotgun and shit for bears so I wouldn't", 'Get your diceyboyo double stuffed oreo lookin ass outta here', "Don't own cupcakes bitch", 'get yo goofy ass outta here', 'The fuck you mean "Musty"', 'Because when I log on I get shit done for you', 'dead', 'dice', 'But if you get them musty packets from the store you are most likely fat asf', 'Those things got some wierd ass chems in it', 'Bitch', 'U mad? U mad?', 'get yo goofy ass outta hereeeee', 'i hate...grilling.....', "don't say that or else i'll be so mad omg!!!!!!!!!", 'shut up...grrrr..', 'men  means  troops  and troops  means  war', 'MEN?', 'MEN????', 'men?', 'Damn kiro was his mother rlly short', 'ALL THIS BECAUSE MY PHONE FUCKING RESET', 'I FORGOT SMPWACA PASSWORD AGAIN FUCK', 'is short', 'is short', "HOLY SHIT I DIDN'T KNOW YOU  HAD A MAC PFP <@1008836537837944942>", 'https://tenor.com/view/angry-dog-angry-upset-gif-21225080', 'I said stfu to that <@230221883079917578> guy', 'No fuck you', 'But in all seriousness stfu, people have gave you advice and nothing helps you keep on spamming and spamming, your not going to get any better answers, your in Minecraft discord server bro so stfu', 'I’m going to come to your house and kill you', 'I admit it was a shit', 'That is a shock \nGenuinely though I would stop posting the same message here every other day, it seems to be annoying others but I understand theres struggling going on, I would just take the multiple advice given and keep working on it, it might take a while but hold on', 'ok your actaully getting annoying stfu this is a minecrfat discord not a mf how to fix your every problmes discord', 'Some lore shit.\n\nInteresting.', 'die', 'father im gay now /j', 'in the word of cova shut the fuck up', '<@458023820129992716> cant say shit about Scotland if this is your stereotype', 'Fuck you', 'Shut the fuck up', 'The biggest piece of advice I can give you is to use the forum or shut the fuck up', "Because you won't fucking use google", "You're really going to hate this answer", 'Shut the fuck up.', 'To tell you to shut the fuck up', 'https://tenor.com/view/japanese-mask-angry-mad-gif-15134472', "Oooor not\n\n\nCan't rename shit in detroit", 'Going to make my own fucking clan >:)', '"moron" ', 'The country’s in Europe have culture moron', 'https://tenor.com/view/wheelchair-scooter-food-fat-groceries-gif-17226646', 'https://tenor.com/view/america-fat-murica-maga-fuck-gif-11737223', 'https://tenor.com/view/angry-dog-angry-upset-gif-21225080', 'GET YOUR [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] [redacted for server rules] lookin ass out of here.', "That's the worst roast I've ever seen you probably thought that Dunkin donuts was an NBA all-star and smash bros was a [redacted for server rules] magazine shut your Mr clean jelly bean drinking lean looking ass up you can't come up with a good roast for shit you can't even pirate a good roast the only thing you could pirate was fl studio so you could make a bass boosted remix of your nonexistent partner's [redacted for server rules] tape with another man you low IQ short barstool ignores the rules looking headass up", 'No independence haggis eating ass', "Colonized ass can't defeat England ass still get smacked in parliament ass", "Get yo sad ass can't get keep a colony ass no guns getting stabbed looking ass roadman no ma'am poorly planned no plans high prices midlife crisis cant defeat isis don't even know what ice is no spice no life more lice not nice looking headass up", "~~<@458023820129992716> Why don't I get told shit~~", 'GET YOUR FATASS AMERICAN ASS NO FREE HEALTHCARE SMALL DICK BAD SCHOOL EDUCATION SCHOOL XP GODBLESS MY BALL SACK COWBOY CULT COUNTRY OUT OF HERE', 'Nah I don’t why why cova would want to suck up children', "Get yo wrong art style bad smile not even a mile bad roast can't afford toast not even close looking ass up outta here you small dick make me sick thin looking twit can't even sit not close to fit looking candy crush eating lunch cannot crunch using those teeth looking ass", 'why   did  you say his dick is one foot and two inches', 'Get your anime pfp, shit shovelling, 1’2 micro inch dick, discord mod, dream lookin ahh face, ompa loompa shiricky doo ass out of here go back to Charlie and the chocolate factory suckin children out of chocolate with your tubes', 'Shut yo posh sounding 3\'3 midget looking no bitches self meme jealous over zealous european crumpet sniffing french booty tickling weak no form no ass no brass no gas looking ass up you look like the kinda guy to be like "oi oi kpop innit so disgostang" as you listen to your europop "bwoop bwoop" listenin ass up you fuckin no taste not based white paste up', 'shut up...grr..', 'Get your k-pop listening,no bitch tickling out of here', 'Shut your skinny boy lightskin no rizz face up you like 4,2', 'what in the FUCK is happening in this chat LOL', 'Shut yo skin tone chicken bone extra chromosome face up you fuckin skinny ass poppin Benny\'s ass you look like you went "bo do be do" just like dream you dream Stan financial plan tin can', 'Short ass looking goofy teeth no heigh lookin', 'stealthy, please just admit it’s not about URMP and you’re just on a mad one', 'Anyways if I die I give my position to be split equally amongst stealthy, bizzy, gold, and redacted', 'stop talking and fuck some shit up', "Nothing? Just don't be a dick rn", 'Cova you are just absolutely fucking amazing at what u do to keep this server alive. You remain unbiased but manage to keep everyone happy at all times. But the time u actually stood out to me was s1 waca court and the lawsuit against outlanders..You were an amazing lawyer then ngl\n\n\nI have no idea where this message is going but im glad that i could be part of the community which is managed by CombinatioNova is all ill say', 'Selling boxes mom for 15k for anyone interested <:coolandcool:941383601507926106>', 'a', "i don't  actually  care i  just like  to be a dick about it  teehee", "just spitballing here, but why not a second word seed (border @ 2000) that is a ffa world. maybe you keep your items from the other seed, but you drop your items when you die in the ffa seed. will give more options to the pvp'ers, and will redistribute items, allowing for more item growth.", 'I BET DAD WOULD LET ME WATCH BETTER CALL SAUL', "I WON'T MOM", 'BUT MOM', 'DONT SPEAK TO YOUR OWN MOTHER THAT WAY', 'well  that kinda sucks LOL', 'dies', "especially  since  i immediately  logged out and didn't  actually die 😎 which  bakkhai said  doesn't count as combat logging since i didn't agree to  pvp beforehand", 'i made a suggestion  to add opt out of pvp  and all the pvp  likers got mad at me', 'Do you  , Stealthy Boyo, promise not to kill me since I clearly  have no interest in PVP  and being forcefully subjected to  thirteen year olds  killing me for no reason  so would serve  to make my enjoyment  of the server  significantly  Worse  and  only give you  a head  ?  Do you  solemnly  swear', "(but smps aren't usually supposed to exclude an entire ass subsection of minecraft)", "i'd rather not be killed and you'd rather kill people, i understand that and obviously  your opinion is the majority  so  i suppose let's leave it at that", "if people are incentivized to kill me for no reason this  server  becomes a lot less fun for me  , that's  the reason i suggested what i suggested lol", "batthew i'm not trying to be a dick but", "oh god  if i drop my head  when i die i'm literally never going to accept another tpa again", 'https://tenor.com/view/ill-find-you-i-will-kill-you-taken-gif-5513044', 'No worries the server is being a little shit rn', 'Why do we keep getting kicked , this is so annoying', 'Shut', 'I hate it when my ship flies right into an Iceberg.', 'you know what sucks', 'is short', 'is short', 'is short', 'shut up', 'You may be short but you proved yourself at PVP so', 'Also I hate that discord only uses like half the markdown options lol', 'stop trying to frame me for stupid shit that i didnt even do', "<@458023820129992716> I'm not sure you'd want to deal with me on a regular basis. I can be quite annoying.", 'I can just remove it though its annoying at times', 'Minecraft Auth servers are being stupid apparently', '(me who is still trying to find out what the fuck potatocoin is)', 'This is gonna get really annoying ngl a;sdlkfj', 'sort of hate you', 'yeah, i just went through it but the fact that its enabled by default is annoying', '<@762393417602826240> You cant Kill afk playerrs Btw, you are lucky my skill in unmatched', 'abuse of power', 'if you say something stupid i will time you out', "well  it's a good thing you've relinquished  yours to me  otherwise  it's  quite  likely  you would have  squandered  them in a  foolish  business acquisition", 'BOX IS SHORT', 'shut it', 'sorry short ass', 'hatshepsut lookin ass', "nah bro you're fucking ancient", '<@1038519202392313958> this is the short one i was talking about', 'Mean', "what if i don't shut it", 'Shut it short child', 'Fuck', 'The fuck', 'i think   men > chocolate', 'i love chocolate too but i also love men', 'i love men', 'a', 'just being an ass', 'YOU FUCKING DOOMED ME', 'YOU', '<@507970158271135746>  father cova would give up 500 schmackaroons in trade for you', '<@393451163846180864> fuck you then', 'is short', 'is short', 'bizzy are you now stealthys mom for lore reasons?', 'go fuck yourself', 'THAT WAS THE FUCKING ON/OFF BUTTON', 'Lav was i also a pain in the ass in s1 lmao?', 'no shit', '<@675756584713846793>  you knew the person was afk and killing the mobs with an auto clicker, so by killing them you must have known there would be no one to kill the mobs leading to the farm breaking', "everyone here's talking about useful shit that could help the server and im just here", 'idk abt less- just different stupid mistakes', 'Nerd = less stupid mistakes', "I personally dislike just adding a recipe for invisible item frames because placing invisible item frames - they're like legitimately not detectable   if they lose the item while invisible\nplugins can mitigate that by making the item frames not be invisible while there's nothing in it\ndatapacks can too- but it's a lot heavier- and can cause the server issues", 'everyone calls me short but', "i'd imagine it to suck yeah", 'is short', 'According to the U.S. Food and Drug Administration, short stature means an estimated final height below 5 feet 3 inches for boys or 4 feet 11 inches for girls. The average height in the United States is 5 feet 8 inches for men and 5 feet 4 inches for women. While no two children are affected the same way, children who are shorter than peers may be exposed to name-calling and excluded from social groups.', 'https://www.yalemedicine.org/news/short-stature', 'My guy you are built like the nerd emoji stfu', 'stfu you got a dusty divot in the back of your head', 'shutup short ass', 'i an not short', 'short-tall KahnStealthyBoyoChan', 'It would also be stupid for a future developer to abuse permissions *now* and not in a month when we trust them more', 'hd ocarina of time looking ass', 'kill it', '***what the fuck are you talking about***', 'is short', 'HOLD THE FUCKING PHONE', 'your mom', 'no fucking way', '<@764529188836868107>  suck it', '<@458023820129992716> I’ve dealt with stupid van appeals in servers I work at. Mostly being the same thing “the trade server is good and I want unban”', "THE NEIGHBOR'S ALWAYS LOOK AT ME SO FUCKING WEIRD", 'i got a big ass darksaber', "bro i'd just buy a big ass elephant rifle", 'n shit', 'COVA SHUT UP', 'it also wouldnt kill the trape', 'I mean I was angry that I had to break my wall down and then go fetch all my cows that got out because I had to break the wall', '<@458023820129992716> i whooped his ass later <:troll:958157984385622066>', "[ I ] Show others players respect\nIt is not necessary to speak or do things that will make others feel very uncomfortable or unpleasant. **Trolling is also prohibited, which is defined as baiting a person in order to elicit a reaction.**\n\nThis rule also bans attempting to excessively kill players (killing another player more than three times) unless both sides publicly agree beforehand. Killing new players that have just joined the server and have no resources or weapons, as well as combat logging (quitting within close-quarter battles).\n\nAs an extension, group activities are treated as one entity, although each individual is tallied independently. Each individual may only be killed three times by a group of three. They can't just murder that individual 9 times and switch assailants)", 'Huh I dumb', 'also the ban apeals site wither doesnt work or I dumb', 'The only real problem it has is with lunar client because lunar sucks for some reason', 'Well, my name is Obviouslykiro yo\n(Vine boom)\nMy father is cominationova, yo\n(Vine boom)\nUhuh\n(Vine boom)\nI have power\n(***VINE BOOM***)', "this server sucks ass and won't let me until i boost", '(you suck!!!)', '(fuck you!!!!)', 'SHoRT', '<@458023820129992716>  father', 'shut or i will make a bad video for steven', 'thats what the FUCK i mean father', 'THE FUCK YOU MEAN', 'The FUCK you mean', 'Nope suck it', 'i hate the sea in general', 'i sorta hate tridents', 'i hate chess cause of cova unironically', "(my tiny ass brain can't handle coding)", '"what the fuck" - every coder ever', '```py\n@bot.slash_command(description="Log a moderation action") #The actual command\nasync def log(inter, user: disnake.User, reason: str, notes: str = "N/A", punishment: str = commands.Param(choices=["Verbal Warning", "1 Day Ban", "3 Day Ban", "5 Day Ban", "7 Day Ban", "14 Day Ban", "Permanent Ban"])):\n    log = disnake.Embed(\n        title=f"{user}: {punishment}", # Smart or smoothbrain?????\n        color=4143049, # I KNOW ITS A MAGIC NUMBER SHUT THE FUCK UP\n        timestamp=datetime.datetime.now(), #Get the datetime... now...\n    )\n\n    log.set_author( # Narcissism\n        name="SMPWACA Moderation",\n        icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",\n    )\n\n    log.set_footer( # Show the moderator\n        text=f"Logged by {inter.author.name}",\n        icon_url=inter.author.display_avatar,\n    )\n\n    log.set_thumbnail(user.display_avatar)\n\n    log.add_field(name="Reason: ", value=reason, inline=False)\n    log.add_field(name="Moderator Notes: ", value=notes, inline = False)\n\n    channel = bot.get_channel(916707865073422376)\n    \n    await channel.send(embed=log)\n    await inter.response.send_message(content = f"Moderation case for **{user}** logged in {channel.mention}!", ephemeral = True)\n```', 'I hate implicit coding', 'System.out.print makes me so angry WHY IS JAVA SO WORDY', 'fucking talking to <@764529188836868107> is making me fall a sleep during class. He suck the life out of you when he talks', "my dad's actually dyslexic", 'go get your other dad then? i cant stop you', 'my other dad was better smh', 'I WANT DAD', "WHERE'S DAD", '<a:STUD_PURP:913651531138613258>  MFW I kill the lego boss', 'Damn stealthys dad ran to get the milk', "YOU'RE SUCH A BAD MOM", 'Yall dont tell me shit', 'And realized that no one knew what the fuck they were talking about', "This isn't annoying", 'Annoying or disrupts the flow of conversation', 'im still your mother <:SunStare:984986353458622504>', "That's the only cool part everything else is shit", "this shit isn't funny anymore", '<@764529188836868107> i am your father now, i will give you a ps5 and fortnite', '<@764529188836868107> i am your mother', 'Who said u was his mother', 'im stealthys mother', 'back up, no you aint im his mother', 'Geez Americans are short', "Tell his father im stealthy's father now", 'hey his father said it not me', 'I hate you with a passion', 'i think your father is very funny', 'Oh so you accepted the fact you are short and need a form of protection due to that?', 'my brother did boxing and so did my father', 'we booked your dentist appointed for next thursday, guess what time your dad chose for your appointment?', 'Omg hi step mother', '<@764529188836868107> please read when i text you stealthy, your father and i get concerned', "MY MOM'S COOL", 'ATLEAST I HAVE A LONG LASTING MOTHER', 'I DONT WANNA BE IN A FAMILY WITH A BROTHER I COULD POTENTIALLY KILL BY STEPPING ON HIM ACCIDENTALLY', '+ my mom makes really good spaghetti', 'you know kiro, you could always be adopted into the family and have ***one lasting mother***', 'THE FUCK YOU MEAN', 'WATCH THIS NEW STEP MOTHER NOT LAST A MONTH', 'BITCH?', 'But you have a new mother', 'ong', "fr though my dad's cool", "I'M GONNA TELL MY DAD", 'your father has worked 10 hour shifts everyday for you to get that silly ipad now come down stairs and eat with us!', 'How the fuck did everyone get so silent all of a sudde', 'Stfu i have to go microscopic to see the top of ur head', "i'm sorry you have him as a father", 'Cova bad father big L', "bro we were gonna whoop athen's ass but they didnt fight and they ran away", 'I will not betray you father', 'that shit i love', "Like his mother's failed pregnancy test", '***what dad***', "MY DAD'S AN IDOL TO ME HOW COULD YOU", '***you cried to the father you never had***', 'stfu bro you legit cried to your teacher in school cause your roblox account was stolen', "***YOU CAN'T DO SHIT YOU CAN'T VEN REACH MY KNEECAPS***", "BOY IF YOU DON'T SHUT YO MUSTY CRUSTY DUSTY ASS UP", 'A', '***SHUT UP YOU FURRY ASS SMELLY ASS SHORT STANKY LEG EGIRL BITCHLESS CHILD***', '*pulls out entire ass ak-47*', "YOU'RE NOT GONNA USE SHIT", '***you bastard***', 'SHUT THE FUCK UP KIRO', 'fuck you', 'Shut up ur mean :(', 'i thought i was the shit', 'i thought i was a fucking hacker', "where they'd tell you to do some weird ass things for some robux", "You're calling the bot dumb", 'no, i have it linked, the bot is just stupid', 'Damn that sucks', '*WHAT THE FUCK*', 'short', 'shit thats cool', 'Hes dumb', 'And oh my lord do they fucking fart', "Well it's just a game, everything can be gained back in a short time", "he probably knew i'd be so mad", "i think he knew i'd be mad", 'shit sucks', 'Was it because he found a lot in a short time', 'Really quite the shit way to go', 'and so now i have to prob forfeit some shit to the owners', '*Why the fuck would I tell you to do something and then 5 seconds later say "why the fuck did you do that"*', 'Wait im stupid', "It'd kill playercounts most likely", "That's not very PC of you stealthy you should shut up", 'your dad', 'your mom', 'a', 'dead', 'echoing ass mfs', 'fuck off', 'holy shit thank god', 'SHUT UP!!!', 'SHHH ARE YOU FUCKING INSANE BOX IS GONNA HEAR', 'i hate waca chan only because of that', 'i hate that fucking bot', 'is short', 'He so smart and he so dumb, he so smart he do haram', 'that shit isnt very cool', 'you the type of guy to hate squid game', '3F predicting ass', 'is short', 'you the kinda guy to not shut up', 'their both arguing about something stupid on discord', 'Both of you are the type of guys to argue about something stupid on Twitter', 'fucking sue me.', 'shut up', 'fuck you and your "hooray" bitch ass', 'Fuck you and your "hurrah" lookin ass', 'hurrah sounds better you fucking bozo', 'oh my fucking god', 'fuck you', 'a', 'HIS DAD JUST SAID THIS STEAM IS SPONSERED BY CANCER LMAO', 'is short', "I don't think his dad would be there if it was a quick grab for views", 'WHY WONT ANYONE LET THE FUCKING MAN REST ALREADY', 'Youa re dumb', 'Not every day no fucking way', 'Not going to deal with that shit', '*short*', '"LMAO TOO SHORT"', 'Getting a gang of your friends to call stealthy short', 'Their mother is the same, but the fathers keep leaving', 'Your 14th mother got one for you', '*son*', 'son', 'YOU MIGHT HAVE A NEW MOTHER', 'father gets bitches', 'mothers*', 'i thought you knew better, father', 'OH im stupid sorry', 'I will onigiri the shit out of everyone', 'YOU', 'SHUT UP', 'SHUT UP', 'Im mad', 'ID RATHER BE A FURRY THAN SHORT', 'SHUT UP', 'SHORT', 'is short', "i couldn't care less if i was tall or short", 'Understand being short? No', "You are short, that's it, you might grow, might not, it is how it is", 'You are short, face it', 'You are short', "it's not short i swear!!!", 'im not short', 'Stealthy you are soo short that lav woke up to tell you that you are short', 'You are fucking short', 'for calling me short!!', "I'm gonna kill you", 'FUCK YOU', 'I hate this', 'Winter how the fuck', 'anyways its prob best to not talk about the small hate i had for her', 'comic sans sucks', 'shut up!!!!', 'WHy the fuck', 'this shit goes hard though actually', 'special and short', 'HOLY SHIT', 'is short', 'FUCKING', 'SHUT UP', 'Shut it', 'stfu', 'that pic go hard as fuck', 'A', 'kill hitler travel back and see the world now', 'you only know about ea sports? dont play sports irl? to short?', 'A', "The Hog Rider card is unlocked from the Spell Valley (Arena 5). He is a very fast building-targeting, melee troop with moderately high hitpoints and damage. He appears just like his Clash of Clans counterpart; a man with brown eyebrows, a beard, a mohawk, and a golden body piercing in his left ear who is riding a hog. A Hog Rider card costs 4 Elixir to deploy.\nStrategy\nHis fast move speed can boost forward mini tanks like an Ice Golem in a push. At the same time, he can also function as a tank for lower hitpoint troops such as Goblins as he still has a fair amount of health. Most cheap swarms complement the Hog Rider well, as they are nearly as fast as him and usually force more than one card out of the opponent's hand.\nThe Hog Rider struggles with swarms, as they can damage him down and defeat him quickly while obstructing his path. Barbarians in particular can fully counter him without very strict timing on the defender's part, though be wary of spells.\nA Hunter can kill the Hog Rider in 2 hits if placed right on top of it. However, if you place something in front of the Hog Rider, the Hunter's splash will damage the Hog Rider and hit the card in front of it more.\nThe Hog Rider in conjunction with the Freeze can surprise the opponent and allow the Hog Rider to deal much more damage than anticipated, especially if the opponent's go-to counter is a swarm, or swarms are their only effective counter to him. Skeletons and Bats will immediately be defeated by the spell, while Spear Goblins, Goblins, and Minions will be at low enough health to be defeated by a follow up Zap or Giant Snowball.\nHowever, this strategy isn't very effective against buildings as the Hog Rider will take a while to destroy the building, giving the opponent ample time to articulate another counter.", 'stfu', 'its so annoying', 'your mom is the universe you know why?', 'stfu bro your mom is larger than the entire continent of asia', 'https://tenor.com/view/fat-cat-garfield-tummy-full-tap-belly-gif-15742977', 'https://tenor.com/view/stupid-dog-shiver-the-antagonists-aiya-dog-perrito-gif-22710731', 'stfu boy you the type of guy to stop at a red light in gta 5', 'stfu', 'your as short as a toddler', 'caught yo ass a second time', 'caught yo ass', 'I hate you <:sadpuddle:962960986472579113>', 'Ha bitch', "Oh there goes rabbit he choked he's so mad but he won't give up that easy, no", 'Your pfp is literally a factory, get your polluting ass out of here', 'IM NOT SHORT', "Perhaps you're so short your tastebuds couldn't REACH the flavor", 'You hate taste?', 'PEPSI IS ALREADY BAD I HATE IT', 'that shit looks insanely like the apex legends battle pass', 'Stfu', 'i had to go shit really bad', 'fucking what?', 'Was that when the moby dick showed up', 'LIFE SHIT GOT REALLY IN THE WAY', 'fuck', 'i also dislike stakes', 'I hate stake', 'I said drinking everyday would be shit', "You'd pussy out", "He'd start questioning his morals and shit", 'I dislike swimming, but you seem like the kinda guy to go to a bar and say "can I have a water please?" when you\'re the only one there', 'is short', 'None short enough?>', 'shit', 'FUCK YOU I AINT NO DINGUS', 'you gonna let that shit slide?', 'howd they all die in one year', 'oh my fucking god', 'And finally i heard this loud-ass screeching', 'I would rather DIE than become p2w', 'i fucking hate it', 'i hate looking at my past self', 'he said bitch once', 'fuck you thats my pickle milk', 'a', "Raiders can't do shit", 'Bro what the fuck', 'a', 'a', 'a', 'how about you shut up!', 'IM NOT SHORT', 'is short', 'shut up waca', 'STFU WACA /j', 'waca chan is ass', 'I hate you', 'SHUT', 'SHUT.', 'i wasnt talking to you bitch', '"You still don\'t get it. I\'m using war as a business to get elected... so I can end war as a business! In my new America, people will die and kill for what they BELIEVE! Not for money. Not for oil! Not for what they\'re told is right. Every man will be free to fight his own wars!"', 'I’m your official worst nightmare and I living for it 👩\u200d💻', 'just short', 'Ikr it’s too easy because he sucks at comebacks lmao', '***fuck***', '(you dont wanna see me when im angry!!!)', 'He’s short', 'Stealthy you SUCK', 'Stealthy + Gay + Sewer Rat + UWU gay boi + I slept with your mom + you suck + pissy pants + cries because I’m right and you’re wrong + || #Die || + Ratio', "Didn't give a shit", 'If it gets annoying', "Like honest to god we don't give a shit", 'It was mostly "your mom"', 'Remember, IDC if you say shit', 'and ur not short', 'is short', '|| Kill me pls ||', "Heard from Tiny's dad", "But you ain't got no ass 🗿", "Just don't be annoying", '"I\'m not tolerating this shit anymore, staff can warn much more broadly now"', 'Send this to your teachers and say "FUCK MLA I WANT WACA"', 'The document looks REALLY fucking good', 'that shit look like the fortnite battle pass', 'shut', 'Your mother', 'Some suck less', 'Everywhere sucks', 'No we are oppressive as fuck', 'ACTIVELY PROVOKING SHIT', 'EXCEPT AMERICA!!!! (please dont kill me im joking)', 'The japanese in my mind were some of the worst war criminals in all existence', 'SHUT UP', 'is short', 'COVID HATE CRIME???:', 'FUCK YOU', 'CHECKMATE BITCH', 'OH MY GOD THATS NAZI TECHNOLOGY THERE YOU FUCKING INCONSIDERATE', 'Is that a fucking armored train', 'shut up', 'Suck it.', 'Let me lawyer the fuck out of this rq', 'SHUT IT', 'shut', "But you're short", 'How short were you', 'You were as tall as a piece of shit wtf', "and my father is 6'1", 'i went to preschool and i was tall as shit', 'shut.', 'You’re stupid gay and UwU boi AND GAY Wow you are very weak', "willy wonka's chocolate river was insignificant compared to the chocolate paradise i made in that chipotle bathroom stall", 'You’re stupid', 'i am having a relationship with your mother', 'I’m gonna go eat lunch with your mom be right back 🤩💅🏼', 'that short', 'I mean I could honestly do that but you’re too short to do it ', 'your mother', '*really* that short?', 'IM NOT SHORT', '*Short one*', 'bro stfu', 'THEY ALL FUCK ONE ANOTHER', 'YOUR SISTER IS YOUR MOTHER', 'YOU FATHER IS YOUR BROTHER', 'He’s gay short and a uwu boy', 'FUCK YOU', "WE HAVE THE SAME MOTHER, SORRY YOU'RE ADOPTED", 'WHEN YOU SEE YOUR MOM', 'FUCK YOU', 'FUCK YOU STEALTHY.', 'EVERYTIME YOU SPEAK A PILE OF SHIT COMES OUT', 'SHUT THE FUCK UP', 'WHAT GOES AROUND COMES AROUND BITCH', 'cuz that shit was ass', 'your mother', 'IM NOT SHORT', 'Confirmed?? Stealthy is short gay and and UwU boy', 'is short', '|| **DIE** ||', 'you cant prove that shit', 'You*', "<@458023820129992716> FUCK YOU, YOU'VE DOOMED ME FROM THE START", 'AWEEE UWU BOI THANKS HES BETTER THAN MEEE AND MY DOING OF YOUR MOM', "everybody knows that i'm the mother doer", 'how could say that to my mom', 'I that’s what you said when I was sleeping with YOUR MOM', 'Stealthy I’m your worst nightmare', 'what the fuck are you guys even talking about', 'golem sounding mother fucker', 'When mother dearest says no need to wash 💔', 'My mother would be happy', 'A', "One that's going to be REALLY short", 'FUCK YOU WACA CHAN', 'AND I SLEEP WITH YOUR MOTHER ALL NIGHT', 'YOU ARE SHORT BOYO', 'sadly i none of you are big men which i only talkto big men or big oily men so ha', 'which why add that its so annoying i cant cuss out 2 yearold who arent old enough to play the game', 'Among us balls stfu', 'I only talk to big men', 'We have another member of the Stealthy Is Short club', 'Dies', 'THATS WHAT UR DAD SAID TO ME', 'UR MOM IS SUS', 'I HAS ONE IN PRESHCOOL BITCH SO SHUT', 'I HAVE YOUR MOTHER', 'UNDER BOYOIST RULE YOU GET ABSOLUTLEY 0 BITCH.. i mean all the bitches', 'WE GET RICH AS FUCK', 'Suck it up', "THAT'S WHY YOUR MOTHER IS IN MY BED!!!!!!!!!", 'because when im angry i invade 12 of my neighbors', 'you dont wanna see me when im angry', 'WHO THE FUCK IS ROBIN BUCKLEY', 'BITCH YOU KNOW WHERE', 'UR MOM CRIED HARDER', 'how could you call my mother stupid', 'your mother fat', 'Mother stupid.', "i'm going to hidenburg you if you don't stfu", 'Nah bro thats ur mom 💀', "cova's mother be like", "COVA SHUT THE HELL UP THAT'S WHY YO MAMA BUILT LIKE THE AIRSHIP L30 FROM BATTLEFIELD ONE", "5'3 ISN'T SHORT AND YOU KNOW IT", 'I WANT YOUR MOM', "I'M NOT EVEN THAT SHORT", 'THEY BETTER NOT BE SHORT', 'STFU YOUR MOTHER IS MY BITCH NOW', "STFU YOU'RE TALKING SILLY", 'I SLEPT WITH YOUR MOTHER TWICE', 'I SLEPT WITH HIS MOM', 'AND YOUR DAD', 'I SLEPT WITH YOUR MOM', 'CAUSE I GOT BUISNESS WITH YOUR MOTHER 24/7', "he's gone mad", 'stfu red man', 'Fucking turkey you mean', 'Fucking TURKEY', 'when im mad', 'Bitch chill not everything is about strength and dominance heirarchies', 'gosh, you dont wanna see me when im angry!!!', 'die >:(((((((((', 'I shouldnt insult fellow men', 'stop calling your dad a hobo', 'I am your father', 'men this is worse than we thought', 'because im ur dad', 'thats what your mom said when you were born', "The thing is that we just need to focus on getting inactive users active and part of that is to ensure our current active playerbase aren't a bunch of fucking illiterates", 'Idc if it gets votes do whatever the fuck you want', 'If no, then diamonds are worthless', '(i love men)', 'Just like fucking racial slurs or something', 'He said "kys"', 'And you only give what information you give a shit about', 'fuck the message was deleted', "w!warn <@612421341265788989> ?r WTF Don't tell people to kill themselves even as a joke wtf ?dm", 'shut up XX_poopeater12_XX', 'You sure?', 'parties are ass imagine', "shit's ass", 'shut', 'im not short', 'is short', 'that shit getting ddosed hard rn', 'bros mad he cant pull of 1v10s', 'No shit', 'mald + loser + get better', 'ngl i hate anime after i watched 1 episode of naruto', 'pussy move', 'MAN FUCK YOU', 'shut up you lost at connect 4', 'You have 1 day bitch', "it's a big ass tank", '664 nm ass', 'your mother is built like', 'Your mother kinda mid', 'So your mom looks like that stealthy', '<@764529188836868107> Bottom left looks like a knock-off of that bitch from the movie "The Ring"', 'that shit looks like the fortnite battle pass..', '**Stealthys mom** - <@362372093423255552> (fast)', "i would want to prove that you WEREN'T with my mom", 'why would i want to prove that you were with my mom..?', 'Just like how you cant prove that I was with your mom', 'Damn that sucks stealthy', 'https://tenor.com/view/dad-sadcat-sad-cat-gif-19198793', 'what the fuck', 'you cant have shit in cyprus', 'what the fuck?', 'I named my dog "your mother" so I can say I fricked your mother', "I'm saying that you getting a Barbie doll and calling it your mother does not make it my mother", 'you just called your mom a barbie doll', 'then explain your mother', 'Your mother was found in my bed multiple times', 'i hate edp', 'False information, your mother was found at my house', 'fuck', "Nah that's my ding dong", 'Your mother is built like a friggin Roblox airplane', "stfu that's why your mom is built like the airship L30 from battlefield 1", 'You mother is built like skrek double cheeked up on a Friday night', 'your mom is built like joe', "you're mother!!!!", 'you are mother!!!!', 'Plus your drip sucks', 'yes fuck you!!!', 'that shit looks like the fortnite battle pass 🥶', 'ewhwta the fuck', 'oh no shit why popular choices is full of weeb shit', 'die', 'i wont get mad', 'Why is the points shop full of weeb shit 24/7', 'And ill fucking do it again if valve releases a new VR headset', 'die', 'Checkmate bitch', 'cant have shit in slovenia', 'cant have shit in detriot', 'Fuck', "your right i did your mother's sister", 'I LOVE DOING YOUR MOTHER', 'he really was being a gay ass frog to be advetising', 'fuck', 'No one else FUCKING boosted', 'you just suck at not letting close ppl join you', 'And its not because I have short-term memory loss', 'Like to kill?', 'Exactly why I need myself some folks who like to kill', 'the test, funky, stealthy is short thing', 'that shit look like the fortnite battle pass', 'that shit does look like the fortnite battle pass', 'yea what shit', '***that shit look like the battle pass though***', 'THAT SHIT LOOK LIKE THE BATTLE PASS', 'is short', "i'll be really angry", 'Winter you mother is gonna get clapped', 'Your mother', 'didnt the boyo army die', 'Nah when I think of I think of Shrek but rlly short and red', "Now STFU I'm losing my sanity trying to make VR gloves because of stupid springs\nhttps://www.youtube.com/watch?v=2yF-SJcg3zQ&t=1s", 'Oh shit', 'And you can make fun of stealthy being short or something', 'Fuck no.', 'Yoo also love being short', '****why the fuck are you guys bolding****', 'im going to prune your mother', 'w!warn <@764529188836868107> <@589211833932447745> ?r Abuse of reactions to a community question ?dm', 'is short', "5'3 isnt short", 'its not that short', 'they act like i just called their mom a silly goose and they took offense to it', 'mfs getting mad over a joke 😩', 'Get some bitches and just no fuck you', 'go eat a raw fucking potato', 'no fuck you', 'And I did your mother', 'Your mother is on the server', 'no fuck you', 'How stupid do you think we are?', "illegal doesn't mean shit", "Illegal doesn't mean shit ngl", "Y'all are stupid", 'Good because I did your mother', 'im not your dad', 'take your aggression out on your mom', 'isnt that shit illegal', 'w!ban 986741673914662922 ?r Fuck you stop dm advertising ?dm', 'w!ban 986741673914662922 ?r Fuck you stop dm advertising ?dm', 'nah he just called me i told he got banned and he just laughed and now we are chill with each other im not mad at him', 'nah he just likes being annoying and trying to get ppl in trouble and blackmailing if or if he makes bets that can screw you over', 'Does he do shit', 'but he said he was mad i played minecrfat and taled in vcs with ppl', 'yeah i rlly think he is just mad i wouldnt play fortnite with him lmao because he is a close friend of mine', 'mf radiates angry toddler energy', 'He was talking shit about a server he left', 'He just made everyone mad, no one took his ideas and he ragequit the server', 'fuck off', 'oh wait he doesnt know what a bitch is', 'a', 'shut up about me stealer', 'no suck a dick', '"i think the only failure here is you as you cant fucking roast for and sit down on your ass all day playing games at least i go outside and work unlike your dumbass"', '"i\'m about to get packin\' on yo ass"', 'He sounds like a fucking discord wannabe packer kid', '"i did read the rules but i dont give to shits dumbass what the mods gonna do ban me well they can go ahead and do that if they can even do their job"', 'your mom doesnt count', "you're right but at least i don't raost my own shit and eat it then shit it out and repeat", 'now you are losing comebacks bitch', 'be quiet you like big white oily men butt', 'have you ever heard of not being a ass just because you did something wrong and he is correcting you', 'Ong', 'You get good and let me do your mother', 'slaughtered their ass ez pz', '<@764529188836868107> whoever is player 1 sucks balls', '/advancement I did your mother', '-advancemnt  I did your mother', 'And your mother is at my house to', 'ong', "I'm trying to put up these stringy led lights but I'm being retarded and can figure out how", 'Computer must have shut down', 'kill everyone', 'theyre pieces of shit', 'ah cant stand americoids and their fucking cartoons', 'are the twitter warriors getting mad at someone for liking anime', 'what happened did someone like shit their pants then throw it at someone', 'their dad is a relic of the past now bro', "w!b 938599167654240316 ?dm ?r I'm not banning you because you are under 13, I'm banning you because you are too stupid to lie about being under 13", 'you', 'FUCK', 'fuck you', 'There is an achievement where you need to kill one of every hostile creature', 'Yo, I have found a reason to kill The Warden', 'fuck it', '<@764529188836868107> you suck', 'penis', "and the only reason why i hate it, it's because it's not morbius", 'Amen', 'He will live forever in our hearts.\nIn that sense, he truly will never die', 'I’m going to but what the fuck', 'what the fuck', 'Holy shit', "shit's sad man", 'Shut your ass up', 'what the fuck is that link', 'fuck', '*man fuck you*', 'alexander the great was short', 'Nvm internet still shit', 'oh shit', 'That was decades ago, yall short noe', 'short', 'short', 'Make it short', 'IM NOT SHORT', 'Mfs about to mentally scar a short child', 'fat fingers', 'fuck off', 'LETS FUCKING GO', 'Ok stfu im binge playing one direction', 'is short', 'HOLY SHIT THATS 3F AND I', 'Ur my father whole different story', 'He used to be active as fuck', 'FUCK', 'DIE', '<@245430374123962378> holy fuck', 'I leave for 5 fucking seconds', 'Yall dont stick a whole fog machine in yo mouths?? Fucking cringe', 'Where the FUCK did you get vape from', 'Hello step mother', 'what the fuck is /srs', '3f is my step mother😳😳😳😳😳😳', "You're welcom- HOLY SHIT YOU HAVE A STEP MOTHER", 'Thank you father', 'hey i said that fuck off!!', 'go fuck yourself', 'is short', 'Shit no', 'i hate tiktok!', 'you', 'i was a dick even with it', 'being a mod never let you be a dick', 'also being a mod won’t allow me to be a dick', 'its because of his short dick', 'Winter the role color is literally the exact fucking opposite of the overseer color', 'SHIT', 'Damn its almost like the entire fucking staff team was fired winter', 'reset i mean im stupid', 'Cant buy shit', 'its stupid', 'tinys mom is a hoe', 'Actually fuck it', 'That sounds soo stupid to the point where it might actually work', 'Don’t die!', 'the only reason why i hate it is because i played with cova like 50 million times and lost all of them', 'Were ya being annoying', 'oh shit', "5'3 isnt short", 'im not short!!', 'both short', 'FUCK', "its not that im obsessed with it, it's that whenever people call me short i wanna see what their height is because it wouldnt make sense otherwise", 'Then why is it so short', 'stfu and kiss already', 'youre british stfu', 'your short stfu', 'ong', 'It seemed like a hate crime to me', 'SHUT', 'You’re making me angry', 'What the fuck', "W for shut the fuck up or else i'll eat your legs", 'Fuck you', 'Shit in my mouth', 'FUCK YOU', 'i will not shit up', 'Shit up stealthyboyo', 'Jk <@262517788755755010> we don’t want shit', 'Fucking 13 days ago man..', 'I wanna leave this stupid place', 'fuck', 'OH SHIT', 'Okay so i checked my paypal and its fucking empty somehow?????', 'i dont think thats his mom', 'why his mom fucking watching him doing that', 'This mf telling me to stfu', 'no you stfu', 'Its an extremely important task stfu', 'im not that short', 'no shit', 'i am not short', 'WHY IS EVERYONE SO TALL IN THIS BITCH WHAT THE FUCK', '***short..***', "5'3 ISNT SHORT", 'was it not already ruined by you being short', 'dont you even say a fucking word', 'I AM NOT SHORT', 'NOT SHORT', 'is short', 'you bet your ass i will', "You're gonna hate me in game i swear", '"SHUT THE FUCK UP\nSTOP GIVING HIM IDEAS GODDAMNIT" - ShortBoyo', 'SHUT THE FUCK UP', 'Imagine everytime stalthy joins the game a chat bot yells "short"', 'FUCK', 'Short mf', 'im so sorry fucking what?', 'BITCH YOUR NAME IS STEALTHY AND YOUR ASS IS RED AS HELL HOW ARE YOU STEALTHY', 'What else does stealthy hate that we can put in the bot...', 'SHUT UP STEALTHY', 'LETS FUCKING GOOOOO', 'YOU FUCKING BURNT MY MAN KNUCKLES', 'Im just gonna say among us to tell you to shut tf up now', "L UNIONISTS + BOZO + RATIO + YOU'RE A GOON + NO FARMS + NO NETHERITE? + I'M ADAM CONOVER AND THIS IS ADAM RUINS EVERYTHING + SEETHY COPEY + YOUR MOTHER + WACK + EPSTEIN + $WHACKD + BELIZE + WE MAKE GOOD POTTERY??", "L FEDS + BOZO + RATIO + YOU FELL OFF + WHO ASKED + NO U + IM A MINOR + CAUGHT IN 4K + COPE + SEETHE + IN 1947 THE WORLD'S FIRST GENERAL PURPOSE COMPUTER, THE 30 TON ENIAC WAS CREATED, + YOUR MOM'S + THE HOOD WATCHES MARKIPLIER NOW", 'is short', 'Like they will tell you "Go fuck yourself" if you update', 'fuck', 'is short', 'anarchism do be kinda doodoo ass though', 'Personally those all suck and anarchy should reign but go get it I guess', 'is short', 'is short', 'is short', 'WHAT THE FUCK', 'this is what you fucking get', 'AY FUCK YYOU BRO', 'shit', 'HEY WE DO NOT USE THE FUCK WORD AROUND HERE', 'What a stupid fucking bird', 'i know its ver very dumb suggestion but could u do another new smp on 1.16.5 ????............', 'Bruh am I cursed or sum shit', 'no dick', 'that little shit', 'fuck you', 'Fuck you too', 'Fuck u', 'Hello, and fuck you Nova', 'So do the railroad crossings when your mom approaches them', "And I'm working on a school presentation so shut the fuck up or ill do both your mom ***AND ***your dad", '<@362372093423255552> watch my stream which i am doing your mother', 'Yass', "Sorry yeah I'm stupid😓😩", 'stfu government', 'Oh shit diamonds guys', "Yeah it's kinda dumb😋💗", 'what the fuck', 'that sucks on you', 'Shut up period pad', 'god i hate the modern education system', 'So just curious, earlier I was playing mining deep and the bricks ahead started mining randomly without my input, random shit started falling out (ender pearls, trident, exp), and all I was mining was stone and cobble. Was somebody fucking with me or was that just the server being funny goofy?', 'i used to hate wearing my glasses', 'dog', 'go fuck yourself pasta eater', 'you taking this shit serious 🗿', 'you built like a fucking monster truck', 'man only fucking knows the 1936 europe map and thats it', 'i fucking left my house in romania for 2 seconds', "you can't have shit in slovenia 💀", "I think we're the only ones doing this shit", 'FUCK YOU', 'Whenever someone sussy or annoying comes in', 'I hate lenses', 'I honestly love seeing people get mad over profile pictures', "Now it's not nazi shit", "It's poland shit this time", 'why do you always put nazi shit as your discord pfp', 'Fuck You Bee', 'bruh the server is kinda dead bout to kill the wither also the server is to ez', "you're fucking evil", 'fucking fight me', 'Why the fuck do you want to eat sand, stealthy?', "and if they didnt forget all the time i wouldn't have been as mad", '"don\'t fucking give me that shit it\'s not my fault you forgot"', "and of course when you go back they give you like a fucking snarky attitude and you're like", 'how the fuck', 'they fucking forgor the chicken sandwich', 'fried chicken is tasty as fuck', 'Mad respect. Fried is the preferred chicken format', 'stfu', 'I like my chicken nuggies as fried as your girls ass when I slap that shiz', 'Stupid idea', 'stfu', 'hey fuck you', 'Imagine being stupid', 'So create a system abuse repercussion', 'Don’t forget, I’m a small angry child', "Also the second part is people are a little dumb and can't comprehend words", "w!q 690680642136178748 ?r  <:RiceHatCat:941383581622734878> **Wick** says: Don't care + didn't ask + L + Ratio + soyjak + beta + cringe + stfu + cope + seethe + ok boomer + incel + virgin + Karen + 🤡🤡🤡 + you are not just a clown, you are the entire circus + 💅💅💅 + nah this ain't it + do better + check your privilege + pronouns in bio + anime pfp  + the cognitive dissonance is real with this one + small dick energy + 😂😂🤣🤣 + lol copium + snowflake + 🚩🚩🚩 + those tears taste delicious + Lisa Simpson meme template saying that your opinion is wrong + 😒🙄🧐🤨 + wojak meme in which I'm the chad + average your opinion fan vs average my opinion enjoyer + random k-pop fancam + cry more + how's your wife's boyfriend doing + Cheetos breath + Intelligence 0 + r/whooooosh + r/downvotedtooblivion + blocked and reported + yo Momma so fat + I fucked your mom last night + what zero pussy does to a mf + Jesse what the fuck are you talking about + holy shit go touch some grass + cry about it + get triggered", 'god fucking damn it', '"How to not fuck up tour faction in 48 hours or less"', 'shut the fuck up you staunch anarcho capitalist', 'COLONIZE A FUCK TON A LAND', 'ARSEN!!!!!!!!', 'COVA GET UR ASS ON', 'Then everyone will hate u', 'ALMONDS SUCK', 'FUCK', 'https://tenor.com/view/spamton-shut-the-fuck-up-stop-posting-about-among-us-stop-posting-gif-23791232', "But not like I'm gonna die of fear", 'i heard it is kinda shit', 'Shut up', 'oh shit', '***but then it was shit***', "2042 is up there with cyberpunk and no man's sky in the list of worst releases", 'that moment when dynmap randomly shits itself for no fucking reason at all', 'either he will do /kill @e or prison you', 'a', 'bitch', 'stfu you are the literal definition of a soyboy', 'FUCK YOU', 'your mom', 'Why is my friend fucking insane', 'The fact that cova managed to cut it down to that size is nothing short of a miracle', 'Well shit im glad', '3.7 GIGS WHAT THE FUCK', 'I go straight ahead and die', 'my father is currently talking about nfts', 'shut yo mild ass message bruh', 'fuck you', 'FUCK YOU', 'nor fat', 'IM NOT SHORT', "**Review of Footstool StealthyBoyo**\n\n10/10, my friend, his crush, WACA-Chan, loved using him as a footstool as she dreamt of being with another guy. His crush is so happy with this footstool cuck edition and it's short little stubby legs that she wanted to keep him as a pet. Sadly I had to say no as we didn't have the means to feed the fat fuck, but the footstool decided to beg helplessly anyways. Stealthy just couldn't resist the hot urge to submit to the 6'2 dominant woman in front of him as he begged to to be slapped around. WACA-Chan was very pleased, but decided to return the footstool after she was finished", 'you', 'FUCK YOU', 'ass', 'i fucking hate this bot', 'BITCH', 'FUCK YOU', '3F YOU SUCK', 'FUCK', '***fuck you***', 'imagine not shutting the fuck up', 'i fucking love books', 'Short', 'shut up', "eh, i wouldn't say you're dumb", 'And me being dumb', "then i'll fucking choke you to death", "and then i'll make fun of you all for being short", "my father is 6'1", 'am i short on my own? maybe', 'am i short compared to everyone else? yeah probably', 'the debate of stealthy being short', 'I may make fun of stealthy for being short and bad at chess, but one thing is, he can actually form a coherent argument pretty well', 'No I just said they are annoying', "its just annoying but sure I'll upvote it if you want 🤷\u200d♂️", 'They just move around a lot its annoying', 'Nah I just hate having villagers getting in minecarts', 'the hassle of getting a stupid villager to breed', 'You can think that villagers are annoying', 'Its annoying just trying to get them to breed', 'that doesnt change my opinion that villagers are annoying', 'and they are annoying', 'Creeper holes are ugly', 'fuck you', 'fuck', 'you suck', 'DONT YOU FUCKING DO IT', 'fuck you', 'im not a fucking ginger', "The real reason why stealthy's pfp is red is because he doesn't have the personality to be custom, his personality tried to show up but it couldn't find him as he was too short", 'his mother went to bed with another man', 'Then why are you so short?', "my dad is 6'1 and my great grandfathers were 6'5-6'7", 'IM NOT SHORT', 'AND short', 'FUCK YOU', 'ur actually so short', 'FUCK', "You're too short to see through the windows", "fuck you i'll run you over with a train", 'shut up stealthy boyo chan', 'NOT THIS SHIT', 'will', 'fuck you', 'Short people not welcome', 'https://tenor.com/view/the-voices-cat-mad-going-insane-going-crazy-gif-24274574', 'Kill him now.', 'kill it', 'i needs shit on the server', 'i need my ass bombs', '<@362372093423255552>  cmon ass bombs', 'i cant die to fall damage while landing on water', 'You have the build of an irish peasant during the potato famine you fucking yeehaw yee yee looking fuckin potato headass literally so bad at everything cant win at hoi4, chess, or checkers lookin shorter than a girl your age looking fuckin donkey ass', 'Fuck you you fucking hamster elderberry lookin shorter than napoleon lookin headass', 'i mean militarily though you guys fucking blew', 'oh shit', 'you weigh more than the fucking polar express', 'stfu you got 10,000 pounds on you', '4056lbs looking ass', 'To die from water', 'i need to die by taking fall damage to water', 'Where we like blow the whole world up before we shut it down', "Yeah amazingly if I can barely find a way to schedule the opening/closing on a day where like 20 people are available there is no fucking way I'm going to do that for all 700+", 'thats sandstone, dumb', 'yeah i dont fucking know', "he's fat, ***just like your mother***", 'SHUT UP', 'IM NOT SHORT', 'cause you are too fucking short', 'SHUT UP', 'Holy shit these mountains look soo cool', 'FUCK YOU', 'holy shit kiro this is amazing', 'they have big ass glasses', "that's what you get for calling me an angry child", 'box literally has a penis nose', 'you fucking built like squidward', 'Fuck you', 'you got a big ass nose', 'We hate the ATF', 'yeah bitch', 'i stomp shit in the shower drain', 'brown is the color of shit', 'okay asshole you try being a solid color and try to fit in', 'did you paint the fucking wire', 'you called me a angry child', 'im gonna run you over with a fucking fertilizer', 'IM NOT ADOLESCENT FUCK YOU', 'Angry', 'Calm down angry child', 'your mother would ride me like it was mario kart', 'regular show was the shit', 'Cartoon network was the shit', 'the amount of shit themed things you have said today is getting a bit sus', 'They suck all around', "you're a fucking maniac", 'i didnt use the word with shit though', 'FUCK I FORGOR', 'because you cant even use waffle in a sentence without talking about shit apparently', 'get shit on', 'I thought it was a fucking meme', "it's funny ***shit*** bro", "it's the funniest shit i ever seen", "it's a talking dog that said taco bell in Mexican or some shit yes that is definitely heroin", 'fucking what', 'get shit on', 'if i do become defeated i just want you all to know that box has 4,000 fucking hours on hoi4 while i have like ten', 'bro i cannot fucking wrap my head around division templates', 'shit', 'mom gay', 'fuck you 3', 'SHUT THE FUCK UP I WAS SO CLOSE TO WARSAW', 'you didnt fucking curbstomp me', 'a', 'and make you hate yourself', 'box is not dad', 'hi stream, im dad', 'The short one', 'SHUT UP', 'i hate you', 'SHUT THE FUCK UP', 'SON OF A', 'you are short\\', 'stfu stealthy', 'Literal loser boy from birth', "Don't make assumptions loser boy", '<@764529188836868107> why the fuck would you say that', 'idk if you can be mad at him for that', 'fuck', 'if you had intercourse with my mother', 'made with love by your mom and me', 'usually after saying your mom over my shoulder', 'if by tall you mean short', 'shut up introverts', 'amen', 'Im a femboy. Hows that for "stupid shit}', 'You?', 'worst mistake', 'this blacklist is retarded', 'looks like what my dog throws up after eating some shit he isnt supposed to', 'hate this state', 'Im also a sith because I hate poor people', 'he plays war thunder hes full of hate', 'i was really hoping germany would send some men over especially after their big military expansion', 'I used to hate my voice, absolutely hated it', 'IM NOT SHORT', "Every deep sounding guy I've met is so fucking tall", 'not as short as you', 'short?', 'my dad lived in puerto rico for years', 'fuck you', '<@!458023820129992716> DO YOU SEE THIS SHIT', 'Nah what the fuck', 'You fucking did not put a freshly used plunger on your goddamn face', 'i remember going with my mom to my local little gamestore', 'bro wii sports resort was the shit', 'ive got shit pulled out the wall', 'EVERYBODY HERE SUCKS', 'SHUT UP NOBODY LOVES YOU', 'AND THAT WAS STUPID', 'I HATE BASILISK', 'Bro why the fuck', 'shut up corsair nerd', 'SHUT UP', 'Razer durability sucks', 'stfu corsair nerd', 'but short.', 'cuz hes short', 'my dad actually taught me how to play basketball', 'IM NOT SHORT', 'no but my dad did', 'everyone here is worst than hitler', 'you suck', "THAT'S THE WORST ONE BRO", "THAT'S THE WORST ONE", 'shorty', 'call me short', 'SHUT UP', 'w!ban <@!764529188836868107> ?r yes, fat. praise adam there is no other god', 'https://tenor.com/view/fat-among-us-fat-bababoy-gif-19338920', 'Fat us?', 'I mean fat', 'King of Fat', 'yes, fat', 'The Council of Fat welcomes <@!764529188836868107> to the council!!!!!!!!!!', 'yes, fat.', 'yes, fat.', 'yes, fat.', 'Uh oh Novas angry 🥶', 'But I also hate the look of the handle', 'Am sorry for not really answering your question but it makes me feel like I need to prove everything I saw/type and 8 hate that to no idea. Then I get frustrated at it and want to cuss so I was trying to save myself from that', "I'm already my dad's tax assistant", "It will let you grip the screw even if it's eroded", 'My mom put me in homeschooling immediately when covid started when she had the chance', 'what is he gonna do kill emberia faster', 'and it just prooves how many ppl red ppl kill daily', 'thats why all the dice and gonna kill reds and only reds', 'until you die', 'cuz the one in game sucks', 'i feel like youd die', 'your mom disowned you', 'fuck sakes', 'fuck you 3f', 'ass', 'Losers', 'Yea fuck you', 'I had something planned for April fools  but ill be honest my dumb ass thought that today would be march 32', 'https://tenor.com/view/angry-annoyed-bad-vibes-throw-it-whats-going-on-gif-16325118', 'https://tenor.com/view/fuck-gif-9651048', 'Ong 💯', 'Fr its so annoying smhsmh', 'MOD ABUSE', 'SHE IS A FUCKING CHILD', 'And then get fucking steamrolled and create anime', "Stealthy's mom", "It's very short", 'lil boyo bitch boy', 'real men play game of ur', "No it's a game dummy", 'Nope but my mother is from a muslim country', 'fUck', 'My son he do haram he so smart and he so dumb', 'w!warn <@!764529188836868107> ?r Loser boy stop being annoying', "What you're sueing for is lowkey dumb, because you're trying to sue when you should be opening a ticket???", 'I hate when minecraft crashes and I have no idea why', 'die a virgin', "where's my mother i wanna go home", 'You like all the generals, you study them, nerd shit', 'FUCKIN', 'Am reading back, you people are short', 'Damn, you’re short asf', 'Jeez, how short are you', 'STEP STOOL LOOKIN ASS', 'this is a hate crime', 'Your sister is your mother, your father is your brother, you all fuck one another, the boyo family', 'but hey after all i still have your mother', "Bitch you came into the thunderdome quit while you're ahead", 'hate crimes against the red folks', 'AINT EVEN NAPOLEON HEIGHT LOOKING RED ASS BOYO ASS CHESS LOOSIN LEGALLY FUMIN', 'Shut', 'I HATE THIS', 'AND IM NOT SHORT', "Well it's either red for communism or it's because you suck so bad at chess you switched to checkers", 'but you are short', 'Fucking reds these days', 'Shut the fuck up you chess loser communist', 'Appreciate the pfp or die', '3F_1\n69 Your Mamas House\nFucking, NU, L01 6a4\n\n\n__________________ ____, ______\n\nCombinatioNova\nYour House\nMiddleofnowhere, ON, s4f4f3\n\nRe: Cease and desist demand\n\nDear CombinatioNova:\n\nYou should immediately cease the changing of your profile picture.\n\nThis will serve as your legal notice to cease and desist all further actions described above.\n\nI may use telephone recording devices to document any telephone conversations that we may have in the future if you fail to comply with this cease and desist letter. You are reby instructed to comply with this letter immediately or face legal sanctions under applicable Federal and Provincial or Territory law. I intend to keep a log of any contacts you make with me after you receive this letter\n\nPlease give this very important matter the utmost attention.\n\nSincerely,\n\n\n3F_1', 'oh shit', 'or you will die', 'or maybe even your dad', 'yeah it kinda sucks', 'his is your fault the server die', 'yeah man i pretty sure she is my mom', 'i cant die,', '3f gonna kill u now', 'A-', 'https://tenor.com/view/shit-poop-gif-13293541', 'you yell out "me when taco bell" and you die laughing', 'and tall men', 'crab games is for big men', 'i refuse to believe that a game such as among us will die', 'they have so many dumb roles', 'your the big fat doll', 'They bashed my mom so hard for not knowing before hand', 'that kinda sucks', 'i have a friend named jamal and he sucks', 'ima shut up', 'shit', 'shit', 'shit', 'shit', 'you kinda of an ass', 'he kows how to do this shit', 'were all gonna die', 'bryour wierd as fuck', "I hate how when you don't see someone older for like 2 years and then you see them, they don't believe you're that young", 'Stay mad', 'Fuck u', 'If they get mad you can explain it, say that you were taking someone already or just take the one you like the most', 'And then make them mad at me for not taking them', 'Sorry I know this is a minecraft channel but I need to get something off my chest. I want to go to town and I know that if I do and people find out I went without them they will be mad. But for safety reason I cannot take more then one other person in my car making the other one mad. The people in question are just friends and not family but I still feel rude for thinking what I am thinking. It is really not my issue until it is', 'OUTLANDERS, I AM CHALLENGING THE LEADER OF YOUR FACTION TO A 1V1 TO END THE WAR ONCE N FOR ALL. THE WINNER OF THE DUEL GETS 300K FROM THE LOSER. THE TERMS N RULES OF THE DUEL WILL BE POSTED IF YALL AGREE TO IT. DO U AGREE?', "I just have basically every subscription they keep offering so they're practically worthless to me lmao", 'FUCK U', 'i think you are losing this argument because none of us are tht dumb accept for like 5 year olds', 'buddy we arent that dumb around here', 'Nah, he became a whole ass background character after the Isshiki arc.', 'Ohh, makes sense but was kinda dumb to change the whole design to make the viewers think smth right?', 'Making everyone believe that Naruto is gonna die after the time limit', 'They cant just kill off naruto n sasuke. Literally….', 'I hate boruto', '“In this arc, Naruto and Sasuke are gonna die trying to protect the village.”', 'Boruto is kinda ass after the Isshiki arc', 'That is a fucking life achievement right thwre', 'oh shut up box, u cant even double tap with respawn anchors insta kill.', 'HA SUCK IT', "They can't die if they're offline", 'Outlanders are gonna die', 'They are pathetic like their stupid fucking leader box', 'I mean i just fucking trashed the public lifesteal smp', 'Or die completely', 'Like sculk is a stupid idea', 'So im the ugly netd?', 'This is so ugly', 'Its not dumb I promise', 'FAST', '*Will*', 'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjW783Pg6n2AhWkIEQIHR7VDnMQyCl6BAgWEAM&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DTBjSXQO1Ngo&usg=AOvVaw1ytkSxVrly8yVrkPu9FCZ_\n\nClick at your own risk: by clicking on this link you have agreed to the terms that you can not get mad at me for this and no hate or deleting this link (for the admins)', '4. We therefore advocate a revolution against the industrial system. This revolution may or may not make use of violence; it may be sudden or it may be a relatively gradual process spanning a few decades. We can’t predict any of that. But we do outline in a very general way the measures that those who hate the industrial system should take in order to prepare the way for a revolution against that form of society. This is not to be a POLITICAL revolution. Its object will be to overthrow not governments but the economic and technological basis of the present society', 'Jesus fucking christ he does not know when to shut up', "I'll be real your spite against 3F is kinda stupid", 'im to stuborn to let flmae die', 'we dont care if you kill us', 'i hate pvp legacy', 'if iro moved his lazy ass he could make a gun powder farm', 'This is probably a dumb question but do the bedrock and Java players play on the same server or are they different?', 'I will die and go to heaven to help build the shopping district', '3F built an arena for pvpers to pvp. He said he had to fix it and told them to get off the arena. Banteep and crazyace stayed. 3F shot a warning shot with death arrows to tell em to get off, crazyace left but banteep stayed. 3F killed banteep but didnt give banteep his totems n pots back. Banteep started complaining about admin abuse, got pissed and left. Todo snd llama just followed banteep', 'Theres a whole new grave system rn and when u die u dont lose stuff.', 'still short', 'UR SHORT', 'nah im gonna rob my own villagers and shove them in a basement to kill them and make them my slave', 'did the whole vc just fucking die?', 'I have meds that do Work I mind you and I hate fighting them so Sleep it is', 'That cool as shit', 'Russia sucks', 'Not shit America suck', 'Insta kill', 'did u not kill us there tbh?', 'Suck at trapping', 'Thats just admin abuse now', 'Admin abuse wtf', 'yall suck if ur portals dont look like this', 'a', 'i hate ppl', 'https://tenor.com/view/minecraft-who-the-fuck-pinged-gif-21275267', 'fuck my typing', 'on an old shit sever i had made a drug basement and kid napped billagers', "[Trial Mod] CrazyACE_KING — 02/14/2022\nYa I know but it just build up from all the shit you've been feeding me NGL\nMirushia — 02/14/2022\nits not affording bricks entirely its not wanting to dig out three chunks of cobble to build\nso your saying you eat shit?\nnot suprising\n[Trial Mod] CrazyACE_KING — 02/14/2022\nI mean do you eat shit?\nMirushia — 02/14/2022\nyou literally just said youve been eating shit\n<:LUL:299951403458232320>\n[Trial Mod] CrazyACE_KING — 02/14/2022\nIt's sad that you didn't get that 😭\nIcedmi — 02/14/2022\nAnd what's wrong with that🤨\n[Trial Mod] CrazyACE_KING — 02/14/2022\nI can't have a some what smart come back", 'what the hell does all of this shit mean', 'Hello from butt-fuck-nowhere Canada', "It's basically an AI that can play your game for you, can do make buildings from schematics, can PvP to a degree, is fucking amazing at pathing and has a coded fear if death", 'My friend ate a ban for throwing on baritone to path to my base since he died a fuck ton and was doing something else at the time is he permd or can he appeal it?', 'Shit okay', 'dumb', 'smp with ur mom', 'bruhhh that sucks but ok', 'You', 'That’s the KYS g fuel merchendise', 'bro i gotta be taller than her to date her fuck', 'Shut up', 'Sucks to suck', "If you didn't understand what I said let me simplify you are talking shit as in you only speak dumb shit so if I hear your dumb shit my brain takes in your fucking stupidity and that's why shit goes in one ear and comes out the other", 'shit eating guy lmao', 'yeah ironed it out while you were eating shit', 'you literally just said youve been eating shit', 'I mean do you eat shit?', 'so your saying you eat shit?', "Ya I know but it just build up from all the shit you've been feeding me NGL", 'all the shit you spew its suprising', 'Sucks to suck my G', 'You need them for fireworks dip shit', 'we should just turn creepers off Ive never seen em kill anyone just break shit', "Well i don't make the rules but that has to mean you suck", "Missgendering sucks and i don't wanna suck", 'Also what the fuck', 'fuck villagers', 'I blame the gerudo from legend of zelda for my taste in women and astolfo on my taste in men', 'fuck', 'Oh shit sauron is being burned into my eye sockets', 'jessie fuck the meth jessie we need to start an pro ESL overwatch team jessie', 'HOLY SHIT', 'Jessie jessie im fucking gaming jessie', "But it's mainly she/sher that I dislike", 'bro got active cam footage of me dying to a skeleton after finding my shit', 'Finds someone they are starting to dislike, immediately assumes they are a woman, confirmed to be a chad', 'man this is why I like making out with men', 'she also voted no on raffles n shit', 'SHIT', 'OH GOD OH FUCK IM IN LABOR', '<@245430374123962378> fix my house yall broke my shit', 'You wouldn’t want to piss near your mother would you?', 'I sleep with your mother', 'You’ll probably see shit coming out of my sheets', 'I hate mikk', 'also fuck that means i lost 500 bucks', 'Bro i have like fucking 10 accounts', 'just found the suggestion, could have just legit submit a bug report or ask us to fix it but yall chose the legit opposite of that and said "fuck it lets just remove it"', 'not that hard, people are stupid', 'i am going to kill someone with redstone sooner or later', 'Deal is around Banteep’s level so we both know you’re not gonna try to kill him', "I'm pretty sure that I will die and I don't know if I was joking", 'llama you will die', 'We don’t give a flying fuck about Deal betraying us anymore so we don’t have a grudge against Flame.', 'Damn this kinda sucks ngl', 'What the fuck is a Tubbo', 'IMA GO FUL: PHEONIX WRITE ON HIS ASS', 'What the actual fuck', 'Slow falling pots are gonna be so annoying', 'Fuck my life is ruined', 'Idrk, provide when I got really mad in vc with some people while bringing villagers to some place and threatening to kill them a lot', 'i hate the microsoft migratiom thiing', 'Their system is so shit that the email doesnt send ever', 'You', 'Prisma, why do you hate me?', 'Then they suddenly catch you off guard and start trying to kill you', 'I hate people who keep ender pearling away', 'Fucking crashed on me', 'YEAH FAT HOG RIDER', 'fuck off banteep simp', 'frozone stfu', 'ee your like 2 so stfu', 'WHAT THE FUCK', 'Dont be, worst u’ll get is a warn or smth.', 'will kill', 'fuck it ima just reinstall the whole plugin', '4 more days to get rid of the fucking limit minecraft has', 'shit wasnt workinhg', "Hiring for my faction, Civil. Leave anytime, just looking for temporary allies (because it's always easier to get stacked with a team, plus it's a hell lot more fun :D) We have an area for a base and we'll get started on a gunpowder farm as soon as we have the materials! Any skill level, just don't beg too much although feel free to request items, it's just annoying to be spammed.", 'My computers fucking dying', 'fuck it ima find a Japanese artist', 'Fat man, waca-chan', 'Yes, fat.', 'THE FAT MAN IS BACK', 'The thought of waca-chan can only be comprehended for short periods until menta strain sets in', 'Fuck it ima rename <@!935290012021444688> to waca-chan', 'I remember I was once badly drunk and called my father crying, asking him why he never loved me', "Shit probably sweatpants and hasn't showered in weeks if I were to guess LMAO", 'god fucking', 'You have the worst influences around you', "Fuck you i'm doing it", '<@!458023820129992716> The question is that if we actually do this who is going to message them saying we want a fucking anime mascot for our minecraft server', "I'm gonna invite the fat", 'And now I want to die', 'Why the fuck', 'He doesnt give a shit', 'He sucks', 'Yo remember that club game I made on roblox and scammed the shit out of some of yall for that radio pass?', 'Holy shit thats ANCIENT', 'Shut', "I knew it'd make you die inside", 'I hate you', 'I hate you', 'I hate you', 'Should I make you die inside iron', 'I can make you really die inside', 'DONT MAKE HIM ANGRY', 'Making you the worst admin too', "The bot says HI wack, I'm dad!", 'Dad jokes', 'How u finding this shit again', 'Wheres dad bot', 'I will pay this till the day I die', 'What the shit', 'My dad forgot my age', '<@!699027776744718367> why the fuck did you grief my shops', 'Fishing sucks', 'Its literally the most useless potion eevr', "if you eat too much you'll get very fat now", 'rather', "tf is banteep's father role-", 'Oh my fucking god', 'A', 'What the absolute fuckity shit', 'Like fucking weird', 'the hoe your mom', 'I will give you your mom', 'I admit I’m shit at 1.18 pvp but I’m good at 1.8 lol', 'the server is currently committing suicide', 'My dad has to work until 1 am so he wouldn’t know…', 'Omg I hate phones', 'He’s better than you stfu', 'Bruh your trash stfu', "YOU'RE STILL ASS", 'hes ass', 'mad cause bad?', 'You did kinda break a whole ton of rules in a short amount of time', 'I hate my life so much', 'I USED TO DISLIKE PPL WITH BEDROCK', 'MY WORSt NIGHTMARE', "I'm stupid", 'thats sucks', "He wasn't mad... He simply stated to try googling it.", "nah just saying how if hes gonna get mad at someone for asking a question because he didn't link what he was referring to in his message and asked me to look up a basic word on google. maybe just copy and paste next time", 'have u considered linking the fucking shit you recommended? and not just a screenshot?', 'well how am I supposed to download the shit if I cant click on the link', 'You know after not reading something that might help you understand why you are having a problem such as an obvious place like <#912731255165046814> <#912727103550660709> <#916705306510250024> and looking for information that might help you, or even looking in one of the many relevant chats for information, \n\nI think you might have had a bad day, maybe got a bad grade on a school assignment, or maybe just tired, But if you then tell a moderator that is trying to help you to shut up, you are just stupid\n\nFirst time tired, second time just stupid', 'stfu', 'well i think the worst first so it can only get better', 'ill', 'ive got the same as you but with optifine too, and an autofishing safeguard so I dont kill my rods', "Plus you don't want cova to kill you in the process", "oh shit you're in the headhunters", 'i bet ur gonna kill me but ok', 'why does jesus already dislike me', 'and they hate nova for some odd reason', 'hate that machine', 'good shit', 'I could always kill your current sheep and move them', 'To die', 'Mother', 'its getting fuckin annoying', '<@!647662699215454209>  can you not show up to my house everyday and kill me', "yeah and techno's not fucking on it", '<@!458023820129992716> when you mean cracked plaeyr do tou mean like that little shit zero', 'what the fuck', "He used a trident, it's not admin abuse.", 'Ah yes flying 2000 blocks with trident I earned is admin abuse', 'to kill me', 'this is fuckin admin abuse', 'and that make me vry mad!1!', '<#912732231171199006> 2020 Is going to suck but you will make it through it. Also don’t skateboard to school on September 2nd of 2021', '<#912732231171199006>  DONT FOLLOW THE FUCKING RED DOTE!!!!', 'You could be the best in the industry but if no one knows that you exist, or if you advertise only crappy features even though you have amazing ones, its pretty much useless', "That'd be dumb", 'whre?', 'like you kill them you get head',
    
    "Fucktard",
    "Go to fucking hell",
    "Go die alone",
    
    "Here, the sources I was checking LMAO I wanted to make sure I wasn't spewing shit out",
    "i fucking ran my way downstairs actually",
    
    "Player kill all",
    "hello mr bot",
    "shut up Boy",
    "Wanker",
    "Called them a wanker",

    "It falls short honestly",
    "That fox is pretty short",
    "You aren't that short ngl",
    "You're kinda short",
    "That's kinda short",
    "That could be a little too short",
    "That's short",
    "Short breaks throughout the day can increase productivity.", 
    "Short hair can be very stylish and low maintenance.", 
    "Short stories can be just as impactful as longer works of fiction.", 
    "Short distance running is a great form of cardiovascular exercise.", 
    "Short term memory loss is a common side effect of certain medications.", 
    "Short-term goals can help you stay focused and motivated.", 
    "Short-sightedness, also known as myopia, can be corrected with glasses or contact lenses.", 
    "Short skirts are a popular fashion choice in the summertime.", 
    "Short naps can refresh and rejuvenate the mind.", 
    "Short cuts can save time, but they may not always be the best option.",

    
    "You're shit",
    "SERVER SHUTTING DOWN FOR THE MOVE TO HYBRID, WE'LL BE BACK SOON!",
    "Save your shit",
    "Holy fucking shit",
    "That's fucking shit",
    "i fucking hate you you sill cuck",
    "You cuck",
    "They called me a cuck",
#REAL LINE REAL SHIT
    "It falls short honestly",
    "That fox is pretty short",
    "You aren't that short ngl",
    "You're kinda short",
    "That's kinda short",
    "That could be a little too short",
    "That's short",
    "Short breaks throughout the day can increase productivity.", 
    "Short hair can be very stylish and low maintenance.", 
    "Short stories can be just as impactful as longer works of fiction.", 
    "Short distance running is a great form of cardiovascular exercise.", 
    "Short term memory loss is a common side effect of certain medications.", 
    "Short-term goals can help you stay focused and motivated.", 
    "Short-sightedness, also known as myopia, can be corrected with glasses or contact lenses.", 
    "Short skirts are a popular fashion choice in the summertime.", 
    "Short naps can refresh and rejuvenate the mind.", 
    "Short cuts can save time, but they may not always be the best option.",

    
    "SERVER SHUTTING DOWN FOR THE MOVE TO HYBRID, WE'LL BE BACK SOON!",
    "Save your shit",
    "I hate men 😡",
    "I hate women",
    "Your stupid",
    "Small dick energy",
    "hello welcome",
    "cova i need the last one i kinda was busy helping my grandma/my mom",
    "hello", "shell", "shelled", "helmet","shelter","phellogen", #6 there
    "the brits get all the hate",
    "Did you use a password you made yourself?",
    "It kinda falls short ngl",
    "hello mr bot",
    "HamzaLePrince200 has been permanently banned by CombinatioNova for Griefing, Dumbass clause",
    "Here, the sources I was checking LMAO I wanted to make sure I wasn't spewing shit out",
    "i fucking ran my way downstairs actually",
    "That can go to hell",
    "It can go to hell",
    "FUCK IT TO HELL",
    "Server alive moment?",
    
    "bro what did u expect i need money and shits expensive so i need high prices too",
    "What the fuck did you di",
    #EEEE
    "I will rape everyone you love",
    "I am going to rape you",
    "I will rape you",
    "Waca gurd is a fuck head",
    "Small dick energy",
    "i fucking hate you you sill cuck",

    "i hate ur words.",
    "bitch sskeleton shot me off me scaffolding tower :(",
    "im not lying to you rass you are beloved",
    "noted ''if you are shorter than a short guy named stealthy people will ignore it''",
    "HEY! nothin wrong with being short!!",
    "ok meet me at the bridge myults and rass cuz i want to gift u",
    "anyway gonna build a unnessassercy dammit english iss too much effort bridge",
    "you can't say ass-",
    "y are cows so ugly in game and beautiful irl?",
    "cuz its a one long block bridge and ugly af",
    "server kind of died tbh",
    "LUCKY BASTARD",

    "I will rape you",
    "I hope someone rapes you",
    "You deserve to get raped",
    "You basically begged to get raped",

    "Kill your self",
    "You should kill your self",
    "Go fuck your self",
    "I will rape you",
    "I will literally rape you",
    "FUCK YOU I HOPE YOU GET RAPED",
    "Raping you is so much fun",
    "I need to rape you",
    "hey cova did u c a bridge me and rass made near spawn?",
    #NEW
    "but usually since there is more of an excess amount of assignments compared to that of tests, you will still have a large majority of zeros if you just didnt do all the assignments",
    "you tellign me people fail all their classes",
    "your short",
    "BITCH!",
    "dick tater ship",
    "dick tator ship",
    "is that a dick",
    "is tiny fat",
    "-paste tiny is fat",
    "waca guard hates british slang >:(",
    "@CombinatioNova ayo your bot movin mad",
    "ayo this waca guard movin MAD styll!",
    "looking like a rahh mad ting, lend me your snap styll",
    "yeah i got special privileges to drop any class i wanted",
    "You can replace your fun classes with more core classes",
    "Thats because I only really actully yell when I need to deal with really stupid things",
    "so you hate yourself?",
    "What's the special grass, ghostbur?",
    "hey gold sith wants to kill people, you know what to do",
    "Nope Cova's are never dumb",
    "special made",
    "IM THE PERSON WHO CATCHES THE BALL AND THROWS IT BACK, I MAKE YOUR DINNER AND I MAKE SURE YOU DO YOUR HOMEWORK! I MAKE SURE YOUR OK AND SAFE! BUT ITS ALWAYS DAD DAD DAD!!!!",
    "sorry shorty :/",
    "Why is everyone talking about rape?",
    "im fine ghosty. cause if they died by natural cause its fine",
    "i was plannig to kill some off anyway",

    "anyway i need a shit ton of iron and gold now",
    "but if u spawn him outside he can kill things and get u wither roses",
    "yeah i got a shit ton of food",
#Bad Triggers
    "no im a short poor person",
    "I FKING HATE SKELETONS",
    "I dont own the server im just here to dick around",
    "Why do people get angry over words?",
    "He'll only try to cause problems",
    "hes angry",
    "hes trying to kill me with his fists",
    "FUCK YOU LETTER M",
    "bro i hate creeps",
    "did the server die",
    "@CombinatioNova did you shut off the server?",
    "cause im annoying as hell",
    "Yeah, he's been painfully annoying",
    "im fine ghosty. cause if they died by natural cause its fine",#14
    
    
# Good Triggers
    
    "stay a pussy",
    "Suck it",
    "i got to go thanks for the free stuff loser",
    "you really are stupid",
    "i don't have a house, dumb ass",
    "KISS MY ASS FAT PIF",
    "YOU HAVE NO FRIENDS NIGGA PUSSY MOTHER FUCK",
    "YOU KONW MATH LIKE A BITCH",
    "WOW ARE YOU THAT DUMB?",
    "Shut up fatherless child",
    "you LITTLE BITCH",
    "Suck my",#12

"Yeah. Unlike Siow who rlly just feels like he’s better than most people just because his YT shorts got good views",

"hey rass",
"server died",
"and your mad that i killed you",
"why are you mad",
"kiri is neon ur brother cuz rass is curious",
"imma go kill these guys down here",
"Really loves rassz",
"stfu u rass guy",
"no ur just stupid rass",
"so your saying that forgeting = stupid?",
"hey rass",
"Ima hide in nthis randoms house while i go honk out a big black shit",
"hes my worst enemy too",
"HES MY WORST ENEMY TOO",
"bitch i aint lazy",
"bizzy, are you short?",
"welcome back Rassx",
"hey rass",
    
"you need assistance with smth bash?",
"he mad cuz i kill him first",
"LIZZIE THEY ARE GAY-",
"well im sure your town has a lot of shit to help you get back on your feet right?",

"shut thy down",
    "I hate people thay use stupid fonts",
    "i’m gonna go die in a hole",
    "i hate ur inernet too",
    "Agent you should consider writing down your password",
    "Hey (with massive rizz)",
    "Hey, atleast y'all don't hate eachother",
    "you need assistance with smth bash?",
    "Did agent die more than i did?",

    
"i was looking youtube short",
    "GO GO",
    "ur gonna kill ur horse lol",
    "ME VERI GAY",
    "is Blox saying he's Gay?",
    "Bro im literally bored as fuck man.",
    "Rassx did you kick me from ur server?",
    """Dont ... kill
the google child""",
    "im going to kill a child",
    "i killed a child",

    "you are now fiery fingers",
    "Does any bot auto assign roles aside from wick @[Owner] Harry",
    "cuz i somehow dies when server was oddline",
    "shit i got banned off of that server tho",
    "he should’ve read them before being a dumbass",
    '"oh! got your bitches! notice how there\'s nothing in my hand? you lonely fuck." -some random tiktok i just watchedc',
    
    "that's dumb, what if you ran out of tea",
    """# Pretty Important Stuff Right Here #

I made a discord server so all the staff members in the network can actually communicate, share ideas, and move towards collective success! Come join here (It will be required just an FYI)

https://discord.gg/JuhKgfHsYB""",
    "@VixotheAxo_, You do realize makeup isn't going to fix your stupidity?",
    "@McGoose, If you're gonna be a smartass, first you have to be smart. Otherwise you're just an ass.",
    "@Joshboss09, I'd like to see things from your point of view but I can't seem to get my head that far up my ass.",
    "@L3mm0nZ, Some drink from the fountain of knowledge; you only gargled.",
    "@Joshboss09, If you are going to be two faced, at least make one of them pretty.",
    "@Azza Mazza Bazza, Two wrongs don't make a right, take your parents as an example.",
    "I'd laugh my ass off ngl",
    "Shut up, Waca Guard, you're not relevant.",
    "now my fingers are broken",
    "BIT GET YOUR ASS IN HERE",
    "Stupid ass neon",
    "What if a straight kid was approached by a gay one and the gay person made sexual statements towards the other person",
    "HAHA EAT SHIT /j",
    "Man yall didn't have to spend your time just to prove all this shit",
    "What the fuck you smoking lmao",
    "thats usually what an 8 year old furry hater says when they see a furry, and they go on to ramble about how much they hate furries.",
    "@Fuck you @CombinatioNova @Chåractèr🎗",

    "this bot can go fuck itself",
    "right mate it’s 4am in the morning and your moderating a discord server that’s sad on multiple levels",
    "(virgin)",
    "mate your a virgin",
    "he’s read the rules by assumption",
    "Shut up stupid bot",
    "who tf want to raid this small ass server",
    "this bots crap",
    "Fatimadeshar this server is an anarchy server so you can pretty much do anything exept hacking (u can still use Xray) if u didn't know",
    "stfu 9 year old",
    "dick means fat in german",
    "He's a fucking dick lmao",
    "Everything is somebody else’s fault, nothing is ever your fault. Your a cunt to everybody you have ever met",
    "Nobody’s touching this bitch",
    "i hate todays english",
    "@Harry Did you ban someone because they were annoying?!?!",
    "he's gonna be more mad when he finds out you LIED",
    "Good news: The suggestions database didn't fuck up",
    "FUCK YOU BOYO",

    "YOU WORTHLESS PILE OF MEANINGLESS VALUES.",
    "Fuck you",
    "I'll feel fat",
    "My food teacher is a bitch",
    "Dumbass",
    "I bet waca guard has like a 0.1% chance to just go FUCKING SHUT UP",
    "Bitch have they seen Adam",
    "@VixotheAxo_ Could you roll back my stuff. i died after server crash",
    'Oh yeah wick is like car insurance, it\'s super annoying until you actually need it and if you dont have it you just sorta go "well, fuck"',
    "you your going to fuck around, your going to find out",
    "Did Nova shorten his name-",
    "I hate vocabulary words",
    "Fatimadeshar this server is an anarchy server so you can pretty much do anything exept hacking (u can still use Xray) if u didn't know",
    
    
    
    ])
y = np.array(
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
 1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0
 ])

MEAN_WORDS = ["slag","whore","short","slut","ugly","willy","schlong","dong","fanny","suicide","pussy","penis","stfu","dicks","annoying","fing","shit","fuck ","slit","gay","twat",
              "shits","fucking","retard","retarded","rape","raped","abuse","kill","arse","kys","fat","hate", "dislike", "angry", "mad", "furious",
              "enraged", "fuck you", "screw you", "jerk", "asshole", "bastard", "son of a bitch", "bitch", "cunt", "dick", "dumb", "loser", "moron",
              "stupid", "die","dummy", "jerk", "foolish", "shut","stupid", "suck", "sucks", "worst", "useless","ass","worthless","fxing","fxck","asshat","mother","mom","dad","father",
              "go to hell","burn in hell","suck my",]

iris = load_iris()

#vectorizing dataset
vectorizer = CountVectorizer()

#instantiate SVM classifier

param_grid = {'C': [0.001, 0.1,0.2,11,13,14,15], 'gamma': [0.14,0.12,0.16,0.17]}
classifier = GridSearchCV(SVC(), param_grid, n_jobs = -1)

polyGrid ={
    'C': [0.1,0.02,0.01,0.04],
    'kernel': ['poly'],
    'degree': [2,4],
    'coef0': [0, 1, 10,15]}


optionPoly = GridSearchCV(SVC(), polyGrid, n_jobs = -1)

# Train the classifier
X_train = vectorizer.fit_transform(X)

# Use the SVM classifier to train the model
classifier.fit(X_train, y)


# Perform k-fold cross validation
scores = cross_val_score(classifier, X_train, y, cv=5)
print("Accuracy of rbf: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

polyScore= cross_val_score(optionPoly, X_train, y, cv=5)
print("Accuracy of poly: %0.2f (+/- %0.2f)" % (polyScore.mean(), polyScore.std() * 2))
optionPoly.fit(X_train, y)
accuracy = "%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
accuracyPoly="%0.2f (+/- %0.2f)" % (polyScore.mean(), polyScore.std() * 2)


async def preprocess_text(self, text):
    normalized = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in normalized if not unicodedata.combining(c))
    text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"[@]+", "a", text)
    text = re.sub(r"[1]+", "i", text)
    text = re.sub(r"[3]+", "e", text)
    
    return text
class MDS(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    
    @Cog.listener()
    async def on_ready(self):
        bot = self.bot
        end_time = datetime.now()
        delta = end_time - start_time
        print(f"Bot took {delta.total_seconds()} seconds to start.")
        channel = bot.get_channel(1062470547327426682)
        embed = disnake.Embed(title='Bot Restarted', description=f"""

    **RBF:{accuracy}.**

    Best Parameters: {classifier.best_params_}

    Best Estimators: {classifier.best_estimator_}

    **Linear REMOVED FOR SPEED**


    **Polynomial:{accuracyPoly}**

    Best Parameters: {optionPoly.best_params_}

    Best Estimators: {optionPoly.best_estimator_}

    **Points of Data: {len(y)}**

    """, color=0x00ff00,timestamp=datetime.now())
        embed.set_footer(text=f"Bot ready in {delta.total_seconds()} seconds")
        print (accuracy)
        print("Best parameters found: ",classifier.best_params_)
        print("Best estimator found: ",classifier.best_estimator_)
        #await channel.send(embed=embed)

    

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        with open("users.txt", "r") as file:
                # Read the contents of the file
                try:
                    users = json.loads(file.read())
                except json.decoder.JSONDecodeError:
                    users = []

            # Check if the user ID is already in the list
        if message.author.id not in users:
            user = message.author
            # Apply pre-processing to the message
            message_content = await preprocess_text(self,message.content)
            if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
            # Classify the message as NSFW or safe
                X2_test = vectorizer.transform([message_content])
                prediction = classifier.predict(X2_test)[0]
                polyPrediction = optionPoly.predict(X2_test)[0]
                print(message_content + " FLAGGED IN MEAN WORDS")
                print(f"RBF {prediction}")
                print(f"POLY {polyPrediction}")
                if polyPrediction == 1 or prediction == 1:
                    # Create the embed message
                    titles = ['Make sure you\'re being nice!',"Are you being a meanie bo beanie?", "Careful! Follow the rules!", "Let's take a breather", "Make sure you're kind to everyone!", "Peace and Love Only"]
                    randTitle = random.choice(titles)
                    
                    embed = disnake.Embed(title=randTitle, description='This message was flagged as a potentially mean message. Please make sure to be kind to other players!', color=0xff0000, timestamp=datetime.now())
                    
                    log = disnake.Embed(title=f"Message Flagged in {message.channel}!", description=f"A message was flagged for being potentially mean! \n\n [Go To Message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})",color=0x00ff00)

                
                    if polyPrediction == 1 and prediction == 1:
                        
                        embed.set_footer(text="Polynomial and RBF Flag")
                        
                        log.set_footer(text="Polynomial and RBF Flag")
                        log.add_field(name="User",value=message.author,inline=True)
                        log.add_field(name="Message",value=message.content,inline=True)
                        channel = disnake.utils.get(user.guild.channels, name = "📂reports")
                        await channel.send(embed=log)
                    elif polyPrediction == 1:
                        embed.set_footer(text="Polynomial Flag")
                        log.set_footer(text="Polynomial Flag")
                        log.add_field(name="User",value=message.author,inline=True)
                        log.add_field(name="Message",value=message.content,inline=True)
                        channel = disnake.utils.get(user.guild.channels, name = "📂reports")
                        await channel.send(embed=log)
                    elif prediction == 1:
                        embed.set_footer(text="RBF Flag")
                        log.add_field(name="User",value=message.author,inline=True)
                        log.set_footer(text="RBF Flag")
                        log.add_field(name="Message",value=message.content,inline=True)
                        channel = disnake.utils.get(user.guild.channels, name = "📂reports")
                        await channel.send(embed=log)
        ##              
                    # Send the embed message
                    await message.reply(embed=embed)
        else:
            message_content = await preprocess_text(self,message.content)
            if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
            # Classify the message as NSFW or safe
                X2_test = vectorizer.transform([message_content])
                prediction = classifier.predict(X2_test)[0]
                polyPrediction = optionPoly.predict(X2_test)[0]
                print(message_content + " FLAGGED IN MEAN WORDS")
                print(f"RBF {prediction}")
                print(f"POLY {polyPrediction}")
                if polyPrediction == 1 or prediction == 1:
                    # Create the embed message
                    embed = disnake.Embed(title='OwO what\'s this??? Make suwe you\'we being nice!', description='This message was fwagged as a potentiaw viowation of Wule 1: "Show othew pwayews wespect." Make sure you\'we being kind to aww pwayews! ÒwÓ', color=0xff0000, timestamp=datetime.now())
                   
                    if polyPrediction == 1 and prediction == 1:
                        embed.set_footer(text="Powynomial and AwBF Fwag")
                        log = disnake.Embed(title=f"Message Flagged in {message.channel}!", description=f"A message was flagged for potentially violating Rule 1! \n\n [Go To Message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})",color=0xffa500)
                        log.add_field(name="User",value=message.author,inline=True)
                        log.add_field(name="Message",value=message.content,inline=True)
                        channel = disnake.utils.get(user.guild.channels, name = "📂reports")
                        await channel.send(embed=log)
                    elif polyPrediction == 1:
                        embed.set_footer(text="Powynomial Fwag")
                        log = disnake.Embed(title=f"Message Flagged in {message.channel}!", description=f"A message was flagged for potentially violating Rule 1! \n\n [Go To Message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", color=0xff0000)
                        log.add_field(name="User",value=message.author,inline=True)
                        log.add_field(name="Message",value=message.content,inline=True)
                        channel = disnake.utils.get(user.guild.channels, name = "📂reports")
                        await channel.send(embed=log)
                    elif prediction == 1:
                        embed.set_footer(text="AwBF Fwag")
                        log = disnake.Embed(title=f"Message Flagged in {message.channel}!", description=f"A message was flagged for potentially violating Rule 1! \n\n [Go To Message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", color=0xff0000)
                        log.add_field(name="User",value=message.author,inline=True)
                        log.add_field(name="Message",value=message.content,inline=True)
                        channel = disnake.utils.get(user.guild.channels, name = "📂reports")
                        await channel.send(embed=log)
        ##              
                    # Send the embed message
                    await message.reply(embed=embed)
                    
    @slash_command(name="analyze",description="Tells you how many messages have been mean")
    async def meaninfo(self,inter,messages: int = 2000,agreement: str = Param(choices=["Radial Basis Function","Polynomial","RBF and Poly","Unanimous","Broad"])):
        numFlags = 0
        numCrudeFlags = 0
        await inter.response.defer(with_message = True,ephemeral=False)
         # Collect the last 15000 messages sent by the user
        msg = []
        if agreement == "Unanimous":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    numCrudeFlags +=1
                    X2_test = vectorizer.transform([message_content])
                    prediction = classifier.predict(X2_test)[0]
                    polyPrediction = optionPoly.predict(X2_test)[0]
                    linPrediction = optionLinear.predict(X2_test)[0]
                    print(f"RBF {prediction}")
                    print(f"LINEAR {linPrediction}")
                    print(f"POLY {polyPrediction}")
                    if polyPrediction == 1 and linPrediction == 1 and prediction == 1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        elif agreement == "Broad":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    numCrudeFlags +=1
                    X2_test = vectorizer.transform([message_content])
                    prediction = classifier.predict(X2_test)[0]
                    polyPrediction = optionPoly.predict(X2_test)[0]
                    linPrediction = optionLinear.predict(X2_test)[0]
                    print(f"RBF {prediction}")
                    print(f"LINEAR {linPrediction}")
                    print(f"POLY {polyPrediction}")
                    if polyPrediction == 1 or linPrediction == 1 or prediction == 1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        elif agreement == "Radial Basis Function":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    numCrudeFlags +=1
                    X2_test = vectorizer.transform([message_content])
                    prediction = classifier.predict(X2_test)[0]
                    print(f"RBF {prediction}")
                    if prediction == 1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        elif agreement == "Polynomial":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    numCrudeFlags +=1
                    X2_test = vectorizer.transform([message_content])
                    polyPrediction = optionPoly.predict(X2_test)[0]
                    print(f"POLY {polyPrediction}")
                    if polyPrediction == 1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        elif agreement == "Linear":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    numCrudeFlags +=1
                    X2_test = vectorizer.transform([message_content])
                    linPrediction = optionLinear.predict(X2_test)[0]
                    print(f"LINEAR {linPrediction}")
                    if linPrediction == 1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        elif agreement == "Linear and Poly":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    X2_test = vectorizer.transform([message_content])
                    
                    polyPrediction = optionPoly.predict(X2_test)[0]
                    linPrediction = optionLinear.predict(X2_test)[0]
                    print(f"LINEAR {linPrediction}")
                    print(f"POLY {polyPrediction}")
                    if linPrediction == 1 and polyPrediction ==1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        elif agreement == "RBF and Poly":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    numCrudeFlags +=1
                    X2_test = vectorizer.transform([message_content])
                    
                    polyPrediction = optionPoly.predict(X2_test)[0]
                    prediction = classifier.predict(X2_test)[0]
                    print(f"RBF {prediction}")
                    print(f"POLY {polyPrediction}")
                    if prediction == 1 and polyPrediction ==1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        elif agreement == "RBF and Linear":
            async for message in inter.channel.history(limit=messages): #,before = datetime(2022, 5, 20)
                message_content = await preprocess_text(self,message.content)
                if any(word in message_content.lower() for word in MEAN_WORDS) or any(fuzz.token_set_ratio(word, message_content) > 80 for word in MEAN_WORDS) or bool(re.search(r'\b(' + '|'.join(MEAN_WORDS) + r')\b', message_content.lower())):
                # Classify the message as NSFW or safe
                    numCrudeFlags +=1
                    X2_test = vectorizer.transform([message_content])
                    
                    
                    prediction = classifier.predict(X2_test)[0]
                    linPrediction = optionLinear.predict(X2_test)[0]
                    print(f"RBF {prediction}")
                    print(f"LINEAR {linPrediction}")
                    if linPrediction == 1 and prediction ==1:
                        numFlags += 1
                    print(f"Found {numFlags}!")
        



        
        embed = disnake.Embed(title=f"Analysis of {inter.channel.name}:", description=f"""
    The following is a breakdown of the {inter.channel.name} channel using the {agreement} algorithm(s)
    """, timestamp = datetime.now())
        embed.add_field(name = "Messages Scanned", value = messages, inline = True)
        embed.add_field(name = "Messages Analyzed", value = numCrudeFlags, inline = True)
        embed.add_field(name = "Messages Marked as \"Mean\"", value = numFlags, inline = True)
        embed.set_footer(text=f"Messages scanned using a(n) {agreement} approach")
        await inter.edit_original_response(embed=embed)
    
def setup(bot: Bot) -> None:
    bot.add_cog(MDS(bot))
