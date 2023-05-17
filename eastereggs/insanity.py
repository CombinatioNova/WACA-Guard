import time
from disnake.ext.commands import Bot, Cog, slash_command
import disnake
import json

last_message_time = {}
previous_message = ""

class EasterEggs(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    @Cog.listener()
    async def on_message(self, message):
        global previous_message
        # Check if the message was sent in the correct channel
        if message.author.id == self.bot.user:
            return
        if message.author == self.bot.user:
            return
        
        elif message.channel.id == 1006509526150828052 and message.author.id != 1032680296396636191:
            # Check if the user has said "playerlist" 5 times in 5 minutes
            if message.content == "playerlist":
                current_time = time.time()
                if message.author.id in last_message_time:
                    last_time = last_message_time[message.author.id]
                    if current_time - last_time < 300:
                           # Send the message
                            embed = disnake.Embed(title = "What are you doing, like actually?", description='A quote for you, you might need it: \n\n "Insanity is doing the same thing over and over and expecting different results" - Albert Einstein', color = 0xffffff)
                            await message.reply(embed=embed)
                    else:
                        last_message_time[message.author.id] = current_time
            

            
            
                # Check if the current message is "playerlist" and the previous message was also "playerlist"
                if previous_message.lower() == "playerlist":
                    print("Registered a dumbass")
                    embed = disnake.Embed(title="What are you doing?", description='What **possibly** could have changed from then to now? Not tryna criticize but... dang...',color=disnake.Color.brand_red())
                    await message.channel.send(embed=embed)
                    previous_message = ""
                    print("Sent message!")
                    last_message_time[message.author.id] = current_time
                else:
                    current_time = time.time()
                    last_message_time[message.author.id] = current_time
            
            previous_message = message.content
def setup(bot: Bot) -> None:
    bot.add_cog(EasterEggs(bot))
