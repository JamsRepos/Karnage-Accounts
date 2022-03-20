import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
# TODO: Remove this when this goes live.
TEST_GUILD = int(os.getenv("TEST_GUILD"))
# TODO: Deprecate this for the database version.
MEMBERSHIP_ROLES = os.getenv("MEMBERSHIP_ROLES").split(",")
JFA_USERNAME = os.getenv("JFA_USERNAME")
JFA_PASSWORD = os.getenv("JFA_PASSWORD")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
OMBI_API_KEY = os.getenv("OMBI_API_KEY")
MONGO_IP = os.getenv("MONGO_IP")
MONGO_PORT = os.getenv("MONGO_PORT")
WORK_DIR = os.getenv("WORK_DIR")