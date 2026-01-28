# ==============================================================================
# 🍌 BANANA HUB V70.2 - FIXED INITIALIZATION ORDER
# ==============================================================================

import discord
from discord import app_commands
from discord.ext import commands
import json
import string
import random
import os
import datetime
import threading
import asyncio
import logging
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# ⚙️ CONFIGURATION
# ==============================================================================
CONFIG = {
    "TOKEN": os.getenv("BOT_TOKEN", "MTQ0NjUyOTgxNzQzOTg5OTc1MA.GKv_XN.iGGQmSnfWVygNTT_qo9R3OIPnc3wFpHjIAKOhE"), 
    "OWNER_ID": int(os.getenv("OWNER_ID", 1269772767516033025)),
    "PREFIX": os.getenv("PREFIX", "/"),
    "DATA_DIR": "data",
    "DB_FILE": "platinum_db.json",
    "WEB_PORT": int(os.getenv("PORT", 5000)),
    "ROLES": {
        "BUYER": "Premium User",
    },
    "URLS": {
        "LOADER": f"{os.getenv('BASE_URL', 'http://127.0.0.1:5000')}/script.lua", 
        "DASHBOARD": f"{os.getenv('WEBSITE_URL', 'http://127.0.0.1:5000')}/dashboard",
        "LOGO": "https://em-content.zobj.net/source/microsoft-teams/337/banana_1f34c.png"
    }
}

SCRIPT_STATUS = "🟢 Undetected"
log = logging.getLogger('werkzeug'); log.setLevel(logging.ERROR)

# ==============================================================================
# 🛡️ DATABASE ENGINE
# ==============================================================================
if not os.path.exists(CONFIG["DATA_DIR"]): os.makedirs(CONFIG["DATA_DIR"])

class DatabaseManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.path = os.path.join(CONFIG["DATA_DIR"], CONFIG["DB_FILE"])
            cls._instance.lock = threading.Lock()
            cls._instance.load()
        return cls._instance

    def get_schema(self): return {"users": {}, "keys": {}, "blacklist": [], "warnings": {}}

    def load(self):
        with self.lock:
            if not os.path.exists(self.path):
                self.data = self.get_schema()
                self.save_unsafe()
            else:
                try:
                    with open(self.path, 'r') as f:
                        self.data = json.load(f)
                except:
                    self.data = self.get_schema()
                    self.save_unsafe()

    def save(self):
        with self.lock:
            self.save_unsafe()

    def save_unsafe(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def get_user(self, uid):
        self.load()
        return self.data["users"].get(str(uid))

    def register_user(self, uid, key):
        self.load()
        self.data["users"][str(uid)] = {"key": key, "hwid": None, "date": str(datetime.datetime.now())}
        self.save()

    def reset_hwid(self, uid): 
        self.load()
        uid = str(uid)
        if uid in self.data["users"]:
            self.data["users"][uid]["hwid"] = None
            self.save()
            return True
        return False

    def add_key(self, key, creator):
        self.load()
        self.data["keys"][key] = {"by": str(creator), "used": False}
        self.save()

    def check_key(self, key):
        self.load()
        return key in self.data["keys"] and not self.data["keys"][key]["used"]

    def use_key(self, key, uid):
        self.load()
        self.data["keys"][key]["used"] = True
        self.data["keys"][key]["used_by"] = str(uid)
        self.save()

    def is_blacklisted(self, uid):
        self.load()
        return str(uid) in self.data["blacklist"]

    def toggle_blacklist(self, uid):
        self.load()
        uid = str(uid)
        if uid in self.data["blacklist"]:
            self.data["blacklist"].remove(uid)
            r = False
        else:
            self.data["blacklist"].append(uid)
            r = True
        self.save()
        return r

# Initialize DB immediately after class definition
db = DatabaseManager()

# ==============================================================================
# 🌐 ULTRA MODERN WEBSITE
# ==============================================================================
app = Flask(__name__)
CORS(app)

# --- CSS & JS SHARED ASSETS ---
HEAD_INCLUDE = """
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
    body { background-color: #09090b; color: white; font-family: 'Space Grotesk', sans-serif; margin: 0; overflow-x: hidden; }
    .glass { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); }
    .gradient-text { background: linear-gradient(135deg, #FACC15 0%, #fb923c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .glow { box-shadow: 0 0 40px rgba(250, 204, 21, 0.15); }
    .btn-primary { background: linear-gradient(135deg, #FACC15, #eab308); color: black; font-weight: bold; transition: all 0.3s ease; }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 25px -5px rgba(250, 204, 21, 0.4); }
    .blob { position: absolute; width: 500px; height: 500px; background: radial-gradient(circle, rgba(250,204,21,0.15) 0%, transparent 70%); filter: blur(80px); z-index: -1; animation: float 10s infinite alternate; }
    @keyframes float { 0% { transform: translate(0,0); } 100% { transform: translate(50px, 50px); } }
</style>
"""

# --- LANDING PAGE ---
HOME_HTML = f"""
<!DOCTYPE html><html lang="en"><head><title>BananaHub | Next Gen</title>{HEAD_INCLUDE}</head>
<body class="flex flex-col min-h-screen">
    <div class="blob" style="top:-10%; left:-10%"></div>
    <div class="blob" style="bottom:-10%; right:-10%; animation-delay: -5s"></div>

    <!-- NAVBAR -->
    <nav class="w-full p-6 flex justify-between items-center max-w-7xl mx-auto z-10">
        <div class="flex items-center gap-3 text-2xl font-bold"><i class="fa-solid fa-bolt text-yellow-400"></i> BananaHub</div>
        <a href="/login" class="px-6 py-2 rounded-full border border-zinc-700 hover:bg-zinc-800 transition">Client Login</a>
    </nav>

    <!-- HERO SECTION -->
    <main class="flex-1 flex flex-col items-center justify-center text-center px-4 mt-10 z-10">
        <div class="inline-flex items-center gap-2 px-4 py-1 rounded-full bg-yellow-400/10 border border-yellow-400/20 text-yellow-400 text-sm mb-6">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> {SCRIPT_STATUS}
        </div>
        <h1 class="text-6xl md:text-8xl font-bold mb-6 leading-tight">Dominate <br><span class="gradient-text">The Game</span></h1>
        <p class="text-zinc-400 text-lg md:text-xl max-w-2xl mb-10">The most advanced, undetected, and powerful script hub for Roblox. Join thousands of users winning every day.</p>
        
        <div class="flex gap-4">
            <a href="/login" class="btn-primary px-8 py-4 rounded-xl text-lg flex items-center gap-2">Get Script <i class="fa-solid fa-arrow-right"></i></a>
            <a href="https://discord.gg/example" target="_blank" class="px-8 py-4 rounded-xl glass hover:bg-white/5 transition flex items-center gap-2 border border-zinc-700">Join Discord <i class="fa-brands fa-discord"></i></a>
        </div>

        <!-- FEATURES -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-24 max-w-5xl w-full text-left">
            <div class="glass p-8 rounded-2xl">
                <div class="w-12 h-12 rounded-lg bg-yellow-400/10 flex items-center justify-center text-yellow-400 text-2xl mb-4"><i class="fa-solid fa-shield-halved"></i></div>
                <h3 class="text-xl font-bold mb-2">Undetected</h3>
                <p class="text-zinc-500">Our advanced bypass technology keeps your account safe from bans.</p>
            </div>
            <div class="glass p-8 rounded-2xl">
                <div class="w-12 h-12 rounded-lg bg-blue-400/10 flex items-center justify-center text-blue-400 text-2xl mb-4"><i class="fa-solid fa-bolt"></i></div>
                <h3 class="text-xl font-bold mb-2">Instant Updates</h3>
                <p class="text-zinc-500">Scripts are updated automatically via the cloud. No re-downloading.</p>
            </div>
            <div class="glass p-8 rounded-2xl">
                <div class="w-12 h-12 rounded-lg bg-purple-400/10 flex items-center justify-center text-purple-400 text-2xl mb-4"><i class="fa-solid fa-code"></i></div>
                <h3 class="text-xl font-bold mb-2">Premium API</h3>
                <p class="text-zinc-500">Powerful Lua environment with 99% UNC compatibility.</p>
            </div>
        </div>
    </main>
    
    <footer class="w-full py-8 text-center text-zinc-600 text-sm mt-20 border-t border-zinc-900">
        &copy; 2025 BananaHub Platinum. All rights reserved.
    </footer>
</body></html>
"""

# --- LOGIN PAGE ---
LOGIN_HTML = f"""
<!DOCTYPE html><html lang="en"><head><title>Login | BananaHub</title>{HEAD_INCLUDE}</head>
<body class="flex items-center justify-center min-h-screen">
    <div class="blob"></div>
    
    <div class="glass p-10 rounded-3xl w-full max-w-md relative z-10 glow">
        <div class="flex justify-center mb-8">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center text-3xl text-black shadow-lg">
                <i class="fa-solid fa-key"></i>
            </div>
        </div>
        
        <h2 class="text-3xl font-bold text-center mb-2">Welcome Back</h2>
        <p class="text-zinc-400 text-center mb-8 text-sm">Enter your credentials to manage your sub.</p>
        
        <div class="space-y-4">
            <div>
                <label class="text-xs font-bold text-zinc-500 ml-1 uppercase">Discord ID</label>
                <input type="text" id="uid" class="w-full bg-black/50 border border-zinc-800 rounded-xl p-4 mt-1 text-white focus:border-yellow-400 focus:outline-none transition" placeholder="123456789...">
            </div>
            <div>
                <label class="text-xs font-bold text-zinc-500 ml-1 uppercase">License Key</label>
                <input type="password" id="key" class="w-full bg-black/50 border border-zinc-800 rounded-xl p-4 mt-1 text-white focus:border-yellow-400 focus:outline-none transition" placeholder="BANANA-XXX-XXX-XXX">
            </div>
            <button onclick="login()" class="btn-primary w-full py-4 rounded-xl mt-4">Authenticate</button>
        </div>
        
        <p id="msg" class="text-center text-red-500 mt-4 text-sm min-h-[20px]"></p>
        
        <div class="mt-8 text-center">
            <a href="/" class="text-zinc-500 text-sm hover:text-white transition"><i class="fa-solid fa-arrow-left"></i> Back to Home</a>
        </div>
    </div>

    <script>
        async function login() {{
            const uid = document.getElementById('uid').value;
            const key = document.getElementById('key').value;
            const msg = document.getElementById('msg');
            
            if(!uid || !key) return msg.innerText = "Please fill all fields.";
            msg.innerText = "Checking...";
            
            const res = await fetch('/api/auth', {{
                method: 'POST', headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{uid, key}})
            }});
            const data = await res.json();
            
            if(data.success) {{
                localStorage.setItem('bh_uid', uid);
                localStorage.setItem('bh_key', key);
                window.location.href = '/dashboard';
            }} else {{
                msg.innerText = data.message;
            }}
        }}
    </script>
</body></html>
"""

# --- DASHBOARD PAGE ---
DASHBOARD_HTML = f"""
<!DOCTYPE html><html lang="en"><head><title>Dashboard | BananaHub</title>{HEAD_INCLUDE}</head>
<body class="min-h-screen flex">
    <!-- SIDEBAR -->
    <aside class="w-20 md:w-64 glass border-r border-white/5 flex flex-col p-4 hidden md:flex z-20">
        <div class="flex items-center gap-3 px-2 mb-10">
            <div class="w-8 h-8 bg-yellow-400 rounded-lg"></div>
            <span class="font-bold text-xl">Platinum</span>
        </div>
        
        <nav class="space-y-2 flex-1">
            <a href="#" class="flex items-center gap-3 px-4 py-3 bg-white/5 rounded-xl text-yellow-400 border border-yellow-400/20"><i class="fa-solid fa-house"></i> Home</a>
            <a href="#" onclick="alert('Coming Soon')" class="flex items-center gap-3 px-4 py-3 text-zinc-400 hover:bg-white/5 rounded-xl transition"><i class="fa-solid fa-book"></i> Docs</a>
            <a href="#" onclick="alert('Coming Soon')" class="flex items-center gap-3 px-4 py-3 text-zinc-400 hover:bg-white/5 rounded-xl transition"><i class="fa-solid fa-gear"></i> Settings</a>
        </nav>
        
        <button onclick="logout()" class="flex items-center gap-3 px-4 py-3 text-zinc-500 hover:text-white transition"><i class="fa-solid fa-right-from-bracket"></i> Logout</button>
    </aside>

    <!-- MOBILE HEADER -->
    <div class="md:hidden fixed top-0 w-full glass p-4 z-50 flex justify-between items-center">
        <div class="font-bold">BananaHub</div>
        <button onclick="logout()" class="text-zinc-400"><i class="fa-solid fa-right-from-bracket"></i></button>
    </div>

    <!-- CONTENT -->
    <main class="flex-1 p-6 md:p-10 mt-14 md:mt-0 relative overflow-hidden">
        <div class="blob" style="top:0; right:0; opacity:0.5"></div>
        
        <header class="flex justify-between items-end mb-10">
            <div>
                <h1 class="text-3xl font-bold mb-1">Dashboard</h1>
                <p class="text-zinc-400">Manage your license and access.</p>
            </div>
            <div class="hidden md:block text-right">
                <div class="text-sm text-zinc-500">USER ID</div>
                <div id="disp_uid" class="font-mono">Loading...</div>
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="glass p-6 rounded-2xl border-l-4 border-green-500">
                <div class="text-zinc-400 text-sm mb-1">Subscription Status</div>
                <div class="text-2xl font-bold text-white">Active <i class="fa-solid fa-circle-check text-green-500 text-sm ml-2"></i></div>
            </div>
            <div class="glass p-6 rounded-2xl border-l-4 border-yellow-400">
                <div class="text-zinc-400 text-sm mb-1">Script Status</div>
                <div class="text-2xl font-bold text-white">{SCRIPT_STATUS}</div>
            </div>
            <div class="glass p-6 rounded-2xl border-l-4 border-blue-500">
                <div class="text-zinc-400 text-sm mb-1">HWID Status</div>
                <div class="text-2xl font-bold text-white" id="hwid_stat">Loading...</div>
            </div>
        </div>

        <div class="glass rounded-3xl p-8 relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-yellow-400 to-orange-500"></div>
            <h3 class="text-xl font-bold mb-6"><i class="fa-solid fa-code mr-2 text-yellow-400"></i> Loader Script</h3>
            
            <div class="bg-black/50 rounded-xl p-6 border border-zinc-800 font-mono text-sm text-green-400 break-all relative group">
                <div id="script_box">Loading script...</div>
                <button onclick="copyScript()" class="absolute top-4 right-4 bg-zinc-800 hover:bg-zinc-700 text-white px-3 py-1 rounded-lg text-xs transition opacity-0 group-hover:opacity-100">COPY</button>
            </div>

            <div class="flex gap-4 mt-6">
                <button onclick="resetHWID()" class="px-6 py-3 rounded-xl bg-zinc-800 hover:bg-zinc-700 transition flex items-center gap-2 border border-zinc-700">
                    <i class="fa-solid fa-rotate"></i> Reset HWID
                </button>
                <a href="https://discord.gg" target="_blank" class="px-6 py-3 rounded-xl bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600/30 transition flex items-center gap-2 border border-indigo-500/30">
                    <i class="fa-brands fa-discord"></i> Support Server
                </a>
            </div>
        </div>
    </main>

    <script>
        // Simple Auth Check
        const uid = localStorage.getItem('bh_uid');
        const key = localStorage.getItem('bh_key');
        
        if(!uid || !key) window.location.href = '/login';

        document.getElementById('disp_uid').innerText = uid;

        // Fetch Data
        async function loadData() {{
            const res = await fetch('/api/auth', {{
                method: 'POST', headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{uid, key}})
            }});
            const d = await res.json();
            
            if(d.success) {{
                document.getElementById('script_box').innerText = d.script;
                document.getElementById('hwid_stat').innerText = "Linked"; // Simplified for demo
            }} else {{
                alert('Session expired');
                logout();
            }}
        }}
        
        loadData();

        async function resetHWID() {{
            const btn = event.currentTarget;
            const ogHtml = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spin fa-spinner"></i> Processing...';
            
            await fetch('/api/reset', {{
                method: 'POST', headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{uid}})
            }});
            
            setTimeout(() => {{
                btn.innerHTML = '<i class="fa-solid fa-check"></i> Success';
                setTimeout(() => btn.innerHTML = ogHtml, 2000);
            }}, 1000);
        }}

        function copyScript() {{
            navigator.clipboard.writeText(document.getElementById('script_box').innerText);
            alert('Copied to clipboard!');
        }}

        function logout() {{
            localStorage.clear();
            window.location.href = '/';
        }}
    </script>
</body></html>
"""

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/login')
def login_page(): return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
def dashboard(): return render_template_string(DASHBOARD_HTML)

@app.route('/script.lua')
def get_script(): 
    if os.path.exists("script.lua"): return send_file("script.lua", mimetype="text/plain")
    return "-- Error: Host Missing Script", 404

@app.route('/api/auth', methods=['POST'])
def auth():
    d = request.json; u = db.get_user(d.get('uid'))
    if u and u['key'] == d.get('key') and not db.is_blacklisted(d.get('uid')):
        # Return the loader script
        loader = f"""getgenv().Key="{d.get('key')}";loadstring(game:HttpGet("{CONFIG['URLS']['LOADER']}"))()"""
        return jsonify(success=True, script=loader)
    return jsonify(success=False, message="Invalid Credentials or Blacklisted")

@app.route('/api/reset', methods=['POST'])
def reset():
    db.reset_hwid(request.json.get('uid'))
    return jsonify(success=True)

# ==============================================================================
# 🤖 DISCORD BOT
# ==============================================================================
class Bot(commands.Bot):
    def __init__(self): super().__init__(command_prefix=CONFIG["PREFIX"], intents=discord.Intents.all(), help_command=None)
    async def setup_hook(self): self.add_view(Panel()); await self.tree.sync()

bot = Bot()

class Panel(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Redeem", style=discord.ButtonStyle.success, custom_id="p:redeem")
    async def b_redeem(self, i, b): await i.response.send_modal(RedeemModal())
    @discord.ui.button(label="Reset HWID", style=discord.ButtonStyle.danger, custom_id="p:reset")
    async def b_reset(self, i, b): 
        if db.reset_hwid(i.user.id): await i.response.send_message("✅ HWID Reset.", ephemeral=True)
        else: await i.response.send_message("❌ No License.", ephemeral=True)
    @discord.ui.button(label="Get Script", style=discord.ButtonStyle.primary, custom_id="p:script")
    async def b_script(self, i, b):
        u = db.get_user(i.user.id)
        if u: await i.response.send_message(f"**Dashboard:** {CONFIG['URLS']['DASHBOARD']}\n**Key:** ||`{u['key']}`||", ephemeral=True)
        else: await i.response.send_message("❌ Redeem first.", ephemeral=True)

class RedeemModal(discord.ui.Modal, title="Redeem License"):
    key = discord.ui.TextInput(label="License Key")
    async def on_submit(self, i):
        k = self.key.value.strip()
        if db.get_user(i.user.id): return await i.response.send_message("⚠️ Already owned.", ephemeral=True)
        if db.check_key(k):
            db.use_key(k, i.user.id); db.register_user(i.user.id, k)
            r = discord.utils.get(i.guild.roles, name=CONFIG["ROLES"]["BUYER"])
            if r: await i.user.add_roles(r)
            await i.response.send_message("🎉 Redeemed!", ephemeral=True)
        else: await i.response.send_message("❌ Invalid.", ephemeral=True)

# --- COMMANDS ---
@bot.tree.command(name="panel", description="[Admin] Send Panel")
async def panel(i: discord.Interaction):
    if i.user.id != CONFIG["OWNER_ID"]: return
    e = discord.Embed(title="🍌 BananaHub Platinum", description=f"**Status:** {SCRIPT_STATUS}\nManage your sub.", color=0xFACC15)
    await i.channel.send(embed=e, view=Panel())
    await i.response.send_message("Done", ephemeral=True)

@bot.tree.command(name="genkey", description="[Admin] Generate Key")
async def genkey(i: discord.Interaction):
    if i.user.id != CONFIG["OWNER_ID"]: return
    chars = string.ascii_uppercase + string.digits
    part1 = ''.join(random.choices(chars, k=3))
    part2 = ''.join(random.choices(chars, k=3))
    part3 = ''.join(random.choices(chars, k=3))
    k = f"BANANA-{part1}-{part2}-{part3}"
    db.add_key(k, i.user.id)
    await i.response.send_message(f"🔑 ||`{k}`||", ephemeral=True)

@bot.tree.command(name="ban", description="Ban user")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(i: discord.Interaction, user: discord.Member, reason: str="None"):
    await user.ban(reason=reason); await i.response.send_message(f"🔨 Banned {user}.")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=CONFIG["WEB_PORT"], debug=False, use_reloader=False)).start()
    bot.run(CONFIG["TOKEN"])
