import discord
from discord.ext import commands
import subprocess
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def music(ctx):
    view = discord.ui.View(timeout=None)

    button = discord.ui.Button(
        label="Open Music Controls 🎶",
        style=discord.ButtonStyle.primary
    )

    async def button_callback(interaction: discord.Interaction):
        button.disabled = True
        await interaction.response.edit_message(content="Launching Music Controls UI...", view=view)
        subprocess.Popen(["python", "MainFAB.py"])

    button.callback = button_callback
    view.add_item(button)

    await ctx.send("", view=view)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")

bot.run(BOT_TOKEN)
