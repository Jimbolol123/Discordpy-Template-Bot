import discord
from discord.ext import commands
import random
import datetime

# In cogs we make our own class
# for d.py which subclasses commands.Cog


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has been loaded\n-----")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if str(channel) == "entrance":
                await channel.send(f"""Welcome to the server {member.mention}""")   



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) is 0 and int(m) is 0:
                await ctx.send(f' You must wait {int(s)} seconds to use this command!')
            elif int(h) is 0 and int(m) is not 0:
                await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("You are not allowed to use this command.")
        raise error

    @commands.Cog.listener()
    async def on_message_delete(self, msg):

        emb = discord.Embed(
            title=f'{msg.guild}',
            description=f'A message was deleted',
            colour=discord.Colour.red()
        )

        emb.add_field(name='Message Deleted', value=f'{msg.content}', inline=True)
        emb.add_field(name='Message Author', value=f'{msg.author}', inline=True)
        emb.set_thumbnail(url=msg.author.avatar_url)

        for chan in msg.guild.channels:
            if chan.name == 'bot-logs':
                await chan.send(embed=emb)
            
    @commands.Cog.listener()
    async def on_message_edit(self, bmsg, amsg):
        if bmsg.author == self.bot.user:
            return
        if amsg.author == self.bot.user:
            return
        emb = discord.Embed(title=f'{bmsg.author}', description=f'A message was edited', colour=discord.Colour.red())
        emb.add_field(name='Before', value=f'{bmsg.content}', inline=True)
        emb.add_field(name='After', value=f'{amsg.content}', inline=True)
        emb.set_thumbnail(url=bmsg.author.avatar_url)

        for chan in bmsg.guild.channels:
            if chan.name == 'bot-logs':
                await chan.send(embed=emb)

def setup(bot):
    bot.add_cog(Events(bot))
