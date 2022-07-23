from discord.ext import commands
from dotenv import load_dotenv
import os

bot = commands.Bot(debug_guilds=[879288794560471050])
load_dotenv()
TOKEN = os.getenv("TOKEN")

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

bot.load_extension('cogs.itudoko')
bot.load_extension('cogs.others')

bot.run(TOKEN)