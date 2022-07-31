from discord.ext import commands
import os
import dotenv

if os.getenv('TOKEN') == None:
    dotenv.load_dotenv('../.env')


bot = commands.Bot(debug_guilds=[int(os.getenv('GUILD'))])
TOKEN = os.getenv('TOKEN')
print(TOKEN)

path = "./cogs"


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error, ephemeral=True)
    else:
        raise error


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")

bot.load_extension('cogs.others')
bot.load_extension('cogs.itudoko')
# bot.load_extension('cogs.point')
bot.load_extension('cogs.hogestory')
bot.load_extension('cogs.superchat')

bot.run(TOKEN)
