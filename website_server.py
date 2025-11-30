# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - WEBSITE SERVER v3.0 (GLASSMORPHISM UI)
# Modern Flask web server with enhanced admin dashboard and user panels
# Features: Sortable tables, filters, activity feed, quick actions, glass UI
# ==============================================================================

from __future__ import annotations

import logging
import os
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
        # Check session admin or API key
        is_session_admin = session.get('is_admin', False)
        api_key = request.headers.get('X-Admin-Key') or request.args.get('api_key')
        is_api_admin = api_key == Config.ADMIN_API_KEY
        
        if not (is_session_admin or is_api_admin):
            return jsonify({'error': 'Unauthorized'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# ==============================================================================
# 🏠 PUBLIC ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Landing page with glassmorphism design."""
    return render_template_string(
        TEMPLATES['landing'],
        website_url=Config.WEBSITE_URL,
        base_url=Config.BASE_URL
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
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
        
        # Set session
        session['user_id'] = user_id
        session['key'] = key
        
        # Check if admin
        try:
            owner_id = str(Config.OWNER_ID)
            session['is_admin'] = (user_id == owner_id)
        except:
            session['is_admin'] = False
        
        # Log login
        db.log_event('web_login', user_id, request.remote_addr, 'User logged in via web')
        
        return jsonify({
            'success': True,
            'redirect': url_for('admin_panel' if session['is_admin'] else 'dashboard')
        })
    
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
    """Enhanced user dashboard with glassmorphism UI."""
    user_id = session.get('user_id')
    user = db.get_user(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Get user analytics
    analytics = db.get_user_analytics(user_id)
    
    # Generate loader script
    loader_script = generate_loader_script(user_id, user.get('key'))
    
    # Get recent activity (last 10 events)
    recent_activity = get_user_recent_activity(user_id, limit=10)
    
    return render_template_string(
        TEMPLATES['dashboard'],
        user=user,
        analytics=analytics,
        loader_script=loader_script,
        recent_activity=recent_activity,
        base_url=Config.BASE_URL,
        website_url=Config.WEBSITE_URL
    )

@app.route('/api/user/reset-hwid', methods=['POST'])
@require_auth
def api_reset_hwid():
    """API endpoint to reset user HWID."""
    user_id = session.get('user_id')
    
    success = db.reset_hwid(user_id)
    if success:
        db.log_event('hwid_reset', user_id, request.remote_addr, 'Web reset')
        return jsonify({'success': True, 'message': 'HWID reset successfully'})
    
    return jsonify({'success': False, 'error': 'Failed to reset HWID'}), 500

@app.route('/api/user/activity')
@require_auth
def api_user_activity():
    """Get user activity with filters."""
    user_id = session.get('user_id')
    event_type = request.args.get('event_type', 'all')
    limit = int(request.args.get('limit', 20))
    
    activity = get_user_recent_activity(user_id, event_type, limit)
    return jsonify({'activity': activity})

# ==============================================================================
# 🛡️ ADMIN PANEL
# ==============================================================================

@app.route('/admin')
@require_auth
@require_admin
def admin_panel():
    """Enhanced admin panel with tables, filters, and analytics."""
    # Get all users
    users = db.get_all_users()
    
    # Get all keys
    all_keys = db.get_all_keys()
    unused_keys = [k for k in all_keys if k.get('used') == 0]
    
    # Get blacklisted users
    blacklisted = db.get_blacklisted_users()
    
    # Get system stats
    stats = db.get_stats()
    
    # Get recent activity (last 50 events)
    recent_activity = get_all_recent_activity(limit=50)
    
    # Get HWID reset history
    hwid_resets = get_hwid_reset_history(limit=20)
    
    # Get recent logins
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

@app.route('/api/admin/users')
@require_admin
def api_admin_users():
    """Get all users with filtering and sorting."""
    users = db.get_all_users()
    
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

@app.route('/api/admin/keys')
@require_admin
def api_admin_keys():
    """Get all keys with filtering."""
    keys = db.get_all_keys()
    
    # Apply filters
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'unused':
        keys = [k for k in keys if k.get('used') == 0]
    elif status_filter == 'used':
        keys = [k for k in keys if k.get('used') == 1]
    
    return jsonify({'keys': keys})

@app.route('/api/admin/generate-key', methods=['POST'])
@require_admin
def api_generate_key():
    """Generate new keys."""
    data = request.get_json()
    count = min(int(data.get('count', 1)), 25)
    
    keys = []
    for _ in range(count):
        key = generate_key()
        if db.generate_key_entry(key, session.get('user_id', 'admin')):
            keys.append(key)
    
    db.log_event('key_generated', session.get('user_id'), request.remote_addr, f'Generated {len(keys)} keys')
    
    return jsonify({'success': True, 'keys': keys, 'count': len(keys)})

@app.route('/api/admin/whitelist', methods=['POST'])
@require_admin
def api_whitelist_user():
    """Whitelist a user with auto key generation."""
    data = request.get_json()
    discord_id = data.get('discord_id', '').strip()
    
    if not discord_id:
        return jsonify({'error': 'Discord ID required'}), 400
    
    # Check if already has key
    existing = db.get_user(discord_id)
    if existing and existing.get('key'):
        return jsonify({'error': 'User already has a key', 'key': existing['key']}), 400
    
    # Generate new key
    key = generate_key()
    if not db.generate_key_entry(key, session.get('user_id', 'admin')):
        return jsonify({'error': 'Failed to generate key'}), 500
    
    # Register user
    db.register_user(discord_id, key)
    db.mark_key_redeemed(key, discord_id)
    db.log_event('whitelist', discord_id, request.remote_addr, f'Whitelisted via web by {session.get("user_id")}')
    
    return jsonify({'success': True, 'key': key, 'discord_id': discord_id})

@app.route('/api/admin/unwhitelist', methods=['POST'])
@require_admin
def api_unwhitelist_user():
    """Remove user from whitelist."""
    data = request.get_json()
    discord_id = data.get('discord_id', '').strip()
    
    if not discord_id:
        return jsonify({'error': 'Discord ID required'}), 400
    
    success = db.unwhitelist(discord_id)
    if success:
        db.log_event('unwhitelist', discord_id, request.remote_addr, f'Unwhitelisted via web')
        return jsonify({'success': True})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/admin/blacklist', methods=['POST'])
@require_admin
def api_blacklist_user():
    """Blacklist or unblacklist a user."""
    data = request.get_json()
    discord_id = data.get('discord_id', '').strip()
    reason = data.get('reason', 'No reason provided')
    
    if not discord_id:
        return jsonify({'error': 'Discord ID required'}), 400
    
    # Toggle blacklist
    is_banned = db.toggle_blacklist(discord_id, reason)
    action = 'blacklist' if is_banned else 'unblacklist'
    
    db.log_event(action, discord_id, request.remote_addr, f'{action.title()}ed via web: {reason}')
    
    return jsonify({'success': True, 'banned': is_banned, 'action': action})

@app.route('/api/admin/reset-hwid', methods=['POST'])
@require_admin
def api_admin_reset_hwid():
    """Force reset user HWID."""
    data = request.get_json()
    discord_id = data.get('discord_id', '').strip()
    
    if not discord_id:
        return jsonify({'error': 'Discord ID required'}), 400
    
    success = db.reset_hwid(discord_id)
    if success:
        db.log_event('hwid_reset', discord_id, request.remote_addr, f'Force reset via web by admin')
        return jsonify({'success': True})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/admin/activity')
@require_admin
def api_admin_activity():
    """Get filtered activity logs."""
    event_type = request.args.get('event_type', 'all')
    limit = int(request.args.get('limit', 50))
    
    activity = get_all_recent_activity(event_type, limit)
    return jsonify({'activity': activity})

@app.route('/api/admin/stats')
@require_admin
def api_admin_stats():
    """Get system statistics."""
    stats = db.get_stats()
    
    # Add more detailed stats
    users = db.get_all_users()
    blacklisted = db.get_blacklisted_users()
    
    stats['total_blacklisted'] = len(blacklisted)
    stats['active_users'] = len(users) - len(blacklisted)
    
    return jsonify(stats)

@app.route('/api/admin/backup', methods=['POST'])
@require_admin
def api_create_backup():
    """Create database backup."""
    try:
        backup_path = db.create_backup()
        db.log_event('backup', session.get('user_id'), request.remote_addr, f'Backup created: {backup_path}')
        return jsonify({'success': True, 'path': backup_path})
    except Exception as e:
        log.error(f"Backup failed: {e}")
        return jsonify({'error': str(e)}), 500

# ==============================================================================
# 📜 SCRIPT ROUTE
# ==============================================================================

@app.route('/script.lua')
def get_script():
    """Serve the loader
