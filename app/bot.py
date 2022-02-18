import os
import disnake
from disnake.ext import commands

from config import BOT_TOKEN

bot = commands.Bot(command_prefix=">", test_guilds=[676592448620724254])

print("Loading Cogs")
for cogs in os.listdir("./app/cogs"):
    if cogs.endswith(".py"):
        bot.load_extension(f"cogs.{cogs[:-3]}")
        print(f"{cogs} loaded")

@bot.event
async def on_ready():
    print(f"Bot User: {bot.user}")
    print(f"Bot UserID: {bot.user.id}")
    await bot.change_presence(
        status=disnake.Status,
        activity=disnake.Activity(type=disnake.ActivityType.watching, name="Karna.ge"),
    )


bot.run(BOT_TOKEN)
