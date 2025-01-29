import discord
from discord.ext import commands, tasks
from datetime import datetime
import json
from config import BOT_TOKEN


def load_birthdays():
    try:
        with open("birthdays.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("birthdays.json", "w") as f:
            json.dump({}, f)  # Ensure the file exists
        return {}

def save_birthdays(birthDays):
    with open("birthdays.json", "w") as f:
        json.dump(birthDays, f, indent=4)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
birthdays = load_birthdays()

CHANNEL_ID = 1333167210750939266  # Replace with your actual channel ID

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f'✅ Bot is ready! Announcements will be sent to: {channel.name}')
    else:
        print("⚠️ ERROR: Could not find the channel! Check the CHANNEL_ID and bot permissions.")

    if not check_birthdays.is_running():
        check_birthdays.start()

@bot.command()
async def add_birthday(ctx, user: discord.Member, date: str):
    """Command to add a user's birthday in YYYY-MM-DD format"""
    if str(user.id) in birthdays:
        await ctx.send(f"{user.mention} already has a birthday set on {birthdays[str(user.id)]}!")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
        birthdays[str(user.id)] = date
        save_birthdays(birthdays)
        await ctx.send(f'🎉 Birthday for {user.mention} added: {date}')
    except ValueError:
        await ctx.send("⚠️ Invalid date format! Use YYYY-MM-DD.")

@bot.command()
async def list_birthdays(ctx):
    """Lists all stored birthdays."""
    if not birthdays:
        await ctx.send("No birthdays have been set yet!")
        return

    message = "🎂 Stored Birthdays:\n"
    for user_id, date in birthdays.items():
        try:
            user = await bot.fetch_user(int(user_id))
            message += f"{user.name}: {date}\n"
        except discord.NotFound:
            message += f"User {user_id}: {date} (User not found)\n"

    await ctx.send(message)

@tasks.loop(hours=24)
async def check_birthdays():
    """Checks if today matches any stored birthdays and sends a message."""
    from datetime import UTC  # Import UTC for timezone handling
    today = datetime.now(UTC).strftime("%Y-%m-%d")  # Timezone-aware datetime

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("⚠️ ERROR: Channel not found! Check permissions or CHANNEL_ID.")
        return

    for user_id, bday in birthdays.items():
        if bday == today:
            try:
                user = await bot.fetch_user(int(user_id))
                await channel.send(f"🎉 Happy Birthday {user.mention}! 🎂")
            except discord.NotFound:
                print(f"User {user_id} not found, skipping.")
            except discord.HTTPException:
                print("Failed to fetch user due to API error.")


if not BOT_TOKEN:
    print("⚠️ ERROR: Bot token is missing!")
else:
    bot.run(BOT_TOKEN)