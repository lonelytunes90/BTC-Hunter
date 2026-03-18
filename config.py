import os
from pathlib import Path

# --- Project Paths ---
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "list.txt"
HISTORY_FILE = BASE_DIR / "processed.log"
HITS_FILE = BASE_DIR / "found.txt"

# --- Telegram Settings ---
# Get from @BotFather and @userinfobot
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
ENABLE_TELEGRAM = True
REMOTE_CONTROL = True  
REPORT_INTERVAL = 3600  # Auto-status every 1 hour

# --- Scan Logic ---
THREADS = 8
DERIVATION_GAP = 100
BATCH_SIZE = 100
MIN_BATTERY = 15
