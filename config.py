# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - CONFIGURATION
# ==============================================================================

from __future__ import annotations  # ✅ MUST BE FIRST!

import os
from pathlib import Path

class Config:
    """
    Centralized configuration for Banana Hub Enterprise.
    Uses environment variables for sensitive data.
    """
    
    # ===========================================================================
    # 🔐 CRITICAL SECURITY SETTINGS
    # ===========================================================================
    
    # 🚨 SECURITY WARNING: Your token is exposed! Reset it immediately at:
    # https://discord.com/developers/applications
    
    # Discord Bot Token - NEVER commit this to Git!
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "MTQ0MzYzODYyODgyMjU0ODUyMg.Gxoatx.e6QlfF592XZhkH4I6Sd2zbH2KESI1QkR80ejfg")
    
    # Owner/Admin Configuration
    OWNER_ID = 1242609091294003221  # Your Discord ID
    ADMIN_IDS = [
        1242609091294003221,  # Add more admin user IDs here
    ]
    
    # Admin API Key for web panel (change this!)
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "your-secret-admin-key-change-this")
    
    # ===========================================================================
    # 🤖 BOT SETTINGS
    # ===========================================================================
    
    PREFIX = "!"  # Legacy prefix (not used for slash commands)
    GUILD_ID = 1443637894647513142  # Your development server ID
    
    # ===========================================================================
    # 🌐 NETWORK SETTINGS
    # ===========================================================================
    
    # Flask Web Server
    WEB_HOST = '0.0.0.0'
    WEB_PORT = 5000
    
    # URLs (change for production/ngrok)
    BASE_URL = os.getenv("BASE_URL", f"http://localhost:{WEB_PORT}")
    WEBSITE_URL = os.getenv("WEBSITE_URL", BASE_URL)
    
    # Environment Detection
    ENV = os.getenv("ENV", "development")
    DEBUG = ENV == "development"
    
    # ===========================================================================
    # 💾 DATABASE SETTINGS
    # ===========================================================================
    
    # Paths
    BASE_DIR = Path(__file__).parent.resolve()
    DATA_DIR = BASE_DIR / "data"
    BACKUP_DIR = DATA_DIR / "backups"
    
    # Database file
    DB_FILE = str(DATA_DIR / "enterprise.db")
    
    # Backup settings
    AUTO_BACKUP_HOURS = 24
    MAX_BACKUPS = 7
    
    # ===========================================================================
    # 📁 FILE PATHS
    # ===========================================================================
    
    SCRIPT_FILE = str(BASE_DIR / "script.lua")
    LOG_FILE = str(DATA_DIR / "system.log")
    
    # ===========================================================================
    # 🎭 DISCORD ROLES
    # ===========================================================================
    
    ROLES = {
        "BUYER": "Premium User",
        "ADMIN": "Administrator",
        "RESELLER": "Reseller",
        "RESET_BYPASS": "Reset Bypass"
    }
    
    # ===========================================================================
    # 🎨 VISUAL ASSETS
    # ===========================================================================
    
    EMBED_COLOR = 0xFACC15
    LOGO_URL = "https://em-content.zobj.net/source/microsoft-teams/337/banana_1f34c.png"
    ICON_URL = "https://em-content.zobj.net/source/microsoft-teams/337/banana_1f34c.png"
    BANNER_URL = "https://dummyimage.com/600x200/000/fff&text=BananaHub+Enterprise"
    
    # ===========================================================================
    # 📜 SCRIPT METADATA
    # ===========================================================================
    
    SCRIPT_VERSION = "V80.1.0-Enterprise"
    SCRIPT_STATUS = "🟢 Undetected"
    LAST_UPDATE = "2025-11-29"
    
    # ===========================================================================
    # ⚙️ FEATURE TOGGLES
    # ===========================================================================
    
    ENABLE_ANALYTICS = True
    ENABLE_RATE_LIMITING = True
    ENABLE_AUTO_BACKUP = True
    ENABLE_LOGGING = True
    
    # ===========================================================================
    # 🚀 INITIALIZATION
    # ===========================================================================
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Directories initialized:")
        print(f"   📁 Data: {cls.DATA_DIR}")
        print(f"   📁 Backups: {cls.BACKUP_DIR}")


# Initialize directories on import
Config.setup_directories()
