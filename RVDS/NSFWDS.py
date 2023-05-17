import disnake
import datetime
import fuzzywuzzy
import logging
import aiofiles
import aiohttp

import numpy as np

from disnake.ext.commands import Bot, Cog,Param
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

verNum = "0.1"
testMode=True
start_time = datetime.now()
logging.getLogger().setLevel(logging.ERROR)
[
    "I love sex",
    "Sex is so fucking hot",
    "The best sex I've ever had was in the back of a car",
    "I want you to suck my balls",
    "Fuck me baby",
    "I love fucking you",
    "I fucking love you",
    "Balls",
    "I love balls!",
    "I love cock",
    "I love dick",
    "I like cock",
    "I like balls",
    "You're such a fucking dick",
    "You're a fucking cock",
    "Suck my fucking balls bitch",
    "Suck my balls idiot",
    "Fuck you",
    "Suck me off bitch",
    "The best sexual experience I've ever had was in the back of a minivan",
    "I love some good sex",]

class __init__(self, bot: Bot):
    self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        
