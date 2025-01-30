import discord
from discord.ext import tasks
from config import BOT_TOKEN
import datetime

# Enable intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
intents.voice_states = True  # Required to track voice state updates

# Bot instance (using discord.Client instead of commands.Bot)
bot = discord.Client(intents=intents)

# Channel IDs (replace with your actual channel IDs)
TOTAL_MEMBERS_CHANNEL_ID = 1334202426026364979
ONLINE_MEMBERS_CHANNEL_ID = 1334202931788120125
MESSAGES_CHANNEL_ID = 1334203213481512980
VOICE_TIME_CHANNEL_ID = 1334203377013362799

# Variables to track messages and voice time
message_count = 0
voice_time_tracker = {}  # {user_id: total_seconds}

@tasks.loop(minutes=5)  # Update the channels every 5 minutes (reduced frequency to avoid rate limits)
async def update_channels():
    print("Running update_channels...")  # Debugging: Check if the loop is running
    guild = bot.get_guild(1333113498594574506)  # Replace with your guild ID

    if not guild:
        print("Guild not found!")  # Debugging: Check if the guild is found
        return

    # Get the channels by their IDs
    total_members_channel = guild.get_channel(TOTAL_MEMBERS_CHANNEL_ID)
    online_members_channel = guild.get_channel(ONLINE_MEMBERS_CHANNEL_ID)
    messages_channel = guild.get_channel(MESSAGES_CHANNEL_ID)
    voice_time_channel = guild.get_channel(VOICE_TIME_CHANNEL_ID)

    try:
        # Update the total members channel
        if total_members_channel:
            total_members = len(guild.members)
            print(f"Updating total members: {total_members}")  # Debugging
            await total_members_channel.edit(name=f"Total Members: {total_members}")

        # Update the online members channel
        if online_members_channel:
            online_members = len([member for member in guild.members if member.status != discord.Status.offline])
            print(f"Updating online members: {online_members}")  # Debugging
            await online_members_channel.edit(name=f"Online: {online_members}")

        # Update the messages channel
        if messages_channel:
            print(f"Updating messages: {message_count}")  # Debugging
            await messages_channel.edit(name=f"Msgs Last 7 Days: {message_count}")

        # Update the voice time channel
        if voice_time_channel:
            total_voice_time = sum(voice_time_tracker.values())  # Total voice time in seconds
            hours, remainder = divmod(total_voice_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            voice_time_str = f"{hours}h{minutes}m{seconds}s"  # Format as "1h30m5s"
            print(f"Updating voice time: {voice_time_str}")  # Debugging
            await voice_time_channel.edit(name=f"Voice Time: {voice_time_str}")

    except discord.HTTPException as e:
        print(f"Failed to update channels: {e}")  # Debugging: Log rate limit errors

# Track messages
@bot.event
async def on_message(message):
    global message_count
    if message.guild and not message.author.bot:  # Ignore DMs and bot messages
        message_count += 1

# Track voice time
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:  # Ignore bots
        return

    user_id = member.id
    now = datetime.datetime.now(datetime.UTC)  # Use timezone-aware datetime

    # User joined a voice channel
    if before.channel is None and after.channel is not None:
        voice_time_tracker[user_id] = now.timestamp()  # Track when they joined

    # User left a voice channel
    elif before.channel is not None and after.channel is None:
        if user_id in voice_time_tracker:
            join_time = voice_time_tracker[user_id]
            time_spent = now.timestamp() - join_time
            voice_time_tracker[user_id] = time_spent  # Update total time spent

# Start the task when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if not update_channels.is_running():  # Ensure the loop isn't already running
        update_channels.start()

bot.run(BOT_TOKEN)