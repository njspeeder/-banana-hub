# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - WEB TEMPLATES v2.1 (FIXED)
# Complete modern templates with admin dashboard - All working!
# ==============================================================================

from __future__ import annotations


class WebTemplates:
    """HTML templates for Banana Hub web frontend."""

    # ==========================================================================
    # 🔤 BASE TEMPLATE
    # ==========================================================================

    BASE = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#020617">
  <title>Banana Hub Enterprise</title>
  
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      min-height: 100vh;
      background: #020617;
      background-image: radial-gradient(at 0% 0%, rgba(250, 204, 21, 0.05) 0px, transparent 50%),
                        radial-gradient(at 100% 100%, rgba(250, 204, 21, 0.05) 0px, transparent 50%);
      color: #e5e7eb;
      font-family: system-ui, -apple-system, sans-serif;
    }
    
    .card {
      background: #0f172a;
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 20px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
      transition: transform 0.2s;
    }
    
    .card:hover { transform: translateY(-2px); }
    
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      border-radius: 12px;
      padding: 0.875rem 2rem;
      background: linear-gradient(135deg, #FACC15 0%, #EAB308 100%);
      color: #111827;
      font-weight: 600;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
      text-decoration: none;
    }
    
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(250, 204, 21, 0.4);
    }
    
    .btn-secondary {
      background: rgba(15, 23, 42, 0.8);
      color: #e5e7eb;
      border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .input {
      width: 100%;
      border-radius: 12px;
      border: 1px solid rgba(148, 163, 184, 0.2);
      padding: 0.875rem 1.25rem;
      background: rgba(15, 23, 42, 0.5);
      color: #e5e7eb;
      outline: none;
      transition: all 0.2s;
    }
    
    .input:focus {
      border-color: #FACC15;
      box-shadow: 0 0 0 3px rgba(250, 204, 21, 0.1);
    }
    
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.375rem;
      border-radius: 9999px;
      padding: 0.375rem 0.875rem;
      font-size: 0.875rem;
      font-weight: 500;
    }
    
    .badge-success {
      background: rgba(34, 197, 94, 0.1);
      color: #86efac;
      border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .badge-error {
      background: rgba(239, 68, 68, 0.1);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .badge-warning {
      background: rgba(250, 204, 21, 0.1);
      color: #fde047;
      border: 1px solid rgba(250, 204, 21, 0.3);
    }
    
    .code {
      background: #0f172a;
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 12px;
      padding: 1rem;
      font-family: monospace;
      font-size: 0.875rem;
      overflow-x: auto;
      white-space: pre-wrap;
    }
    
    .navbar {
      background: rgba(15, 23, 42, 0.8);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid rgba(148, 163, 184, 0.2);
      position: sticky;
      top: 0;
      z-index: 50;
    }
    
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid rgba(148, 163, 184, 0.2); }
    th { background: rgba(15, 23, 42, 0.5); font-weight: 600; }
    tr:hover { background: rgba(15, 23, 42, 0.3); }
    
    .fade-in { animation: fadeIn 0.5s ease-in-out; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  BODY_CONTENT
</body>
</html>"""

    # ==========================================================================
    # 🏠 LANDING PAGE
    # ==========================================================================

    LANDING = BASE.replace("BODY_CONTENT", """
<div class="min-h-screen flex flex-col">
  <div class="container mx-auto px-6 py-12 flex-1 flex items-center justify-center" style="max-width: 1200px;">
    <div class="w-full">
      <div class="card p-12 text-center mb-8 fade-in">
        <div style="font-size: 5rem; margin-bottom: 1.5rem;">🍌</div>
        <h1 style="font-size: 3rem; font-weight: bold; margin-bottom: 1rem; background: linear-gradient(to right, #FACC15, #CA8A04); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          Banana Hub Enterprise
        </h1>
        <p style="font-size: 1.25rem; color: #9ca3af; margin-bottom: 2rem;">Premium Roblox Script Hub</p>
        <div class="badge badge-success" style="margin-bottom: 2rem;">
          <i class="fas fa-shield-alt"></i>
          <span>🟢 Undetected</span>
        </div>
        
        <div style="display: flex; flex-direction: column; gap: 1rem; align-items: center; max-width: 400px; margin: 0 auto;">
          <a href="/login" class="btn" style="width: 100%;">
            <i class="fas fa-sign-in-alt"></i>
            <span>Login to Panel</span>
          </a>
          <a href="https://discord.gg/bananahub" target="_blank" class="btn-secondary" style="width: 100%;">
            <i class="fab fa-discord"></i>
            <span>Join Discord</span>
          </a>
        </div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
        <div class="card p-8 text-center">
          <div style="font-size: 2.5rem; font-weight: bold; color: #FACC15; margin-bottom: 0.5rem;">100+</div>
          <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase;">Active Users</div>
        </div>
        <div class="card p-8 text-center">
          <div style="font-size: 2.5rem; font-weight: bold; color: #FACC15; margin-bottom: 0.5rem;">50+</div>
          <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase;">Available Keys</div>
        </div>
        <div class="card p-8 text-center">
          <div style="font-size: 2.5rem; font-weight: bold; color: #FACC15; margin-bottom: 0.5rem;">1000+</div>
          <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase;">Total Logins</div>
        </div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
        <div class="card p-6">
          <div style="font-size: 2rem; margin-bottom: 0.75rem;">⚡</div>
          <h3 style="font-weight: 600; font-size: 1.125rem; margin-bottom: 0.5rem;">Lightning Fast</h3>
          <p style="color: #9ca3af; font-size: 0.875rem;">Optimized scripts with minimal impact</p>
        </div>
        <div class="card p-6">
          <div style="font-size: 2rem; margin-bottom: 0.75rem;">🔒</div>
          <h3 style="font-weight: 600; font-size: 1.125rem; margin-bottom: 0.5rem;">Secure & Safe</h3>
          <p style="color: #9ca3af; font-size: 0.875rem;">Advanced HWID protection</p>
        </div>
        <div class="card p-6">
          <div style="font-size: 2rem; margin-bottom: 0.75rem;">🎮</div>
          <h3 style="font-weight: 600; font-size: 1.125rem; margin-bottom: 0.5rem;">Multi-Game</h3>
          <p style="color: #9ca3af; font-size: 0.875rem;">Dozens of popular games</p>
        </div>
      </div>
    </div>
  </div>
  
  <footer style="text-align: center; padding: 1.5rem; color: #6b7280; font-size: 0.875rem; border-top: 1px solid rgba(148, 163, 184, 0.2);">
    <p>&copy; 2025 Banana Hub Enterprise</p>
  </footer>
</div>
""")

    # ==========================================================================
    # 🔐 LOGIN PAGE
    # ==========================================================================

    LOGIN = BASE.replace("BODY_CONTENT", """
<div class="min-h-screen flex items-center justify-center px-6 py-12">
  <div style="max-width: 28rem; width: 100%;">
    <div class="card p-10 fade-in">
      <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🍌</div>
        <h2 style="font-size: 1.875rem; font-weight: bold; margin-bottom: 0.5rem;">Welcome Back</h2>
        <p style="color: #9ca3af;">Sign in to your Banana Hub account</p>
      </div>
      
      <button id="showRedeemBtn" class="btn-secondary" style="width: 100%; margin-bottom: 1.5rem;">
        <i class="fas fa-key"></i>
        <span>Redeem New Key</span>
      </button>
      
      <form id="loginForm" style="display: flex; flex-direction: column; gap: 1.25rem;">
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; color: #d1d5db;">Discord ID</label>
          <input type="text" id="discordId" class="input" placeholder="123456789012345678" required>
          <p style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">Your Discord user ID</p>
        </div>
        
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; color: #d1d5db;">License Key</label>
          <input type="password" id="licenseKey" class="input" placeholder="BANANA-XXXXXXXXXXXX" required>
          <p style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">Your Banana Hub license key</p>
        </div>
        
        <button type="submit" class="btn" style="width: 100%;">
          <i class="fas fa-sign-in-alt"></i>
          <span>Sign In</span>
        </button>
      </form>
      
      <div id="statusMessage" style="margin-top: 1.5rem; display: none;"></div>
    </div>
    
    <div style="text-align: center; margin-top: 1.5rem;">
      <a href="/" style="color: #FACC15; font-size: 0.875rem; text-decoration: none;">
        <i class="fas fa-arrow-left" style="margin-right: 0.25rem;"></i>
        Back to Home
      </a>
    </div>
  </div>
</div>

<div id="redeemModal" style="display: none; position: fixed; inset: 0; z-index: 50; background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(4px); align-items: center; justify-content: center; padding: 1.5rem;">
  <div class="card p-8" style="max-width: 28rem; width: 100%;">
    <h3 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
      <span>🔑</span>
      <span>Redeem License Key</span>
    </h3>
    <p style="color: #9ca3af; margin-bottom: 1.5rem; font-size: 0.875rem;">
      Enter your Discord ID and license key to activate your account.
    </p>
    
    <form id="redeemForm" style="display: flex; flex-direction: column; gap: 1rem;">
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">Discord ID</label>
        <input type="text" id="redeemDiscordId" class="input" placeholder="123456789012345678" required>
      </div>
      
      <div>
        <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;">License Key</label>
        <input type="text" id="redeemKey" class="input" placeholder="BANANA-XXXXXXXXXXXX" required>
      </div>
      
      <div style="display: flex; gap: 0.75rem; padding-top: 0.5rem;">
        <button type="button" id="cancelRedeemBtn" class="btn-secondary" style="flex: 1;">Cancel</button>
        <button type="submit" class="btn" style="flex: 1;">Redeem</button>
      </div>
    </form>
  </div>
</div>

<script>
  function showStatus(message, type) {
    const statusDiv = document.getElementById('statusMessage');
    const colors = {
      success: 'badge-success',
      error: 'badge-error',
      info: 'badge-warning'
    };
    const icons = {
      success: 'fa-check-circle',
      error: 'fa-exclamation-circle',
      info: 'fa-info-circle'
    };
    
    statusDiv.innerHTML = '<div class="badge ' + colors[type] + '" style="width: 100%; justify-content: center;"><i class="fas ' + icons[type] + '"></i><span>' + message + '</span></div>';
    statusDiv.style.display = 'block';
  }
  
  document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    showStatus('Authenticating...', 'info');
    
    const uid = document.getElementById('discordId').value.trim();
    const key = document.getElementById('licenseKey').value.trim();
    
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid, key })
      });
      
      const result = await response.json();
      
      if (result.success) {
        showStatus('Login successful!', 'success');
        localStorage.setItem('banana_uid', uid);
        localStorage.setItem('banana_key', key);
        setTimeout(() => window.location.href = '/dashboard', 1000);
      } else {
        showStatus(result.message || 'Login failed', 'error');
      }
    } catch (error) {
      showStatus('Connection error', 'error');
    }
  });
  
  document.getElementById('showRedeemBtn').addEventListener('click', () => {
    document.getElementById('redeemModal').style.display = 'flex';
  });
  
  document.getElementById('cancelRedeemBtn').addEventListener('click', () => {
    document.getElementById('redeemModal').style.display = 'none';
  });
  
  document.getElementById('redeemForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const uid = document.getElementById('redeemDiscordId').value.trim();
    const key = document.getElementById('redeemKey').value.trim();
    
    try {
      const response = await fetch('/api/auth/redeem', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid, key })
      });
      
      const result = await response.json();
      
      if (result.success) {
        alert('✅ Key redeemed! You can now log in.');
        document.getElementById('redeemModal').style.display = 'none';
        document.getElementById('discordId').value = uid;
        document.getElementById('licenseKey').value = key;
      } else {
        alert('❌ ' + (result.message || 'Redemption failed'));
      }
    } catch (error) {
      alert('❌ Connection error');
    }
  });
  
  document.getElementById('redeemModal').addEventListener('click', (e) => {
    if (e.target.id === 'redeemModal') {
      document.getElementById('redeemModal').style.display = 'none';
    }
  });
</script>
""")

    # ==========================================================================
    # 📊 USER DASHBOARD
    # ==========================================================================

    DASHBOARD = BASE.replace("BODY_CONTENT", """
<div class="min-h-screen">
  <nav class="navbar">
    <div class="container mx-auto px-6 py-4" style="display: flex; align-items: center; justify-content: space-between; max-width: 1200px;">
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <span style="font-size: 1.5rem;">🍌</span>
        <h1 style="font-size: 1.25rem; font-weight: bold;">Banana Hub</h1>
      </div>
      <button id="logoutBtn" class="btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.875rem;">
        <i class="fas fa-sign-out-alt"></i>
        <span>Logout</span>
      </button>
    </div>
  </nav>
  
  <div class="container mx-auto px-6 py-8" style="max-width: 1200px;">
    <div style="margin-bottom: 2rem;">
      <h2 style="font-size: 1.875rem; font-weight: bold; margin-bottom: 0.5rem;">Dashboard</h2>
      <p style="color: #9ca3af;">Manage your Banana Hub account</p>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
      <div class="card p-6">
        <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          <i class="fas fa-key" style="color: #FACC15;"></i>
          <span>Your License</span>
        </h3>
        <div id="userKey" class="code" style="font-size: 0.75rem; margin-bottom: 1rem;">Loading...</div>
        <button id="copyKeyBtn" class="btn-secondary" style="width: 100%; font-size: 0.875rem;">
          <i class="fas fa-copy"></i>
          <span>Copy Key</span>
        </button>
      </div>
      
      <div class="card p-6">
        <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          <i class="fas fa-desktop" style="color: #FACC15;"></i>
          <span>HWID Status</span>
        </h3>
        <div id="hwidStatus" class="badge badge-warning" style="margin-bottom: 1rem;">
          <span>Checking...</span>
        </div>
        <button id="resetHwidBtn" class="btn" style="width: 100%; font-size: 0.875rem;">
          <i class="fas fa-redo"></i>
          <span>Reset HWID</span>
        </button>
      </div>
      
      <div class="card p-6">
        <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          <i class="fas fa-chart-line" style="color: #FACC15;"></i>
          <span>Activity</span>
        </h3>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #9ca3af; font-size: 0.875rem;">Logins</span>
            <span id="loginCount" style="font-weight: 600;">-</span>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #9ca3af; font-size: 0.875rem;">Last Login</span>
            <span id="lastLogin" style="font-size: 0.875rem;">-</span>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #9ca3af; font-size: 0.875rem;">Joined</span>
            <span id="joinedAt" style="font-size: 0.875rem;">-</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card p-8">
      <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
        <i class="fas fa-code" style="color: #FACC15;"></i>
        <span>Loader Script</span>
      </h3>
      <p style="color: #9ca3af; margin-bottom: 1rem; font-size: 0.875rem;">
        Copy this into your Roblox executor
      </p>
      <textarea id="loaderScript" class="code" style="width: 100%; height: 12rem; resize: none; outline: none;" readonly>-- Loading...</textarea>
      <div style="display: flex; gap: 0.75rem; margin-top: 1rem;">
        <button id="copyLoaderBtn" class="btn" style="flex: 1;">
          <i class="fas fa-copy"></i>
          <span>Copy Loader</span>
        </button>
        <button id="downloadLoaderBtn" class="btn-secondary" style="flex: 1;">
          <i class="fas fa-download"></i>
          <span>Download</span>
        </button>
      </div>
    </div>
  </div>
</div>

<script>
  const uid = localStorage.getItem('banana_uid');
  const key = localStorage.getItem('banana_key');
  
  if (!uid || !key) {
    window.location.href = '/login';
  }
  
  async function loadDashboard() {
    try {
      const response = await fetch('/api/auth/user_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid, key })
      });
      
      const result = await response.json();
      
      if (!result.success) {
        localStorage.clear();
        window.location.href = '/login';
        return;
      }
      
      const user = result.user;
      document.getElementById('userKey').textContent = user.key;
      document.getElementById('loaderScript').value = result.script;
      
      const hwidStatus = document.getElementById('hwidStatus');
      if (user.hwid_set) {
        hwidStatus.innerHTML = '<i class="fas fa-check"></i><span>HWID Set</span>';
        hwidStatus.className = 'badge badge-success';
      } else {
        hwidStatus.innerHTML = '<i class="fas fa-times"></i><span>Not Set</span>';
        hwidStatus.className = 'badge badge-warning';
      }
      
      document.getElementById('loginCount').textContent = user.login_count || 0;
      document.getElementById('lastLogin').textContent = user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never';
      document.getElementById('joinedAt').textContent = user.joined_at ? new Date(user.joined_at).toLocaleDateString() : 'Unknown';
      
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to load dashboard');
    }
  }
  
  document.getElementById('copyKeyBtn').addEventListener('click', async () => {
    const keyText = document.getElementById('userKey').textContent;
    await navigator.clipboard.writeText(keyText);
    const btn = document.getElementById('copyKeyBtn');
    btn.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
    setTimeout(() => btn.innerHTML = '<i class="fas fa-copy"></i><span>Copy Key</span>', 2000);
  });
  
  document.getElementById('copyLoaderBtn').addEventListener('click', async () => {
    const script = document.getElementById('loaderScript').value;
    await navigator.clipboard.writeText(script);
    const btn = document.getElementById('copyLoaderBtn');
    btn.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
    setTimeout(() => btn.innerHTML = '<i class="fas fa-copy"></i><span>Copy Loader</span>', 2000);
  });
  
  document.getElementById('downloadLoaderBtn').addEventListener('click', () => {
    const script = document.getElementById('loaderScript').value;
    const blob = new Blob([script], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'banana_loader.lua';
    a.click();
    URL.revokeObjectURL(url);
  });
  
  document.getElementById('resetHwidBtn').addEventListener('click', async () => {
    if (!confirm('Reset HWID?')) return;
    
    const response = await fetch('/api/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ uid })
    });
    
    const result = await response.json();
    alert(result.success ? '✅ HWID reset!' : '❌ Failed');
    if (result.success) location.reload();
  });
  
  document.getElementById('logoutBtn').addEventListener('click', () => {
    if (confirm('Logout?')) {
      localStorage.clear();
      window.location.href = '/login';
    }
  });
  
  loadDashboard();
</script>
""")

    # ==========================================================================
    # 🔧 ADMIN DASHBOARD
    # ==========================================================================

    ADMIN = BASE.replace("BODY_CONTENT", """
<div class="min-h-screen">
  <nav class="navbar">
    <div class="container mx-auto px-6 py-4" style="display: flex; align-items: center; justify-content: space-between; max-width: 1200px;">
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <span style="font-size: 1.5rem;">🍌</span>
        <h1 style="font-size: 1.25rem; font-weight: bold;">Admin Panel</h1>
      </div>
      <a href="/" class="btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.875rem;">
        <i class="fas fa-home"></i>
        <span>Home</span>
      </a>
    </div>
  </nav>
  
  <div class="container mx-auto px-6 py-8" style="max-width: 1400px;">
    <div style="margin-bottom: 2rem;">
      <h2 style="font-size: 1.875rem; font-weight: bold; margin-bottom: 0.5rem;">Admin Dashboard</h2>
      <p style="color: #9ca3af;">Manage users, keys, and system settings</p>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
      <div class="card p-6 text-center">
        <div style="font-size: 2rem; font-weight: bold; color: #FACC15;">STATS_TOTAL_USERS</div>
        <div style="color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; margin-top: 0.25rem;">Users</div>
      </div>
      <div class="card p-6 text-center">
        <div style="font-size: 2rem; font-weight: bold; color: #FACC15;">STATS_TOTAL_KEYS</div>
        <div style="color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; margin-top: 0.25rem;">Total Keys</div>
      </div>
      <div class="card p-6 text-center">
        <div style="font-size: 2rem; font-weight: bold; color: #86efac;">STATS_AVAILABLE_KEYS</div>
        <div style="color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; margin-top: 0.25rem;">Available</div>
      </div>
      <div class="card p-6 text-center">
        <div style="font-size: 2rem; font-weight: bold; color: #93c5fd;">STATS_TOTAL_LOGINS</div>
        <div style="color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; margin-top: 0.25rem;">Logins</div>
      </div>
      <div class="card p-6 text-center">
        <div style="font-size: 2rem; font-weight: bold; color: #fca5a5;">STATS_BLACKLISTED</div>
        <div style="color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; margin-top: 0.25rem;">Banned</div>
      </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
      <div class="card p-6">
        <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          <i class="fas fa-key" style="color: #FACC15;"></i>
          <span>Key Management</span>
        </h3>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <button onclick="genKeys()" class="btn" style="width: 100%;">
            <i class="fas fa-plus"></i>
            <span>Generate Keys</span>
          </button>
          <button onclick="viewKeys()" class="btn-secondary" style="width: 100%;">
            <i class="fas fa-list"></i>
            <span>View All Keys</span>
          </button>
        </div>
      </div>
      
      <div class="card p-6">
        <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          <i class="fas fa-users" style="color: #FACC15;"></i>
          <span>User Management</span>
        </h3>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <button onclick="viewUsers()" class="btn-secondary" style="width: 100%;">
            <i class="fas fa-list"></i>
            <span>View All Users</span>
          </button>
          <button onclick="lookupUser()" class="btn-secondary" style="width: 100%;">
            <i class="fas fa-search"></i>
            <span>Lookup User</span>
          </button>
        </div>
      </div>
      
      <div class="card p-6">
        <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          <i class="fas fa-shield-alt" style="color: #FACC15;"></i>
          <span>Security</span>
        </h3>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <button onclick="viewBlacklist()" class="btn-secondary" style="width: 100%;">
            <i class="fas fa-ban"></i>
            <span>View Blacklist</span>
          </button>
          <button onclick="alert('Backup feature coming soon')" class="btn-secondary" style="width: 100%;">
            <i class="fas fa-database"></i>
            <span>Backup Database</span>
          </button>
        </div>
      </div>
    </div>
    
    <div id="contentArea" class="card p-6" style="display: none;">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <h3 id="contentTitle" style="font-size: 1.25rem; font-weight: 600;">Content</h3>
        <button onclick="closeContent()" class="btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.875rem;">
          <i class="fas fa-times"></i>
          <span>Close</span>
        </button>
      </div>
      <div id="contentBody" style="overflow-x: auto;"></div>
    </div>
  </div>
</div>

<script>
  const API_KEY = 'CONFIG_API_KEY';
  
  async function api(endpoint, method, body) {
    method = method || 'GET';
    const options = {
      method: method,
      headers: {
        'Authorization': 'Bearer ' + API_KEY,
        'Content-Type': 'application/json'
      }
    };
    if (body) options.body = JSON.stringify(body);
    
    const response = await fetch(endpoint, options);
    return await response.json();
  }
  
  function showContent(title, html) {
    document.getElementById('contentTitle').textContent = title;
    document.getElementById('contentBody').innerHTML = html;
    document.getElementById('contentArea').style.display = 'block';
    document.getElementById('contentArea').scrollIntoView({ behavior: 'smooth' });
  }
  
  function closeContent() {
    document.getElementById('contentArea').style.display = 'none';
  }
  
  async function genKeys() {
    const amount = prompt('How many keys? (1-25)', '1');
    if (!amount) return;
    
    const result = await api('/api/admin/genkey', 'POST', { amount: parseInt(amount) });
    if (result.success) {
      alert('✅ Generated ' + result.data.keys.length + ' keys:\\n\\n' + result.data.keys.join('\\n'));
    } else {
      alert('❌ Failed: ' + result.message);
    }
  }
  
  async function viewKeys() {
    const result = await api('/api/admin/keys');
    if (!result.success) return alert('Failed to load keys');
    
    let html = '<table><thead><tr><th>Key</th><th>Status</th><th>Used By</th><th>Created</th></tr></thead><tbody>';
    result.keys.forEach(k => {
      html += '<tr><td style="font-family: monospace; font-size: 0.75rem;">' + k.key + '</td>';
      html += '<td>' + (k.used ? '<span class="badge badge-error">Used</span>' : '<span class="badge badge-success">Available</span>') + '</td>';
      html += '<td>' + (k.used_by || '-') + '</td>';
      html += '<td>' + new Date(k.created_at).toLocaleDateString() + '</td></tr>';
    });
    html += '</tbody></table>';
    showContent('All Keys', html);
  }
  
  async function viewUsers() {
    const result = await api('/api/admin/users');
    if (!result.success) return alert('Failed to load users');
    
    let html = '<table><thead><tr><th>Discord ID</th><th>Key</th><th>HWID</th><th>Last Login</th></tr></thead><tbody>';
    result.users.forEach(u => {
      html += '<tr><td style="font-family: monospace; font-size: 0.75rem;">' + u.discord_id + '</td>';
      html += '<td style="font-family: monospace; font-size: 0.75rem;">' + u.key + '</td>';
      html += '<td>' + (u.hwid ? '<span class="badge badge-success">Set</span>' : '<span class="badge badge-warning">None</span>') + '</td>';
      html += '<td>' + (u.last_login ? new Date(u.last_login).toLocaleDateString() : 'Never') + '</td></tr>';
    });
    html += '</tbody></table>';
    showContent('All Users', html);
  }
  
  async function lookupUser() {
    const id = prompt('Enter Discord ID:');
    if (!id) return;
    
    const result = await api('/api/admin/lookup?discord_id=' + id);
    if (!result.success) return alert('User not found');
    
    const u = result.user;
    const a = result.analytics;
    let html = '<div style="display: flex; flex-direction: column; gap: 1rem;">';
    html += '<div><strong>Discord ID:</strong> ' + u.discord_id + '</div>';
    html += '<div><strong>Key:</strong> de style="background: #1e293b; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">' + u.key + '</code></div>';
    html += '<div><strong>HWID:</strong> ' + (u.hwid || 'Not set') + '</div>';
    html += '<div><strong>Joined:</strong> ' + new Date(u.joined_at).toLocaleString() + '</div>';
    html += '<div><strong>Last Login:</strong> ' + (u.last_login ? new Date(u.last_login).toLocaleString() : 'Never') + '</div>';
    html += '<div><strong>Total Logins:</strong> ' + a.login_count + '</div>';
    html += '<div><strong>HWID Resets:</strong> ' + a.reset_count + '</div>';
    html += '<div><strong>Blacklisted:</strong> ' + (result.is_blacklisted ? 'Yes ❌' : 'No ✅') + '</div>';
    html += '</div>';
    showContent('User: ' + id, html);
  }
  
  async function viewBlacklist() {
    const result = await api('/api/admin/blacklist');
    if (!result.success) return alert('Failed to load blacklist');
    
    let html = '<table><thead><tr><th>Discord ID</th><th>Reason</th><th>Banned At</th></tr></thead><tbody>';
    result.blacklisted.forEach(b => {
      html += '<tr><td style="font-family: monospace; font-size: 0.75rem;">' + b.discord_id + '</td>';
      html += '<td>' + b.reason + '</td>';
      html += '<td>' + new Date(b.banned_at).toLocaleDateString() + '</td></tr>';
    });
    html += '</tbody></table>';
    showContent('Blacklisted Users', html);
  }
</script>
""")

    # ==========================================================================
    # ❌ ERROR PAGES
    # ==========================================================================

    ERROR_404 = BASE.replace("BODY_CONTENT", """
<div class="min-h-screen flex items-center justify-center px-6">
  <div class="card p-12 text-center" style="max-width: 28rem;">
    <div style="font-size: 4rem; margin-bottom: 1rem;">🤔</div>
    <h1 style="font-size: 2.25rem; font-weight: bold; margin-bottom: 1rem;">404</h1>
    <p style="color: #9ca3af; margin-bottom: 1.5rem;">Page not found</p>
    <a href="/" class="btn">
      <i class="fas fa-home"></i>
      <span>Go Home</span>
    </a>
  </div>
</div>
""")

    ERROR_500 = BASE.replace("BODY_CONTENT", """
<div class="min-h-screen flex items-center justify-center px-6">
  <div class="card p-12 text-center" style="max-width: 28rem;">
    <div style="font-size: 4rem; margin-bottom: 1rem;">💥</div>
    <h1 style="font-size: 2.25rem; font-weight: bold; margin-bottom: 1rem;">500</h1>
    <p style="color: #9ca3af; margin-bottom: 1.5rem;">Internal server error</p>
    <a href="/" class="btn">
      <i class="fas fa-home"></i>
      <span>Go Home</span>
    </a>
  </div>
</div>
""")
