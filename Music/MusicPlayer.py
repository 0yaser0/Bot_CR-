import discord
from discord.ext import commands
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True  # ✅ Important for commands
bot = commands.Bot(command_prefix="!", intents=intents)


# 🎵 Music Controls View
class MusicControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="▶️ Play", style=discord.ButtonStyle.success, custom_id="play")
    async def play(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🎵 **Playing Music...**", ephemeral=True)

    @discord.ui.button(label="⏸ Pause", style=discord.ButtonStyle.primary, custom_id="pause")
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏸ **Music Paused**", ephemeral=True)

    @discord.ui.button(label="⏭ Skip", style=discord.ButtonStyle.secondary, custom_id="skip")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏩ **Skipped to Next Track**", ephemeral=True)

    @discord.ui.button(label="⏮ Back", style=discord.ButtonStyle.secondary, custom_id="back")
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏮ **Playing Previous Track**", ephemeral=True)


# 📌 Command to Show Music Button
@bot.command()
async def music(ctx):
    """Sends the floating music button to open controls."""
    view = discord.ui.View(timeout=None)  # ✅ Persistent View

    # Adding an icon to the button
    button = discord.ui.Button(label="🎵 Open Music Controls", style=discord.ButtonStyle.primary, emoji="🎶")

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.edit_message(content="🎶 **Music Controls:**", view=MusicControls())

    button.callback = button_callback
    view.add_item(button)

    await ctx.send("Click below to control music 🎵", view=view)


@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    bot.add_view(MusicControls())  # ✅ Keep the buttons alive across restarts


bot.run(BOT_TOKEN)
