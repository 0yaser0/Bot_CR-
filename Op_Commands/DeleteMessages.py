import discord
from discord.ext import commands

class DeleteMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="del")
    @commands.has_permissions(administrator=True)
    async def delete_messages(self, ctx, number: int):
        # Check if the command is used in a text channel
        if not isinstance(ctx.channel, discord.TextChannel):
            await ctx.send("This command can only be used in text channels.")
            return

        # Fetch the last 'number' messages in the channel
        messages_to_delete = []
        async for message in ctx.channel.history(limit=number):
            messages_to_delete.append(message)
            print(f"Message to delete: {message.author} - {message.content}")

        # Delete the messages
        if messages_to_delete:
            try:
                await ctx.channel.delete_messages(messages_to_delete)
                print(f"Deleted {len(messages_to_delete)} messages in #{ctx.channel.name}.")
            except discord.Forbidden:
                print("The bot does not have permission to delete messages in this channel.")
            except discord.HTTPException as e:
                print(f"Failed to delete messages: {e}")
        else:
            print("No messages to delete.")

async def setup(bot):
    await bot.add_cog(DeleteMessages(bot))