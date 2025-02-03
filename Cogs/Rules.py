import discord
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.send_rules_image()

    async def send_rules_image(self):
        guild = self.bot.guilds[0]  # Assuming the bot is in at least one server
        channel = discord.utils.get(guild.text_channels, name="•📚•-rules-of-the-server")

        rules = "** ١. إحترام جميع الموجودين في السيرفر **.......................................\n** ٢. عدم العنصريه القبلية او الدينيه **..............................................\n** ٣. عدم التدخل في المواضيع السياسيه او الدينيه **............................\n** ٤. ممنوع طلب الرتب مهما كانت قرابتك من الإدارة **.........................\n**٥. اذا واجهتك مشكله تواصل مع اي اداري**.....................................\n** ٦. يمنع الشتم حتى لو عن طريق المزح او حتى مع صديقك** ................\n**٧. يمنع تقمص دور الاداري في السيرفر**.........................................\n**٨. في حال وجود إنتهاك للقوانين من احد المشرفين يرجى ابلاغ الإدارة**..\n**٩. قراءة القوانين الدسكورد كل فترة لأنها قد تتغير في أي وقت**.............\n**١٠. اذا كنت تريد اي مساعد ابلغ الإدارة**............................................\n\n"

        if channel:
            # Delete previous bot messages in the channel
            async for message in channel.history(limit=100):
                if message.author == self.bot.user:
                    await message.delete()

            embed = discord.Embed(
                title="**                    :black_heart: Robotics Club :black_heart:  حياكم الله في السيرفر                  **\n **يفضل قراءة القوانين كاملة                                         **\n\n ",
                description=rules,
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Other suggestions:",
                value="Introduce yourself \nAsk questions \nRa7na gha f discord"
            )
            embed.set_footer(
                text="Have a Fun asahbi✨🖤"
            )

            await channel.send(embed=embed)

        else:
         print("Channel not found")


# Required setup function
async def setup(bot):
    await bot.add_cog(Rules(bot))
