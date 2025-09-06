import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    raise RuntimeError("Переменная окружения BOT_TOKEN не установлена")

VOTING_URL = "https://burgerkingapp.onelink.me/220f/u7awyumy"
