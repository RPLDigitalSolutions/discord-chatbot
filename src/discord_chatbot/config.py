import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
NVIDIA_API_TOKEN = os.getenv("NVIDIA_API_TOKEN", "")
NVIDIA_MODEL_NAME = os.getenv("NVIDIA_MODEL_NAME", "meta/muse-glimmer-30b")
