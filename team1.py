import discord
from discord.ext import commands
from config import BOT_TOKEN

# Intents and bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Privileged intent

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
TEMP_ROLE_NAME = "⛔ | None"
VERIFIED_ROLE_NAME = "「📗」Verified"
VERIFICATION_CHANNEL = "•📑•-verification"
CHECK_EMOJI = "✅"
CANCEL_EMOJI = "❌"

bot.verification_messages = {}  # Store verification message IDs


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.event
async def on_member_join(member):
    """Assigns temporary role and sends verification message with reactions."""
    temp_role = discord.utils.get(member.guild.roles, name=TEMP_ROLE_NAME)
    if temp_role:
        await member.add_roles(temp_role)
        print(f"Assigned {TEMP_ROLE_NAME} to {member.name}")

    channel = discord.utils.get(member.guild.channels, name=VERIFICATION_CHANNEL)
    if channel:
        verification_msg = await channel.send(
            f"👋 Welcome {member.mention}! React with {CHECK_EMOJI} to verify or {CANCEL_EMOJI} to cancel."
        )
        await verification_msg.add_reaction(CHECK_EMOJI)
        await verification_msg.add_reaction(CANCEL_EMOJI)

        # Store the message ID for tracking
        bot.verification_messages[verification_msg.id] = (member.id, verification_msg)


@bot.event
async def on_raw_reaction_add(payload):
    """Handles reaction-based verification and deletes the message."""
    if payload.message_id not in bot.verification_messages:
        return  # Ignore reactions that are not on verification messages

    guild = bot.get_guild(payload.guild_id)
    member_id, verification_msg = bot.verification_messages.pop(payload.message_id, (None, None))
    member = guild.get_member(member_id)

    if not member:
        return  # Ignore if member left

    temp_role = discord.utils.get(guild.roles, name=TEMP_ROLE_NAME)
    verified_role = discord.utils.get(guild.roles, name=VERIFIED_ROLE_NAME)
    channel = guild.get_channel(payload.channel_id)

    if str(payload.emoji) == CHECK_EMOJI:
        # Assign verified role & remove temp role
        if temp_role:
            await member.remove_roles(temp_role)
        await member.add_roles(verified_role)
        await channel.send(f"✅ {member.mention} has been verified!", delete_after=5)
        print(f"Verified {member.name}")

    elif str(payload.emoji) == CANCEL_EMOJI:
        # Kick member & send rejection message
        await member.kick(reason="Verification rejected")
        await channel.send(f"❌ {member.mention} has been removed for not verifying.", delete_after=5)
        print(f"Kicked {member.name}")

    # Delete verification message
    try:
        await verification_msg.delete()
    except discord.NotFound:
        pass  # Ignore if message is already deleted


bot.run(BOT_TOKEN)
