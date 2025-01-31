import discord
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TEMP_ROLE_NAME = "⛔ | None"
        self.VERIFIED_ROLE_NAME = "「📗」Verified"
        self.VERIFICATION_CHANNEL = "•📑•-verification"
        self.CHECK_EMOJI = "✅"
        self.CANCEL_EMOJI = "❌"
        self.verification_messages = {}  # Store verification message IDs

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Assigns temporary role and sends verification message with reactions."""
        temp_role = discord.utils.get(member.guild.roles, name=self.TEMP_ROLE_NAME)
        if temp_role:
            await member.add_roles(temp_role)
            print(f"Assigned {self.TEMP_ROLE_NAME} to {member.name}")

        channel = discord.utils.get(member.guild.channels, name=self.VERIFICATION_CHANNEL)
        if channel:
            verification_msg = await channel.send(
                f"👋 Welcome {member.mention}! React with {self.CHECK_EMOJI} to verify or {self.CANCEL_EMOJI} to cancel."
            )
            await verification_msg.add_reaction(self.CHECK_EMOJI)
            await verification_msg.add_reaction(self.CANCEL_EMOJI)

            # Store the message ID for tracking
            self.verification_messages[verification_msg.id] = (member.id, verification_msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handles reaction-based verification and deletes the message."""
        if payload.message_id not in self.verification_messages:
            return  # Ignore reactions that are not on verification messages

        guild = self.bot.get_guild(payload.guild_id)
        member_id, verification_msg = self.verification_messages.pop(payload.message_id, (None, None))
        member = guild.get_member(member_id)

        if not member:
            return  # Ignore if member left

        temp_role = discord.utils.get(guild.roles, name=self.TEMP_ROLE_NAME)
        verified_role = discord.utils.get(guild.roles, name=self.VERIFIED_ROLE_NAME)
        channel = guild.get_channel(payload.channel_id)

        if str(payload.emoji) == self.CHECK_EMOJI:
            # Assign verified role & remove temp role
            if temp_role:
                await member.remove_roles(temp_role)
            await member.add_roles(verified_role)
            await channel.send(f"✅ {member.mention} has been verified!", delete_after=5)
            print(f"Verified {member.name}")

        elif str(payload.emoji) == self.CANCEL_EMOJI:
            # Kick member & send rejection message
            await member.kick(reason="Verification rejected")
            await channel.send(f"❌ {member.mention} has been removed for not verifying.", delete_after=5)
            print(f"Kicked {member.name}")

        # Delete verification message
        try:
            await verification_msg.delete()
        except discord.NotFound:
            pass  # Ignore if message is already deleted

async def setup(bot):
    await bot.add_cog(Verification(bot))