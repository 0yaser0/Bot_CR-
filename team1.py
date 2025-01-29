import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
from config import Token_Key

# Intents and bot setup
intents = discord.Intents.default()
intents.members = True  
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
TEMP_ROLE_NAME = "None" 
VERIFIED_ROLE_NAME = "Verified"
VERIFICATION_CHANNEL = "verification" 
UNVERIFIED_TIMEOUT = 86400  


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.event
async def on_member_join(member):
    temp_role = discord.utils.get(member.guild.roles, name=TEMP_ROLE_NAME)
    if temp_role:
        await member.add_roles(temp_role)
        print(f"Assigned {TEMP_ROLE_NAME} to {member.name}")

        channel = discord.utils.get(member.guild.channels, name=VERIFICATION_CHANNEL)
        if channel:
            await channel.send(
                f"👋 Welcome {member.mention}! Please wait for a moderator to verify you."
            )

        await asyncio.sleep(UNVERIFIED_TIMEOUT)

        if temp_role in member.roles:
            await member.kick(reason="Failed to verify in time")
            print(f"Kicked {member.name} for not verifying in time.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def accept(ctx, member: discord.Member):
    """Command for moderators to verify a member."""
    temp_role = discord.utils.get(ctx.guild.roles, name=TEMP_ROLE_NAME)
    verified_role = discord.utils.get(ctx.guild.roles, name=VERIFIED_ROLE_NAME)

    if temp_role in member.roles:
        # Remove the temporary role and add the verified role
        await member.remove_roles(temp_role)
        await member.add_roles(verified_role)
        await ctx.send(f"✅ {member.mention} has been verified!")
        print(f"Verified {member.name}")
    else:
        await ctx.send(f"{member.mention} is already verified or does not need verification.")


@bot.command()
@commands.has_permissions(kick_members=True)
async def reject(ctx, member: discord.Member):
    """Command for moderators to reject a member."""
    temp_role = discord.utils.get(ctx.guild.roles, name=TEMP_ROLE_NAME)

    if temp_role in member.roles:
        await member.kick(reason="Verification rejected")
        await ctx.send(f"❌ {member.name} has been rejected and removed from the server.")
        print(f"Rejected {member.name}")
    else:
        await ctx.send(f"{member.mention} does not have the temporary role or is already verified.")


@bot.event
async def on_member_remove(member):
    """Logs when a member leaves the server."""
    print(f"{member.name} has left the server.")


# Error handler for missing permissions
@accept.error
@reject.error
async def permission_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ You don't have the required permissions to use this command.")
    else:
        raise error

bot.run(Token_Key)