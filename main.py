import discord
from discord.ext import commands
from config import BOT_TOKEN  # Import the token from config.py

# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True  # Privileged intent
intents.members = True  # Required for the on_member_join event
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Command: !hello
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

# Command: !ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Load the welcome cog
async def load_extensions():
    await bot.load_extension('cogs.Welcome')
    await bot.load_extension('cogs.GoodBye')

async def main():
    await load_extensions()
    await bot.start(BOT_TOKEN)

# Run the bot
import asyncio
asyncio.run(main())
