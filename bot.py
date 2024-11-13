import discord
from discord.ext import commands
import os
from discord import FFmpegPCMAudio

# Intents are required to access some features, like member information.
intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Import configuration settings
from config import TOKEN, MUSIC_DIR

# Define a simple command
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# Command to join a voice channel and play a song
@bot.command()
async def play(ctx, song: str):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    # Join the voice channel
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

    # Play the audio file
    source_path = os.path.join(MUSIC_DIR, song)
    if not os.path.isfile(source_path):
        await ctx.send("The requested song was not found.")
        return

    ctx.voice_client.stop()  # Stop any current audio playing
    ctx.voice_client.play(FFmpegPCMAudio(source_path), after=lambda e: print(f"Finished playing: {e}"))
    await ctx.send(f'Now playing: {song}')

# Command to stop playing and disconnect
@bot.command()
async def stop(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I'm not connected to a voice channel.")

# Run the bot with your token
bot.run(TOKEN)
