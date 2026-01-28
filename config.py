import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for Banana Hub - Production Ready"""
    
    # ========== BOT SETTINGS ==========
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    PREFIX = os.getenv("PREFIX", "!")
    
    # ========== WEB SETTINGS ==========
    WEB_HOST = "0.0.0.0"  # Required for Render
    WEB_PORT = int(os.getenv("PORT", 5000))  # Render provides this
    
    # Base URLs (Render will provide these)
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
    WEBSITE_URL = os.getenv("WEBSITE_URL", "http://localhost:5000")
    
    # ========== DATABASE ==========
    DB_FILE = "data/banana_hub.db"
    
    # ========== SCRIPT ==========
    SCRIPT_FILE = "script.lua"
    
    # ========== ADMIN ==========
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "banana-admin-secret-2024-xyz789")
    OWNER_ID = int(os.getenv("OWNER_ID", "1269772767516033025"))
    ADMIN_IDS = []  # Add more admin IDs if needed
    
    # ========== DISCORD ==========
    GUILD_ID = os.getenv("GUILD_ID", None)  # Optional: for faster command sync
    
    # ========== MODE ==========
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # ========== COLORS ==========
    EMBED_COLOR = 0xFACC15  # Banana yellow
