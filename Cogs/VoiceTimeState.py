import discord
from discord.ext import commands
from datetime import datetime

class VoiceTimeState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_time_tracker = {}  # {user_id: join_time}
        self.total_voice_time = 0

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # User joined a voice channel
        if after.channel is not None:
            self.voice_time_tracker[member.id] = datetime.now()
            print(f"{member.name} joined {after.channel.name} at {self.voice_time_tracker[member.id]}")

        # User left a voice channel
        if before.channel is not None and member.id in self.voice_time_tracker:
            join_time = self.voice_time_tracker.pop(member.id)
            time_spent = (datetime.now() - join_time).total_seconds()
            self.total_voice_time += time_spent
            print(f"{member.name} left {before.channel.name} after {time_spent:.2f} seconds")

    @commands.command()
    async def total_voice_time(self, ctx):
        # Convert total seconds to hours, minutes, and seconds
        hours = int(self.total_voice_time // 3600)
        minutes = int((self.total_voice_time % 3600) // 60)
        seconds = int(self.total_voice_time % 60)

        await ctx.send(f"Total voice time in the server: {hours} hours, {minutes} minutes, {seconds} seconds")

    @commands.command()
    async def current_voice_time(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel!")
            return

        # Get the voice channel the user is in
        voice_channel = ctx.author.voice.channel

        # Calculate the total time spent by all users in the channel so far
        current_time = datetime.now()
        total_time = 0

        for member_id, join_time in self.voice_time_tracker.items():
            member = ctx.guild.get_member(member_id)
            if member and member.voice and member.voice.channel == voice_channel:
                time_spent = (current_time - join_time).total_seconds()
                total_time += time_spent

        # Convert total seconds to hours, minutes, and seconds
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)

        await ctx.send(f"Total time spent in {voice_channel.name} so far: {hours} hours, {minutes} minutes, {seconds} seconds")

async def setup(bot):
    await bot.add_cog(VoiceTimeState(bot))