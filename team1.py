import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
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
UNVERIFIED_TIMEOUT = 86400  # 24 hours in seconds

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

class VerificationView(View):
    def __init__(self, member, ctx):
        super().__init__()
        self.member = member  # The member who joined the server
        self.ctx = ctx  # The context for sending messages

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Action for the Accept button"""
        temp_role = discord.utils.get(self.ctx.guild.roles, name=TEMP_ROLE_NAME)
        verified_role = discord.utils.get(self.ctx.guild.roles, name=VERIFIED_ROLE_NAME)

        if temp_role in self.member.roles:
            await self.member.remove_roles(temp_role)
            await self.member.add_roles(verified_role)
            await interaction.response.send_message(f"✅ {self.member.mention} has been verified!")
            print(f"Verified {self.member.name}")
        else:
            await interaction.response.send_message(f"{self.member.mention} is already verified or does not need verification.")

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Action for the Decline button"""
        temp_role = discord.utils.get(self.ctx.guild.roles, name=TEMP_ROLE_NAME)

        if temp_role in self.member.roles:
            await self.member.kick(reason="Verification rejected")
            await interaction.response.send_message(f"❌ {self.member.name} has been rejected and removed from the server.")
            print(f"Rejected {self.member.name}")
        else:
            await interaction.response.send_message(f"{self.member.mention} does not have the temporary role or is already verified.")


@bot.event
async def on_member_join(member):
    temp_role = discord.utils.get(member.guild.roles, name=TEMP_ROLE_NAME)
    if temp_role:
        await member.add_roles(temp_role)
        print(f"Assigned {TEMP_ROLE_NAME} to {member.name}")

        channel = discord.utils.get(member.guild.channels, name=VERIFICATION_CHANNEL)
        if channel:
            verification_message = await channel.send(
                f"👋 Welcome {member.mention}! Please wait for a moderator to verify you."
            )

            # Create buttons for verification
            view = VerificationView(member, channel)
            await verification_message.edit(view=view)

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

bot.run(BOT_TOKEN)
