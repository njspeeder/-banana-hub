# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - DATABASE MODULE (FULLY FIXED)
# Thread-safe SQLite operations with proper connection management
# All methods use fresh connections - NO MORE CLOSED DATABASE ERRORS
# ==============================================================================

from __future__ import annotations

import logging
import os
import shutil
import sqlite3
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, Optional, List, Any

from config import Config

# ==============================================================================
# 🔧 LOGGING
# ==============================================================================

log = logging.getLogger("database")

# ==============================================================================
# 💾 DATABASE CLASS
# ==============================================================================

class Database:
    """
    Thread-safe SQLite database manager for Banana Hub.
    
    Every method creates its own fresh connection and closes it.
    No connection reuse = No closed database errors.
    """

    def __init__(self, filepath: str = "data/banana_hub.db"):
        """Initialize database."""
        self.filepath = filepath
        self._ensure_directory()
        self._initialize_schema()
        log.info(f"✅ Database initialized: {filepath}")

    def _ensure_directory(self) -> None:
        """Ensure data directory exists."""
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """
        Get a NEW database connection.
        
        Returns:
            sqlite3.Connection: Fresh database connection
        """
        conn = sqlite3.connect(
            self.filepath,
            check_same_thread=False,
            timeout=30.0
        )
        conn.row_factory = sqlite3.Row
        
        try:
            conn.execute("PRAGMA journal_mode=WAL")
        except:
            pass
        
        return conn

    def _initialize_schema(self) -> None:
        """Create database tables if they don't exist."""
        schema = """
        CREATE TABLE IF NOT EXISTS users (
            discord_id TEXT PRIMARY KEY,
            key TEXT,
            hwid TEXT,
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT
        );
        
        CREATE TABLE IF NOT EXISTS keys (
            key TEXT PRIMARY KEY,
            created_by TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            used INTEGER DEFAULT 0,
            used_by TEXT,
            used_at TEXT
        );
        
        CREATE TABLE IF NOT EXISTS blacklist (
            discord_id TEXT PRIMARY KEY,
            reason TEXT,
            banned_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            discord_id TEXT,
            ip_address TEXT,
            details TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_key ON users(key);
        CREATE INDEX IF NOT EXISTS idx_keys_used ON keys(used);
        CREATE INDEX IF NOT EXISTS idx_analytics_discord ON analytics(discord_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_event ON analytics(event_type);
        """
        
        conn = None
        try:
            conn = self.get_connection()
            conn.executescript(schema)
            conn.commit()
            log.info("✅ Database schema initialized")
        except Exception as e:
            log.error(f"❌ Failed to initialize schema: {e}")
            raise
        finally:
            if conn:
                conn.close()

    # ==========================================================================
    # 👤 USER OPERATIONS
    # ==========================================================================

    def register_user(self, discord_id: int | str, key: str) -> bool:
        """Register a new user or update existing user."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO users (discord_id, key, joined_at)
                VALUES (?, ?, ?)
                ON CONFLICT(discord_id) DO UPDATE SET key = excluded.key
                """,
                (discord_id_str, key, datetime.now(UTC).isoformat())
            )
            conn.commit()
            log.info(f"✅ Registered user: {discord_id_str} with key: {key}")
            return True
            
        except Exception as e:
            log.error(f"❌ Error registering user {discord_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_user(self, discord_id: int | str) -> Optional[Dict[str, Any]]:
        """Get user data by Discord ID."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id_str,))
            row = cur.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            log.error(f"Error getting user {discord_id}: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def update_last_login(self, discord_id: int | str, ip_address: Optional[str] = None) -> bool:
        """Update user's last login time."""
        discord_id_str = str(discord_id)
        timestamp = datetime.now(UTC).isoformat()
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET last_login = ? WHERE discord_id = ?",
                (timestamp, discord_id_str)
            )
            conn.commit()
            self.log_event("login", discord_id_str, ip_address, "User logged in")
            return True
            
        except Exception as e:
            log.error(f"Error updating last login for {discord_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def reset_hwid(self, discord_id: int | str) -> bool:
        """Reset user's HWID."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET hwid = NULL WHERE discord_id = ?", (discord_id_str,))
            rows_affected = cur.rowcount
            conn.commit()
            
            if rows_affected > 0:
                log.info(f"✅ Reset HWID for user: {discord_id_str}")
                return True
            return False
            
        except Exception as e:
            log.error(f"Error resetting HWID for {discord_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def unwhitelist(self, discord_id: int | str) -> int:
        """Remove a user's key (unwhitelist them)."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET key = NULL WHERE discord_id = ?", (discord_id_str,))
            rows_affected = cur.rowcount
            conn.commit()
            
            if rows_affected > 0:
                log.info(f"✅ Unwhitelisted user: {discord_id_str}")
            
            return rows_affected
            
        except Exception as e:
            log.error(f"Error unwhitelisting user {discord_id}: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    # ==========================================================================
    # 🔑 KEY OPERATIONS
    # ==========================================================================

    def generate_key_entry(self, key: str, created_by: int | str) -> bool:
        """Create a new key entry in database."""
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO keys (key, created_by, created_at) VALUES (?, ?, ?)",
                (key, str(created_by), datetime.now(UTC).isoformat())
            )
            conn.commit()
            log.info(f"✅ Generated key: {key}")
            return True
            
        except sqlite3.IntegrityError:
            log.warning(f"Key already exists: {key}")
            return False
        except Exception as e:
            log.error(f"Error generating key: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def check_key_available(self, key: str) -> bool:
        """Check if a key exists and is not used."""
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT used FROM keys WHERE key = ?", (key,))
            row = cur.fetchone()
            
            if row and row['used'] == 0:
                return True
            return False
            
        except Exception as e:
            log.error(f"Error checking key availability: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def mark_key_redeemed(self, key: str, discord_id: int | str) -> bool:
        """Mark a key as redeemed."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE keys SET used = 1, used_by = ?, used_at = ? WHERE key = ?",
                (discord_id_str, datetime.now(UTC).isoformat(), key)
            )
            conn.commit()
            log.info(f"✅ Marked key as redeemed: {key} by {discord_id_str}")
            return True
            
        except Exception as e:
            log.error(f"Error marking key as redeemed: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def redeem_key(self, discord_id: int | str, key: str) -> bool:
        """Redeem a key for a user (combined operation)."""
        if not self.register_user(discord_id, key):
            return False
        if not self.mark_key_redeemed(key, discord_id):
            return False
        return True

    # ==========================================================================
    # 🚫 BLACKLIST OPERATIONS
    # ==========================================================================

    def is_blacklisted(self, discord_id: int | str) -> bool:
        """Check if user is blacklisted."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM blacklist WHERE discord_id = ?", (discord_id_str,))
            result = cur.fetchone()
            return result is not None
            
        except Exception as e:
            log.error(f"Error checking blacklist: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def toggle_blacklist(self, discord_id: int | str, reason: str = "No reason") -> bool:
        """Toggle blacklist status for a user."""
        discord_id_str = str(discord_id)
        
        # Check if already blacklisted
        is_banned = self.is_blacklisted(discord_id_str)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            if is_banned:
                # Remove from blacklist
                cur.execute("DELETE FROM blacklist WHERE discord_id = ?", (discord_id_str,))
                conn.commit()
                log.info(f"✅ Removed from blacklist: {discord_id_str}")
                return False
            else:
                # Add to blacklist
                cur.execute(
                    "INSERT INTO blacklist (discord_id, reason, banned_at) VALUES (?, ?, ?)",
                    (discord_id_str, reason, datetime.now(UTC).isoformat())
                )
                conn.commit()
                log.info(f"✅ Added to blacklist: {discord_id_str} - Reason: {reason}")
                return True
                
        except Exception as e:
            log.error(f"Error toggling blacklist for {discord_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def unblacklist(self, discord_id: int | str) -> int:
        """Explicitly remove a user from blacklist."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM blacklist WHERE discord_id = ?", (discord_id_str,))
            rows_affected = cur.rowcount
            conn.commit()
            
            if rows_affected > 0:
                log.info(f"✅ Unblacklisted user: {discord_id_str}")
            
            return rows_affected
            
        except Exception as e:
            log.error(f"Error unblacklisting user {discord_id}: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    # ==========================================================================
    # 📊 ANALYTICS & LOGGING
    # ==========================================================================

    def log_event(
        self,
        event_type: str,
        discord_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[str] = None
    ) -> bool:
        """Log an event to analytics."""
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO analytics (event_type, discord_id, ip_address, details, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (event_type, discord_id, ip_address, details, datetime.now(UTC).isoformat())
            )
            conn.commit()
            return True
            
        except Exception as e:
            log.error(f"Error logging event: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_stats(self) -> Dict[str, int]:
        """Get system statistics."""
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Total users
            cur.execute("SELECT COUNT(*) FROM users")
            total_users = cur.fetchone()[0]
            
            # Available keys
            cur.execute("SELECT COUNT(*) FROM keys WHERE used = 0")
            available_keys = cur.fetchone()[0]
            
            # Total logins
            cur.execute("SELECT COUNT(*) FROM analytics WHERE event_type = 'login'")
            total_logins = cur.fetchone()[0]
            
            return {
                'total_users': total_users,
                'available_keys': available_keys,
                'total_logins': total_logins
            }
            
        except Exception as e:
            log.error(f"Error getting stats: {e}")
            return {
                'total_users': 0,
                'available_keys': 0,
                'total_logins': 0
            }
        finally:
            if conn:
                conn.close()

    # ==========================================================================
    # 🔧 UTILITY OPERATIONS
    # ==========================================================================

    def create_backup(self) -> str:
        """Create a backup of the database."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        backup_dir = "data/backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_path = os.path.join(backup_dir, f"banana_hub_backup_{timestamp}.db")
        
        try:
            shutil.copy2(self.filepath, backup_path)
            log.info(f"✅ Database backup created: {backup_path}")
            return backup_path
        except Exception as e:
            log.error(f"❌ Failed to create backup: {e}")
            raise

    def vacuum(self) -> bool:
        """Vacuum the database to optimize storage."""
        conn = None
        
        try:
            conn = self.get_connection()
            conn.execute("VACUUM")
            log.info("✅ Database vacuumed")
            return True
        except Exception as e:
            log.error(f"Error vacuuming database: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_all_users(self) -> List[Dict]:
        """Get all users from database."""
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users ORDER BY joined_at DESC")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            log.error(f"Error getting all users: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_all_keys(self, unused_only: bool = False) -> List[Dict]:
        """Get all keys from database."""
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            if unused_only:
                cur.execute("SELECT * FROM keys WHERE used = 0 ORDER BY created_at DESC")
            else:
                cur.execute("SELECT * FROM keys ORDER BY created_at DESC")
            
            rows = cur.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            log.error(f"Error getting keys: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_blacklisted_users(self) -> List[Dict]:
        """Get all blacklisted users."""
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM blacklist ORDER BY banned_at DESC")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            log.error(f"Error getting blacklisted users: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_user_analytics(self, discord_id: int | str) -> Dict[str, int]:
        """Get analytics for a specific user."""
        discord_id_str = str(discord_id)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Login count
            cur.execute(
                "SELECT COUNT(*) FROM analytics WHERE discord_id = ? AND event_type = 'login'",
                (discord_id_str,)
            )
            login_count = cur.fetchone()[0]
            
            # HWID reset count
            cur.execute(
                "SELECT COUNT(*) FROM analytics WHERE discord_id = ? AND event_type = 'hwid_reset'",
                (discord_id_str,)
            )
            reset_count = cur.fetchone()[0]
            
            return {
                'login_count': login_count,
                'reset_count': reset_count
            }
            
        except Exception as e:
            log.error(f"Error getting user analytics: {e}")
            return {
                'login_count': 0,
                'reset_count': 0
            }
        finally:
            if conn:
                conn.close()


# ==============================================================================
# 🌍 GLOBAL DATABASE INSTANCE
# ==============================================================================

# Initialize global database instance
db = Database(filepath=Config.DB_FILE)

# Optimize database on startup
try:
    db.vacuum()
    log.info("✅ Database ready and optimized")
except Exception as e:
    log.warning(f"Could not vacuum database: {e}")
