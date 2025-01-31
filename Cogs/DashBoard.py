import discord
from discord.ext import commands, tasks
import time

class DashBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dashboard_message = None  # Store the dashboard message
        self.user_voice_times = {}  # Store voice time for users in seconds

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'✅ Logged in as {self.bot.user}')
        await self.setup_dashboard()
        self.update_server_stats.start()  # Start updating stats

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Track time spent in voice channels."""
        current_time = time.time()

        # User joins a voice channel
        if before.channel is None and after.channel is not None:
            self.user_voice_times[member.id] = {"join_time": current_time,
                                               "total_time": self.user_voice_times.get(member.id, {}).get("total_time", 0)}

        # User leaves a voice channel
        elif before.channel is not None and after.channel is None:
            if member.id in self.user_voice_times and "join_time" in self.user_voice_times[member.id]:
                join_time = self.user_voice_times[member.id]["join_time"]
                total_time = self.user_voice_times[member.id].get("total_time", 0)
                self.user_voice_times[member.id]["total_time"] = total_time + (current_time - join_time)
                del self.user_voice_times[member.id]["join_time"]

        # User switches voice channels
        elif before.channel != after.channel:
            if member.id in self.user_voice_times and "join_time" in self.user_voice_times[member.id]:
                join_time = self.user_voice_times[member.id]["join_time"]
                total_time = self.user_voice_times[member.id].get("total_time", 0)
                self.user_voice_times[member.id]["total_time"] = total_time + (current_time - join_time)
                self.user_voice_times[member.id]["join_time"] = current_time

    async def setup_dashboard(self):
        """Find the dashboard channel and send an initial message."""
        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name="⦿dashboard⦿")
            if channel:
                async for msg in channel.history(limit=10):  # Check if message exists
                    if msg.author == self.bot.user:
                        self.dashboard_message = msg
                        break

                if self.dashboard_message is None:
                    embed = await self.create_dashboard_embed()
                    self.dashboard_message = await channel.send(embed=embed)

    async def count_total_messages(self):
        """Counts the total messages in all text channels."""
        total_messages = 0
        guild = self.bot.guilds[0]  # Get the first guild

        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=None):  # Async iteration over history
                    total_messages += 1  # Count each message
            except discord.Forbidden:
                continue  # Skip channels the bot doesn't have permission to read

        return total_messages

    async def count_total_voice_time(self):
        """Counts the total voice time spent in all voice channels and converts to hours, minutes, seconds."""
        total_seconds = sum(user_data.get("total_time", 0) for user_data in self.user_voice_times.values())

        hours = int(total_seconds // 3600)  # Convert to integer
        minutes = int((total_seconds % 3600) // 60)  # Convert to integer
        seconds = int(total_seconds % 60)  # Convert to integer

        # Format with leading zeros
        return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

    async def update_dashboard(self):
        """Update the dashboard message with latest stats."""
        if self.dashboard_message:
            embed = await self.create_dashboard_embed()
            await self.dashboard_message.edit(embed=embed)

    async def create_dashboard_embed(self):
        """Create an embed with the latest stats."""
        guild = self.bot.guilds[0]  # Get the first guild
        total_members = guild.member_count
        online_members = sum(
            1 for m in guild.members if m.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd])
        total_messages = await self.count_total_messages()
        total_voice_time = await self.count_total_voice_time()

        embed = discord.Embed(title="📊 Server Dashboard", color=discord.Color.blue())
        embed.add_field(name="👥 Total Members", value=f"`{total_members}`", inline=True)
        embed.add_field(name="🟢 Online Members", value=f"`{online_members}`", inline=True)
        embed.add_field(name="💬 Total Messages", value=f"`{total_messages}`", inline=True)
        embed.add_field(name="🎤 Total Voice Time", value=f"`{total_voice_time}`", inline=True)
        embed.set_footer(text="Updated every 30 seconds")

        return embed

    @tasks.loop(seconds=30)
    async def update_server_stats(self):
        """Loop to update stats every 30 seconds."""
        await self.update_dashboard()

async def setup(bot):
    await bot.add_cog(DashBoard(bot))