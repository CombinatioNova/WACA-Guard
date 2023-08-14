import disnake
from disnake.ext import commands
import sqlite3
import random

conn = sqlite3.connect('8ball.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                    question TEXT PRIMARY KEY,
                    answer TEXT)''')
conn.commit()
class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="8ball",
        description="Ask the magic 8 ball a question",
        options=[
            disnake.Option(
                name="question",
                description="Ask a question",
                required=True
            )
        ]
    )
    async def eightball(self, inter, question: str):
        cursor.execute("SELECT answer FROM questions WHERE question=?", (question,))
        result = cursor.fetchone()

        if result:
            embed = disnake.Embed(title=f'{inter.author.display_name.capitalize()} asked: {question}', description=f'{inter.author.mention}, you have already asked that question. You should know the answer is: {result[0]}', color=disnake.Color.blue())
            embed.set_footer( # Show the moderator
                text=f"Department of Celestial Readings and Prediction"
            )
            await inter.response.send_message(embed=embed)
        else:
            answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
            answer = random.choice(answers)

            cursor.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (question, answer))
            conn.commit()

            embed = disnake.Embed(title=f'{inter.author.display_name.capitalize()} asked: {question}', description=answer, color=disnake.Color.blue())
            embed.set_footer( # Show the moderator
                text=f"Department of Celestial Readings and Prediction"
            )
            await inter.response.send_message(embed=embed)
