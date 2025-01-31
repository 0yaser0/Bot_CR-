import discord
import asyncio
from discord.ext import commands
from config import BOT_TOKEN

# Intents and bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Privileged intent

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Load the Cogs
async def load_extensions():
    await bot.load_extension('Cogs.Verification')
    await bot.load_extension('Cogs.BirthdayTracker')

async def main():
    await load_extensions()
    await bot.start(BOT_TOKEN)

# Run bot
asyncio.run(main())