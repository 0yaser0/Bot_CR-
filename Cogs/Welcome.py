import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="•👋•-joins")
        if channel:
            embed = discord.Embed(
                title="🎉 Welcome to the Robotics Club's Server! 🎉",
                description=f"Hey {member.mention}, we're happy to have you here!\nMake sure to check out the rules and introduce yourself!\n ",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.add_field(name="📜 Rules", value="Make sure to check out `#⦿📚⦿-rules-of-the-server`", inline=False)
            embed.add_field(name="💬 Engage", value="Join discussions in `#「💬」main-chat`", inline=False)
            embed.set_footer(text="Enjoy your stay!", icon_url="https://cdn-icons-png.flaticon.com/512/1035/1035670.png")

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
