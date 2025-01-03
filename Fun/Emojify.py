import disnake
from disnake.ext import commands

class EmojifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='emojify',
        description='Emojifies the given text',
        
    )
    async def emojify(self, inter: disnake.ApplicationCommandInteraction, text: str):
        """
        Emojifies the given text
        """
        emoji_mapping = {
        'a': ':regional_indicator_a:',
        'b': ':regional_indicator_b:',
        'c': ':regional_indicator_c:',
        'd': ':regional_indicator_d:',
        'e': ':regional_indicator_e:',
        'f': ':regional_indicator_f:',
        'g': ':regional_indicator_g:',
        'h': ':regional_indicator_h:',
        'i': ':regional_indicator_i:',
        'j': ':regional_indicator_j:',
        'k': ':regional_indicator_k:',
        'l': ':regional_indicator_l:',
        'm': ':regional_indicator_m:',
        'n': ':regional_indicator_n:',
        'o': ':regional_indicator_o:',
        'p': ':regional_indicator_p:',
        'q': ':regional_indicator_q:',
        'r': ':regional_indicator_r:',
        's': ':regional_indicator_s:',
        't': ':regional_indicator_t:',
        'u': ':regional_indicator_u:',
        'v': ':regional_indicator_v:',
        'w': ':regional_indicator_w:',
        'x': ':regional_indicator_x:',
        'y': ':regional_indicator_y:',
        'z': ':regional_indicator_z:',
        '0': ':zero:',
        '1': ':one:',
        '2': ':two:',
        '3': ':three:',
        '4': ':four:',
        '5': ':five:',
        '6': ':six:',
        '7': ':seven:',
        '8': ':eight:',
        '9': ':nine:',
        '!': ':exclamation:',
        '?': ':question:',
        '#': ':hash:',
        '*': ':asterisk:'
    }

        emojified_text = ''.join(emoji_mapping.get(c.lower(), c) for c in text)
        await inter.response.send_message(emojified_text)

def setup(bot):
    bot.add_cog(EmojifyCog(bot))
