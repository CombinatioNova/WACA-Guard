from disnake.ext.commands import Bot, Cog, slash_command
import disnake
Choices = ["And it came to pass that a man was troubled by a peanut butter sandwich, for it had been placed within his VCR, and he knew not how to remove it. And he cried out to the Lord, saying, \"Oh, Lord, how can I remove this sandwich from my VCR, for it is stuck fast and will not budge?\" And the Lord spoke unto him, saying, \"Fear not, my child, for I shall guide thy hand and show thee the way. Take thy butter knife, and carefully insert it between the sandwich and he VCR, and gently pry them apart. And with patience and perseverance, the sandwict shall be removed, and thy VCR shall be saved.\" And the man did as the Lord commanded, and lo and behold, the sandwich was removed from the VCR, and the man was saved Ind the Lord said, \"Verily I say unto thee, seek not to put thy peanut butter sandwiches in thy VCR, for it is not a suitable place for such things. Rather, keep thy sandwiches in thy refrigerator or on thy plate, where they belong. And the man heeded the Lord's words, and from that day forth, he kept his sandwiches in their proper place, and was saved from trouble and woe. Amen","""
And Saint Attila raised the hand grenade up on high, saying, "O Lord, bless this thy hand grenade, that with it thou mayst blow thine enemies to tiny bits, in thy mercy." And the Lord did grin. And the people did feast upon the lambs and sloths, and carp and anchovies, and orangutans and breakfast cereals, and fruit-bats and large chu...

And the Lord spake, saying, "First shalt thou take out the Holy Pin. Then shalt thou count to three, no more, no less. Three shall be the number thou shalt count, and the number of the counting shall be three. Four shalt thou not count, neither count thou two, excepting that thou then proceed to three. Five is right out. Once the number three, being the third number, be reached, then lobbest thou thy Holy Hand Grenade of Antioch towards thy foe, who, being naughty in my sight, shall snuff it.

Thanks be to God
"""]
class Bless(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        IED = ["improvised explosive device"]
        if message.content.lower() == "achoo" or message.content.lower().startswith("achoo"):
            await message.reply(
    
'''God, our father, our one and only divine being that has made us men stand up and walk freely, shall bless your name in the name of the father, the son, and the Holy Spirit, amen. We humbly request your overflowing blessings upon our lives. We also take this opportunity to thank you for those blessings you have bestowed upon us that we take for granted and the numerous ones on the way. Bless us with love, joy, peace and happiness. Bless us spiritually, financially and also with good health. Keep us safe, Oh loving Lord. Those among us who lack wisdom, bless with knowledge. Those who are weak, bless with strength. Shower with energy those who are weary. Those who are blind, bless with sight. And those who are burdened, set completely free. Shower these blessings on our family and friends, as well. Help us all to remember that we are blessed to be a blessing to others. Help us to help others even when we’re struggling with our own difficulties. Lord, you know the desires of our hearts and you also know what we deserve. Bless us, with what you know is truly best for us. Thank you for all you have done for us and we declare that your overflowing blessings will rain down upon us, today.

Also, while you are being blessed for your sneeze, y’all mind if I turn up to some Christian bars? 🤭🤭🤭''')

            await message.channel.send('''ɴᴏᴡ ᴘʟᴀʏɪɴɢ: How Great Is Our God by Chris Tomlin ───────────────⚪─────────────────── ◄◄⠀▐▐ ⠀►►⠀⠀ ⠀ 1:17 / 3:48 ⠀ ───○ 🔊⠀ ᴴᴰ ⚙ ❐ ⊏⊐

The splendor of a King, clothed in majesty Let all the Earth rejoice All the Earth rejoice He wraps himself in light And darkness tries to hide And trembles at His voice Trembles at His voice How great is our God, sing with me How great is our God, and all will see How great, how great is our God Age to age He stands And time is in His hands Beginning and the end The Godhead Three in One Father Spirit Son The Lion and the Lamb The Lion and the Lamb How great is our God, sing with me How great is our God, and all will see How great, how great is our God Name above all names Worthy of our praise My heart will sing How great is our God You're the name above all names You are worthy of our praise And my heart will sing How great is our God How great is our God, sing with me How great is our God, and all will see How great, how great is our God How great is our God, sing with me How great is our God, and all will see How great, how great is our God The whole world sings, the whole world sings How great is our God How great is our God How great, how great is our God

Damn, that was some Jesus heat forreal forreal 💃💃🕺🕺👯‍♀️👯‍♂️👯‍♀️👯‍♂️🤟🤜🏻👉🤝👍🤛🏿🤘👹🤮😳😳😧😫😩😩😩✌️✌️🔥🔥🔥🔥🔥🔥🤭🤭🤭👍👌🔥🔥''')
        elif any(word in message.content.lower() for word in IED):
            await message.reply("""I'm sorry Your Honour but to call my client's pipebomb an "Improvised Explosive Device" is a personal insult to both him and his entire legal team, i assure you, and so does the rest of the lawyer team, that our client planned out the device in such a manner that it could not be missfired and will work under most unusual circumstances, not only is it safe from not working under "normal" conditions it can, and will work under extreme conditions, in extreme heat up to 675.4°C, under water, and under pressure up to three atmospheres, it was meticulously crafted down to perfection in each and every step from the most fine, carefully selected, tested, and then refined materials, my client refuses to acknowledge and or to comply with the Court at both small and large unless you, the staff of the court, and the jury, all acknowledge the mastery of my client and the value of the masterpiece he had created thoughout his 10 years of work, retract such a statement, and apologize to him personally.""")

            
def setup(bot: Bot) -> None:
    bot.add_cog(Bless(bot))
