# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - WEBSITE SERVER v5.0
# Complete Flask server for modern multi-page dashboard and admin panel
# ==============================================================================

from __future__ import annotations

import logging
import os
import random
import string
from datetime import datetime, UTC
from functools import wraps
from typing import Optional, Dict, Any, List

from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
from flask_cors import CORS

from config import Config
from database import db
from web_templates import TEMPLATES

# ==============================================================================
# 🔧 LOGGING
# ==============================================================================

log = logging.getLogger("website_server")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ==============================================================================
# 🌐 FLASK APP INITIALIZATION
# ==============================================================================

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", Config.ADMIN_API_KEY)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

CORS(app)

# ==============================================================================
# 🛡️ AUTHENTICATION DECORATORS
# ==============================================================================

def require_auth(f):
    """Require user authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """Require admin authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_session_admin = session.get('is_admin', False)
        api_key = request.headers.get('X-Admin-Key') or request.args.get('api_key')
        is_api_admin = api_key == Config.ADMIN_API_KEY
        
        if not (is_session_admin or is_api_admin):
            return jsonify({'error': 'Unauthorized - Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# ==============================================================================
# 🔧 HELPER FUNCTIONS
# ==============================================================================

def generate_key() -> str:
    """Generate a random license key in BANANA-XXX-XXX-XXX format."""
    chars = string.ascii_uppercase + string.digits
    part1 = ''.join(random.choices(chars, k=3))
    part2 = ''.join(random.choices(chars, k=3))
    part3 = ''.join(random.choices(chars, k=3))
    return f'BANANA-{part1}-{part2}-{part3}'


def generate_loader_script(user_id: str, key: str) -> str:
    """Generate Lua loader script for user."""
    website_url = getattr(Config, 'WEBSITE_URL', 'https://banana-hub.onrender.com')
    
    return f"""-- 🍌 BANANA HUB ENTERPRISE LOADER
-- User: {user_id}
-- Key: {key}
-- Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}

local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local WEBSITE_URL = "{website_url}"
local USER_ID = "{user_id}"
local KEY = "{key}"

print("🍌 Banana Hub - Initializing...")
print("👤 User ID: " .. USER_ID)

-- Authentication & Script Loading
local function authenticateAndLoad()
    local success, result = pcall(function()
        return game:HttpGet(WEBSITE_URL .. "/script.lua?user_id=" .. USER_ID .. "&key=" .. KEY)
    end)
    
    if success then
        print("✅ Authentication successful!")
        print("🚀 Loading Banana Hub...")
        loadstring(result)()
    else
        warn("❌ Authentication failed: " .. tostring(result))
        warn("💡 Please verify your license key and internet connection")
    end
end

authenticateAndLoad()
"""


def safe_get_user_data(user_id: str) -> Dict[str, Any]:
    """Get user data safely with comprehensive defaults."""
    try:
        user = db.get_user(user_id)
        
        if not user or not isinstance(user, dict):
            return {
                'discord_id': user_id or 'Unknown',
                'key': 'No key',
                'hwid': '',
                'last_login': 'Never',
                'joined_at': 'Unknown',
                'login_count': 0
            }
        
        return {
            'discord_id': user.get('discord_id') or user_id or 'Unknown',
            'key': user.get('key') or 'No key',
            'hwid': user.get('hwid') or '',
            'last_login': user.get('last_login') or 'Never',
            'joined_at': user.get('joined_at') or 'Unknown',
            'login_count': user.get('login_count') or 0
        }
    except Exception as e:
        log.error(f"Error getting user data for {user_id}: {e}")
        return {
            'discord_id': user_id or 'Unknown',
            'key': 'Error',
            'hwid': '',
            'last_login': 'Never',
            'joined_at': 'Unknown',
            'login_count': 0
        }


def safe_get_user_analytics(user_id: str) -> Dict[str, Any]:
    """Get user analytics safely with fallback."""
    default_analytics = {
        'total_logins': 0,
        'last_login': 'Never'
    }
    
    try:
        if not user_id:
            return default_analytics
            
        user = db.get_user(user_id)
        
        if not user or not isinstance(user, dict):
            return default_analytics
        
        return {
            'total_logins': int(user.get('login_count', 0) or 0),
            'last_login': str(user.get('last_login', 'Never') or 'Never'),
        }
        
    except Exception as e:
        log.warning(f"Analytics error for {user_id}: {e}")
        return default_analytics


def get_system_stats() -> Dict[str, int]:
    """Get comprehensive system statistics."""
    try:
        users = db.get_all_users() or []
        all_keys = db.get_all_keys() or []
        blacklisted = db.get_blacklisted_users() or []
        
        unused_keys = [k for k in all_keys if k.get('used') == 0]
        total_logins = sum(u.get('login_count', 0) for u in users)
        
        return {
            'total_users': len(users),
            'total_keys': len(all_keys),
            'available_keys': len(unused_keys),
            'total_logins': total_logins,
            'total_blacklisted': len(blacklisted),
            'active_users': len(users) - len(blacklisted)
        }
    except Exception as e:
        log.error(f"Error getting system stats: {e}")
        return {
            'total_users': 0,
            'total_keys': 0,
            'available_keys': 0,
            'total_logins': 0,
            'total_blacklisted': 0,
            'active_users': 0
        }

# ==============================================================================
# 🏠 PUBLIC ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Landing page with modern design."""
    try:
        return render_template_string(TEMPLATES['landing'])
    except Exception as e:
        log.error(f"Landing page error: {e}", exc_info=True)
        return f"<h1>Error Loading Page</h1><pre>{str(e)}</pre>", 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page and authentication handler."""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            user_id = data.get('user_id', '').strip()
            key = data.get('key', '').strip().upper()
            
            if not user_id or not key:
                return jsonify({'error': 'User ID and Key required'}), 400
            
            # Verify user
            user = db.get_user(user_id)
            if not user:
                log.warning(f"Login attempt for non-existent user: {user_id}")
                return jsonify({'error': 'Invalid credentials'}), 401
            
            user_key = user.get('key', '').upper()
            if user_key != key:
                log.warning(f"Invalid key attempt for user: {user_id}")
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Check blacklist
            if db.is_blacklisted(user_id):
                log.warning(f"Blacklisted user login attempt: {user_id}")
                return jsonify({'error': 'Account banned'}), 403
            
            # Clear old session and create new one
            session.clear()
            
            # Set session data
            session['user_id'] = user_id
            session['key'] = key
            session.permanent = True
            
            # Check if admin
            try:
                owner_id = str(getattr(Config, 'OWNER_ID', ''))
                session['is_admin'] = (user_id == owner_id)
            except Exception:
                session['is_admin'] = False
            
            # Log login
            try:
                db.log_event('web_login', user_id, request.remote_addr, 'Web panel login')
            except Exception as e:
                log.warning(f"Failed to log login event: {e}")
            
            # Return appropriate redirect
            redirect_url = '/admin' if session['is_admin'] else '/dashboard'
            
            log.info(f"Successful login: {user_id} (Admin: {session['is_admin']})")
            
            return jsonify({
                'success': True,
                'redirect': redirect_url
            })
            
        except Exception as e:
            log.error(f"Login error: {e}", exc_info=True)
            return jsonify({'error': 'Login failed', 'details': str(e)}), 500
    
    # GET request - show login form
    try:
        return render_template_string(TEMPLATES['login'])
    except Exception as e:
        log.error(f"Login page error: {e}", exc_info=True)
        return f"<h1>Error Loading Login</h1><pre>{str(e)}</pre>", 500


@app.route('/logout')
def logout():
    """Logout user and clear session."""
    user_id = session.get('user_id', 'Unknown')
    session.clear()
    log.info(f"User logged out: {user_id}")
    return redirect(url_for('index'))

# ==============================================================================
# 👤 USER DASHBOARD ROUTES
# ==============================================================================

@app.route('/dashboard')
@app.route('/dashboard/')
@app.route('/dashboard/<page>')
@require_auth
def dashboard(page='overview'):
    """User dashboard with multi-page navigation."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            session.clear()
            return redirect(url_for('login'))
        
        # Get user data
        user_data = safe_get_user_data(user_id)
        analytics = safe_get_user_analytics(user_id)
        
        # Generate loader script
        try:
            loader_script = generate_loader_script(user_id, user_data['key'])
        except Exception as e:
            log.warning(f"Loader script generation error: {e}")
            loader_script = "-- Error generating loader script"
        
        # Get config URLs
        base_url = getattr(Config, 'BASE_URL', '')
        website_url = getattr(Config, 'WEBSITE_URL', 'https://banana-hub.onrender.com')
        
        # Render dashboard template
        return render_template_string(
            TEMPLATES['dashboard'],
            user=user_data,
            analytics=analytics,
            loader_script=loader_script,
            base_url=base_url,
            website_url=website_url
        )
        
    except Exception as e:
        log.error(f"Dashboard error: {e}", exc_info=True)
        return f"""
        <html>
        <head>
            <title>Dashboard Error</title>
            <style>
                body {{ font-family: monospace; padding: 2rem; background: #0A0E1A; color: #fff; }}
                pre {{ background: #141824; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
                .error {{ color: #EF4444; }}
                a {{ color: #FACC15; text-decoration: none; }}
            </style>
        </head>
        <body>
            <h1 class="error">Dashboard Error</h1>
            <p>An error occurred while loading your dashboard.</p>
            <pre>{str(e)}</pre>
            <p><a href="/logout">← Logout and try again</a></p>
        </body>
        </html>
        """, 500

# ==============================================================================
# 👤 USER API ENDPOINTS
# ==============================================================================

@app.route('/api/user/reset-hwid', methods=['POST'])
@require_auth
def api_reset_hwid():
    """Reset user HWID."""
    try:
        user_id = session.get('user_id')
        success = db.reset_hwid(user_id)
        
        if success:
            try:
                db.log_event('hwid_reset', user_id, request.remote_addr, 'Web HWID reset')
            except Exception:
                pass
            
            log.info(f"HWID reset successful: {user_id}")
            return jsonify({'success': True, 'message': 'HWID reset successfully'})
        
        return jsonify({'success': False, 'error': 'Failed to reset HWID'}), 500
        
    except Exception as e:
        log.error(f"HWID reset error: {e}")
        return jsonify({'error': str(e)}), 500

# ==============================================================================
# 🛡️ ADMIN PANEL ROUTES
# ==============================================================================

@app.route('/admin')
@app.route('/admin/')
@app.route('/admin/<page>')
@require_auth
@require_admin
def admin_panel(page='dashboard'):
    """Admin panel with multi-page navigation."""
    try:
        # Gather all required data
        users = db.get_all_users() or []
        all_keys = db.get_all_keys() or []
        unused_keys = [k for k in all_keys if k.get('used') == 0]
        blacklisted = db.get_blacklisted_users() or []
        
        # Calculate comprehensive stats
        stats = get_system_stats()
        
        # Get config URLs
        base_url = getattr(Config, 'BASE_URL', '')
        website_url = getattr(Config, 'WEBSITE_URL', 'https://banana-hub.onrender.com')
        
        # Render admin template
        return render_template_string(
            TEMPLATES['admin'],
            users=users,
            recent_users=users[:20] if users else [],
            unused_keys=unused_keys,
            all_keys=all_keys,
            recent_keys=all_keys[:20] if all_keys else [],
            blacklisted=blacklisted,
            stats=stats,
            base_url=base_url,
            website_url=website_url
        )
        
    except Exception as e:
        log.error(f"Admin panel error: {e}", exc_info=True)
        return f"""
        <html>
        <head>
            <title>Admin Error</title>
            <style>
                body {{ font-family: monospace; padding: 2rem; background: #0A0E1A; color: #fff; }}
                pre {{ background: #141824; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
                .error {{ color: #EF4444; }}
                a {{ color: #FACC15; text-decoration: none; }}
            </style>
        </head>
        <body>
            <h1 class="error">Admin Panel Error</h1>
            <p>An error occurred while loading the admin panel.</p>
            <pre>{str(e)}</pre>
            <p><a href="/logout">← Logout and try again</a></p>
        </body>
        </html>
        """, 500

# ==============================================================================
# 🛡️ ADMIN API ENDPOINTS
# ==============================================================================

@app.route('/api/admin/users')
@app.route('/api/users')
@require_admin
def api_admin_users():
    """Get all users with filtering and sorting."""
    try:
        users = db.get_all_users() or []
        
        # Apply filters
        search = request.args.get('search', '').lower()
        status_filter = request.args.get('status', 'all')
        
        if search:
            users = [u for u in users if search in u.get('discord_id', '').lower() or search in u.get('key', '').lower()]
        
        blacklisted_ids = [b.get('discord_id') for b in (db.get_blacklisted_users() or [])]
        
        if status_filter == 'banned':
            users = [u for u in users if u.get('discord_id') in blacklisted_ids]
        elif status_filter == 'active':
            users = [u for u in users if u.get('discord_id') not in blacklisted_ids]
        
        # Apply sorting
        sort_by = request.args.get('sort', 'joined_at')
        reverse = request.args.get('order', 'desc') == 'desc'
        
        try:
            users.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)
        except Exception:
            pass
        
        return jsonify({'users': users, 'count': len(users)})
        
    except Exception as e:
        log.error(f"Users API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/stats')
@app.route('/api/stats')
@require_admin
def api_admin_stats():
    """Get system statistics."""
    try:
        stats = get_system_stats()
        return jsonify(stats)
    except Exception as e:
        log.error(f"Stats API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def api_status_check():
    """Health check endpoint."""
    return jsonify({'success': True, 'data': {'status': 'online'}})


@app.route('/api/admin/generate-key', methods=['POST'])
@app.route('/api/generate-key', methods=['POST'])
@require_admin
def api_generate_key():
    """Generate new license keys."""
    try:
        data = request.get_json() or {}
        count = min(int(data.get('count', 1)), 25)
        
        keys = []
        admin_user = session.get('user_id', 'admin')
        
        for _ in range(count):
            key = generate_key()
            if db.generate_key_entry(key, admin_user):
                keys.append(key)
        
        try:
            db.log_event('key_generated', admin_user, request.remote_addr, f'Generated {len(keys)} keys')
        except Exception:
            pass
        
        log.info(f"Generated {len(keys)} keys by {admin_user}")
        
        return jsonify({'success': True, 'keys': keys, 'count': len(keys)})
        
    except Exception as e:
        log.error(f"Key generation error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/whitelist', methods=['POST'])
@app.route('/api/whitelist', methods=['POST'])
@require_admin
def api_whitelist_user():
    """Whitelist a user with auto-generated key."""
    try:
        data = request.get_json() or {}
        discord_id = data.get('discord_id', '').strip()
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        # Check if user already exists
        existing = db.get_user(discord_id)
        if existing and existing.get('key'):
            return jsonify({'error': 'User already has a key', 'key': existing['key']}), 400
        
        # Generate and assign key
        key = generate_key()
        admin_user = session.get('user_id', 'admin')
        
        if not db.generate_key_entry(key, admin_user):
            return jsonify({'error': 'Failed to generate key'}), 500
        
        db.register_user(discord_id, key)
        db.mark_key_redeemed(key, discord_id)
        
        try:
            db.log_event('whitelist', discord_id, request.remote_addr, f'Whitelisted by {admin_user}')
        except Exception:
            pass
        
        log.info(f"User whitelisted: {discord_id} by {admin_user}")
        
        return jsonify({'success': True, 'key': key, 'discord_id': discord_id})
        
    except Exception as e:
        log.error(f"Whitelist error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/unwhitelist', methods=['POST'])
@app.route('/api/unwhitelist', methods=['POST'])
@require_admin
def api_unwhitelist_user():
    """Remove user from whitelist."""
    try:
        data = request.get_json() or {}
        discord_id = data.get('discord_id', '').strip()
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        success = db.unwhitelist(discord_id)
        
        if success:
            try:
                db.log_event('unwhitelist', discord_id, request.remote_addr, f'Removed by {session.get("user_id")}')
            except Exception:
                pass
            
            log.info(f"User unwhitelisted: {discord_id}")
            return jsonify({'success': True})
        
        return jsonify({'error': 'User not found'}), 404
        
    except Exception as e:
        log.error(f"Unwhitelist error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/blacklist', methods=['POST'])
@app.route('/api/blacklist', methods=['POST'])
@require_admin
def api_blacklist_user():
    """Blacklist or unblacklist a user."""
    try:
        data = request.get_json() or {}
        discord_id = data.get('discord_id', '').strip()
        reason = data.get('reason', 'No reason provided')
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        is_banned = db.toggle_blacklist(discord_id, reason)
        action = 'blacklist' if is_banned else 'unblacklist'
        
        try:
            db.log_event(action, discord_id, request.remote_addr, f'{action}: {reason}')
        except Exception:
            pass
        
        log.info(f"User {action}ed: {discord_id} - {reason}")
        
        return jsonify({'success': True, 'banned': is_banned, 'action': action})
        
    except Exception as e:
        log.error(f"Blacklist error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/reset-hwid', methods=['POST'])
@app.route('/api/reset-hwid-admin', methods=['POST'])
@app.route('/api/user/reset-hwid', methods=['POST']) # fallback alias if routed purely by path
@require_admin
def api_admin_reset_hwid():
    """Force reset user HWID (admin)."""
    try:
        data = request.get_json() or {}
        discord_id = data.get('discord_id', '').strip()
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        success = db.reset_hwid(discord_id)
        
        if success:
            try:
                db.log_event('hwid_reset', discord_id, request.remote_addr, f'Admin reset by {session.get("user_id")}')
            except Exception:
                pass
            
            log.info(f"Admin HWID reset for: {discord_id}")
            return jsonify({'success': True})
        
        return jsonify({'error': 'User not found'}), 404
        
    except Exception as e:
        log.error(f"Admin HWID reset error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>', methods=['GET'])
@require_admin
def api_get_user_info(user_id):
    """Get specific user info (Admin)."""
    try:
        user = safe_get_user_data(user_id)
        if not user or user.get('discord_id') == 'Unknown':
             # Even if unknown, return safe structure so client doesn't crash
             return jsonify({'success': True, 'user': user})
             
        return jsonify({'success': True, 'user': user})
    except Exception as e:
        log.error(f"Get user info error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>/reset-hwid', methods=['POST'])
@require_admin
def api_user_reset_hwid_endpoint(user_id):
    """Reset specific user's HWID (Admin)."""
    try:
        if not user_id:
             return jsonify({'error': 'User ID required'}), 400
             
        success = db.reset_hwid(user_id)
        if success:
             try:
                 db.log_event('hwid_reset', user_id, request.remote_addr, f'Bot reset for {user_id}')
             except: pass
             return jsonify({'success': True, 'message': 'HWID reset successfully'})
             
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        log.error(f"User HWID reset error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/check-key', methods=['POST'])
@require_admin
def api_check_key():
    """Check if a license key is valid and available."""
    try:
        data = request.get_json() or {}
        key = data.get('key', '').strip().upper()
        
        if not key:
            return jsonify({'success': False, 'error': 'Key required'}), 400
            
        is_available = db.check_key_available(key)
        
        return jsonify({
            'success': True,
            'key': key,
            'available': is_available
        })
    except Exception as e:
        log.error(f"Check key error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth', methods=['POST'])
@require_admin
def api_authenticate_user():
    """Authenticate user logic for API clients."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', '')
        key = data.get('key', '').strip().upper()
        hwid = data.get('hwid', '')
        
        if not user_id or not key:
             return jsonify({'success': False, 'error': 'Missing credentials'}), 400
             
        user = db.get_user(user_id)
        if not user or user.get('key') != key:
             return jsonify({'success': False, 'authenticated': False, 'message': 'Invalid credentials'}), 401
             
        # Check blacklist
        if db.is_blacklisted(user_id):
             return jsonify({'success': False, 'authenticated': False, 'message': 'Account banned'}), 403
             
        # HWID Logic
        stored_hwid = user.get('hwid')
        hwid_match = False
        hwid_set = bool(stored_hwid)
        
        if hwid and not stored_hwid:
             # First time HWID set
             db.set_hwid(user_id, hwid)
             hwid_match = True
             hwid_set = True
        elif hwid and stored_hwid:
             hwid_match = (hwid == stored_hwid)
        elif not hwid:
             # If no HWID sent, we just verify creds
             hwid_match = True 
             
        return jsonify({
            'success': True,
            'authenticated': True,
            'hwid_match': hwid_match,
            'hwid_set': hwid_set,
            'message': 'Authenticated'
        })
    except Exception as e:
        log.error(f"Auth API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/verify', methods=['POST'])
@require_admin
def api_verify_license():
    """Quick license verification."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', '')
        key = data.get('key', '').strip().upper()
        
        user = db.get_user(user_id)
        if user and user.get('key') == key:
             if db.is_blacklisted(user_id):
                  return jsonify({'valid': False, 'reason': 'Banned'})
             return jsonify({'valid': True, 'user_id': user_id})
             
        return jsonify({'valid': False, 'reason': 'Invalid credentials'})
    except Exception as e:
        log.error(f"Verify API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/backup', methods=['POST'])
@require_admin
def api_create_backup():
    """Create database backup."""
    try:
        backup_path = db.create_backup()
        
        try:
            db.log_event('backup', session.get('user_id'), request.remote_addr, f'Backup created: {backup_path}')
        except Exception:
            pass
        
        log.info(f"Database backup created: {backup_path}")
        
        return jsonify({'success': True, 'path': backup_path})
        
    except Exception as e:
        log.error(f"Backup error: {e}")
        return jsonify({'error': str(e)}), 500

# ==============================================================================
# 📜 SCRIPT SERVING ROUTES
# ==============================================================================

@app.route('/script.lua')
def get_script():
    """Serve the loader script for authenticated users."""
    try:
        user_id = request.args.get('user_id', '')
        key = request.args.get('key', '')
        
        if not user_id or not key:
            return "-- Error: Missing authentication credentials", 400
        
        user = db.get_user(user_id)
        if not user or user.get('key', '').upper() != key.upper():
            return "-- Error: Invalid credentials", 401
        
        if db.is_blacklisted(user_id):
            return "-- Error: Account has been banned", 403
        
        try:
            db.log_event('script_access', user_id, request.remote_addr, 'Loader script accessed')
        except Exception:
            pass
        
        loader = generate_loader_script(user_id, key)
        
        return app.response_class(
            response=loader,
            status=200,
            mimetype='text/plain'
        )
        
    except Exception as e:
        log.error(f"Script serve error: {e}")
        return f"-- Error: {str(e)}", 500


@app.route('/main.lua')
def get_main_script():
    """Serve the main Banana Hub script."""
    try:
        user_id = request.args.get('user_id', '')
        key = request.args.get('key', '')
        
        if not user_id or not key:
            return "-- Error: Missing credentials", 400
        
        user = db.get_user(user_id)
        if not user or user.get('key', '').upper() != key.upper():
            return "-- Error: Invalid credentials", 401
        
        if db.is_blacklisted(user_id):
            return "-- Error: Account banned", 403
        
        try:
            db.log_event('main_script_access', user_id, request.remote_addr, 'Main script loaded')
        except Exception:
            pass
        
        # Main Banana Hub script
        main_script = f"""-- 🍌 BANANA HUB ENTERPRISE - MAIN SCRIPT
-- User: {user_id}
-- Authenticated: true
-- Loaded: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}

print("🍌 Banana Hub Enterprise loaded successfully!")
print("✅ Authentication verified")
print("👤 User ID: {user_id}")

-- Game Detection
local game_id = game.PlaceId
print("🎮 Game ID: " .. tostring(game_id))

-- Universal Features
local function enableESP()
    print("👁️ ESP enabled")
end

local function speedHack()
    print("⚡ Speed hack activated")
end

-- Load game-specific scripts
if game_id == 2788229376 then
    print("🎯 Da Hood detected - Loading custom scripts")
elseif game_id == 286090429 then
    print("🏃 Arsenal detected - Loading custom scripts")
else
    print("🌐 Universal mode - Core features loaded")
end

print("✅ Banana Hub ready to use!")
print("💡 Press INSERT to open GUI (coming soon)")
"""
        
        return app.response_class(
            response=main_script,
            status=200,
            mimetype='text/plain'
        )
        
    except Exception as e:
        log.error(f"Main script error: {e}")
        return f"-- Error: {str(e)}", 500

# ==============================================================================
# 🚀 ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return """
    <html>
    <head>
        <title>404 - Page Not Found</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                padding: 4rem 2rem; 
                background: #0A0E1A; 
                color: #fff; 
                text-align: center;
            }
            h1 { font-size: 4rem; color: #FACC15; margin-bottom: 1rem; }
            p { font-size: 1.25rem; color: #9CA3AF; margin-bottom: 2rem; }
            a { 
                display: inline-block;
                padding: 1rem 2rem; 
                background: linear-gradient(135deg, #FACC15, #F59E0B); 
                color: #0A0E1A; 
                text-decoration: none; 
                border-radius: 0.5rem; 
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Oops! The page you're looking for doesn't exist.</p>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    """, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    log.error(f"Internal server error: {error}")
    return """
    <html>
    <head>
        <title>500 - Internal Server Error</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                padding: 4rem 2rem; 
                background: #0A0E1A; 
                color: #fff; 
                text-align: center;
            }
            h1 { font-size: 4rem; color: #EF4444; margin-bottom: 1rem; }
            p { font-size: 1.25rem; color: #9CA3AF; margin-bottom: 2rem; }
            a { 
                display: inline-block;
                padding: 1rem 2rem; 
                background: linear-gradient(135deg, #FACC15, #F59E0B); 
                color: #0A0E1A; 
                text-decoration: none; 
                border-radius: 0.5rem; 
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <h1>500</h1>
        <p>Something went wrong on our end. Please try again later.</p>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    """, 500

# ==============================================================================
# 🚀 SERVER RUNNER
# ==============================================================================

def run_server():
    """Run the Flask web server."""
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    log.info("=" * 70)
    log.info("🍌 BANANA HUB ENTERPRISE - WEB SERVER v5.0")
    log.info("=" * 70)
    log.info(f"🌐 Server Port: {port}")
    log.info(f"🔗 Website URL: {getattr(Config, 'WEBSITE_URL', 'Not configured')}")
    log.info(f"🔗 Base URL: {getattr(Config, 'BASE_URL', 'Not configured')}")
    log.info(f"🔒 Debug Mode: {debug_mode}")
    log.info(f"👑 Admin: {getattr(Config, 'OWNER_ID', 'Not configured')}")
    log.info("=" * 70)
    log.info("✅ Server starting...")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


if __name__ == '__main__':
    run_server()
