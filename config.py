import os
from dotenv import load_dotenv

load_dotenv()

TAIGA_HOST = os.environ['TAIGA_HOST']
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']

TARGET_MILESTONES = [
    {
        "project_id": 1,
        "milestone_id": 1,
    }
]

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["TARGET_CHAT_ID"]
