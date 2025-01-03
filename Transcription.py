import discord
import disnake
from disnake import ApplicationCommandInteraction, Option
from disnake.ext import commands
import asyncio
import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    transcribed_text = ""
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            transcribed_text = recognizer.recognize_google(audio)
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
    return transcribed_text

class TranscriptionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="transcribe", description="Transcribe voice chat.")
    async def transcribe_command(
        self,
        interaction: ApplicationCommandInteraction,
        action: str = Option("start", "Start or stop the transcription process."),
    ):
        voice_channel = interaction.author.voice.channel
        if action == "start":
            vc = await voice_channel.connect(cls=discord.VoiceClient)
            vc.pause()

            def save_audio(data):
                with open("audio.pcm", "wb") as file:
                    file.write(data)

            vc.listen(save_audio)
            vc.resume()
            await interaction.response.send_message(f"Started recording in {voice_channel.name}.")
        elif action == "stop":
            if voice_channel.guild.voice_client is None:
                await interaction.response.send_message("No active recording found.")
            else:
                voice_channel.guild.voice_client.stop()
                await voice_channel.guild.voice_client.disconnect()

                if os.path.exists("audio.pcm"):
                    AudioSegment.from_file("audio.pcm", format="raw", frame_rate=48000, channels=2, sample_width=2).export("audio.wav", format="wav")
                    transcribed_text = transcribe_audio("audio.wav")
                    with open("transcription.txt", "w") as file:
                        file.write(transcribed_text)
                    await interaction.response.send_message(f"Transcription saved as 'transcription.txt'.")
                else:
                    await interaction.response.send_message("No audio file found.")
        else:
            await interaction.response.send_message("Invalid action. Please use 'start' or 'stop'.")

def setup(bot):
    bot.add_cog(TranscriptionCog(bot))
