import discord
from discord.ext import commands
from config import BOT_TOKEN
from datetime import datetime

# Enable intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
intents.voice_states = True  # Required to track voice state updates

# Bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Variables to track data
voice_time_tracker = {}  # {user_id: join_time}
total_voice_time = 0
message_count = 0  # Total message count

# Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Track when a member joins or leaves a voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    global total_voice_time

    # User joined a voice channel
    if after.channel is not None:
        voice_time_tracker[member.id] = datetime.now()
        print(f"{member.name} joined {after.channel.name} at {voice_time_tracker[member.id]}")

    # User left a voice channel
    if before.channel is not None and member.id in voice_time_tracker:
        join_time = voice_time_tracker.pop(member.id)
        time_spent = (datetime.now() - join_time).total_seconds()
        total_voice_time += time_spent
        print(f"{member.name} left {before.channel.name} after {time_spent:.2f} seconds")

# Track messages
@bot.event
async def on_message(message):
    global message_count

    # Ignore messages from bots and DMs
    if not message.author.bot and message.guild:
        message_count += 1

    # Process commands
    await bot.process_commands(message)

# Command: Total voice time in the server
@bot.command()
async def voice_time(ctx):
    global total_voice_time

    # Convert total seconds to hours, minutes, and seconds
    hours = int(total_voice_time // 3600)
    minutes = int((total_voice_time % 3600) // 60)
    seconds = int(total_voice_time % 60)

    await ctx.send(f"Total voice time in the server: {hours} hours, {minutes} minutes, {seconds} seconds")

# Command: Current voice time in a specific channel
@bot.command()
async def current_voice_time(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not in a voice channel!")
        return

    # Get the voice channel the user is in
    voice_channel = ctx.author.voice.channel

    # Calculate the total time spent by all users in the channel so far
    current_time = datetime.now()
    total_time = 0

    for member_id, join_time in voice_time_tracker.items():
        member = ctx.guild.get_member(member_id)
        if member and member.voice and member.voice.channel == voice_channel:
            time_spent = (current_time - join_time).total_seconds()
            total_time += time_spent

    # Convert total seconds to hours, minutes, and seconds
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)

    await ctx.send(f"Total time spent in {voice_channel.name} so far: {hours} hours, {minutes} minutes, {seconds} seconds")

# Command: Total messages in the server
@bot.command()
async def total_messages(ctx):
    global message_count
    await ctx.send(f"Total messages sent in the server: {message_count}")

# Command: Number of online members
@bot.command()
async def online_members(ctx):
    guild = ctx.guild
    online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
    await ctx.send(f"Number of online members: {online_members}")

# Run bot
bot.run(BOT_TOKEN)