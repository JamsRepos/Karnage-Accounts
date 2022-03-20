import os
import disnake
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from disnake.ext import commands
from cum import cum

from config import BOT_TOKEN, GUILD_ID

intents = disnake.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", test_guilds=[GUILD_ID], intents=intents, )

cum()

mongo = AsyncIOMotorClient(
    os.getenv("MONGO_IP", "localhost"),
    int(os.getenv("MONGO_PORT", 27017))
)

try:
    mongo.server_info()
    mongo = mongo[os.getenv("MONGO_DB", "karnagebot")]
    print("Connected to MongoDB")
except Exception:
    sys.exit("Could not connect to MongoDB")



print("Loading Cogs:")
for cogs in os.listdir("/app/cogs"):
    if cogs.endswith(".py"):
        bot.load_extension(f"cogs.{cogs[:-3]}")
        print(f"    - {cogs[:-3].capitalize()} loaded!")

@bot.event
async def on_ready():
    print(f"Bot User: {bot.user}")
    print(f"Bot UserID: {bot.user.id}")
    await bot.change_presence(
        status=disnake.Status,
        activity=disnake.Activity(type=disnake.ActivityType.watching, name="Karna.ge"),
    )

bot.run(BOT_TOKEN)