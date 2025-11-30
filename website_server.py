# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - WEBSITE SERVER v3.0 (FIXED)
# Modern Flask web server with enhanced admin dashboard and user panels
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

# ==============================================================================
# 🌐 FLASK APP INITIALIZATION
# ==============================================================================

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", Config.ADMIN_API_KEY)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

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
            return jsonify({'error': 'Unauthorized'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# ==============================================================================
# 🔧 HELPER FUNCTIONS
# ==============================================================================

def generate_key() -> str:
    """Generate a random key."""
    chars = string.ascii_uppercase + string.digits
    return 'BH-' + ''.join(random.choices(chars, k=12))


def generate_loader_script(user_id: str, key: str) -> str:
    """Generate Lua loader script for user."""
    return f"""-- 🍌 BANANA HUB LOADER
-- User: {user_id}
-- Key: {key}
-- Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}

local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local WEBSITE_URL = "{Config.WEBSITE_URL}"
local USER_ID = "{user_id}"
local KEY = "{key}"

print("🍌 Banana Hub - Initializing...")
print("👤 User: " .. USER_ID)

-- Load main script
local function loadMain()
    local success, result = pcall(function()
        return game:HttpGet(WEBSITE_URL .. "/main.lua?user_id=" .. USER_ID .. "&key=" .. KEY)
    end)
    
    if success then
        print("✅ Authentication verified")
        loadstring(result)()
    else
        warn("❌ Failed to load: " .. tostring(result))
    end
end

loadMain()
"""


def safe_get_user_analytics(user_id: str) -> Dict:
    """Get user analytics safely with fallback."""
    try:
        return {
            'total_logins': db.get_user_login_count(user_id) if hasattr(db, 'get_user_login_count') else 0,
            'last_login': db.get_user_last_login(user_id) if hasattr(db, 'get_user_last_login') else 'Never',
        }
    except Exception as e:
        log.warning(f"Analytics error for {user_id}: {e}")
        return {
            'total_logins': 0,
            'last_login': 'Never',
        }


def get_user_recent_activity(user_id: str, event_type: str = 'all', limit: int = 10) -> List[Dict]:
    """Get recent activity for a user."""
    try:
        if hasattr(db, 'get_user_logs'):
            logs = db.get_user_logs(user_id, limit * 2)
            if event_type != 'all':
                logs = [log for log in logs if log.get('event_type') == event_type]
            return logs[:limit] if logs else []
    except Exception as e:
        log.warning(f"Activity fetch error: {e}")
    return []


def get_all_recent_activity(event_type: str = 'all', limit: int = 50) -> List[Dict]:
    """Get all recent activity."""
    try:
        if hasattr(db, 'get_all_logs'):
            logs = db.get_all_logs(limit * 2)
            if event_type != 'all':
                logs = [log for log in logs if log.get('event_type') == event_type]
            return logs[:limit] if logs else []
    except Exception as e:
        log.warning(f"All activity fetch error: {e}")
    return []


def get_hwid_reset_history(limit: int = 20) -> List[Dict]:
    """Get HWID reset history."""
    try:
        if hasattr(db, 'get_all_logs'):
            logs = db.get_all_logs(limit * 5)
            hwid_logs = [log for log in logs if log.get('event_type') == 'hwid_reset']
            return hwid_logs[:limit] if hwid_logs else []
    except Exception as e:
        log.warning(f"HWID history fetch error: {e}")
    return []


def get_recent_logins(limit: int = 20) -> List[Dict]:
    """Get recent login history."""
    try:
        if hasattr(db, 'get_all_logs'):
            logs = db.get_all_logs(limit * 3)
            login_logs = [log for log in logs if log.get('event_type') in ['web_login', 'login']]
            return login_logs[:limit] if login_logs else []
    except Exception as e:
        log.warning(f"Login history fetch error: {e}")
    return []

# ==============================================================================
# 🏠 PUBLIC ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Landing page."""
    return render_template_string(TEMPLATES['landing'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            user_id = data.get('user_id', '').strip()
            key = data.get('key', '').strip().upper()
            
            if not user_id or not key:
                return jsonify({'error': 'User ID and Key required'}), 400
            
            # Verify user
            user = db.get_user(user_id)
            if not user or user.get('key') != key:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Check blacklist
            if db.is_blacklisted(user_id):
                return jsonify({'error': 'Account banned'}), 403
            
            # Clear and set session
            session.clear()
            session['user_id'] = user_id
            session['key'] = key
            session.permanent = True
            
            # Check if admin
            try:
                owner_id = str(Config.OWNER_ID)
                session['is_admin'] = (user_id == owner_id)
            except:
                session['is_admin'] = False
            
            # Log login
            try:
                db.log_event('web_login', user_id, request.remote_addr, 'Web login')
            except:
                pass
            
            return jsonify({
                'success': True,
                'redirect': url_for('admin_panel' if session['is_admin'] else 'dashboard')
            })
        except Exception as e:
            log.error(f"Login error: {e}")
            return jsonify({'error': 'Login failed'}), 500
    
    return render_template_string(TEMPLATES['login'])


@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    return redirect(url_for('index'))

# ==============================================================================
# 👤 USER DASHBOARD
# ==============================================================================

@app.route('/dashboard')
@require_auth
def dashboard():
    """User dashboard."""
    try:
        user_id = session.get('user_id')
        user = db.get_user(user_id)
        
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        # Safe data gathering
        analytics = safe_get_user_analytics(user_id)
        loader_script = generate_loader_script(user_id, user.get('key', ''))
        recent_activity = get_user_recent_activity(user_id, limit=10)
        
        # Ensure all required fields exist
        user_data = {
            'discord_id': user.get('discord_id', user_id),
            'key': user.get('key', 'No key'),
            'hwid': user.get('hwid', ''),
            'last_login': user.get('last_login', 'Never'),
            'joined_at': user.get('joined_at', 'Unknown'),
        }
        
        return render_template_string(
            TEMPLATES['dashboard'],
            user=user_data,
            analytics=analytics,
            loader_script=loader_script,
            recent_activity=recent_activity,
            base_url=Config.BASE_URL,
            website_url=Config.WEBSITE_URL
        )
    except Exception as e:
        log.error(f"Dashboard error: {e}", exc_info=True)
        return f"<h1>Error loading dashboard</h1><pre>{str(e)}</pre>", 500


@app.route('/api/user/reset-hwid', methods=['POST'])
@require_auth
def api_reset_hwid():
    """Reset user HWID."""
    try:
        user_id = session.get('user_id')
        success = db.reset_hwid(user_id)
        
        if success:
            try:
                db.log_event('hwid_reset', user_id, request.remote_addr, 'Web reset')
            except:
                pass
            return jsonify({'success': True, 'message': 'HWID reset successfully'})
        
        return jsonify({'success': False, 'error': 'Failed to reset HWID'}), 500
    except Exception as e:
        log.error(f"HWID reset error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/activity')
@require_auth
def api_user_activity():
    """Get user activity."""
    try:
        user_id = session.get('user_id')
        event_type = request.args.get('event_type', 'all')
        limit = int(request.args.get('limit', 20))
        
        activity = get_user_recent_activity(user_id, event_type, limit)
        return jsonify({'activity': activity})
    except Exception as e:
        log.error(f"Activity API error: {e}")
        return jsonify({'error': str(e)}), 500

# ==============================================================================
# 🛡️ ADMIN PANEL
# ==============================================================================

@app.route('/admin')
@require_auth
@require_admin
def admin_panel():
    """Admin panel."""
    try:
        # Safe data gathering with fallbacks
        users = db.get_all_users() or []
        all_keys = db.get_all_keys() or []
        unused_keys = [k for k in all_keys if k.get('used') == 0]
        blacklisted = db.get_blacklisted_users() or []
        
        # Calculate stats safely
        stats = {
            'total_users': len(users),
            'total_keys': len(all_keys),
            'available_keys': len(unused_keys),
            'total_logins': sum(u.get('login_count', 0) for u in users),
            'total_blacklisted': len(blacklisted)
        }
        
        # Get activity logs safely
        recent_activity = get_all_recent_activity(limit=50)
        hwid_resets = get_hwid_reset_history(limit=20)
        recent_logins = get_recent_logins(limit=20)
        
        return render_template_string(
            TEMPLATES['admin'],
            users=users,
            unused_keys=unused_keys,
            all_keys=all_keys,
            blacklisted=blacklisted,
            stats=stats,
            recent_activity=recent_activity,
            hwid_resets=hwid_resets,
            recent_logins=recent_logins,
            base_url=Config.BASE_URL,
            website_url=Config.WEBSITE_URL
        )
    except Exception as e:
        log.error(f"Admin panel error: {e}", exc_info=True)
        return f"<h1>Error loading admin panel</h1><pre>{str(e)}</pre>", 500


@app.route('/api/admin/users')
@require_admin
def api_admin_users():
    """Get all users with filtering."""
    try:
        users = db.get_all_users() or []
        
        # Apply filters
        search = request.args.get('search', '').lower()
        status_filter = request.args.get('status', 'all')
        
        if search:
            users = [u for u in users if search in u.get('discord_id', '').lower() or search in u.get('key', '').lower()]
        
        if status_filter == 'banned':
            users = [u for u in users if db.is_blacklisted(u.get('discord_id'))]
        elif status_filter == 'active':
            users = [u for u in users if not db.is_blacklisted(u.get('discord_id'))]
        
        # Apply sorting
        sort_by = request.args.get('sort', 'joined_at')
        reverse = request.args.get('order', 'desc') == 'desc'
        
        try:
            users.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)
        except:
            pass
        
        return jsonify({'users': users})
    except Exception as e:
        log.error(f"Users API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/keys')
@require_admin
def api_admin_keys():
    """Get all keys with filtering."""
    try:
        keys = db.get_all_keys() or []
        
        status_filter = request.args.get('status', 'all')
        
        if status_filter == 'unused':
            keys = [k for k in keys if k.get('used') == 0]
        elif status_filter == 'used':
            keys = [k for k in keys if k.get('used') == 1]
        
        return jsonify({'keys': keys})
    except Exception as e:
        log.error(f"Keys API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/generate-key', methods=['POST'])
@require_admin
def api_generate_key():
    """Generate new keys."""
    try:
        data = request.get_json()
        count = min(int(data.get('count', 1)), 25)
        
        keys = []
        for _ in range(count):
            key = generate_key()
            if db.generate_key_entry(key, session.get('user_id', 'admin')):
                keys.append(key)
        
        try:
            db.log_event('key_generated', session.get('user_id'), request.remote_addr, f'Generated {len(keys)} keys')
        except:
            pass
        
        return jsonify({'success': True, 'keys': keys, 'count': len(keys)})
    except Exception as e:
        log.error(f"Key generation error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/whitelist', methods=['POST'])
@require_admin
def api_whitelist_user():
    """Whitelist a user."""
    try:
        data = request.get_json()
        discord_id = data.get('discord_id', '').strip()
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        # Check if exists
        existing = db.get_user(discord_id)
        if existing and existing.get('key'):
            return jsonify({'error': 'User already has a key', 'key': existing['key']}), 400
        
        # Generate and assign key
        key = generate_key()
        if not db.generate_key_entry(key, session.get('user_id', 'admin')):
            return jsonify({'error': 'Failed to generate key'}), 500
        
        db.register_user(discord_id, key)
        db.mark_key_redeemed(key, discord_id)
        
        try:
            db.log_event('whitelist', discord_id, request.remote_addr, f'Whitelisted by {session.get("user_id")}')
        except:
            pass
        
        return jsonify({'success': True, 'key': key, 'discord_id': discord_id})
    except Exception as e:
        log.error(f"Whitelist error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/unwhitelist', methods=['POST'])
@require_admin
def api_unwhitelist_user():
    """Remove user from whitelist."""
    try:
        data = request.get_json()
        discord_id = data.get('discord_id', '').strip()
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        success = db.unwhitelist(discord_id)
        if success:
            try:
                db.log_event('unwhitelist', discord_id, request.remote_addr, 'Unwhitelisted')
            except:
                pass
            return jsonify({'success': True})
        
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        log.error(f"Unwhitelist error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/blacklist', methods=['POST'])
@require_admin
def api_blacklist_user():
    """Blacklist or unblacklist a user."""
    try:
        data = request.get_json()
        discord_id = data.get('discord_id', '').strip()
        reason = data.get('reason', 'No reason provided')
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        is_banned = db.toggle_blacklist(discord_id, reason)
        action = 'blacklist' if is_banned else 'unblacklist'
        
        try:
            db.log_event(action, discord_id, request.remote_addr, f'{action}: {reason}')
        except:
            pass
        
        return jsonify({'success': True, 'banned': is_banned, 'action': action})
    except Exception as e:
        log.error(f"Blacklist error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/reset-hwid', methods=['POST'])
@require_admin
def api_admin_reset_hwid():
    """Force reset user HWID."""
    try:
        data = request.get_json()
        discord_id = data.get('discord_id', '').strip()
        
        if not discord_id:
            return jsonify({'error': 'Discord ID required'}), 400
        
        success = db.reset_hwid(discord_id)
        if success:
            try:
                db.log_event('hwid_reset', discord_id, request.remote_addr, 'Admin force reset')
            except:
                pass
            return jsonify({'success': True})
        
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        log.error(f"Admin HWID reset error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/activity')
@require_admin
def api_admin_activity():
    """Get filtered activity logs."""
    try:
        event_type = request.args.get('event_type', 'all')
        limit = int(request.args.get('limit', 50))
        
        activity = get_all_recent_activity(event_type, limit)
        return jsonify({'activity': activity})
    except Exception as e:
        log.error(f"Activity API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/stats')
@require_admin
def api_admin_stats():
    """Get system statistics."""
    try:
        users = db.get_all_users() or []
        blacklisted = db.get_blacklisted_users() or []
        all_keys = db.get_all_keys() or []
        
        stats = {
            'total_users': len(users),
            'total_blacklisted': len(blacklisted),
            'active_users': len(users) - len(blacklisted),
            'total_keys': len(all_keys),
            'available_keys': len([k for k in all_keys if k.get('used') == 0]),
            'total_logins': sum(u.get('login_count', 0) for u in users)
        }
        
        return jsonify(stats)
    except Exception as e:
        log.error(f"Stats API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/backup', methods=['POST'])
@require_admin
def api_create_backup():
    """Create database backup."""
    try:
        backup_path = db.create_backup()
        try:
            db.log_event('backup', session.get('user_id'), request.remote_addr, f'Backup: {backup_path}')
        except:
            pass
        return jsonify({'success': True, 'path': backup_path})
    except Exception as e:
        log.error(f"Backup error: {e}")
        return jsonify({'error': str(e)}), 500

# ==============================================================================
# 📜 SCRIPT ROUTES
# ==============================================================================

@app.route('/script.lua')
def get_script():
    """Serve the loader script."""
    try:
        user_id = request.args.get('user_id', '')
        key = request.args.get('key', '')
        
        if not user_id or not key:
            return "-- Error: Missing credentials", 400
        
        user = db.get_user(user_id)
        if not user or user.get('key') != key:
            return "-- Error: Invalid credentials", 401
        
        if db.is_blacklisted(user_id):
            return "-- Error: Account banned", 403
        
        try:
            db.log_event('script_access', user_id, request.remote_addr, 'Loader accessed')
        except:
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
    """Serve the main script."""
    try:
        user_id = request.args.get('user_id', '')
        key = request.args.get('key', '')
        
        if not user_id or not key:
            return "-- Error: Missing credentials", 400
        
        user = db.get_user(user_id)
        if not user or user.get('key') != key:
            return "-- Error: Invalid credentials", 401
        
        if db.is_blacklisted(user_id):
            return "-- Error: Account banned", 403
        
        try:
            db.log_event('main_script_access', user_id, request.remote_addr, 'Main script loaded')
        except:
            pass
        
        main_script = f"""-- 🍌 BANANA HUB MAIN SCRIPT
print("🍌 Banana Hub loaded successfully!")
print("User ID: {user_id}")

-- Your main script content here

print("✅ Ready to use!")
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
# 🚀 SERVER RUNNER
# ==============================================================================

def run_server():
    """Run the Flask web server."""
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    log.info(f"🌐 Starting web server on port {port}")
    log.info(f"🔗 Website: {Config.WEBSITE_URL}")
    log.info(f"🔗 Base: {Config.BASE_URL}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


if __name__ == '__main__':
    run_server()
