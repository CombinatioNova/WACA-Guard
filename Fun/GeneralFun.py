import disnake
from disnake.ext import commands
import requests
import random

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='joke',
        description='Get a random joke'
    )
    async def random_joke(self, inter: disnake.ApplicationCommandInteraction):
        """
        Get a random joke
        """
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        if response.status_code == 200:
            joke_data = response.json()
            setup = joke_data['setup']
            punchline = joke_data['punchline']
            joke = f"{setup}\n\n{punchline}"
            await inter.response.send_message(joke)
        else:
            await inter.response.send_message("Oops! Failed to fetch a joke.")

    @commands.slash_command(
        name='cat',
        description='Get a random cat image'
    )
    async def random_cat(self, inter: disnake.ApplicationCommandInteraction):
        """
        Get a random cat image
        """
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            cat_data = response.json()
            cat_url = cat_data[0]['url']

            uplifting_phrases = [
    "Believe in yourself and all that you are.",
    "You are capable of amazing things.",
    "Every day is a fresh start.",
    "You are loved and appreciated.",
    "Stay positive and good things will happen.",
    "Your dreams are within reach.",
    "You have the power to make a difference.",
    "Challenges help you grow and become stronger.",
    "Your hard work will pay off.",
    "Embrace the possibilities that each day brings.",
    "You are worthy of happiness and success.",
    "Trust the journey and enjoy the ride.",
    "You are stronger than you think.",
    "Choose joy and let it radiate from within.",
    "Keep going, you're making progress.",
    "You have the strength to overcome any obstacle.",
    "Believe in the power of your dreams.",
    "Your positive attitude can change everything.",
    "You are a unique and valuable individual.",
    "Happiness is a choice, so choose it every day.",
    "You are braver than you believe, stronger than you seem, and smarter than you think.",
    "Success comes to those who never give up.",
    "You have the ability to create the life you want.",
    "You are surrounded by love and support.",
    "Your potential is limitless.",
    "You are deserving of all the good things life has to offer.",
    "Every setback is a setup for a comeback.",
    "You have the power to overcome any challenge.",
    "You are an inspiration to others.",
    "The best is yet to come.",
    "You are capable of handling anything that comes your way.",
    "Your positive energy is contagious and uplifting to those around you.",
    "You have the courage to follow your heart and intuition.",
    "You are making a difference in the world.",
    "The universe is working in your favor.",
    "You are filled with endless possibilities.",
    "You are worthy of love, happiness, and abundance.",
    "You are resilient and can bounce back from any setback.",
    "Your dreams are worth pursuing.",
    "You are exactly where you need to be right now.",
    "You are a magnet for success and positivity.",
    "Your journey is unique and beautiful.",
    "You are surrounded by infinite opportunities for growth and success.",
    "Your optimism and enthusiasm are contagious.",
    "You have the power to create positive change in your life and the lives of others.",
    "You have the strength to overcome any adversity.",
    "You are deserving of all the love and joy in the world.",
    "Your potential is limitless, and your possibilities are endless.",
    "You are capable of achieving greatness."
]
            random_message = random.choice(uplifting_phrases)
            embed = disnake.Embed(title=random_message, color = disnake.Color.green())
            embed.set_author( # Narcissism
                name="Emotional Protection",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
            )
            embed.set_image(url=cat_url)
        
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("Oops! Failed to fetch a cat image.")

    @commands.slash_command(
        name='dog',
        description='Get a random dog image'
    )
    async def random_dog(self, inter: disnake.ApplicationCommandInteraction):
        """
        Get a random dog image
        """
        response = requests.get('https://random.dog/woof.json')
        if response.status_code == 200:
            dog_data = response.json()
            dog_url = dog_data['url']
            uplifting_phrases = [
    "Believe in yourself and all that you are.",
    "You are capable of amazing things.",
    "Every day is a fresh start.",
    "You are loved and appreciated.",
    "Stay positive and good things will happen.",
    "Your dreams are within reach.",
    "You have the power to make a difference.",
    "Challenges help you grow and become stronger.",
    "Your hard work will pay off.",
    "Embrace the possibilities that each day brings.",
    "You are worthy of happiness and success.",
    "Trust the journey and enjoy the ride.",
    "You are stronger than you think.",
    "Choose joy and let it radiate from within.",
    "Keep going, you're making progress.",
    "You have the strength to overcome any obstacle.",
    "Believe in the power of your dreams.",
    "Your positive attitude can change everything.",
    "You are a unique and valuable individual.",
    "Happiness is a choice, so choose it every day.",
    "You are braver than you believe, stronger than you seem, and smarter than you think.",
    "Success comes to those who never give up.",
    "You have the ability to create the life you want.",
    "You are surrounded by love and support.",
    "Your potential is limitless.",
    "You are deserving of all the good things life has to offer.",
    "Every setback is a setup for a comeback.",
    "You have the power to overcome any challenge.",
    "You are an inspiration to others.",
    "The best is yet to come.",
    "You are capable of handling anything that comes your way.",
    "Your positive energy is contagious and uplifting to those around you.",
    "You have the courage to follow your heart and intuition.",
    "You are making a difference in the world.",
    "The universe is working in your favor.",
    "You are filled with endless possibilities.",
    "You are worthy of love, happiness, and abundance.",
    "You are resilient and can bounce back from any setback.",
    "Your dreams are worth pursuing.",
    "You are exactly where you need to be right now.",
    "You are a magnet for success and positivity.",
    "Your journey is unique and beautiful.",
    "You are surrounded by infinite opportunities for growth and success.",
    "Your optimism and enthusiasm are contagious.",
    "You have the power to create positive change in your life and the lives of others.",
    "You have the strength to overcome any adversity.",
    "You are deserving of all the love and joy in the world.",
    "Your potential is limitless, and your possibilities are endless.",
    "You are capable of achieving greatness."
]
            
            random_message = random.choice(uplifting_phrases)
            embed = disnake.Embed(title=random_message, color = disnake.Color.green())
            embed.set_author( # Narcissism
                name="Emotional Protection",
                icon_url="https://cdn.discordapp.com/attachments/1003324050950586488/1036996275985453067/Protection_Color.png",
            )
            embed.set_image(url=dog_url)
        
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("Oops! Failed to fetch a dog image.")

    

    @commands.slash_command(
        name='rps',
        description='Play Rock-Paper-Scissors',
        options=[
            disnake.Option(
                name='choice',
                description='Your choice (rock, paper, or scissors)',
                type=disnake.OptionType.string,
                required=True,
                choices=[
                    disnake.OptionChoice(name='Rock', value='rock'),
                    disnake.OptionChoice(name='Paper', value='paper'),
                    disnake.OptionChoice(name='Scissors', value='scissors')
                ]
            )
        ]
    )
    async def rock_paper_scissors(self, inter: disnake.ApplicationCommandInteraction, choice: str):
        """
        Play Rock-Paper-Scissors
        """
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)

        result = ""
        if choice == bot_choice:
            result = "It's a tie!"
        elif (
            (choice == 'rock' and bot_choice == 'scissors') or
            (choice == 'paper' and bot_choice == 'rock') or
            (choice == 'scissors' and bot_choice == 'paper')
        ):
            result = "You win!"
        else:
            result = "You lose!"

            
        if result == "You win!":
            embed = disnake.Embed(title=result, color = disnake.Color.green())
            
        elif result == "You lose!":
            embed = disnake.Embed(title=result, color = disnake.Color.red())
            
        else:
            embed = disnake.Embed(title=result, color = disnake.Color.blue())
            
        embed.set_author( # Narcissism
            name="Rock, Paper, Scissors"
        )
        embed.description=f"""
**Your choice:** {choice}

**My choice:** {bot_choice}
"""
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(FunCog(bot))
