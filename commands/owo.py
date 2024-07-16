
from disnake.ext.commands import Bot, Cog, slash_command
import disnake
import json
import re

class OWO(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    owoPlayers = []
    @slash_command(description="Fuck you.") #The actual command
    async def owoify(self,inter, text: str):
        
        
        replacements = {
            "ove": "uv",
            "oing": "owing",
            "you": "yow",
            "the": "da",
            "this": "dis",
            "that": "dat",
            "with": "wif",
            "have": "hav",
            "has": "haz",
            "is": "iz",
            "was": "waz",
            "were": "werez",
            "hello": "hewwo",
            "hi": "hai",
            "hey": "hewwo",
            "good": "gud",
            "night": "nite",
            "okay": "okie",
            "please": "pwease",
            "stop": "stawp",
            "sorry": "sowwy",
            "no": "nu",
            "yes": "yus",
            "love": "wuv"
        }

        owoified_text = text
        for key, value in replacements.items():
            owoified_text = re.sub(re.compile(re.escape(key), re.IGNORECASE), lambda match: value.capitalize() if match.group().istitle() else value, owoified_text)
        owoified_text = owoified_text.replace("r", "w").replace("l", "w")
        owoified_text = owoified_text.replace("R", "W").replace("L", "W")
        
        owoified_text = re.sub(r"([a-zA-Z])s\b", r"\1z", owoified_text)
        owoified_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", owoified_text)
        owoified_text = re.sub(r"N([AEIOU])", r"NY\1", owoified_text)
        
        # Add OwO, UwU, or ÒwÓ randomly to the end of the message
        import random
        suffixes = [" OwO", " UwU", " ÒwÓ"]
        owoified_text += random.choice(suffixes)
        
        await inter.response.send_message(owoified_text)
    
    @slash_command(description="Why did I make this.") #The actual command
    async def owoall(self, inter, everything: bool = False):
        if everything == False:
            # Open the text file
            
            with open("users.txt", "r") as file:
                # Read the contents of the file
                try:
                    users = json.loads(file.read())
                except json.decoder.JSONDecodeError:
                    users = []

            # Check if the user ID is already in the list
            if inter.author.id not in users:
                print("User ID not in the list.")
                
                await inter.send("Done!", ephemeral = True)
            else:
                # Remove the user ID from the list
                users.remove(inter.author.id)
                # Open the text file for writing
                with open("users.txt", "w") as file:
                    # Write the updated list to the file
                    file.write(json.dumps(users))
                    
                await inter.send("Done!", ephemeral = True)

        else:
                        # Open the text file
            with open("users.txt", "r") as file:
                # Read the contents of the file
                try:
                    users = json.loads(file.read())
                except json.decoder.JSONDecodeError:
                    users = []

            # Check if the user ID is already in the list
            if inter.author.id in users:
                print("User ID already exists.")
                
                await inter.send("Done!", ephemeral = True)
            else:
                # Append the new user ID to the list
                users.append(inter.author.id)
                # Open the text file for writing
                with open("users.txt", "w") as file:
                    # Write the updated list to the file
                    file.write(json.dumps(users))
                await inter.send("Done!", ephemeral = True)
