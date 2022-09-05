import traceback
from discord.ext import commands
import os
from dotenv import load_dotenv
import discord
load_dotenv()

bot = commands.Bot(debug_guilds=[os.getenv('GUILD'), 782890710324084767])
TOKEN = os.getenv('TOKEN')
print(TOKEN)

path = "./cogs"


# @bot.event
# async def on_application_command_error(ctx: discord.ApplicationContext, error:Exception):
#     if isinstance(error, commands.CommandOnCooldown):
#         await ctx.respond(error, ephemeral=True)
#     else:
#         bot.get_partial_messageable(channel_id).send(traceback.format_exc())
#         raise error


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")

# bot.load_extension('cogs.others')
# bot.load_extension('cogs.itudoko')
# bot.load_extension('cogs.point')
# bot.load_extension('cogs.hogestory')
# bot.load_extension('cogs.superchat')
# bot.load_extension('cogs.help')
# bot.load_extension('cogs.todo')
# bot.load_extension('cogs.shogi')
# bot.load_extension('cogs.nb')
# bot.load_extension('cogs.keiba')
# # bot.load_extension('cogs.multiplay')
# bot.load_extension('cogs.stat')
# bot.load_extension('cogs.timer')
# bot.load_extension('cogs.talk')
# bot.load_extension(name='cogs.genshin', store=False)
# bot.load_extension('cogs.test')

bot.run(TOKEN)
