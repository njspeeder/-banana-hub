# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - API MODULE
# ==============================================================================
from flask import Blueprint, request, jsonify
from functools import wraps
from config import Config
from database import db

api = Blueprint('api', __name__)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth != f"Bearer {Config.ADMIN_API_KEY}":
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@api.route('/unwhitelist', methods=['POST'])
@require_api_key
def unwhitelist():
    discord_id = request.json.get('discord_id')
    if db.unwhitelist(discord_id):
        db.log_event('unwhitelist', discord_id, request.remote_addr)
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "message": "User not found"}), 404

@api.route('/unblacklist', methods=['POST'])
@require_api_key
def unblacklist():
    discord_id = request.json.get('discord_id')
    if db.unblacklist(discord_id):
        db.log_event('unblacklist', discord_id, request.remote_addr)
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "message": "User not in blacklist"}), 404

@api.route('/getkey')
def getkey():
    discord_id = request.args.get('id')
    user = db.get_user(discord_id)
    if user:
        return jsonify({"status": "ok", "key": user['key']}), 200
    return jsonify({"status": "error", "message": "Key not found"}), 404
