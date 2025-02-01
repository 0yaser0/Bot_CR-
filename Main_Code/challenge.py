import discord
import random
import asyncio
import json
from config import BOT_TOKEN
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
client = commands.Bot(command_prefix='!', intents=intents)

# Load XP data
try:
    with open("xp_data.json", "r") as f:
        xp = json.load(f)
except FileNotFoundError:
    xp = {}

# List of daily challenges
challenges = [
    {"text": "Write a short story using only emojis 😍!", "verify": "emoji"},
    {"text": "Send a meme related to gaming! 🎮", "verify": "image"},
    {"text": "Follow member in the server! 🤷‍♀️", "verify": "mention"},
    {"text": "Share your favorite motivational quote 📜!", "verify": "text"},
    {"text": "Post a fun fact about history! 🎭", "verify": "text"},
    {"text": "Use an ASCII art generator and share the result! 🎨", "verify": "ascii"}
]

current_challenge = None


@tasks.loop(hours=24)
async def post_daily_challenge():
    global current_challenge
    channel = client.get_channel(1333167210750939266)  # Replace with your channel ID
    if channel:
        current_challenge = random.choice(challenges)
        await channel.send(f"🌟 **Daily Challenge:** {current_challenge['text']}\nReply here to complete it!")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    post_daily_challenge.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == 1333167210750939266 and current_challenge:
        user = message.author
        content = message.content.lower()

        # Verify challenge completion
        verified = False
        if current_challenge["verify"] == "emoji" and any(
                char in content for char in "😀😁😂🤣😃😄😅😆"):  # Example emoji check
            verified = True
        elif current_challenge["verify"] == "image" and message.attachments:
            verified = True
        elif current_challenge["verify"] == "mention" and message.mentions:
            verified = True
        elif current_challenge["verify"] == "text" and len(content) > 10:
            verified = True
        elif current_challenge["verify"] == "ascii" and "|" in content:
            verified = True

        if verified:
            xp[user.id] = xp.get(str(user.id), 0) + 10  # Award XP
            with open("xp_data.json", "w") as f:
                json.dump(xp, f)
            await message.channel.send(f'🎉 {user.mention} completed the challenge! You earned 10 XP!')
        else:
            await message.channel.send(
                f'❌ {user.mention}, your message doesn’t match the challenge requirement! Try again.')

    await client.process_commands(message)


client.run(BOT_TOKEN)