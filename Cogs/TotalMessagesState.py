import discord
from discord.ext import commands

class TotalMessageState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_count = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots and DMs
        if not message.author.bot and message.guild:
            self.message_count += 1

    @commands.command()
    async def total_messages(self, ctx):
        await ctx.send(f"Total messages sent in the server: {self.message_count}")

async def setup(bot):
    await bot.add_cog(TotalMessageState(bot))