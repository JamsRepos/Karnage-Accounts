import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
JFA_GO_API_KEY = os.getenv("JFA_GO_API_KEY")
OMBI_API_KEY = os.getenv("OMBI_API_KEY")
