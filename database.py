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
import random
import string
import uuid
import secrets
import hashlib
from datetime import datetime, UTC, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Any

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

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

        CREATE TABLE IF NOT EXISTS trials (
            key TEXT PRIMARY KEY,
            discord_id TEXT,
            created_at TEXT,
            expires_at TEXT,
            ip_address TEXT
        );

        CREATE TABLE IF NOT EXISTS trial_sessions (
            token TEXT PRIMARY KEY,
            discord_id TEXT,
            created_at TEXT,
            expires_at TEXT,
            step1_done INTEGER DEFAULT 0,
            step2_done INTEGER DEFAULT 0,
            ip_address TEXT
        );

        -- New accounts table for username/password authentication
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            email_verified INTEGER DEFAULT 0,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (discord_id) REFERENCES users(discord_id)
        );

        -- Email verification codes
        CREATE TABLE IF NOT EXISTS email_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT NOT NULL,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_key ON users(key);
        CREATE INDEX IF NOT EXISTS idx_keys_used ON keys(used);
        CREATE INDEX IF NOT EXISTS idx_analytics_discord ON analytics(discord_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_event ON analytics(event_type);
        CREATE INDEX IF NOT EXISTS idx_trials_discord ON trials(discord_id);
        CREATE INDEX IF NOT EXISTS idx_trial_sessions_discord ON trial_sessions(discord_id);
        CREATE INDEX IF NOT EXISTS idx_accounts_username ON accounts(username);
        CREATE INDEX IF NOT EXISTS idx_accounts_discord ON accounts(discord_id);
        CREATE INDEX IF NOT EXISTS idx_email_codes_discord ON email_codes(discord_id);
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
    # ⏱️ TRIAL OPERATIONS
    # ==========================================================================

    def _generate_trial_key(self) -> str:
        chars = string.ascii_uppercase + string.digits
        part1 = ''.join(random.choices(chars, k=4))
        part2 = ''.join(random.choices(chars, k=4))
        return f"TRIAL-{part1}-{part2}"

    def get_trial_by_key(self, key: str) -> Optional[Dict[str, Any]]:
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM trials WHERE key = ?", (key,))
            row = cur.fetchone()
            return dict(row) if row else None
        except Exception as e:
            log.error(f"Error getting trial by key: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_active_trial_by_user(self, discord_id: int | str) -> Optional[Dict[str, Any]]:
        discord_id_str = str(discord_id)
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM trials WHERE discord_id = ? ORDER BY created_at DESC LIMIT 1",
                (discord_id_str,)
            )
            row = cur.fetchone()
            if not row:
                return None
            trial = dict(row)
            expires_at = trial.get("expires_at")
            if not expires_at:
                return None
            if datetime.fromisoformat(expires_at) <= datetime.now(UTC):
                return None
            return trial
        except Exception as e:
            log.error(f"Error getting trial for user: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def create_trial(self, discord_id: int | str, ip_address: Optional[str] = None, hours: int = 24) -> Optional[Dict[str, Any]]:
        discord_id_str = str(discord_id)
        now = datetime.now(UTC)
        expires = now + timedelta(hours=hours)
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            # Reuse active trial if exists
            cur.execute(
                "SELECT * FROM trials WHERE discord_id = ? ORDER BY created_at DESC LIMIT 1",
                (discord_id_str,)
            )
            row = cur.fetchone()
            if row:
                trial = dict(row)
                expires_at = trial.get("expires_at")
                if expires_at and datetime.fromisoformat(expires_at) > now:
                    return trial

            key = self._generate_trial_key()
            cur.execute(
                "INSERT INTO trials (key, discord_id, created_at, expires_at, ip_address) VALUES (?, ?, ?, ?, ?)",
                (key, discord_id_str, now.isoformat(), expires.isoformat(), ip_address)
            )
            conn.commit()
            return {
                "key": key,
                "discord_id": discord_id_str,
                "created_at": now.isoformat(),
                "expires_at": expires.isoformat(),
                "ip_address": ip_address
            }
        except Exception as e:
            log.error(f"Error creating trial: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # =======================================================================
    # 🧭 TRIAL SESSION FLOW (LINKVERTISE STEPS)
    # =======================================================================

    def create_trial_session(self, discord_id: int | str, ip_address: Optional[str] = None, hours: int = 2) -> Optional[Dict[str, Any]]:
        discord_id_str = str(discord_id)
        now = datetime.now(UTC)
        expires = now + timedelta(hours=hours)
        token = str(uuid.uuid4())
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO trial_sessions (token, discord_id, created_at, expires_at, step1_done, step2_done, ip_address)
                VALUES (?, ?, ?, ?, 0, 0, ?)
                """,
                (token, discord_id_str, now.isoformat(), expires.isoformat(), ip_address)
            )
            conn.commit()
            return {
                "token": token,
                "discord_id": discord_id_str,
                "created_at": now.isoformat(),
                "expires_at": expires.isoformat(),
                "step1_done": 0,
                "step2_done": 0,
                "ip_address": ip_address
            }
        except Exception as e:
            log.error(f"Error creating trial session: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_trial_session(self, token: str) -> Optional[Dict[str, Any]]:
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM trial_sessions WHERE token = ?", (token,))
            row = cur.fetchone()
            if not row:
                return None
            session = dict(row)
            expires_at = session.get("expires_at")
            if expires_at and datetime.fromisoformat(expires_at) <= datetime.now(UTC):
                return None
            return session
        except Exception as e:
            log.error(f"Error getting trial session: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def mark_trial_step1(self, token: str) -> bool:
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE trial_sessions SET step1_done = 1 WHERE token = ?", (token,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            log.error(f"Error marking step1: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def mark_trial_step2(self, token: str) -> bool:
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE trial_sessions SET step2_done = 1 WHERE token = ?", (token,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            log.error(f"Error marking step2: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def delete_trial_session(self, token: str) -> None:
        conn = None
        try:
            conn = self.get_connection()
            conn.execute("DELETE FROM trial_sessions WHERE token = ?", (token,))
            conn.commit()
        except Exception as e:
            log.error(f"Error deleting trial session: {e}")
        finally:
            if conn:
                conn.close()

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


    # ==========================================================================
    # 🔐 ACCOUNT OPERATIONS (Username/Password Auth)
    # ==========================================================================

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt or fallback."""
        if BCRYPT_AVAILABLE:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            # Fallback: SHA256 with salt (less secure, but works without bcrypt)
            salt = secrets.token_hex(16)
            hashed = hashlib.sha256((salt + password).encode()).hexdigest()
            return f"{salt}${hashed}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        if BCRYPT_AVAILABLE:
            try:
                return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
            except Exception:
                return False
        else:
            # Fallback verification
            try:
                salt, hashed = password_hash.split('$')
                return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
            except Exception:
                return False

    def check_username_available(self, username: str) -> bool:
        """Check if username is available."""
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM accounts WHERE LOWER(username) = LOWER(?)", (username,))
            return cur.fetchone() is None
        except Exception as e:
            log.error(f"Error checking username: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def create_account(self, discord_id: int | str, email: str, username: str, password: str) -> bool:
        """Create a new account with username/password."""
        discord_id_str = str(discord_id)
        password_hash = self.hash_password(password)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO accounts (discord_id, email, email_verified, username, password_hash, created_at)
                VALUES (?, ?, 1, ?, ?, ?)
                """,
                (discord_id_str, email, username, password_hash, datetime.now(UTC).isoformat())
            )
            conn.commit()
            log.info(f"✅ Created account for user: {discord_id_str} with username: {username}")
            return True
        except sqlite3.IntegrityError as e:
            log.warning(f"Account creation failed (duplicate): {e}")
            return False
        except Exception as e:
            log.error(f"Error creating account: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_account_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get account by username for login."""
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM accounts WHERE LOWER(username) = LOWER(?)", (username,))
            row = cur.fetchone()
            return dict(row) if row else None
        except Exception as e:
            log.error(f"Error getting account by username: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_account_by_discord(self, discord_id: int | str) -> Optional[Dict[str, Any]]:
        """Get account by Discord ID."""
        discord_id_str = str(discord_id)
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM accounts WHERE discord_id = ?", (discord_id_str,))
            row = cur.fetchone()
            return dict(row) if row else None
        except Exception as e:
            log.error(f"Error getting account by discord: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # ==========================================================================
    # 📧 EMAIL VERIFICATION OPERATIONS
    # ==========================================================================

    def store_email_code(self, discord_id: int | str, email: str, code: str, expires_minutes: int = 10) -> bool:
        """Store an email verification code."""
        discord_id_str = str(discord_id)
        now = datetime.now(UTC)
        expires_at = now + timedelta(minutes=expires_minutes)
        conn = None
        
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            # Delete any existing codes for this user
            cur.execute("DELETE FROM email_codes WHERE discord_id = ?", (discord_id_str,))
            # Insert new code
            cur.execute(
                """
                INSERT INTO email_codes (discord_id, email, code, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (discord_id_str, email, code, now.isoformat(), expires_at.isoformat())
            )
            conn.commit()
            log.info(f"✅ Stored email code for: {discord_id_str}")
            return True
        except Exception as e:
            log.error(f"Error storing email code: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def verify_email_code(self, discord_id: int | str, code: str) -> Optional[str]:
        """Verify email code and return email if valid."""
        discord_id_str = str(discord_id)
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT email, expires_at FROM email_codes WHERE discord_id = ? AND code = ?",
                (discord_id_str, code)
            )
            row = cur.fetchone()
            
            if not row:
                return None
            
            expires_at = datetime.fromisoformat(row['expires_at'])
            if expires_at <= datetime.now(UTC):
                # Code expired
                cur.execute("DELETE FROM email_codes WHERE discord_id = ?", (discord_id_str,))
                conn.commit()
                return None
            
            # Valid code - delete it and return email
            email = row['email']
            cur.execute("DELETE FROM email_codes WHERE discord_id = ?", (discord_id_str,))
            conn.commit()
            return email
        except Exception as e:
            log.error(f"Error verifying email code: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_pending_email(self, discord_id: int | str) -> Optional[str]:
        """Get pending email for a user's verification."""
        discord_id_str = str(discord_id)
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT email FROM email_codes WHERE discord_id = ?", (discord_id_str,))
            row = cur.fetchone()
            return row['email'] if row else None
        except Exception as e:
            log.error(f"Error getting pending email: {e}")
            return None
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
