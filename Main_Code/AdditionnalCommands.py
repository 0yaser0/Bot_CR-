import discord
from discord.ext import commands, tasks
from config import BOT_TOKEN  #

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for tracking message replies

# Create bot with the prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents)

#COMMAND TO SHOW ALL COMMANDS
@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="📢 Command List", description="Use the following commands to get server stats:", color=0xE91E63)

    embed.add_field(name="🟢 Online Members", value="`!online_members`", inline=False)
    embed.add_field(name="👥 Total Members", value="`!total_members`", inline=False)
    embed.add_field(name="🎤 Current Voice Time", value="`!current_voice_time`", inline=False)
    embed.add_field(name="⏳ Total Voice Time", value="`!voice_time`", inline=False)

    embed.set_footer(text="Enjoy your commands! 🚀")

    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)