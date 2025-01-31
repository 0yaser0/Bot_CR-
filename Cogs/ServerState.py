import discord
from discord.ext import commands, tasks
from config import BOT_TOKEN
import time

# ✅ Enable intents for members, presence, message content, and voice states
intents = discord.Intents.default()
intents.members = True  # Track members
intents.presences = True  # Track online status
intents.message_content = True  # Track messages
intents.voice_states = True  # Track voice state changes

bot = commands.Bot(command_prefix="!", intents=intents)

dashboard_message = None  # Store the dashboard message
user_voice_times = {}  # Store voice time for users in seconds


@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    await setup_dashboard()
    update_server_stats.start()  # Start updating stats


@bot.event
async def on_voice_state_update(member, before, after):
    """Track time spent in voice channels."""
    global user_voice_times

    current_time = time.time()

    # User joins a voice channel
    if before.channel is None and after.channel is not None:
        user_voice_times[member.id] = {"join_time": current_time,
                                       "total_time": user_voice_times.get(member.id, {}).get("total_time", 0)}

    # User leaves a voice channel
    elif before.channel is not None and after.channel is None:
        if member.id in user_voice_times and "join_time" in user_voice_times[member.id]:
            join_time = user_voice_times[member.id]["join_time"]
            total_time = user_voice_times[member.id].get("total_time", 0)
            user_voice_times[member.id]["total_time"] = total_time + (current_time - join_time)
            del user_voice_times[member.id]["join_time"]

    # User switches voice channels
    elif before.channel != after.channel:
        if member.id in user_voice_times and "join_time" in user_voice_times[member.id]:
            join_time = user_voice_times[member.id]["join_time"]
            total_time = user_voice_times[member.id].get("total_time", 0)
            user_voice_times[member.id]["total_time"] = total_time + (current_time - join_time)
            user_voice_times[member.id]["join_time"] = current_time


async def setup_dashboard():
    """Find the dashboard channel and send an initial message."""
    global dashboard_message

    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="⦿dashboard⦿")
        if channel:
            async for msg in channel.history(limit=10):  # Check if message exists
                if msg.author == bot.user:
                    dashboard_message = msg
                    break

            if dashboard_message is None:
                embed = await create_dashboard_embed()
                dashboard_message = await channel.send(embed=embed)


async def count_total_messages():
    """Counts the total messages in all text channels."""
    total_messages = 0
    guild = bot.guilds[0]  # Get the first guild

    for channel in guild.text_channels:
        try:
            async for message in channel.history(limit=None):  # Async iteration over history
                total_messages += 1  # Count each message
        except discord.Forbidden:
            continue  # Skip channels the bot doesn't have permission to read

    return total_messages


async def count_total_voice_time():
    """Counts the total voice time spent in all voice channels and converts to hours, minutes, seconds."""
    total_seconds = sum(user_data.get("total_time", 0) for user_data in user_voice_times.values())

    hours = int(total_seconds // 3600)  # Convert to integer
    minutes = int((total_seconds % 3600) // 60)  # Convert to integer
    seconds = int(total_seconds % 60)  # Convert to integer

    # Format with leading zeros
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"


async def update_dashboard():
    """Update the dashboard message with latest stats."""
    if dashboard_message:
        embed = await create_dashboard_embed()
        await dashboard_message.edit(embed=embed)


async def create_dashboard_embed():
    """Create an embed with the latest stats."""
    guild = bot.guilds[0]  # Get the first guild
    total_members = guild.member_count
    online_members = sum(
        1 for m in guild.members if m.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd])
    total_messages = await count_total_messages()
    total_voice_time = await count_total_voice_time()

    embed = discord.Embed(title="📊 Server Dashboard", color=discord.Color.blue())
    embed.add_field(name="👥 Total Members", value=f"`{total_members}`", inline=True)
    embed.add_field(name="🟢 Online Members", value=f"`{online_members}`", inline=True)
    embed.add_field(name="💬 Total Messages", value=f"`{total_messages}`", inline=True)
    embed.add_field(name="🎤 Total Voice Time", value=f"`{total_voice_time}`", inline=True)
    embed.set_footer(text="Updated every 30 seconds")

    return embed


@tasks.loop(seconds=30)
async def update_server_stats():
    """Loop to update stats every 30 seconds."""
    await update_dashboard()


bot.run(BOT_TOKEN)