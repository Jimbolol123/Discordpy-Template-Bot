# Libs
import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import datetime
import os

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

#Defining a few things
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix='!', case_insensitive=True, owner_id=YOURDISCORDID)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = '1.0'

bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

memberCount = len(set(bot.get_all_members()))

@bot.event
async def on_ready():
    # On ready, print some details to standard out
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: !\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Template Bot")) # This changes the bots 'activity'


@bot.event
async def on_message(message):
    #Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('I am not sure about that one... use !help.')

if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)
