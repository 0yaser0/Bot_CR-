import discord
from discord.ext import commands
import asyncio
from config import BOT_TOKEN  # Import the token from .env
from KeepAlive import keep_alive

keep_alive()

# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True  # Privileged intent
intents.presences = True  # Track online status
intents.members = True  # Required for the on_member_join event
intents.voice_states = True  # Track voice state changes

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
    await bot.load_extension('Cogs.Welcome')
    await bot.load_extension('Cogs.GoodBye')
    await bot.load_extension('Cogs.VoiceTimeState')
    await bot.load_extension('Cogs.TotalMessagesState')
    await bot.load_extension('Cogs.MembersState')
    await bot.load_extension('Cogs.DashBoard')
    await bot.load_extension('Cogs.Verification')
    await bot.load_extension('Cogs.BirthdayTracker')
    await bot.load_extension('Op_Commands.DeleteMessages')

async def main():
    await load_extensions()
    await bot.start(BOT_TOKEN)

# Run the bot
asyncio.run(main())
