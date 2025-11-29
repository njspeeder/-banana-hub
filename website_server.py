# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - FLASK WEB SERVER v2.1 (FINAL)
# Complete web server with all fixes - Dashboard working!
# ==============================================================================

from __future__ import annotations

import logging
import os
from datetime import datetime
from functools import wraps
from typing import Any, Dict, Optional

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from config import Config
from database import db
from web_templates import WebTemplates

# ==============================================================================
# 🔧 FLASK APP SETUP
# ==============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for API access
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Setup logging
log = logging.getLogger("website_server")
log.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)

# ==============================================================================
# 🔨 HELPER FUNCTIONS
# ==============================================================================

def render_page(template: str, **context) -> str:
    """Render a template with context replacements (no Jinja2 needed)."""
    # Always include config
    context['config'] = Config
    
    # Replace stats placeholders (for admin page)
    if 'stats' in context:
        stats = context['stats']
        template = template.replace('STATS_TOTAL_USERS', str(stats.get('total_users', 0)))
        template = template.replace('STATS_TOTAL_KEYS', str(stats.get('total_keys', 0)))
        template = template.replace('STATS_AVAILABLE_KEYS', str(stats.get('available_keys', 0)))
        template = template.replace('STATS_TOTAL_LOGINS', str(stats.get('total_logins', 0)))
        template = template.replace('STATS_BLACKLISTED', str(stats.get('blacklisted_users', 0)))
    
    # Replace config API key (for admin page JavaScript)
    template = template.replace('CONFIG_API_KEY', Config.ADMIN_API_KEY)
    
    return template


def require_api_key(f):
    """Decorator to require admin API key for protected endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        expected = f"Bearer {Config.ADMIN_API_KEY}"
        
        if auth_header != expected:
            log.warning(f"Unauthorized API access attempt from {request.remote_addr}")
            return jsonify({
                "success": False,
                "status": "error",
                "message": "Unauthorized - Invalid API key",
                "data": {}
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def validate_discord_id(discord_id: str) -> bool:
    """Validate Discord ID format (17-20 digit snowflake)."""
    return discord_id.isdigit() and 17 <= len(discord_id) <= 20


def validate_key_format(key: str) -> bool:
    """Validate Banana Hub key format."""
    import re
    return bool(re.match(r'^BANANA-[A-Z0-9]{12,}$', key.strip().upper()))


# ==============================================================================
# 🌐 PUBLIC WEB ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Landing page with stats."""
    try:
        stats = db.get_stats()
    except Exception as e:
        log.error(f"Error loading stats: {e}")
        stats = {
            'total_users': 0,
            'available_keys': 0,
            'total_logins': 0
        }
    
    return render_page(WebTemplates.LANDING, stats=stats)


@app.route('/login')
def login():
    """Login page."""
    return render_page(WebTemplates.LOGIN)


@app.route('/dashboard')
def dashboard():
    """User dashboard (client-side auth via localStorage)."""
    try:
        return render_page(WebTemplates.DASHBOARD)
    except Exception as e:
        log.error(f"Dashboard error: {e}", exc_info=True)
        return f"<h1>Error Loading Dashboard</h1><pre>{str(e)}</pre>", 500


@app.route('/admin')
def admin_panel():
    """Admin dashboard with full statistics."""
    try:
        # Get basic stats
        stats = db.get_stats()
        
        # Get additional stats
        conn = db.get_connection()
        cur = conn.cursor()
        
        # Total keys (all)
        cur.execute("SELECT COUNT(*) FROM keys")
        stats['total_keys'] = cur.fetchone()[0]
        
        # Blacklisted users
        cur.execute("SELECT COUNT(*) FROM blacklist")
        stats['blacklisted_users'] = cur.fetchone()[0]
        
        conn.close()
        
    except Exception as e:
        log.error(f"Error loading admin stats: {e}")
        stats = {
            'total_users': 0,
            'total_keys': 0,
            'available_keys': 0,
            'total_logins': 0,
            'blacklisted_users': 0
        }
    
    return render_page(WebTemplates.ADMIN, stats=stats)


@app.route('/script.lua')
def get_script():
    """Serve the Roblox script file."""
    try:
        if os.path.exists(Config.SCRIPT_FILE):
            return send_file(Config.SCRIPT_FILE, mimetype='text/plain')
        else:
            log.error(f"Script file not found: {Config.SCRIPT_FILE}")
            return "-- Script file not found", 404
    except Exception as e:
        log.error(f"Error serving script: {e}")
        return f"-- Error loading script: {e}", 500


# ==============================================================================
# 🔐 AUTHENTICATION API
# ==============================================================================

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    """Authenticate user with Discord ID and key."""
    try:
        data = request.get_json() or {}
        uid = str(data.get('uid', '')).strip()
        key = str(data.get('key', '')).strip().upper()
        
        if not uid or not key:
            return jsonify({
                "success": False,
                "message": "Missing Discord ID or key"
            }), 400
        
        if not validate_discord_id(uid):
            return jsonify({
                "success": False,
                "message": "Invalid Discord ID format"
            }), 400
        
        # Check if blacklisted
        if db.is_blacklisted(uid):
            return jsonify({
                "success": False,
                "message": "Account is blacklisted"
            }), 403
        
        # Get user
        user = db.get_user(uid)
        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401
        
        # Verify key
        if user.get('key') != key:
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401
        
        # Update last login
        try:
            db.update_last_login(uid, request.remote_addr)
        except:
            pass
        
        log.info(f"✅ User login: {uid}")
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "discord_id": uid,
                "key": key
            }
        })
        
    except Exception as e:
        log.error(f"Login error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/auth/redeem', methods=['POST'])
def auth_redeem():
    """Redeem a license key."""
    try:
        data = request.get_json() or {}
        uid = str(data.get('uid', '')).strip()
        key = str(data.get('key', '')).strip().upper()
        
        if not uid or not key:
            return jsonify({
                "success": False,
                "message": "Missing Discord ID or key"
            }), 400
        
        if not validate_discord_id(uid):
            return jsonify({
                "success": False,
                "message": "Invalid Discord ID"
            }), 400
        
        if not validate_key_format(key):
            return jsonify({
                "success": False,
                "message": "Invalid key format"
            }), 400
        
        # Check if key is available
        if not db.check_key_available(key):
            return jsonify({
                "success": False,
                "message": "Key is invalid or already used"
            }), 400
        
        # Check if user already has a key
        existing = db.get_user(uid)
        if existing and existing.get('key'):
            return jsonify({
                "success": False,
                "message": "You already have an active key"
            }), 400
        
        # Redeem key
        try:
            db.register_user(uid, key)
            db.mark_key_redeemed(key, uid)
            db.log_event("key_redeemed", uid, request.remote_addr, f"Redeemed {key}")
        except Exception as e:
            log.error(f"Error redeeming key: {e}")
            return jsonify({
                "success": False,
                "message": "Failed to redeem key"
            }), 500
        
        log.info(f"✅ Key redeemed: {key} by user {uid}")
        
        return jsonify({
            "success": True,
            "status": "ok",
            "message": "Key redeemed successfully"
        })
        
    except Exception as e:
        log.error(f"Redeem error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/auth/user_data', methods=['POST'])
def auth_user_data():
    """Get user dashboard data."""
    try:
        data = request.get_json() or {}
        uid = str(data.get('uid', '')).strip()
        key = str(data.get('key', '')).strip().upper()
        
        if not uid or not key:
            return jsonify({
                "success": False,
                "message": "Missing credentials"
            }), 400
        
        # Get user
        user = db.get_user(uid)
        if not user or user.get('key') != key:
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401
        
        # Get login count
        login_count = 0
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM analytics WHERE discord_id = ? AND event_type = 'login'",
                (uid,)
            )
            login_count = cur.fetchone()[0]
            conn.close()
        except Exception as e:
            log.error(f"Error getting login count: {e}")
        
        # Generate loader script
        loader_script = f"""-- 🍌 BANANA HUB ENTERPRISE LOADER
-- Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
-- User: {uid}

getgenv().BananaKey = "{key}"
getgenv().BananaID = "{uid}"
loadstring(game:HttpGet("{Config.BASE_URL}/script.lua"))()
"""
        
        return jsonify({
            "success": True,
            "user": {
                "discord_id": uid,
                "key": key,
                "hwid": user.get('hwid'),
                "hwid_set": bool(user.get('hwid')),
                "joined_at": user.get('joined_at'),
                "last_login": user.get('last_login'),
                "login_count": login_count
            },
            "script": loader_script
        })
        
    except Exception as e:
        log.error(f"User data error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset_hwid():
    """Reset user's HWID."""
    try:
        data = request.get_json() or {}
        uid = str(data.get('uid', '')).strip()
        
        if not uid:
            return jsonify({
                "success": False,
                "message": "Missing Discord ID"
            }), 400
        
        success = db.reset_hwid(uid)
        
        if success:
            db.log_event("hwid_reset", uid, request.remote_addr, "User reset via web")
            log.info(f"🔄 HWID reset for user {uid}")
            
            return jsonify({
                "success": True,
                "message": "HWID reset successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
            
    except Exception as e:
        log.error(f"HWID reset error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# ==============================================================================
# 🛡️ ADMIN API ENDPOINTS
# ==============================================================================

@app.route('/api/admin/genkey', methods=['POST'])
@require_api_key
def admin_genkey():
    """Generate new license keys (admin only)."""
    try:
        data = request.get_json() or {}
        amount = int(data.get('amount', 1))
        
        if amount < 1 or amount > 25:
            return jsonify({
                "success": False,
                "message": "Amount must be between 1 and 25"
            }), 400
        
        keys = []
        import secrets
        import string
        
        for _ in range(amount):
            # Generate key
            alphabet = string.ascii_uppercase + string.digits
            body = ''.join(secrets.choice(alphabet) for _ in range(12))
            key = f"BANANA-{body}"
            
            if db.generate_key_entry(key, "admin"):
                keys.append(key)
        
        log.info(f"🔑 Admin generated {len(keys)} keys")
        
        return jsonify({
            "success": True,
            "message": f"Generated {len(keys)} keys",
            "data": {
                "keys": keys,
                "count": len(keys)
            }
        })
        
    except Exception as e:
        log.error(f"Key generation error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/admin/keys', methods=['GET'])
@require_api_key
def admin_keys():
    """Get all license keys (admin only)."""
    try:
        unused_only = request.args.get('unused_only', 'false').lower() == 'true'
        
        conn = db.get_connection()
        cur = conn.cursor()
        
        if unused_only:
            cur.execute("SELECT * FROM keys WHERE used = 0 ORDER BY created_at DESC")
        else:
            cur.execute("SELECT * FROM keys ORDER BY created_at DESC")
        
        keys = []
        for row in cur.fetchall():
            keys.append({
                "key": row['key'],
                "created_by": row['created_by'],
                "created_at": row['created_at'],
                "used": bool(row['used']),
                "used_by": row['used_by'],
                "used_at": row['used_at']
            })
        
        conn.close()
        
        return jsonify({
            "success": True,
            "keys": keys,
            "count": len(keys)
        })
        
    except Exception as e:
        log.error(f"Error fetching keys: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/admin/users', methods=['GET'])
@require_api_key
def admin_users():
    """Get all users (admin only)."""
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY joined_at DESC")
        
        users = []
        for row in cur.fetchall():
            users.append({
                "discord_id": row['discord_id'],
                "key": row['key'],
                "hwid": row['hwid'],
                "joined_at": row['joined_at'],
                "last_login": row['last_login']
            })
        
        conn.close()
        
        return jsonify({
            "success": True,
            "users": users,
            "count": len(users)
        })
        
    except Exception as e:
        log.error(f"Error fetching users: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/admin/lookup', methods=['GET'])
@require_api_key
def admin_lookup():
    """Lookup user by Discord ID (admin only)."""
    try:
        discord_id = request.args.get('discord_id', '').strip()
        
        if not discord_id:
            return jsonify({
                "success": False,
                "message": "Missing discord_id parameter"
            }), 400
        
        user = db.get_user(discord_id)
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
        
        # Get analytics
        login_count = 0
        reset_count = 0
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            
            cur.execute(
                "SELECT COUNT(*) FROM analytics WHERE discord_id = ? AND event_type = 'login'",
                (discord_id,)
            )
            login_count = cur.fetchone()[0]
            
            cur.execute(
                "SELECT COUNT(*) FROM analytics WHERE discord_id = ? AND event_type = 'hwid_reset'",
                (discord_id,)
            )
            reset_count = cur.fetchone()[0]
            
            conn.close()
        except Exception as e:
            log.error(f"Error fetching analytics: {e}")
        
        is_blacklisted = db.is_blacklisted(discord_id)
        
        return jsonify({
            "success": True,
            "user": user,
            "analytics": {
                "login_count": login_count,
                "reset_count": reset_count
            },
            "is_blacklisted": is_blacklisted
        })
        
    except Exception as e:
        log.error(f"Lookup error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/admin/blacklist', methods=['GET'])
@require_api_key
def admin_blacklist():
    """Get all blacklisted users (admin only)."""
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM blacklist ORDER BY banned_at DESC")
        
        blacklisted = []
        for row in cur.fetchall():
            blacklisted.append({
                "discord_id": row['discord_id'],
                "reason": row['reason'],
                "banned_at": row['banned_at'],
                "banned_by": None
            })
        
        conn.close()
        
        return jsonify({
            "success": True,
            "blacklisted": blacklisted,
            "count": len(blacklisted)
        })
        
    except Exception as e:
        log.error(f"Error fetching blacklist: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


@app.route('/api/admin/reset-hwid', methods=['POST'])
@require_api_key
def admin_reset_hwid():
    """Force reset user HWID (admin only)."""
    try:
        data = request.get_json() or {}
        discord_id = str(data.get('discord_id', '')).strip()
        
        if not discord_id:
            return jsonify({
                "success": False,
                "message": "Missing discord_id"
            }), 400
        
        success = db.reset_hwid(discord_id)
        
        if success:
            db.log_event("hwid_reset", discord_id, request.remote_addr, "Admin force reset")
            log.info(f"🔄 Admin force reset HWID for {discord_id}")
            
            return jsonify({
                "success": True,
                "message": "HWID reset successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
            
    except Exception as e:
        log.error(f"Admin HWID reset error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# ==============================================================================
# ❌ ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_page(WebTemplates.ERROR_404), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    log.error(f"500 error: {error}", exc_info=True)
    return render_page(WebTemplates.ERROR_500), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle uncaught exceptions."""
    log.error(f"Unhandled exception: {error}", exc_info=True)
    return render_page(WebTemplates.ERROR_500), 500


# ==============================================================================
# 🚀 SERVER RUNNER
# ==============================================================================

def run_server():
    """Run the Flask web server."""
    try:
        log.info("=" * 60)
        log.info("🌐 BANANA HUB WEB SERVER")
        log.info("=" * 60)
        log.info(f"Host: {Config.WEB_HOST}:{Config.WEB_PORT}")
        log.info(f"Base URL: {Config.BASE_URL}")
        log.info(f"Debug Mode: {Config.DEBUG}")
        log.info("=" * 60)
        
        # Run server
        app.run(
            host=Config.WEB_HOST,
            port=Config.WEB_PORT,
            debug=Config.DEBUG,
            use_reloader=False  # Disable reloader to prevent double initialization
        )
        
    except Exception as e:
        log.error(f"❌ Failed to start web server: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    run_server()
