import discord
import random
from discord.ext import commands, tasks
from config import BOT_TOKEN  # Make sure you have a config.py file with BOT_TOKEN

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for message tracking

# Create bot with the prefix '!'
Bot = commands.Bot(command_prefix='!', intents=intents)

# List of daily challenges
challenges = [
    "Write a short story using only emojis 😍!",
    "Send a meme related to gaming 🎮!",
    "Compliment another member in the server 🤝!",
    "Share your favorite motivational quote 📜!",
    "Post a fun fact about history 🎭!",
    "Use an ASCII art generator and share the result 🎨!"
]

# XP tracking dictionary
chanell_id = 0
xp = {}
challenge_message_id = None  # Store the message ID of the daily challenge
challenge_channel_id = chanell_id  # Replace with your actual challenge channel ID

# Function to get a random challenge
def get_daily_challenge():
    return random.choice(challenges)

# Task to post a daily challenge every 24 hours
@tasks.loop(hours=24)
async def post_daily_challenge():
    global challenge_message_id
    channel = Bot.get_channel(challenge_channel_id)
    if channel:
        challenge = get_daily_challenge()
        message = await channel.send(f"🌟 *Daily Challenge:* {challenge}\nReply to this message to complete it!")
        challenge_message_id = message.id  # Store the message ID

# Event: When bot is ready
@Bot.event
async def on_ready():
    print(f'✅ Logged in as {Bot.user}')
    post_daily_challenge.start()

# Event: Handling messages
@Bot.event
async def on_message(message):
    global challenge_message_id

    if message.author == Bot.user:
        return

    # Check if the message is a reply to the challenge message
    if message.channel.id == challenge_channel_id and message.reference:
        if message.reference.message_id == challenge_message_id:
            user = message.author
            xp[user.id] = xp.get(user.id, 0) + 10  # Award 10 XP
            await message.channel.send(f'🎉 {user.mention}, you completed today\'s challenge! You earned *10 XP! You now have **{xp[user.id]} XP*!')

    await Bot.process_commands(message)

# Run the bot
Bot.run(BOT_TOKEN)