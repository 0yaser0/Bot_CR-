import discord
from discord.ext import commands

class MembersState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def online_members(self, ctx):
        guild = ctx.guild
        online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
        await ctx.send(f"Number of online members: {online_members}")

async def setup(bot):
    await bot.add_cog(MembersState(bot))