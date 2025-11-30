# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - WEB TEMPLATES v4.0 (FULLY FIXED)
# Modern sidebar design with corrected Jinja2 syntax
# ==============================================================================

from __future__ import annotations

# ==============================================================================
# 🎨 BASE TEMPLATE WITH MODERN SIDEBAR
# ==============================================================================

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#7C3AED">
    <title>Banana Hub Enterprise</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #7C3AED;
            --primary-dark: #6D28D9;
            --primary-light: #8B5CF6;
            --secondary: #FACC15;
            --bg-dark: #0F172A;
            --bg-card: #1E293B;
            --text: #F1F5F9;
            --text-muted: #94A3B8;
            --border: #334155;
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            line-height: 1.6;
        }
        
        /* Sidebar Styles */
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
            width: 280px;
            background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
            padding: 2rem 0;
            overflow-y: auto;
            transition: transform 0.3s ease;
            z-index: 1000;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
        }
        
        .sidebar::-webkit-scrollbar {
            width: 6px;
        }
        
        .sidebar::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }
        
        .sidebar::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
        }
        
        .sidebar-header {
            padding: 0 1.5rem 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.5rem;
            font-weight: 800;
            color: white;
            text-decoration: none;
        }
        
        .user-profile {
            margin-top: 1.5rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .user-avatar {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--secondary), #FCD34D);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--bg-dark);
        }
        
        .user-info h4 {
            font-size: 0.875rem;
            font-weight: 600;
            color: white;
            margin-bottom: 0.25rem;
        }
        
        .user-info p {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .sidebar-nav {
            padding: 1.5rem 1rem;
        }
        
        .nav-section {
            margin-bottom: 2rem;
        }
        
        .nav-section-title {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: rgba(255, 255, 255, 0.5);
            padding: 0 0.5rem;
            margin-bottom: 0.75rem;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 0.75rem;
            border-radius: 8px;
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: all 0.2s;
            margin-bottom: 0.25rem;
            font-size: 0.875rem;
            cursor: pointer;
        }
        
        .nav-item:hover, .nav-item.active {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            transform: translateX(4px);
        }
        
        .nav-item i {
            width: 20px;
            text-align: center;
        }
        
        /* Main Content */
        .main-content {
            margin-left: 280px;
            min-height: 100vh;
            background: var(--bg-dark);
        }
        
        .topbar {
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .topbar-left h1 {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
        }
        
        .topbar-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .content-area {
            padding: 2rem;
        }
        
        /* Cards */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s;
        }
        
        .card:hover {
            border-color: var(--primary-light);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.15);
        }
        
        .card-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .card-title i {
            color: var(--primary-light);
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, var(--primary), var(--primary-light));
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.5rem;
        }
        
        .stat-change {
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .stat-change.positive {
            color: var(--success);
        }
        
        .stat-change.negative {
            color: var(--error);
        }
        
        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            border: none;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(124, 58, 237, 0.3);
        }
        
        .btn-secondary {
            background: var(--bg-card);
            color: var(--text);
            border: 1px solid var(--border);
        }
        
        .btn-secondary:hover {
            border-color: var(--primary);
        }
        
        .btn-success {
            background: var(--success);
            color: white;
        }
        
        .btn-danger {
            background: var(--error);
            color: white;
        }
        
        /* Input */
        .input {
            width: 100%;
            padding: 0.875rem 1rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text);
            font-size: 0.875rem;
            transition: all 0.2s;
            outline: none;
        }
        
        .input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
        }
        
        .input::placeholder {
            color: var(--text-muted);
        }
        
        /* Badge */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.375rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-success {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
        }
        
        .badge-warning {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
        }
        
        .badge-error {
            background: rgba(239, 68, 68, 0.1);
            color: var(--error);
        }
        
        .badge-primary {
            background: rgba(124, 58, 237, 0.1);
            color: var(--primary-light);
        }
        
        /* Table */
        .table-container {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        
        th {
            background: rgba(124, 58, 237, 0.05);
            color: var(--primary-light);
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        td {
            font-size: 0.875rem;
            color: var(--text);
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        tr:hover {
            background: rgba(124, 58, 237, 0.03);
        }
        
        /* Code Block */
        .code {
            background: #0D1117;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.813rem;
            overflow-x: auto;
            color: #C9D1D9;
            line-height: 1.6;
        }
        
        /* Grid Layouts */
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
        }
        
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
        }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .sidebar {
                transform: translateX(-100%);
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .main-content {
                margin-left: 0;
            }
            
            .mobile-menu-btn {
                display: block;
            }
        }
        
        @media (max-width: 768px) {
            .content-area {
                padding: 1rem;
            }
            
            .stats-grid, .grid-2, .grid-3 {
                grid-template-columns: 1fr;
            }
            
            .topbar {
                padding: 1rem;
            }
        }
        
        .mobile-menu-btn {
            display: none;
            background: var(--primary);
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
</head>
<body>
    {BODY_CONTENT}
    
    <script>
        function toggleSidebar() {
            document.querySelector('.sidebar').classList.toggle('active');
        }
    </script>
</body>
</html>"""

# ==============================================================================
# 🏠 LANDING PAGE
# ==============================================================================

LANDING_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem; background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);">
    <div style="max-width: 1200px; width: 100%; text-align: center;">
        
        <div class="fade-in" style="margin-bottom: 3rem;">
            <div style="font-size: 5rem; margin-bottom: 1rem;">🍌</div>
            <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; background: linear-gradient(135deg, #7C3AED, #A78BFA, #FACC15); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                Banana Hub Enterprise
            </h1>
            <p style="font-size: 1.25rem; color: var(--text-muted); margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Premium Roblox Script Hub with Advanced Features
            </p>
            
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 3rem;">
                <a href="/login" class="btn btn-primary" style="font-size: 1rem; padding: 1rem 2.5rem;">
                    <i class="fas fa-sign-in-alt"></i>
                    <span>Access Dashboard</span>
                </a>
                <a href="https://discord.gg/bananahub" target="_blank" class="btn btn-secondary" style="font-size: 1rem; padding: 1rem 2.5rem;">
                    <i class="fab fa-discord"></i>
                    <span>Join Discord</span>
                </a>
            </div>
        </div>
        
        <div class="grid-3 fade-in" style="animation-delay: 0.2s;">
            <div class="card">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚡</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--text);">Lightning Fast</h3>
                <p style="color: var(--text-muted); font-size: 0.875rem;">Optimized performance with instant execution</p>
            </div>
            
            <div class="card">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔒</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--text);">Secure</h3>
                <p style="color: var(--text-muted); font-size: 0.875rem;">HWID protection and encrypted auth</p>
            </div>
            
            <div class="card">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎮</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--text);">Multi-Game</h3>
                <p style="color: var(--text-muted); font-size: 0.875rem;">Works with all major executors</p>
            </div>
        </div>
        
    </div>
</div>
""")

# ==============================================================================
# 🔐 LOGIN PAGE
# ==============================================================================

LOGIN_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem; background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);">
    <div style="max-width: 450px; width: 100%;">
        <div class="card fade-in">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🍌</div>
                <h2 style="font-size: 1.75rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--text);">Welcome Back</h2>
                <p style="color: var(--text-muted); font-size: 0.875rem;">Sign in to your account</p>
            </div>
            
            <form id="loginForm" style="display: flex; flex-direction: column; gap: 1.25rem;" onsubmit="handleLogin(event)">
                <div>
                    <label style="display: block; font-size: 0.813rem; font-weight: 500; margin-bottom: 0.5rem; color: var(--text);">Discord ID</label>
                    <input type="text" id="user_id" name="user_id" class="input" placeholder="123456789012345678" required>
                </div>
                
                <div>
                    <label style="display: block; font-size: 0.813rem; font-weight: 500; margin-bottom: 0.5rem; color: var(--text);">License Key</label>
                    <input type="password" id="key" name="key" class="input" placeholder="BH-XXXXXXXXXXXX" required>
                </div>
                
                <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; margin-top: 0.5rem;">
                    <i class="fas fa-sign-in-alt"></i>
                    <span>Sign In</span>
                </button>
            </form>
            
            <div id="statusMessage" style="margin-top: 1.25rem; display: none;"></div>
            
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="/" style="color: var(--primary-light); font-size: 0.813rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem;">
                    <i class="fas fa-arrow-left"></i>
                    <span>Back to Home</span>
                </a>
            </div>
        </div>
    </div>
</div>

<script>
    function showStatus(message, type) {
        const statusDiv = document.getElementById('statusMessage');
        const classes = {
            'success': 'badge-success',
            'error': 'badge-error',
            'info': 'badge-warning'
        };
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'info': 'fa-info-circle'
        };
        
        statusDiv.innerHTML = `<div class="badge ${classes[type]}" style="width: 100%; justify-content: center;"><i class="fas ${icons[type]}"></i><span>${message}</span></div>`;
        statusDiv.style.display = 'block';
    }
    
    async function handleLogin(e) {
        e.preventDefault();
        showStatus('Authenticating...', 'info');
        
        const formData = new FormData(e.target);
        const data = {
            user_id: formData.get('user_id').trim(),
            key: formData.get('key').trim()
        };
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success || response.ok) {
                showStatus('Login successful!', 'success');
                setTimeout(() => {
                    window.location.href = result.redirect || '/dashboard';
                }, 800);
            } else {
                showStatus(result.error || 'Login failed', 'error');
            }
        } catch (error) {
            showStatus('Connection error', 'error');
        }
    }
</script>
""")

# ==============================================================================
# 👤 USER DASHBOARD
# ==============================================================================

DASHBOARD_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<!-- Sidebar -->
<aside class="sidebar">
    <div class="sidebar-header">
        <a href="/" class="logo">
            <span>🍌</span>
            <span>Banana Hub</span>
        </a>
        
        <div class="user-profile">
            <div class="user-avatar">{{ user.get('discord_id', 'U')[0]|upper }}</div>
            <div class="user-info">
                <h4>{{ user.get('discord_id', 'User')[:12] }}...</h4>
                <p>User Account</p>
            </div>
        </div>
    </div>
    
    <nav class="sidebar-nav">
        <div class="nav-section">
            <div class="nav-section-title">Main</div>
            <a href="/dashboard" class="nav-item active">
                <i class="fas fa-chart-line"></i>
                <span>Dashboard</span>
            </a>
            <a href="#loader" class="nav-item">
                <i class="fas fa-code"></i>
                <span>Script Loader</span>
            </a>
            <a href="#activity" class="nav-item">
                <i class="fas fa-history"></i>
                <span>Activity</span>
            </a>
        </div>
        
        <div class="nav-section">
            <div class="nav-section-title">Account</div>
            <a href="#profile" class="nav-item">
                <i class="fas fa-user"></i>
                <span>Profile</span>
            </a>
            <a href="#settings" class="nav-item">
                <i class="fas fa-cog"></i>
                <span>Settings</span>
            </a>
            <a href="/logout" class="nav-item">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </a>
        </div>
    </nav>
</aside>

<!-- Main Content -->
<main class="main-content">
    <!-- Topbar -->
    <div class="topbar">
        <div class="topbar-left">
            <button class="mobile-menu-btn" onclick="toggleSidebar()">
                <i class="fas fa-bars"></i>
            </button>
            <h1>Dashboard</h1>
        </div>
        <div class="topbar-right">
            <span style="color: var(--text-muted); font-size: 0.875rem;">Welcome back!</span>
        </div>
    </div>
    
    <!-- Content Area -->
    <div class="content-area">
        
        <!-- Stats Grid -->
        <div class="stats-grid fade-in">
            <div class="stat-card">
                <div class="stat-label">License Key</div>
                <div class="stat-value" style="font-size: 1.25rem; word-break: break-all;">{{ user.get('key', 'N/A')[:15] }}...</div>
                <div class="stat-change positive">
                    <i class="fas fa-check-circle"></i>
                    <span>Active</span>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">HWID Status</div>
                <div class="stat-value" style="font-size: 1.5rem;">
                    {% if user.get('hwid') %}
                    <span class="badge badge-success"><i class="fas fa-check"></i> Set</span>
                    {% else %}
                    <span class="badge badge-warning"><i class="fas fa-times"></i> Not Set</span>
                    {% endif %}
                </div>
                <button onclick="resetHWID()" class="btn btn-primary" style="margin-top: 0.75rem; font-size: 0.75rem; padding: 0.5rem 1rem;">
                    <i class="fas fa-redo"></i> Reset
                </button>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Total Logins</div>
                <div class="stat-value">{{ analytics.get('total_logins', 0) }}</div>
                <div class="stat-change positive">
                    <i class="fas fa-arrow-up"></i>
                    <span>All time</span>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Member Since</div>
                <div class="stat-value" style="font-size: 1.25rem;">{{ user.get('joined_at', 'Unknown')[:10] }}</div>
                <div class="stat-change">
                    <i class="fas fa-calendar"></i>
                    <span>{{ user.get('last_login', 'Never')[:10] }}</span>
                </div>
            </div>
        </div>
        
        <!-- Main Cards Grid -->
        <div class="grid-2" style="margin-top: 2rem;">
            
            <!-- Loader Script Card -->
            <div class="card fade-in" id="loader">
                <h3 class="card-title">
                    <i class="fas fa-code"></i>
                    <span>Script Loader</span>
                </h3>
                <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">
                    Copy this script into your executor
                </p>
                <textarea id="loaderScript" class="code" style="width: 100%; height: 180px; resize: none; outline: none; margin-bottom: 1rem;" readonly>{{ loader_script }}</textarea>
                <div style="display: flex; gap: 0.75rem;">
                    <button onclick="copyLoader()" class="btn btn-primary" style="flex: 1;">
                        <i class="fas fa-copy"></i>
                        <span>Copy</span>
                    </button>
                    <button onclick="downloadLoader()" class="btn btn-secondary">
                        <i class="fas fa-download"></i>
                        <span>Download</span>
                    </button>
                </div>
            </div>
            
            <!-- Quick Actions Card -->
            <div class="card fade-in">
                <h3 class="card-title">
                    <i class="fas fa-bolt"></i>
                    <span>Quick Actions</span>
                </h3>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <button onclick="copyKey()" class="btn btn-secondary" style="justify-content: flex-start; width: 100%;">
                        <i class="fas fa-key"></i>
                        <span>Copy License Key</span>
                    </button>
                    <button onclick="resetHWID()" class="btn btn-secondary" style="justify-content: flex-start; width: 100%;">
                        <i class="fas fa-desktop"></i>
                        <span>Reset HWID</span>
                    </button>
                    <button onclick="window.open('https://discord.gg/bananahub')" class="btn btn-secondary" style="justify-content: flex-start; width: 100%;">
                        <i class="fab fa-discord"></i>
                        <span>Join Discord</span>
                    </button>
                    <a href="/logout" class="btn btn-danger" style="justify-content: flex-start; width: 100%;">
                        <i class="fas fa-sign-out-alt"></i>
                        <span>Logout</span>
                    </a>
                </div>
            </div>
            
        </div>
        
    </div>
</main>

<script>
    async function copyKey() {
        const keyText = '{{ user.get("key", "") }}';
        await navigator.clipboard.writeText(keyText);
        alert('✅ Key copied!');
    }
    
    async function copyLoader() {
        const script = document.getElementById('loaderScript').value;
        await navigator.clipboard.writeText(script);
        alert('✅ Loader copied!');
    }
    
    function downloadLoader() {
        const script = document.getElementById('loaderScript').value;
        const blob = new Blob([script], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'banana_loader.lua';
        a.click();
        URL.revokeObjectURL(url);
    }
    
    async function resetHWID() {
        if (!confirm('Reset your HWID? (5 min cooldown)')) return;
        
        try {
            const response = await fetch('/api/user/reset-hwid', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert('✅ HWID reset!');
                location.reload();
            } else {
                alert('❌ ' + (result.error || 'Failed'));
            }
        } catch (error) {
            alert('❌ Connection error');
        }
    }
</script>
""")

# ==============================================================================
# 🛡️ ADMIN PANEL
# ==============================================================================

ADMIN_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<!-- Sidebar -->
<aside class="sidebar">
    <div class="sidebar-header">
        <a href="/" class="logo">
            <span>🍌</span>
            <span>Banana Hub</span>
        </a>
        
        <div class="user-profile">
            <div class="user-avatar">A</div>
            <div class="user-info">
                <h4>Admin</h4>
                <p>Administrator</p>
            </div>
        </div>
    </div>
    
    <nav class="sidebar-nav">
        <div class="nav-section">
            <div class="nav-section-title">Main</div>
            <a href="/admin" class="nav-item active">
                <i class="fas fa-chart-pie"></i>
                <span>Dashboard</span>
            </a>
            <a href="#users" class="nav-item">
                <i class="fas fa-users"></i>
                <span>Users</span>
            </a>
            <a href="#keys" class="nav-item">
                <i class="fas fa-key"></i>
                <span>License Keys</span>
            </a>
        </div>
        
        <div class="nav-section">
            <div class="nav-section-title">Management</div>
            <a href="#" onclick="generateKeys(); return false;" class="nav-item">
                <i class="fas fa-plus-circle"></i>
                <span>Generate Keys</span>
            </a>
            <a href="#" onclick="whitelistUser(); return false;" class="nav-item">
                <i class="fas fa-user-plus"></i>
                <span>Whitelist User</span>
            </a>
            <a href="#" onclick="createBackup(); return false;" class="nav-item">
                <i class="fas fa-database"></i>
                <span>Backup</span>
            </a>
        </div>
        
        <div class="nav-section">
            <div class="nav-section-title">Account</div>
            <a href="/dashboard" class="nav-item">
                <i class="fas fa-user"></i>
                <span>User View</span>
            </a>
            <a href="/logout" class="nav-item">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </a>
        </div>
    </nav>
</aside>

<!-- Main Content -->
<main class="main-content">
    <!-- Topbar -->
    <div class="topbar">
        <div class="topbar-left">
            <button class="mobile-menu-btn" onclick="toggleSidebar()">
                <i class="fas fa-bars"></i>
            </button>
            <h1>Admin Dashboard</h1>
        </div>
        <div class="topbar-right">
            <span class="badge badge-error"><i class="fas fa-shield-alt"></i> Admin Access</span>
        </div>
    </div>
    
    <!-- Content Area -->
    <div class="content-area">
        
        <!-- Stats Grid -->
        <div class="stats-grid fade-in">
            <div class="stat-card">
                <div class="stat-label">Total Users</div>
                <div class="stat-value">{{ stats.get('total_users', 0) }}</div>
                <div class="stat-change positive">
                    <i class="fas fa-arrow-up"></i>
                    <span>Active</span>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Total Keys</div>
                <div class="stat-value">{{ stats.get('total_keys', 0) }}</div>
                <div class="stat-change">
                    <i class="fas fa-key"></i>
                    <span>Generated</span>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Available Keys</div>
                <div class="stat-value">{{ stats.get('available_keys', 0) }}</div>
                <div class="stat-change positive">
                    <i class="fas fa-check"></i>
                    <span>Ready</span>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Total Logins</div>
                <div class="stat-value">{{ stats.get('total_logins', 0) }}</div>
                <div class="stat-change">
                    <i class="fas fa-chart-line"></i>
                    <span>All time</span>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Banned Users</div>
                <div class="stat-value">{{ stats.get('total_blacklisted', 0) }}</div>
                <div class="stat-change negative">
                    <i class="fas fa-ban"></i>
                    <span>Blacklisted</span>
                </div>
            </div>
        </div>
        
        <!-- Users Table -->
        <div class="card fade-in" style="margin-top: 2rem;" id="users">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h3 class="card-title">
                    <i class="fas fa-users"></i>
                    <span>All Users ({{ users|length }})</span>
                </h3>
                <input type="text" id="userSearch" onkeyup="searchUsers()" placeholder="Search users..." class="input" style="width: 300px; padding: 0.625rem 1rem;">
            </div>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Discord ID</th>
                            <th>Key</th>
                            <th>HWID</th>
                            <th>Joined</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="usersTable">
                        {% for user in users[:20] %}
                        <tr data-user-id="{{ user.get('discord_id', '') }}">
                            <td>
                                <span style="background: rgba(124, 58, 237, 0.1); padding: 0.375rem 0.625rem; border-radius: 6px; color: var(--primary-light); font-family: monospace; font-size: 0.813rem;">
                                    {{ user.get('discord_id', '')[:16] }}
                                </span>
                            </td>
                            <td>
                                <span style="background: rgba(16, 185, 129, 0.1); padding: 0.375rem 0.625rem; border-radius: 6px; color: var(--success); font-family: monospace; font-size: 0.75rem;">
                                    {{ user.get('key', 'None')[:12] }}...
                                </span>
                            </td>
                            <td>
                                <span style="font-family: monospace; font-size: 0.75rem; color: var(--text-muted);">
                                    {% if user.get('hwid') %}
                                        {% if user.get('hwid')|length > 12 %}
                                            {{ user.get('hwid')[:12] }}...
                                        {% else %}
                                            {{ user.get('hwid') }}
                                        {% endif %}
                                    {% else %}
                                        Not set
                                    {% endif %}
                                </span>
                            </td>
                            <td style="font-size: 0.813rem; color: var(--text-muted);">{{ user.get('joined_at', 'Unknown')[:10] }}</td>
                            <td>
                                <span class="badge badge-success user-status" data-status="active"><i class="fas fa-check"></i> Active</span>
                            </td>
                            <td>
                                <button onclick="manageUser('{{ user.get('discord_id', '') }}')" class="btn btn-secondary" style="padding: 0.375rem 0.75rem; font-size: 0.75rem;">
                                    <i class="fas fa-cog"></i>
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Keys Table -->
        <div class="card fade-in" style="margin-top: 2rem;" id="keys">
            <h3 class="card-title">
                <i class="fas fa-key"></i>
                <span>Available Keys ({{ unused_keys|length }})</span>
            </h3>
            
            <div class="table-container" style="margin-top: 1rem;">
                <table>
                    <thead>
                        <tr>
                            <th>Key</th>
                            <th>Created</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for key in unused_keys[:15] %}
                        <tr>
                            <td>
                                <span style="background: rgba(16, 185, 129, 0.1); padding: 0.375rem 0.625rem; border-radius: 6px; color: var(--success); font-family: monospace; font-size: 0.813rem;">
                                    {{ key.get('key', '') }}
                                </span>
                            </td>
                            <td style="font-size: 0.813rem; color: var(--text-muted);">{{ key.get('created_at', 'Unknown')[:10] }}</td>
                            <td><span class="badge badge-success">Available</span></td>
                            <td>
                                <button onclick="copyText('{{ key.get('key', '') }}')" class="btn btn-primary" style="padding: 0.375rem 0.75rem; font-size: 0.75rem;">
                                    <i class="fas fa-copy"></i>
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        
    </div>
</main>

<script>
    // Mark banned users on page load
    document.addEventListener('DOMContentLoaded', function() {
        const blacklistedIds = {{ blacklisted|map(attribute='discord_id')|list|tojson }};
        
        document.querySelectorAll('[data-user-id]').forEach(row => {
            const userId = row.getAttribute('data-user-id');
            const statusBadge = row.querySelector('.user-status');
            
            if (blacklistedIds.includes(userId)) {
                statusBadge.className = 'badge badge-error user-status';
                statusBadge.innerHTML = '<i class="fas fa-ban"></i> Banned';
                statusBadge.setAttribute('data-status', 'banned');
            }
        });
    });
    
    function searchUsers() {
        const input = document.getElementById('userSearch');
        const filter = input.value.toUpperCase();
        const table = document.getElementById('usersTable');
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length; j++) {
                if (cells[j].textContent.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
            
            rows[i].style.display = found ? '' : 'none';
        }
    }
    
    async function generateKeys() {
        const count = prompt('How many keys? (1-25):', '1');
        if (!count) return;
        
        const num = parseInt(count);
        if (isNaN(num) || num < 1 || num > 25) {
            alert('❌ Invalid count');
            return;
        }
        
        try {
            const response = await fetch('/api/admin/generate-key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({count: num})
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert(`✅ Generated ${data.count} keys!\\n\\n${data.keys.join('\\n')}`);
                location.reload();
            } else {
                alert('❌ Failed');
            }
        } catch (error) {
            alert('❌ Error');
        }
    }
    
    async function whitelistUser() {
        const discordId = prompt('Discord User ID:');
        if (!discordId) return;
        
        try {
            const response = await fetch('/api/admin/whitelist', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({discord_id: discordId})
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert(`✅ Whitelisted!\\nKey: ${data.key}`);
                location.reload();
            } else {
                alert('❌ ' + data.error);
            }
        } catch (error) {
            alert('❌ Error');
        }
    }
    
    async function manageUser(discordId) {
        const action = prompt(`Manage: ${discordId}\\n\\n1 - Reset HWID\\n2 - Ban\\n3 - Unban\\n4 - Unwhitelist\\n\\nChoice:`);
        
        if (action === '1') {
            if (!confirm('Reset HWID?')) return;
            
            try {
                const response = await fetch('/api/admin/reset-hwid', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({discord_id: discordId})
                });
                
                const data = await response.json();
                alert(data.success ? '✅ HWID reset!' : '❌ Failed');
                if (data.success) location.reload();
            } catch (error) {
                alert('❌ Error');
            }
        } else if (action === '2' || action === '3') {
            const reason = action === '2' ? (prompt('Reason:') || 'No reason') : 'Unbanned';
            
            try {
                const response = await fetch('/api/admin/blacklist', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({discord_id: discordId, reason: reason})
                });
                
                const data = await response.json();
                alert(data.success ? `✅ ${data.action}ed!` : '❌ Failed');
                if (data.success) location.reload();
            } catch (error) {
                alert('❌ Error');
            }
        } else if (action === '4') {
            if (!confirm('Unwhitelist?')) return;
            
            try {
                const response = await fetch('/api/admin/unwhitelist', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({discord_id: discordId})
                });
                
                const data = await response.json();
                alert(data.success ? '✅ Unwhitelisted!' : '❌ Failed');
                if (data.success) location.reload();
            } catch (error) {
                alert('❌ Error');
            }
        }
    }
    
    async function createBackup() {
        if (!confirm('Create backup?')) return;
        
        try {
            const response = await fetch('/api/admin/backup', {
                method: 'POST'
            });
            
            const data = await response.json();
            alert(data.success ? `✅ Backup: ${data.path}` : '❌ ' + data.error);
        } catch (error) {
            alert('❌ Error');
        }
    }
    
    async function copyText(text) {
        await navigator.clipboard.writeText(text);
        alert('✅ Copied!');
    }
</script>
""")

# ==============================================================================
# 📦 TEMPLATES DICTIONARY
# ==============================================================================

TEMPLATES = {
    'landing': LANDING_PAGE,
    'login': LOGIN_PAGE,
    'dashboard': DASHBOARD_PAGE,
    'admin': ADMIN_PAGE,
}

# Export for use in website_server.py
__all__ = ['TEMPLATES']
