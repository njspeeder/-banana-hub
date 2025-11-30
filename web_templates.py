# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - WEB TEMPLATES v3.0 (GLASSMORPHISM UI)
# Modern templates with enhanced admin dashboard and user panels
# Features: Sortable tables, filters, activity feed, quick actions, glass UI
# ==============================================================================

from __future__ import annotations

# ==============================================================================
# 🎨 BASE TEMPLATE WITH GLASSMORPHISM STYLES
# ==============================================================================

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#FACC15">
    <title>Banana Hub Enterprise</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
            background-attachment: fixed;
            color: #e5e7eb;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 20% 50%, rgba(250, 204, 21, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(250, 204, 21, 0.06) 0%, transparent 50%);
            animation: float 20s ease-in-out infinite;
            pointer-events: none;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(30px, -30px) rotate(120deg); }
            66% { transform: translate(-20px, 20px) rotate(240deg); }
        }
        
        /* Glass card effect */
        .glass {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                        inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .glass::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(250, 204, 21, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .glass:hover {
            transform: translateY(-4px);
            border-color: rgba(250, 204, 21, 0.3);
            box-shadow: 0 12px 48px rgba(250, 204, 21, 0.15);
        }
        
        .glass:hover::before {
            left: 100%;
        }
        
        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 2rem;
            border-radius: 16px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            border: none;
            position: relative;
            overflow: hidden;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #FACC15, #FCD34D);
            color: #0a0f1e;
            box-shadow: 0 4px 16px rgba(250, 204, 21, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(250, 204, 21, 0.5);
        }
        
        .btn-secondary {
            background: rgba(15, 23, 42, 0.8);
            color: #e5e7eb;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }
        
        .btn-secondary:hover {
            border-color: rgba(250, 204, 21, 0.5);
            background: rgba(15, 23, 42, 0.95);
        }
        
        .btn-danger {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        .btn-danger:hover {
            background: rgba(239, 68, 68, 0.3);
            border-color: rgba(239, 68, 68, 0.5);
        }
        
        /* Input fields */
        .input {
            width: 100%;
            padding: 1rem 1.25rem;
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            color: #e5e7eb;
            font-size: 1rem;
            transition: all 0.2s;
            outline: none;
        }
        
        .input:focus {
            border-color: #FACC15;
            background: rgba(15, 23, 42, 0.8);
            box-shadow: 0 0 0 4px rgba(250, 204, 21, 0.1);
        }
        
        .input::placeholder {
            color: #64748b;
        }
        
        /* Badges */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .badge-success {
            background: rgba(34, 197, 94, 0.1);
            color: #86efac;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        
        .badge-warning {
            background: rgba(250, 204, 21, 0.1);
            color: #fde047;
            border: 1px solid rgba(250, 204, 21, 0.3);
        }
        
        .badge-error {
            background: rgba(239, 68, 68, 0.1);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        /* Table */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }
        
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        th {
            background: rgba(15, 23, 42, 0.5);
            color: #FACC15;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            user-select: none;
        }
        
        th:hover {
            background: rgba(15, 23, 42, 0.7);
        }
        
        tr:hover {
            background: rgba(250, 204, 21, 0.05);
        }
        
        /* Code block */
        .code {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.875rem;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #94a3b8;
        }
        
        /* Animation */
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .glass {
                border-radius: 16px;
            }
            
            .btn {
                padding: 0.875rem 1.5rem;
                font-size: 0.875rem;
            }
            
            table {
                display: block;
                overflow-x: auto;
            }
        }
    </style>
</head>
<body>
    {BODY_CONTENT}
</body>
</html>"""

# ==============================================================================
# 🏠 LANDING PAGE
# ==============================================================================

LANDING_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<div style="min-height: 100vh; display: flex; flex-direction: column; position: relative; z-index: 1;">
    <!-- Main Content -->
    <div style="flex: 1; display: flex; align-items: center; justify-content: center; padding: 4rem 1.5rem;">
        <div style="max-width: 1400px; width: 100%;">
            
            <!-- Hero Section -->
            <div class="glass fade-in" style="padding: 4rem; text-align: center; margin-bottom: 3rem;">
                <div style="font-size: 5rem; margin-bottom: 1.5rem;">🍌</div>
                <h1 style="font-size: 4rem; font-weight: 800; margin-bottom: 1.5rem; background: linear-gradient(135deg, #FACC15, #FCD34D, #FACC15); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    Banana Hub Enterprise
                </h1>
                <p style="font-size: 1.5rem; color: #9ca3af; margin-bottom: 2.5rem; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6;">
                    The #1 Premium Roblox Script Hub
                </p>
                <div class="badge badge-success" style="margin-bottom: 3rem; font-size: 1.1rem; padding: 0.75rem 1.5rem;">
                    <i class="fas fa-shield-check"></i>
                    <span>Undetected & Secure</span>
                </div>
                
                <div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap;">
                    <a href="/login" class="btn btn-primary" style="font-size: 1.1rem; padding: 1.25rem 3rem;">
                        <i class="fas fa-sign-in-alt"></i>
                        <span>Login to Panel</span>
                    </a>
                    <a href="https://discord.gg/bananahub" target="_blank" class="btn btn-secondary" style="font-size: 1.1rem; padding: 1.25rem 3rem;">
                        <i class="fab fa-discord"></i>
                        <span>Join Discord</span>
                    </a>
                </div>
            </div>
            
            <!-- Features Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem;">
                <div class="glass" style="padding: 2.5rem;">
                    <div style="font-size: 3.5rem; margin-bottom: 1.5rem;">⚡</div>
                    <h3 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: #FACC15;">Lightning Fast</h3>
                    <p style="color: #9ca3af; line-height: 1.8;">Optimized scripts with minimal performance impact and instant execution times.</p>
                </div>
                <div class="glass" style="padding: 2.5rem;">
                    <div style="font-size: 3.5rem; margin-bottom: 1.5rem;">🔒</div>
                    <h3 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: #FACC15;">Secure & Safe</h3>
                    <p style="color: #9ca3af; line-height: 1.8;">Advanced HWID protection and military-grade encrypted authentication.</p>
                </div>
                <div class="glass" style="padding: 2.5rem;">
                    <div style="font-size: 3.5rem; margin-bottom: 1.5rem;">🎮</div>
                    <h3 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: #FACC15;">Multi-Game Support</h3>
                    <p style="color: #9ca3af; line-height: 1.8;">Works with dozens of popular Roblox games and all major executors.</p>
                </div>
            </div>
            
        </div>
    </div>
    
    <!-- Footer -->
    <footer style="text-align: center; padding: 2rem; color: #6b7280; border-top: 1px solid rgba(148, 163, 184, 0.1);">
        <p>&copy; 2025 Banana Hub Enterprise. All rights reserved.</p>
    </footer>
</div>
""")

# ==============================================================================
# 🔐 LOGIN PAGE
# ==============================================================================

LOGIN_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem;">
    <div style="max-width: 480px; width: 100%;">
        <div class="glass fade-in" style="padding: 3rem;">
            <!-- Header -->
            <div style="text-align: center; margin-bottom: 2.5rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🍌</div>
                <h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">Welcome Back</h2>
                <p style="color: #9ca3af;">Sign in to your Banana Hub account</p>
            </div>
            
            <!-- Login Form -->
            <form id="loginForm" style="display: flex; flex-direction: column; gap: 1.5rem;" onsubmit="handleLogin(event)">
                <div>
                    <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; color: #d1d5db;">Discord ID</label>
                    <input type="text" id="user_id" name="user_id" class="input" placeholder="123456789012345678" required>
                </div>
                
                <div>
                    <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; color: #d1d5db;">License Key</label>
                    <input type="password" id="key" name="key" class="input" placeholder="BH-XXXXXXXXXXXX" required>
                </div>
                
                <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center;">
                    <i class="fas fa-sign-in-alt"></i>
                    <span>Sign In</span>
                </button>
            </form>
            
            <!-- Status Message -->
            <div id="statusMessage" style="margin-top: 1.5rem; display: none;"></div>
            
            <!-- Back Link -->
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="/" style="color: #FACC15; font-size: 0.875rem; text-decoration: none;">
                    <i class="fas fa-arrow-left" style="margin-right: 0.5rem;"></i>
                    Back to Home
                </a>
            </div>
        </div>
    </div>
</div>

<script>
    function showStatus(message, type) {
        const statusDiv = document.getElementById('statusMessage');
        const colors = {
            'success': 'badge-success',
            'error': 'badge-error',
            'info': 'badge-warning'
        };
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'info': 'fa-info-circle'
        };
        
        statusDiv.innerHTML = `<div class="badge ${colors[type]}" style="width: 100%; justify-content: center;"><i class="fas ${icons[type]}"></i><span>${message}</span></div>`;
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
                showStatus('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = result.redirect || '/dashboard';
                }, 1000);
            } else {
                showStatus(result.error || 'Login failed', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            showStatus('Connection error. Please try again.', 'error');
        }
    }
</script>
""")

# ==============================================================================
# 👤 USER DASHBOARD
# ==============================================================================

DASHBOARD_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<div style="min-height: 100vh; display: flex; flex-direction: column;">
    <!-- Navbar -->
    <nav style="background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(148, 163, 184, 0.2); position: sticky; top: 0; z-index: 50;">
        <div style="max-width: 1400px; margin: 0 auto; padding: 1rem 1.5rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 1.5rem;">🍌</span>
                <h1 style="font-size: 1.25rem; font-weight: 700;">Banana Hub</h1>
            </div>
            <a href="/logout" class="btn btn-secondary" style="padding: 0.5rem 1.5rem; font-size: 0.875rem;">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </a>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div style="flex: 1; padding: 2rem 1.5rem;">
        <div style="max-width: 1400px; margin: 0 auto;">
            
            <!-- Header -->
            <div style="margin-bottom: 2.5rem;">
                <h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">Dashboard</h2>
                <p style="color: #9ca3af;">Welcome back, {{ user.get('discord_id', 'User') }}!</p>
            </div>
            
            <!-- Info Cards Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                
                <!-- License Card -->
                <div class="glass" style="padding: 2rem;">
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-key" style="color: #FACC15;"></i>
                        <span>Your License</span>
                    </h3>
                    <div class="code" style="font-size: 0.9rem; margin-bottom: 1.25rem; filter: blur(5px); cursor: pointer;" onclick="this.style.filter='blur(0px)'">{{ user.get('key', 'No key') }}</div>
                    <button onclick="copyKey()" class="btn btn-secondary" style="width: 100%; font-size: 0.875rem; justify-content: center;">
                        <i class="fas fa-copy"></i>
                        <span>Copy Key</span>
                    </button>
                </div>
                
                <!-- HWID Card -->
                <div class="glass" style="padding: 2rem;">
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-desktop" style="color: #FACC15;"></i>
                        <span>HWID Status</span>
                    </h3>
                    <div class="badge {{ 'badge-success' if user.get('hwid') else 'badge-warning' }}" style="margin-bottom: 1.25rem;">
                        <i class="fas {{ 'fa-check' if user.get('hwid') else 'fa-times' }}"></i>
                        <span>{{ 'HWID Set' if user.get('hwid') else 'Not Set' }}</span>
                    </div>
                    <button onclick="resetHWID()" class="btn btn-primary" style="width: 100%; font-size: 0.875rem; justify-content: center;">
                        <i class="fas fa-redo"></i>
                        <span>Reset HWID</span>
                    </button>
                </div>
                
                <!-- Activity Card -->
                <div class="glass" style="padding: 2rem;">
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-chart-line" style="color: #FACC15;"></i>
                        <span>Activity</span>
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #9ca3af; font-size: 0.875rem;">Total Logins</span>
                            <span style="font-weight: 600;">{{ analytics.get('total_logins', 0) }}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #9ca3af; font-size: 0.875rem;">Last Login</span>
                            <span style="font-size: 0.875rem;">{{ user.get('last_login', 'Never')[:10] }}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #9ca3af; font-size: 0.875rem;">Joined</span>
                            <span style="font-size: 0.875rem;">{{ user.get('joined_at', 'Unknown')[:10] }}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Loader Script Card -->
            <div class="glass" style="padding: 2.5rem;">
                <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
                    <i class="fas fa-code" style="color: #FACC15;"></i>
                    <span>Loader Script</span>
                </h3>
                <p style="color: #9ca3af; margin-bottom: 1.5rem; font-size: 0.875rem;">
                    Copy this into your Roblox executor
                </p>
                <textarea id="loaderScript" class="code" style="width: 100%; height: 12rem; resize: none; outline: none;" readonly>{{ loader_script }}</textarea>
                <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                    <button onclick="copyLoader()" class="btn btn-primary" style="flex: 1; justify-content: center;">
                        <i class="fas fa-copy"></i>
                        <span>Copy Loader</span>
                    </button>
                    <button onclick="downloadLoader()" class="btn btn-secondary" style="flex: 1; justify-content: center;">
                        <i class="fas fa-download"></i>
                        <span>Download</span>
                    </button>
                </div>
            </div>
            
        </div>
    </div>
</div>

<script>
    async function copyKey() {
        const keyText = '{{ user.get("key", "") }}';
        await navigator.clipboard.writeText(keyText);
        alert('✅ Key copied to clipboard!');
    }
    
    async function copyLoader() {
        const script = document.getElementById('loaderScript').value;
        await navigator.clipboard.writeText(script);
        alert('✅ Loader copied to clipboard!');
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
        if (!confirm('Reset your HWID? This can only be done once every 5 minutes.')) return;
        
        try {
            const response = await fetch('/api/user/reset-hwid', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert('✅ HWID reset successfully!');
                location.reload();
            } else {
                alert('❌ ' + (result.error || 'Failed to reset HWID'));
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
<div style="min-height: 100vh; display: flex; flex-direction: column;">
    <!-- Navbar -->
    <nav style="background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(148, 163, 184, 0.2); position: sticky; top: 0; z-index: 50;">
        <div style="max-width: 1600px; margin: 0 auto; padding: 1rem 1.5rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 1.5rem;">🍌</span>
                <h1 style="font-size: 1.25rem; font-weight: 700;">Admin Panel</h1>
            </div>
            <div style="display: flex; gap: 1rem;">
                <a href="/dashboard" class="btn btn-secondary" style="padding: 0.5rem 1.5rem; font-size: 0.875rem;">
                    <i class="fas fa-user"></i>
                    <span>Dashboard</span>
                </a>
                <a href="/logout" class="btn btn-secondary" style="padding: 0.5rem 1.5rem; font-size: 0.875rem;">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div style="flex: 1; padding: 2rem 1.5rem;">
        <div style="max-width: 1600px; margin: 0 auto;">
            
            <!-- Header -->
            <div style="margin-bottom: 2.5rem;">
                <h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">Admin Dashboard</h2>
                <p style="color: #9ca3af;">Manage users, keys, and system settings</p>
            </div>
            
            <!-- Stats Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 2.5rem;">
                <div class="glass" style="padding: 2rem; text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #FACC15;">{{ stats.get('total_users', 0) }}</div>
                    <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Total Users</div>
                </div>
                <div class="glass" style="padding: 2rem; text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #FACC15;">{{ stats.get('total_keys', 0) }}</div>
                    <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Total Keys</div>
                </div>
                <div class="glass" style="padding: 2rem; text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #86efac;">{{ stats.get('available_keys', 0) }}</div>
                    <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Available</div>
                </div>
                <div class="glass" style="padding: 2rem; text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #93c5fd;">{{ stats.get('total_logins', 0) }}</div>
                    <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Total Logins</div>
                </div>
                <div class="glass" style="padding: 2rem; text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #fca5a5;">{{ stats.get('total_blacklisted', 0) }}</div>
                    <div style="color: #9ca3af; font-size: 0.875rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Banned</div>
                </div>
            </div>
            
            <!-- Action Buttons -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2.5rem;">
                <button onclick="generateKeys()" class="glass" style="padding: 2rem; text-align: left; border: none; cursor: pointer; color: inherit;">
                    <i class="fas fa-key" style="font-size: 2rem; color: #FACC15; margin-bottom: 1rem;"></i>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.5rem;">Generate Keys</h3>
                    <p style="color: #9ca3af; font-size: 0.875rem;">Create new license keys</p>
                </button>
                
                <button onclick="whitelistUser()" class="glass" style="padding: 2rem; text-align: left; border: none; cursor: pointer; color: inherit;">
                    <i class="fas fa-user-plus" style="font-size: 2rem; color: #86efac; margin-bottom: 1rem;"></i>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.5rem;">Whitelist User</h3>
                    <p style="color: #9ca3af; font-size: 0.875rem;">Add user with auto key</p>
                </button>
                
                <button onclick="createBackup()" class="glass" style="padding: 2rem; text-align: left; border: none; cursor: pointer; color: inherit;">
                    <i class="fas fa-database" style="font-size: 2rem; color: #93c5fd; margin-bottom: 1rem;"></i>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.5rem;">Backup Database</h3>
                    <p style="color: #9ca3af; font-size: 0.875rem;">Create data backup</p>
                </button>
            </div>
            
            <!-- Users Table -->
            <div class="glass" style="padding: 2rem; margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="font-size: 1.25rem; font-weight: 600;">All Users</h3>
                    <input type="text" id="userSearch" onkeyup="searchUsers()" placeholder="Search users..." class="input" style="width: 300px; padding: 0.5rem 1rem;">
                </div>
                <div style="overflow-x: auto;">
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
                            {% for user in users %}
                            <tr>
                                <td><code style="background: rgba(139, 92, 246, 0.1); padding: 0.25rem 0.5rem; border-radius: 6px; color: #a78bfa;">{{ user.get('discord_id', '') }}</code></td>
                                <td><code style="background: rgba(139, 92, 246, 0.1); padding: 0.25rem 0.5rem; border-radius: 6px; color: #a78bfa; font-size: 0.75rem;">{{ user.get('key', 'None') }}</code></td>
                                <td><code style="font-size: 0.75rem;">{{ (user.get('hwid', 'Not set')[:16] + '...') if user.get('hwid') and len(user.get('hwid', '')) > 16 else user.get('hwid', 'Not set') }}</code></td>
                                <td style="font-size: 0.875rem;">{{ user.get('joined_at', 'Unknown')[:10] }}</td>
                                <td>
                                    {% if user.get('discord_id') in [b.get('discord_id') for b in blacklisted] %}
                                    <span class="badge badge-error">Banned</span>
                                    {% else %}
                                    <span class="badge badge-success">Active</span>
                                    {% endif %}
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
            <div class="glass" style="padding: 2rem;">
                <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1.5rem;">Available Keys ({{ unused_keys|length }})</h3>
                <div style="overflow-x: auto;">
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
                            {% for key in unused_keys[:10] %}
                            <tr>
                                <td><code style="background: rgba(139, 92, 246, 0.1); padding: 0.25rem 0.5rem; border-radius: 6px; color: #a78bfa;">{{ key.get('key', '') }}</code></td>
                                <td style="font-size: 0.875rem;">{{ key.get('created_at', 'Unknown')[:10] }}</td>
                                <td><span class="badge badge-success">Available</span></td>
                                <td>
                                    <button onclick="copyText('{{ key.get('key', '') }}')" class="btn btn-secondary" style="padding: 0.375rem 0.75rem; font-size: 0.75rem;">
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
    </div>
</div>

<script>
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
        const count = prompt('How many keys to generate? (1-25):', '1');
        if (!count) return;
        
        const num = parseInt(count);
        if (isNaN(num) || num < 1 || num > 25) {
            alert('❌ Invalid count (1-25)');
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
                alert('❌ Failed to generate keys');
            }
        } catch (error) {
            alert('❌ Error generating keys');
        }
    }
    
    async function whitelistUser() {
        const discordId = prompt('Enter Discord User ID:');
        if (!discordId) return;
        
        try {
            const response = await fetch('/api/admin/whitelist', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({discord_id: discordId})
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert(`✅ Whitelisted ${discordId}\\nKey: ${data.key}`);
                location.reload();
            } else {
                alert('❌ ' + data.error);
            }
        } catch (error) {
            alert('❌ Failed to whitelist user');
        }
    }
    
    async function manageUser(discordId) {
        const action = prompt(`Manage user ${discordId}\\n\\nEnter:\\n1 - Reset HWID\\n2 - Ban User\\n3 - Unban User\\n4 - Unwhitelist\\n\\nChoice:`);
        
        if (action === '1') {
            if (!confirm(`Reset HWID for ${discordId}?`)) return;
            
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
                alert('❌ Error resetting HWID');
            }
        } else if (action === '2' || action === '3') {
            const reason = action === '2' ? (prompt('Ban reason:') || 'No reason') : 'Unbanned via web';
            
            try {
                const response = await fetch('/api/admin/blacklist', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({discord_id: discordId, reason: reason})
                });
                
                const data = await response.json();
                alert(data.success ? `✅ User ${data.action}ed!` : '❌ Failed');
                if (data.success) location.reload();
            } catch (error) {
                alert('❌ Error updating ban status');
            }
        } else if (action === '4') {
            if (!confirm(`Remove ${discordId} from whitelist?`)) return;
            
            try {
                const response = await fetch('/api/admin/unwhitelist', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({discord_id: discordId})
                });
                
                const data = await response.json();
                alert(data.success ? '✅ User unwhitelisted!' : '❌ Failed');
                if (data.success) location.reload();
            } catch (error) {
                alert('❌ Error unwhitelisting');
            }
        }
    }
    
    async function createBackup() {
        if (!confirm('Create database backup?')) return;
        
        try {
            const response = await fetch('/api/admin/backup', {
                method: 'POST'
            });
            
            const data = await response.json();
            alert(data.success ? `✅ Backup created: ${data.path}` : '❌ ' + data.error);
        } catch (error) {
            alert('❌ Failed to create backup');
        }
    }
    
    async function copyText(text) {
        await navigator.clipboard.writeText(text);
        alert('✅ Copied to clipboard!');
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
__all__ = ['TEMPLATES', 'LANDING_PAGE', 'LOGIN_PAGE', 'DASHBOARD_PAGE', 'ADMIN_PAGE']
