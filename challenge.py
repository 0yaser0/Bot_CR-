import discord
from discord.ext import commands, tasks
from config import BOT_TOKEN
import random
import asyncio

intents = discord.Intents.default()
intents.members = True  # Enable member intents

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store daily challenges
challenges = {}

def get_server_stats(guild):
    total_members = guild.member_count
    online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
    total_channels = len(guild.channels)
    total_roles = len(guild.roles)
    return total_members, online_members, total_channels, total_roles

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    daily_challenge.start()

@bot.command()
async def serverstats(ctx):
    guild = ctx.guild
    total_members, online_members, total_channels, total_roles = get_server_stats(guild)

    embed = discord.Embed(title=f"Server Stats - {guild.name}", color=discord.Color.blue())
    embed.add_field(name="Total Members", value=total_members, inline=False)
    embed.add_field(name="Online Members", value=online_members, inline=False)
    embed.add_field(name="Total Channels", value=total_channels, inline=False)
    embed.add_field(name="Total Roles", value=total_roles, inline=False)

    await ctx.send(embed=embed)

@tasks.loop(hours=24)
async def daily_challenge():
    global challenges
    challenge_list = [
        "Send a positive message in the chat!",
        "Help a new member with a question!",
        "Share your favorite song in the music channel!",
        "Post a funny meme in the meme channel!"
    ]
    challenge = random.choice(challenge_list)
    challenges["current"] = challenge

    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="general")
        if channel:
            await channel.send(f"Today's Daily Challenge: {challenge}")

@bot.command()
async def challenge(ctx):
    if "current" in challenges:
        await ctx.send(f"Today's challenge: {challenges['current']}")
    else:
        await ctx.send("No challenge set yet!")

bot.run("BOT_TOKEN")
