import os
import disnake
import sys

from disnake.ext import commands
from pymongo import MongoClient
from cum import cum

from config import BOT_TOKEN, GUILD_ID

intents = disnake.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=">", test_guilds=[GUILD_ID], intents=intents)

cum()

print("Connecting to MongoDB")
mongo = MongoClient(
    os.getenv("MONGO_IP", "localhost"),
    int(os.getenv("MONGO_PORT", 27017))
)

try:
    mongo.server_info()
except Exception:
    sys.exit("Could not connect to MongoDB")

mongo = mongo[os.getenv("MONGO_DB", "karnagebot")]



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