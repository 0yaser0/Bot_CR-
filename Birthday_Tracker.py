import discord
from discord.ext import commands, tasks
import json
from datetime import datetime
import pytz
from dateutil import parser
from config import BOT_TOKEN

# Set the timezone (e.g., Morocco)
tz = pytz.timezone("Africa/Casablanca")

# Load and save birthdays
def load_birthdays():
    try:
        with open("birthdays.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_birthdays(birthdays):
    with open("birthdays.json", "w") as f:
        json.dump(birthdays, f, indent=4)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
birthdays = load_birthdays()

# 🎂 Birthday Modal
class BirthdayModal(discord.ui.Modal, title="Enter Your Birthday"):
    date = discord.ui.TextInput(label="Enter your birthdate (any format)", placeholder="e.g., 2004-12-25 or 25/12/2004")

    async def on_submit(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        birthdate_input = self.date.value.strip()

        try:
            # Auto-detect and normalize date format
            parsed_date = parser.parse(birthdate_input, dayfirst=False)  # Converts any format
            formatted_birthday = parsed_date.strftime("%Y-%m-%d")  # Ensure YYYY-MM-DD format

            birthdays[user_id] = {
                "username": interaction.user.name,
                "birthday": formatted_birthday
            }
            save_birthdays(birthdays)

            await interaction.response.send_message(f"🎉 Your birthday has been saved: {formatted_birthday}", ephemeral=True)
        except (ValueError, OverflowError):
            await interaction.response.send_message("⚠️ Invalid date! Try again (e.g., 2004-12-25).", ephemeral=True)

# 🎉 Button to Open Modal
class BirthdayButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.birthday_button = discord.ui.Button(label="Set Your Birthday 🎂", style=discord.ButtonStyle.primary, custom_id="birthday_button")
        self.birthday_button.callback = self.birthday_button_callback  # Link button to function
        self.add_item(self.birthday_button)  # Add button to view

    async def birthday_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BirthdayModal())  # Open modal

@bot.event
async def on_member_join(member):
    """Send a DM with a button to open the birthday modal when a user joins."""
    try:
        view = BirthdayButton()
        await member.send("🎉 Welcome! Click the button below to set your birthday:", view=view)
    except discord.Forbidden:
        print(f"❌ Cannot send message to {member} (DMs are closed)")

# 🎉 Check Birthdays Daily
@tasks.loop(hours=24)
async def check_birthdays():
    await bot.wait_until_ready()  # Ensure bot is ready before running
    today = datetime.now(tz).strftime("%m-%d")

    print(f"📅 Checking birthdays for today: {today}")
    print(f"📂 Loaded Birthdays: {birthdays}")

    channel_id = None
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="⦿announcements⦿")
        if channel:
            channel_id = channel.id
            print(f"✅ Found channel: {channel.name} in guild: {guild.name}")
            break

    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            for user_id, info in birthdays.items():
                user_birthday = info["birthday"]
                if datetime.strptime(user_birthday, "%Y-%m-%d").strftime("%m-%d") == today:
                    print(f"🎉 Sending birthday message for {info['username']}")
                    await channel.send(f"🎉 Happy Birthday to {info['username']}! 🎂🎈")
        else:
            print("⚠️ Channel ID found, but bot cannot access the channel.")
    else:
        print("⚠️ No valid announcement channel found.")

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    check_birthdays.start()

if not BOT_TOKEN:
    print("⚠️ ERROR: Bot token is missing!")
else:
    bot.run(BOT_TOKEN)