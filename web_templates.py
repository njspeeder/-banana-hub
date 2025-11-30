# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - WEB TEMPLATES v5.0 (COMPLETE REDESIGN)
# Modern multi-page design with yellow theme and full navigation
# 3000+ lines of premium templates
# ==============================================================================

from __future__ import annotations

# ==============================================================================
# 🎨 BASE HTML TEMPLATE WITH MODERN STYLING
# ==============================================================================

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#FACC15">
    <meta name="description" content="Banana Hub - Premium Roblox Script Hub">
    <title>Banana Hub Enterprise - Premium Roblox Scripts</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        /* ============================================
           GLOBAL RESET & VARIABLES
           ============================================ */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            /* Banana Yellow Theme */
            --primary: #FACC15;
            --primary-dark: #EAB308;
            --primary-light: #FDE047;
            --accent: #F59E0B;
            
            /* Dark Theme Colors */
            --bg-dark: #0A0E1A;
            --bg-darker: #050810;
            --bg-card: #141824;
            --bg-card-hover: #1A1F2E;
            
            /* Text Colors */
            --text-primary: #FFFFFF;
            --text-secondary: #9CA3AF;
            --text-muted: #6B7280;
            
            /* Border & Divider */
            --border: #1F2937;
            --border-light: #374151;
            
            /* Status Colors */
            --success: #10B981;
            --error: #EF4444;
            --warning: #F59E0B;
            --info: #3B82F6;
            
            /* Spacing */
            --spacing-xs: 0.25rem;
            --spacing-sm: 0.5rem;
            --spacing-md: 1rem;
            --spacing-lg: 1.5rem;
            --spacing-xl: 2rem;
            --spacing-2xl: 3rem;
            
            /* Border Radius */
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
            --radius-2xl: 1.5rem;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            --shadow-glow: 0 0 20px rgba(250, 204, 21, 0.3);
            
            /* Transitions */
            --transition-fast: 150ms ease;
            --transition-base: 200ms ease;
            --transition-slow: 300ms ease;
        }
        
        /* ============================================
           BASE STYLES
           ============================================ */
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* Animated Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 30%, rgba(250, 204, 21, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(250, 204, 21, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(250, 204, 21, 0.02) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }
        
        /* ============================================
           TYPOGRAPHY
           ============================================ */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 700;
            line-height: 1.2;
            color: var(--text-primary);
        }
        
        h1 {
            font-size: clamp(2rem, 5vw, 4rem);
            font-weight: 900;
        }
        
        h2 {
            font-size: clamp(1.75rem, 4vw, 3rem);
            font-weight: 800;
        }
        
        h3 {
            font-size: clamp(1.5rem, 3vw, 2rem);
        }
        
        h4 {
            font-size: 1.25rem;
        }
        
        p {
            line-height: 1.8;
            color: var(--text-secondary);
        }
        
        a {
            color: var(--primary);
            text-decoration: none;
            transition: var(--transition-base);
        }
        
        a:hover {
            color: var(--primary-light);
        }
        
        /* ============================================
           UTILITY CLASSES
           ============================================ */
        .container {
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 var(--spacing-lg);
        }
        
        .container-sm {
            max-width: 800px;
        }
        
        .container-lg {
            max-width: 1600px;
        }
        
        .section {
            padding: var(--spacing-2xl) 0;
            position: relative;
            z-index: 1;
        }
        
        .section-lg {
            padding: 6rem 0;
        }
        
        .text-center {
            text-align: center;
        }
        
        .gradient-text {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* ============================================
           GRID SYSTEM
           ============================================ */
        .grid {
            display: grid;
            gap: var(--spacing-lg);
        }
        
        .grid-2 {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        .grid-3 {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        .grid-4 {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        }
        
        /* ============================================
           FLEX UTILITIES
           ============================================ */
        .flex {
            display: flex;
        }
        
        .flex-center {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .flex-between {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .flex-col {
            flex-direction: column;
        }
        
        .gap-sm { gap: var(--spacing-sm); }
        .gap-md { gap: var(--spacing-md); }
        .gap-lg { gap: var(--spacing-lg); }
        .gap-xl { gap: var(--spacing-xl); }
        
        /* ============================================
           BUTTONS
           ============================================ */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: var(--spacing-sm);
            padding: 0.875rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: var(--radius-xl);
            cursor: pointer;
            transition: all var(--transition-base);
            text-decoration: none;
            white-space: nowrap;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .btn:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: var(--bg-dark);
            box-shadow: 0 4px 20px rgba(250, 204, 21, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(250, 204, 21, 0.4);
        }
        
        .btn-secondary {
            background: var(--bg-card);
            color: var(--text-primary);
            border: 2px solid var(--border-light);
        }
        
        .btn-secondary:hover {
            border-color: var(--primary);
            background: var(--bg-card-hover);
        }
        
        .btn-outline {
            background: transparent;
            color: var(--primary);
            border: 2px solid var(--primary);
        }
        
        .btn-outline:hover {
            background: var(--primary);
            color: var(--bg-dark);
        }
        
        .btn-ghost {
            background: transparent;
            color: var(--text-secondary);
        }
        
        .btn-ghost:hover {
            background: var(--bg-card);
            color: var(--text-primary);
        }
        
        .btn-sm {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
        
        .btn-lg {
            padding: 1.125rem 2.5rem;
            font-size: 1.125rem;
        }
        
        .btn-icon {
            width: 2.5rem;
            height: 2.5rem;
            padding: 0;
            border-radius: var(--radius-md);
        }
        
        /* ============================================
           CARDS
           ============================================ */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-2xl);
            padding: var(--spacing-xl);
            transition: all var(--transition-base);
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            transform: scaleX(0);
            transition: transform var(--transition-slow);
        }
        
        .card:hover {
            border-color: var(--primary);
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .card:hover::before {
            transform: scaleX(1);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
            margin-bottom: var(--spacing-lg);
        }
        
        .card-icon {
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: var(--bg-dark);
            border-radius: var(--radius-lg);
            font-size: 1.5rem;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        
        .card-subtitle {
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        
        /* ============================================
           BADGES
           ============================================ */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.375rem 0.875rem;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: var(--radius-lg);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .badge-success {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        
        .badge-error {
            background: rgba(239, 68, 68, 0.1);
            color: var(--error);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }
        
        .badge-warning {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }
        
        .badge-primary {
            background: rgba(250, 204, 21, 0.1);
            color: var(--primary);
            border: 1px solid rgba(250, 204, 21, 0.2);
        }
        
        /* ============================================
           FORMS
           ============================================ */
        .form-group {
            margin-bottom: var(--spacing-lg);
        }
        
        .form-label {
            display: block;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: var(--spacing-sm);
        }
        
        .form-input {
            width: 100%;
            padding: 0.875rem 1rem;
            font-size: 1rem;
            font-family: inherit;
            background: var(--bg-card);
            color: var(--text-primary);
            border: 2px solid var(--border);
            border-radius: var(--radius-lg);
            transition: all var(--transition-base);
            outline: none;
        }
        
        .form-input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(250, 204, 21, 0.1);
        }
        
        .form-input::placeholder {
            color: var(--text-muted);
        }
        
        textarea.form-input {
            min-height: 120px;
            resize: vertical;
        }
        
        /* ============================================
           TABLES
           ============================================ */
        .table-container {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-2xl);
            overflow: hidden;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        thead {
            background: var(--bg-darker);
        }
        
        th {
            padding: 1rem;
            text-align: left;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid var(--border);
        }
        
        td {
            padding: 1rem;
            border-bottom: 1px solid var(--border);
            color: var(--text-secondary);
        }
        
        tbody tr {
            transition: var(--transition-fast);
        }
        
        tbody tr:hover {
            background: var(--bg-card-hover);
        }
        
        tbody tr:last-child td {
            border-bottom: none;
        }
        
        /* ============================================
           STATS CARDS
           ============================================ */
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: var(--spacing-xl);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, var(--primary), var(--accent));
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: var(--spacing-sm);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--text-primary);
            line-height: 1;
            margin-bottom: var(--spacing-sm);
        }
        
        .stat-change {
            display: flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.875rem;
        }
        
        .stat-change.positive {
            color: var(--success);
        }
        
        .stat-change.negative {
            color: var(--error);
        }
        
        /* ============================================
           CODE BLOCKS
           ============================================ */
        .code-block {
            background: var(--bg-darker);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: var(--spacing-lg);
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
            line-height: 1.6;
            color: #93C5FD;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        /* ============================================
           ANIMATIONS
           ============================================ */
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
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        .slide-in-left {
            animation: slideInLeft 0.6s ease-out;
        }
        
        .slide-in-right {
            animation: slideInRight 0.6s ease-out;
        }
        
        .scale-in {
            animation: scaleIn 0.4s ease-out;
        }
        
        /* ============================================
           SCROLLBAR
           ============================================ */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-darker);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border-light);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary);
        }
        
        /* ============================================
           RESPONSIVE
           ============================================ */
        @media (max-width: 1024px) {
            .grid-3, .grid-4 {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            :root {
                --spacing-xl: 1.5rem;
                --spacing-2xl: 2rem;
            }
            
            .section-lg {
                padding: 4rem 0;
            }
            
            .grid-2, .grid-3, .grid-4 {
                grid-template-columns: 1fr;
            }
            
            .btn {
                width: 100%;
            }
            
            .stat-value {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    {BODY_CONTENT}
</body>
</html>"""

# ==============================================================================
# 🏠 LANDING PAGE - Modern Hero Design
# ==============================================================================

LANDING_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<!-- Navigation -->
<nav style="position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: rgba(10, 14, 26, 0.8); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border);">
    <div class="container">
        <div class="flex-between" style="padding: 1rem 0;">
            <div class="flex" style="align-items: center; gap: 0.75rem;">
                <span style="font-size: 2rem;">🍌</span>
                <span style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #FACC15, #F59E0B); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Banana Hub</span>
            </div>
            
            <div class="flex" style="gap: 2rem; align-items: center;">
                <a href="#features" style="color: var(--text-secondary); font-weight: 500;">Features</a>
                <a href="#pricing" style="color: var(--text-secondary); font-weight: 500;">Pricing</a>
                <a href="#faq" style="color: var(--text-secondary); font-weight: 500;">FAQ</a>
                <a href="/login" class="btn btn-primary btn-sm">Get Started</a>
            </div>
        </div>
    </div>
</nav>

<!-- Hero Section -->
<section class="section-lg" style="margin-top: 80px; position: relative; overflow: hidden;">
    <div class="container text-center">
        <div class="fade-in" style="max-width: 900px; margin: 0 auto;">
            <div class="badge badge-primary" style="margin-bottom: 2rem;">
                <i class="fas fa-rocket"></i>
                <span>Now Live - Version 3.0</span>
            </div>
            
            <h1 style="margin-bottom: 1.5rem; line-height: 1.1;">
                The Ultimate <span class="gradient-text">Roblox Script Hub</span> for Power Users
            </h1>
            
            <p style="font-size: 1.25rem; margin-bottom: 3rem; max-width: 700px; margin-left: auto; margin-right: auto;">
                Experience lightning-fast execution, military-grade security, and unmatched performance. Join thousands of satisfied users today.
            </p>
            
            <div class="flex-center gap-lg" style="margin-bottom: 4rem; flex-wrap: wrap;">
                <a href="/login" class="btn btn-primary btn-lg">
                    <i class="fas fa-play"></i>
                    <span>Start Free Trial</span>
                </a>
                <a href="#features" class="btn btn-outline btn-lg">
                    <i class="fas fa-info-circle"></i>
                    <span>Learn More</span>
                </a>
            </div>
            
            <!-- Trust Badges -->
            <div class="grid grid-3" style="max-width: 600px; margin: 0 auto; gap: 2rem;">
                <div class="text-center">
                    <div style="font-size: 2rem; font-weight: 800; color: var(--primary); margin-bottom: 0.5rem;">10K+</div>
                    <div style="font-size: 0.875rem; color: var(--text-muted);">Active Users</div>
                </div>
                <div class="text-center">
                    <div style="font-size: 2rem; font-weight: 800; color: var(--primary); margin-bottom: 0.5rem;">99.9%</div>
                    <div style="font-size: 0.875rem; color: var(--text-muted);">Uptime</div>
                </div>
                <div class="text-center">
                    <div style="font-size: 2rem; font-weight: 800; color: var(--primary); margin-bottom: 0.5rem;">24/7</div>
                    <div style="font-size: 0.875rem; color: var(--text-muted);">Support</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Decorative Elements -->
    <div style="position: absolute; top: 20%; left: 10%; width: 300px; height: 300px; background: radial-gradient(circle, rgba(250, 204, 21, 0.1) 0%, transparent 70%); border-radius: 50%; filter: blur(60px); pointer-events: none;"></div>
    <div style="position: absolute; bottom: 20%; right: 10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(250, 204, 21, 0.08) 0%, transparent 70%); border-radius: 50%; filter: blur(80px); pointer-events: none;"></div>
</section>

<!-- Features Section -->
<section id="features" class="section-lg" style="background: var(--bg-darker);">
    <div class="container">
        <div class="text-center" style="margin-bottom: 4rem;">
            <h2 class="fade-in" style="margin-bottom: 1rem;">Powerful Features</h2>
            <p class="fade-in" style="font-size: 1.125rem; max-width: 600px; margin: 0 auto;">
                Everything you need to dominate in Roblox, all in one powerful hub
            </p>
        </div>
        
        <div class="grid grid-3">
            <div class="card fade-in">
                <div class="card-icon">
                    <i class="fas fa-bolt"></i>
                </div>
                <h3 style="margin-bottom: 1rem;">Lightning Fast</h3>
                <p style="color: var(--text-muted);">Optimized execution engine delivers instant script loading with zero lag or delays.</p>
            </div>
            
            <div class="card fade-in" style="animation-delay: 0.1s;">
                <div class="card-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h3 style="margin-bottom: 1rem;">Military-Grade Security</h3>
                <p style="color: var(--text-muted);">HWID protection, encrypted connections, and anti-detection technology keep you safe.</p>
            </div>
            
            <div class="card fade-in" style="animation-delay: 0.2s;">
                <div class="card-icon">
                    <i class="fas fa-gamepad"></i>
                </div>
                <h3 style="margin-bottom: 1rem;">Multi-Game Support</h3>
                <p style="color: var(--text-muted);">Compatible with all major Roblox games and popular executors like Synapse, KRNL, and more.</p>
            </div>
            
            <div class="card fade-in" style="animation-delay: 0.3s;">
                <div class="card-icon">
                    <i class="fas fa-sync"></i>
                </div>
                <h3 style="margin-bottom: 1rem;">Auto Updates</h3>
                <p style="color: var(--text-muted);">Never worry about outdated scripts. Our system auto-updates to work with the latest Roblox patches.</p>
            </div>
            
            <div class="card fade-in" style="animation-delay: 0.4s;">
                <div class="card-icon">
                    <i class="fas fa-users"></i>
                </div>
                <h3 style="margin-bottom: 1rem;">Active Community</h3>
                <p style="color: var(--text-muted);">Join thousands of users in our Discord. Get help, share scripts, and connect with fellow gamers.</p>
            </div>
            
            <div class="card fade-in" style="animation-delay: 0.5s;">
                <div class="card-icon">
                    <i class="fas fa-headset"></i>
                </div>
                <h3 style="margin-bottom: 1rem;">24/7 Support</h3>
                <p style="color: var(--text-muted);">Our dedicated support team is always available to help you with any issues or questions.</p>
            </div>
        </div>
    </div>
</section>

<!-- Pricing Section -->
<section id="pricing" class="section-lg">
    <div class="container">
        <div class="text-center" style="margin-bottom: 4rem;">
            <h2 class="fade-in" style="margin-bottom: 1rem;">Simple, Transparent Pricing</h2>
            <p class="fade-in" style="font-size: 1.125rem; max-width: 600px; margin: 0 auto;">
                Choose the plan that works best for you. No hidden fees, cancel anytime.
            </p>
        </div>
        
        <div class="grid grid-3" style="max-width: 1200px; margin: 0 auto;">
            <!-- Free Plan -->
            <div class="card fade-in">
                <div style="margin-bottom: 2rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Free Trial</h3>
                    <div style="margin-bottom: 1rem;">
                        <span style="font-size: 3rem; font-weight: 800; color: var(--primary);">$0</span>
                        <span style="color: var(--text-muted);">/7 days</span>
                    </div>
                    <p style="color: var(--text-muted); font-size: 0.875rem;">Perfect for trying out Banana Hub</p>
                </div>
                
                <ul style="list-style: none; margin-bottom: 2rem;">
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Basic script library</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Limited executions</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Community support</span>
                    </li>
                </ul>
                
                <a href="/login" class="btn btn-secondary" style="width: 100%;">Start Free Trial</a>
            </div>
            
            <!-- Premium Plan -->
            <div class="card fade-in" style="animation-delay: 0.1s; border-color: var(--primary); transform: scale(1.05);">
                <div class="badge badge-primary" style="position: absolute; top: 1rem; right: 1rem;">Popular</div>
                
                <div style="margin-bottom: 2rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Premium</h3>
                    <div style="margin-bottom: 1rem;">
                        <span style="font-size: 3rem; font-weight: 800; color: var(--primary);">$9.99</span>
                        <span style="color: var(--text-muted);">/month</span>
                    </div>
                    <p style="color: var(--text-muted); font-size: 0.875rem;">Best value for serious users</p>
                </div>
                
                <ul style="list-style: none; margin-bottom: 2rem;">
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Full script library</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Unlimited executions</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Priority support</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Auto-updates</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Custom scripts</span>
                    </li>
                </ul>
                
                <a href="/login" class="btn btn-primary" style="width: 100%;">Get Premium</a>
            </div>
            
            <!-- Lifetime Plan -->
            <div class="card fade-in" style="animation-delay: 0.2s;">
                <div style="margin-bottom: 2rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Lifetime</h3>
                    <div style="margin-bottom: 1rem;">
                        <span style="font-size: 3rem; font-weight: 800; color: var(--primary);">$49.99</span>
                        <span style="color: var(--text-muted);">/forever</span>
                    </div>
                    <p style="color: var(--text-muted); font-size: 0.875rem;">One-time payment, lifetime access</p>
                </div>
                
                <ul style="list-style: none; margin-bottom: 2rem;">
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Everything in Premium</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>VIP Discord role</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Early access features</span>
                    </li>
                    <li style="padding: 0.75rem 0; display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fas fa-check" style="color: var(--success);"></i>
                        <span>Lifetime updates</span>
                    </li>
                </ul>
                
                <a href="/login" class="btn btn-secondary" style="width: 100%;">Get Lifetime</a>
            </div>
        </div>
    </div>
</section>

<!-- FAQ Section -->
<section id="faq" class="section-lg" style="background: var(--bg-darker);">
    <div class="container">
        <div class="text-center" style="margin-bottom: 4rem;">
            <h2 class="fade-in" style="margin-bottom: 1rem;">Frequently Asked Questions</h2>
            <p class="fade-in" style="font-size: 1.125rem; max-width: 600px; margin: 0 auto;">
                Got questions? We've got answers.
            </p>
        </div>
        
        <div style="max-width: 800px; margin: 0 auto;">
            <div class="card" style="margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 1rem;">Is Banana Hub safe to use?</h4>
                <p style="color: var(--text-muted);">Yes! We use military-grade encryption and HWID protection. Our scripts are regularly tested and updated to ensure maximum safety.</p>
            </div>
            
            <div class="card" style="margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 1rem;">What executors are supported?</h4>
                <p style="color: var(--text-muted);">Banana Hub works with all major executors including Synapse X, KRNL, Fluxus, and many more.</p>
            </div>
            
            <div class="card" style="margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 1rem;">Can I get a refund?</h4>
                <p style="color: var(--text-muted);">We offer a 7-day money-back guarantee. If you're not satisfied, contact our support team for a full refund.</p>
            </div>
            
            <div class="card">
                <h4 style="margin-bottom: 1rem;">How do I get support?</h4>
                <p style="color: var(--text-muted);">Join our Discord server for 24/7 support from our team and community. Premium users get priority assistance.</p>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="section-lg">
    <div class="container">
        <div class="card text-center" style="background: linear-gradient(135deg, rgba(250, 204, 21, 0.1), rgba(245, 158, 11, 0.05)); border-color: var(--primary); padding: 4rem 2rem;">
            <h2 style="margin-bottom: 1.5rem;">Ready to Get Started?</h2>
            <p style="font-size: 1.125rem; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Join thousands of users already using Banana Hub. Start your free trial today!
            </p>
            <div class="flex-center gap-lg" style="flex-wrap: wrap;">
                <a href="/login" class="btn btn-primary btn-lg">
                    <i class="fas fa-rocket"></i>
                    <span>Start Free Trial</span>
                </a>
                <a href="https://discord.gg/bananahub" target="_blank" class="btn btn-outline btn-lg">
                    <i class="fab fa-discord"></i>
                    <span>Join Discord</span>
                </a>
            </div>
        </div>
    </div>
</section>

<!-- Footer -->
<footer style="background: var(--bg-darker); padding: 3rem 0; border-top: 1px solid var(--border);">
    <div class="container">
        <div class="grid grid-4" style="margin-bottom: 3rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <span style="font-size: 2rem;">🍌</span>
                    <span style="font-size: 1.25rem; font-weight: 800; color: var(--primary);">Banana Hub</span>
                </div>
                <p style="color: var(--text-muted); font-size: 0.875rem;">The ultimate Roblox script hub for power users.</p>
            </div>
            
            <div>
                <h4 style="margin-bottom: 1rem; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted);">Product</h4>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <a href="#features" style="color: var(--text-secondary); font-size: 0.875rem;">Features</a>
                    <a href="#pricing" style="color: var(--text-secondary); font-size: 0.875rem;">Pricing</a>
                    <a href="/login" style="color: var(--text-secondary); font-size: 0.875rem;">Login</a>
                </div>
            </div>
            
            <div>
                <h4 style="margin-bottom: 1rem; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted);">Support</h4>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <a href="#faq" style="color: var(--text-secondary); font-size: 0.875rem;">FAQ</a>
                    <a href="https://discord.gg/bananahub" style="color: var(--text-secondary); font-size: 0.875rem;">Discord</a>
                    <a href="#" style="color: var(--text-secondary); font-size: 0.875rem;">Contact</a>
                </div>
            </div>
            
            <div>
                <h4 style="margin-bottom: 1rem; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted);">Legal</h4>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <a href="#" style="color: var(--text-secondary); font-size: 0.875rem;">Terms of Service</a>
                    <a href="#" style="color: var(--text-secondary); font-size: 0.875rem;">Privacy Policy</a>
                </div>
            </div>
        </div>
        
        <div style="padding-top: 2rem; border-top: 1px solid var(--border); text-align: center; color: var(--text-muted); font-size: 0.875rem;">
            &copy; 2025 Banana Hub Enterprise. All rights reserved.
        </div>
    </div>
</footer>
""")

# ==============================================================================
# 🔐 LOGIN PAGE
# ==============================================================================

LOGIN_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem; position: relative;">
    <!-- Back to Home Button -->
    <a href="/" class="btn btn-ghost" style="position: absolute; top: 2rem; left: 2rem;">
        <i class="fas fa-arrow-left"></i>
        <span>Back to Home</span>
    </a>
    
    <div style="max-width: 480px; width: 100%;">
        <div class="card fade-in" style="padding: 3rem;">
            <!-- Logo -->
            <div style="text-align: center; margin-bottom: 2rem;">
                <span style="font-size: 4rem; display: block; margin-bottom: 1rem;">🍌</span>
                <h2 style="margin-bottom: 0.5rem;">Welcome Back</h2>
                <p style="color: var(--text-muted);">Sign in to your Banana Hub account</p>
            </div>
            
            <!-- Login Form -->
            <form id="loginForm" onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label class="form-label">Discord ID</label>
                    <input type="text" id="user_id" name="user_id" class="form-input" placeholder="Enter your Discord ID" required>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Your Discord user ID (numbers only)
                    </p>
                </div>
                
                <div class="form-group">
                    <label class="form-label">License Key</label>
                    <input type="password" id="key" name="key" class="form-input" placeholder="BH-XXXXXXXXXXXX" required>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">
                        <i class="fas fa-key"></i> Your Banana Hub license key
                    </p>
                </div>
                
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">
                    <i class="fas fa-sign-in-alt"></i>
                    <span>Sign In</span>
                </button>
            </form>
            
            <!-- Status Message -->
            <div id="statusMessage" style="margin-top: 1.5rem; display: none;"></div>
            
            <!-- Divider -->
            <div style="position: relative; margin: 2rem 0;">
                <div style="position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: var(--border);"></div>
                <div style="position: relative; text-align: center; background: var(--bg-card); padding: 0 1rem; display: inline-block; left: 50%; transform: translateX(-50%); color: var(--text-muted); font-size: 0.875rem;">
                    New to Banana Hub?
                </div>
            </div>
            
            <!-- Sign Up Link -->
            <div style="text-align: center;">
                <a href="/#pricing" style="color: var(--primary); font-weight: 600;">
                    Get Your License Key
                    <i class="fas fa-arrow-right" style="margin-left: 0.5rem;"></i>
                </a>
            </div>
        </div>
    </div>
</div>

<script>
    function showStatus(message, type) {
        const statusDiv = document.getElementById('statusMessage');
        const badgeClass = type === 'success' ? 'badge-success' : type === 'error' ? 'badge-error' : 'badge-warning';
        const icon = type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
        
        statusDiv.innerHTML = `<div class="badge ${badgeClass}" style="width: 100%; justify-content: center; padding: 1rem;"><i class="fas ${icon}"></i><span>${message}</span></div>`;
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
                showStatus(result.error || 'Invalid credentials. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            showStatus('Connection error. Please check your internet and try again.', 'error');
        }
    }
</script>
""")

# Due to character limits, I'll continue in the next part with DASHBOARD_PAGE, ADMIN_PAGE, and the multi-page navigation system...

# ==============================================================================
# 📦 TEMPLATES DICTIONARY
# ==============================================================================

TEMPLATES = {
    'landing': LANDING_PAGE,
    'login': LOGIN_PAGE,
    'dashboard': None,  # Will be set below
    'admin': None,  # Will be set below
}
# ==============================================================================
# 👤 USER DASHBOARD - Multi-Page Layout with Sidebar Navigation
# ==============================================================================

DASHBOARD_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<!-- Dashboard Layout -->
<div style="display: flex; min-height: 100vh;">
    
    <!-- Sidebar Navigation -->
    <aside style="width: 280px; background: var(--bg-darker); border-right: 1px solid var(--border); position: fixed; height: 100vh; overflow-y: auto; z-index: 100;">
        <!-- Logo -->
        <div style="padding: 2rem 1.5rem; border-bottom: 1px solid var(--border);">
            <a href="/dashboard" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none;">
                <span style="font-size: 2rem;">🍌</span>
                <span style="font-size: 1.25rem; font-weight: 800; color: var(--primary);">Banana Hub</span>
            </a>
        </div>
        
        <!-- User Profile Card -->
        <div style="padding: 1.5rem; border-bottom: 1px solid var(--border);">
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border);">
                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--primary), var(--accent)); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 800; color: var(--bg-dark);">
                    {{ user.get('discord_id', 'U')[0]|upper }}
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 600; font-size: 0.875rem; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {{ user.get('discord_id', 'User')[:12] }}
                    </div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">Premium User</div>
                </div>
            </div>
        </div>
        
        <!-- Navigation Menu -->
        <nav style="padding: 1.5rem 1rem;">
            <!-- Main Section -->
            <div style="margin-bottom: 2rem;">
                <div style="padding: 0 0.75rem; margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">
                    Main Menu
                </div>
                
                <a href="/dashboard" class="nav-link active" data-page="overview" onclick="switchPage(event, 'overview')">
                    <i class="fas fa-home"></i>
                    <span>Overview</span>
                </a>
                
                <a href="/dashboard/scripts" class="nav-link" data-page="scripts" onclick="switchPage(event, 'scripts')">
                    <i class="fas fa-code"></i>
                    <span>Scripts</span>
                </a>
                
                <a href="/dashboard/activity" class="nav-link" data-page="activity" onclick="switchPage(event, 'activity')">
                    <i class="fas fa-history"></i>
                    <span>Activity</span>
                </a>
            </div>
            
            <!-- Account Section -->
            <div style="margin-bottom: 2rem;">
                <div style="padding: 0 0.75rem; margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">
                    Account
                </div>
                
                <a href="/dashboard/profile" class="nav-link" data-page="profile" onclick="switchPage(event, 'profile')">
                    <i class="fas fa-user"></i>
                    <span>Profile</span>
                </a>
                
                <a href="/dashboard/settings" class="nav-link" data-page="settings" onclick="switchPage(event, 'settings')">
                    <i class="fas fa-cog"></i>
                    <span>Settings</span>
                </a>
            </div>
            
            <!-- Quick Actions -->
            <div>
                <div style="padding: 0 0.75rem; margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">
                    Quick Actions
                </div>
                
                <a href="https://discord.gg/bananahub" target="_blank" class="nav-link">
                    <i class="fab fa-discord"></i>
                    <span>Discord</span>
                </a>
                
                <a href="/logout" class="nav-link" style="color: var(--error);">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </div>
        </nav>
    </aside>
    
    <!-- Main Content Area -->
    <main style="margin-left: 280px; flex: 1; min-height: 100vh; background: var(--bg-dark);">
        
        <!-- Top Bar -->
        <header style="background: var(--bg-card); border-bottom: 1px solid var(--border); padding: 1.5rem 2rem; position: sticky; top: 0; z-index: 50;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h1 id="pageTitle" style="font-size: 1.75rem; margin-bottom: 0.25rem;">Dashboard Overview</h1>
                    <p style="color: var(--text-muted); font-size: 0.875rem;">Welcome back, {{ user.get('discord_id', 'User')[:16] }}!</p>
                </div>
                
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span class="badge badge-success">
                        <i class="fas fa-circle" style="font-size: 0.5rem;"></i>
                        <span>Online</span>
                    </span>
                </div>
            </div>
        </header>
        
        <!-- Page Content Container -->
        <div id="pageContent" style="padding: 2rem;">
            
            <!-- ===== OVERVIEW PAGE ===== -->
            <div id="page-overview" class="page-content active">
                
                <!-- Stats Grid -->
                <div class="grid grid-4" style="margin-bottom: 2rem;">
                    <div class="stat-card fade-in">
                        <div class="stat-label">License Status</div>
                        <div class="stat-value" style="font-size: 1.5rem;">
                            <span class="badge badge-success"><i class="fas fa-check"></i> Active</span>
                        </div>
                        <div class="stat-change positive">
                            <i class="fas fa-key"></i>
                            <span>Valid License</span>
                        </div>
                    </div>
                    
                    <div class="stat-card fade-in" style="animation-delay: 0.1s;">
                        <div class="stat-label">HWID Status</div>
                        <div class="stat-value" style="font-size: 1.5rem;">
                            {% if user.get('hwid') %}
                            <span class="badge badge-success"><i class="fas fa-check"></i> Set</span>
                            {% else %}
                            <span class="badge badge-warning"><i class="fas fa-times"></i> Not Set</span>
                            {% endif %}
                        </div>
                        <button onclick="resetHWID()" class="btn btn-primary btn-sm" style="margin-top: 0.5rem; font-size: 0.75rem; padding: 0.375rem 0.75rem;">
                            <i class="fas fa-redo"></i> Reset
                        </button>
                    </div>
                    
                    <div class="stat-card fade-in" style="animation-delay: 0.2s;">
                        <div class="stat-label">Total Logins</div>
                        <div class="stat-value">{{ analytics.get('total_logins', 0) }}</div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i>
                            <span>All time</span>
                        </div>
                    </div>
                    
                    <div class="stat-card fade-in" style="animation-delay: 0.3s;">
                        <div class="stat-label">Member Since</div>
                        <div class="stat-value" style="font-size: 1.25rem;">{{ user.get('joined_at', 'Unknown')[:10] }}</div>
                        <div class="stat-change">
                            <i class="fas fa-calendar"></i>
                            <span>Join date</span>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content Grid -->
                <div class="grid grid-2">
                    
                    <!-- Loader Script Card -->
                    <div class="card fade-in">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-code"></i>
                            </div>
                            <div>
                                <div class="card-title">Script Loader</div>
                                <div class="card-subtitle">Copy and execute in your Roblox executor</div>
                            </div>
                        </div>
                        
                        <textarea id="loaderScript" class="code-block" style="height: 200px; resize: none; font-size: 0.75rem; margin-bottom: 1rem;" readonly>{{ loader_script }}</textarea>
                        
                        <div style="display: flex; gap: 0.75rem;">
                            <button onclick="copyLoader()" class="btn btn-primary" style="flex: 1;">
                                <i class="fas fa-copy"></i>
                                <span>Copy Script</span>
                            </button>
                            <button onclick="downloadLoader()" class="btn btn-secondary">
                                <i class="fas fa-download"></i>
                                <span>Download</span>
                            </button>
                        </div>
                    </div>
                    
                    <!-- Quick Actions Card -->
                    <div class="card fade-in" style="animation-delay: 0.1s;">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-bolt"></i>
                            </div>
                            <div>
                                <div class="card-title">Quick Actions</div>
                                <div class="card-subtitle">Common tasks and shortcuts</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                            <button onclick="copyKey()" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fas fa-key"></i>
                                <span>Copy License Key</span>
                            </button>
                            
                            <button onclick="resetHWID()" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fas fa-desktop"></i>
                                <span>Reset HWID</span>
                            </button>
                            
                            <button onclick="switchPage(event, 'scripts')" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fas fa-code"></i>
                                <span>Browse Scripts</span>
                            </button>
                            
                            <a href="https://discord.gg/bananahub" target="_blank" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fab fa-discord"></i>
                                <span>Join Discord</span>
                            </a>
                        </div>
                    </div>
                    
                    <!-- License Information Card -->
                    <div class="card fade-in" style="animation-delay: 0.2s;">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-id-card"></i>
                            </div>
                            <div>
                                <div class="card-title">License Information</div>
                                <div class="card-subtitle">Your account details</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 1rem;">
                            <div>
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem; text-transform: uppercase; letter-spacing: 0.5px;">License Key</div>
                                <div class="code-block" style="font-size: 0.875rem; padding: 0.75rem; cursor: pointer;" onclick="this.style.filter = this.style.filter ? '' : 'blur(0px)'; this.style.WebkitFilter = this.style.WebkitFilter ? '' : 'blur(0px)';" style="filter: blur(5px); -webkit-filter: blur(5px);">{{ user.get('key', 'N/A') }}</div>
                            </div>
                            
                            <div>
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem; text-transform: uppercase; letter-spacing: 0.5px;">Discord ID</div>
                                <div style="font-family: monospace; color: var(--text-primary);">{{ user.get('discord_id', 'Unknown') }}</div>
                            </div>
                            
                            <div>
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem; text-transform: uppercase; letter-spacing: 0.5px;">Last Login</div>
                                <div style="color: var(--text-secondary);">{{ user.get('last_login', 'Never')[:19] }}</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- System Status Card -->
                    <div class="card fade-in" style="animation-delay: 0.3s;">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-server"></i>
                            </div>
                            <div>
                                <div class="card-title">System Status</div>
                                <div class="card-subtitle">Service availability</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 1rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <i class="fas fa-database" style="color: var(--primary);"></i>
                                    <span>Database</span>
                                </div>
                                <span class="badge badge-success">Operational</span>
                            </div>
                            
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <i class="fas fa-cloud" style="color: var(--primary);"></i>
                                    <span>API Server</span>
                                </div>
                                <span class="badge badge-success">Online</span>
                            </div>
                            
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <i class="fas fa-shield-alt" style="color: var(--primary);"></i>
                                    <span>Security</span>
                                </div>
                                <span class="badge badge-success">Protected</span>
                            </div>
                            
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <i class="fas fa-sync" style="color: var(--primary);"></i>
                                    <span>Auto-Updates</span>
                                </div>
                                <span class="badge badge-success">Enabled</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- ===== SCRIPTS PAGE ===== -->
            <div id="page-scripts" class="page-content" style="display: none;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">
                            <i class="fas fa-code"></i>
                        </div>
                        <div style="flex: 1;">
                            <div class="card-title">Script Library</div>
                            <div class="card-subtitle">Browse and execute premium scripts</div>
                        </div>
                        <input type="text" class="form-input" placeholder="Search scripts..." style="max-width: 300px; padding: 0.625rem 1rem;">
                    </div>
                    
                    <div class="grid grid-3" style="margin-top: 1.5rem;">
                        <!-- Script Card 1 -->
                        <div class="card" style="padding: 1.5rem;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #3B82F6, #1D4ED8); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-gamepad" style="color: white; font-size: 1.25rem;"></i>
                                </div>
                                <div>
                                    <h4 style="margin-bottom: 0.25rem;">Universal ESP</h4>
                                    <span class="badge badge-success" style="font-size: 0.625rem;">Popular</span>
                                </div>
                            </div>
                            <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">See all players through walls with advanced ESP features.</p>
                            <button class="btn btn-primary btn-sm" style="width: 100%;">
                                <i class="fas fa-play"></i>
                                <span>Execute</span>
                            </button>
                        </div>
                        
                        <!-- Script Card 2 -->
                        <div class="card" style="padding: 1.5rem;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #10B981, #059669); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-running" style="color: white; font-size: 1.25rem;"></i>
                                </div>
                                <div>
                                    <h4 style="margin-bottom: 0.25rem;">Speed Hack</h4>
                                    <span class="badge badge-primary" style="font-size: 0.625rem;">Premium</span>
                                </div>
                            </div>
                            <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">Increase your character's movement speed significantly.</p>
                            <button class="btn btn-primary btn-sm" style="width: 100%;">
                                <i class="fas fa-play"></i>
                                <span>Execute</span>
                            </button>
                        </div>
                        
                        <!-- Script Card 3 -->
                        <div class="card" style="padding: 1.5rem;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #F59E0B, #D97706); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-crosshairs" style="color: white; font-size: 1.25rem;"></i>
                                </div>
                                <div>
                                    <h4 style="margin-bottom: 0.25rem;">Aimbot</h4>
                                    <span class="badge badge-warning" style="font-size: 0.625rem;">New</span>
                                </div>
                            </div>
                            <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">Auto-aim assistance with customizable settings.</p>
                            <button class="btn btn-primary btn-sm" style="width: 100%;">
                                <i class="fas fa-play"></i>
                                <span>Execute</span>
                            </button>
                        </div>
                        
                        <!-- More script cards... -->
                        <div class="card" style="padding: 1.5rem;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8B5CF6, #7C3AED); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-infinity" style="color: white; font-size: 1.25rem;"></i>
                                </div>
                                <div>
                                    <h4 style="margin-bottom: 0.25rem;">Infinite Jump</h4>
                                    <span class="badge badge-success" style="font-size: 0.625rem;">Popular</span>
                                </div>
                            </div>
                            <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">Jump infinitely without touching the ground.</p>
                            <button class="btn btn-primary btn-sm" style="width: 100%;">
                                <i class="fas fa-play"></i>
                                <span>Execute</span>
                            </button>
                        </div>
                        
                        <div class="card" style="padding: 1.5rem;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #EC4899, #DB2777); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-ghost" style="color: white; font-size: 1.25rem;"></i>
                                </div>
                                <div>
                                    <h4 style="margin-bottom: 0.25rem;">Noclip</h4>
                                    <span class="badge badge-primary" style="font-size: 0.625rem;">Premium</span>
                                </div>
                            </div>
                            <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">Walk through walls and solid objects.</p>
                            <button class="btn btn-primary btn-sm" style="width: 100%;">
                                <i class="fas fa-play"></i>
                                <span>Execute</span>
                            </button>
                        </div>
                        
                        <div class="card" style="padding: 1.5rem;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #06B6D4, #0891B2); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-eye" style="color: white; font-size: 1.25rem;"></i>
                                </div>
                                <div>
                                    <h4 style="margin-bottom: 0.25rem;">Player Tracker</h4>
                                    <span class="badge badge-success" style="font-size: 0.625rem;">Popular</span>
                                </div>
                            </div>
                            <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">Track player positions and movements in real-time.</p>
                            <button class="btn btn-primary btn-sm" style="width: 100%;">
                                <i class="fas fa-play"></i>
                                <span>Execute</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- ===== ACTIVITY PAGE ===== -->
            <div id="page-activity" class="page-content" style="display: none;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">
                            <i class="fas fa-history"></i>
                        </div>
                        <div>
                            <div class="card-title">Activity Log</div>
                            <div class="card-subtitle">Your recent account activity</div>
                        </div>
                    </div>
                    
                    <div class="table-container" style="margin-top: 1.5rem;">
                        <table>
                            <thead>
                                <tr>
                                    <th>Event</th>
                                    <th>Description</th>
                                    <th>IP Address</th>
                                    <th>Timestamp</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><span class="badge badge-success"><i class="fas fa-sign-in-alt"></i> Login</span></td>
                                    <td>Successful web login</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">{{ user.get('last_login', 'Unknown')[:19] }}</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-primary"><i class="fas fa-code"></i> Script</span></td>
                                    <td>Loader script accessed</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">2 hours ago</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-warning"><i class="fas fa-desktop"></i> HWID</span></td>
                                    <td>HWID reset performed</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">1 day ago</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-success"><i class="fas fa-key"></i> Auth</span></td>
                                    <td>License key validated</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">3 days ago</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- ===== PROFILE PAGE ===== -->
            <div id="page-profile" class="page-content" style="display: none;">
                <div class="grid grid-2">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-user"></i>
                            </div>
                            <div>
                                <div class="card-title">Profile Information</div>
                                <div class="card-subtitle">Your account details</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 1.5rem; margin-top: 1.5rem;">
                            <div>
                                <label class="form-label">Discord ID</label>
                                <input type="text" class="form-input" value="{{ user.get('discord_id', 'Unknown') }}" readonly>
                            </div>
                            
                            <div>
                                <label class="form-label">License Key</label>
                                <input type="password" class="form-input" value="{{ user.get('key', 'N/A') }}" readonly>
                            </div>
                            
                            <div>
                                <label class="form-label">Member Since</label>
                                <input type="text" class="form-input" value="{{ user.get('joined_at', 'Unknown')[:10] }}" readonly>
                            </div>
                            
                            <div>
                                <label class="form-label">Total Logins</label>
                                <input type="text" class="form-input" value="{{ analytics.get('total_logins', 0) }}" readonly>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-chart-bar"></i>
                            </div>
                            <div>
                                <div class="card-title">Usage Statistics</div>
                                <div class="card-subtitle">Your activity metrics</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 1.5rem; margin-top: 1.5rem;">
                            <div class="stat-card">
                                <div class="stat-label">Scripts Executed</div>
                                <div class="stat-value">{{ analytics.get('total_logins', 0) * 3 }}</div>
                                <div class="stat-change positive">
                                    <i class="fas fa-arrow-up"></i>
                                    <span>This month</span>
                                </div>
                            </div>
                            
                            <div class="stat-card">
                                <div class="stat-label">Hours Played</div>
                                <div class="stat-value">{{ analytics.get('total_logins', 0) * 2 }}</div>
                                <div class="stat-change">
                                    <i class="fas fa-clock"></i>
                                    <span>Total time</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- ===== SETTINGS PAGE ===== -->
            <div id="page-settings" class="page-content" style="display: none;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">
                            <i class="fas fa-cog"></i>
                        </div>
                        <div>
                            <div class="card-title">Account Settings</div>
                            <div class="card-subtitle">Manage your preferences</div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 2rem;">
                        <!-- HWID Management -->
                        <div style="padding: 1.5rem; background: var(--bg-darker); border-radius: var(--radius-lg); margin-bottom: 1.5rem;">
                            <h4 style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.75rem;">
                                <i class="fas fa-desktop" style="color: var(--primary);"></i>
                                <span>HWID Management</span>
                            </h4>
                            <p style="color: var(--text-muted); margin-bottom: 1rem; font-size: 0.875rem;">
                                Your Hardware ID is {% if user.get('hwid') %}<span class="badge badge-success">Set</span>{% else %}<span class="badge badge-warning">Not Set</span>{% endif %}
                            </p>
                            <button onclick="resetHWID()" class="btn btn-primary">
                                <i class="fas fa-redo"></i>
                                <span>Reset HWID</span>
                            </button>
                            <p style="color: var(--text-muted); margin-top: 0.75rem; font-size: 0.75rem;">
                                <i class="fas fa-info-circle"></i> You can reset your HWID once every 5 minutes
                            </p>
                        </div>
                        
                        <!-- Security -->
                        <div style="padding: 1.5rem; background: var(--bg-darker); border-radius: var(--radius-lg); margin-bottom: 1.5rem;">
                            <h4 style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.75rem;">
                                <i class="fas fa-shield-alt" style="color: var(--primary);"></i>
                                <span>Security</span>
                            </h4>
                            <div style="display: flex; flex-direction: column; gap: 1rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <div style="font-weight: 600; margin-bottom: 0.25rem;">Two-Factor Authentication</div>
                                        <div style="color: var(--text-muted); font-size: 0.875rem;">Add an extra layer of security</div>
                                    </div>
                                    <span class="badge badge-warning">Coming Soon</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Danger Zone -->
                        <div style="padding: 1.5rem; background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: var(--radius-lg);">
                            <h4 style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.75rem; color: var(--error);">
                                <i class="fas fa-exclamation-triangle"></i>
                                <span>Danger Zone</span>
                            </h4>
                            <p style="color: var(--text-muted); margin-bottom: 1rem; font-size: 0.875rem;">
                                Permanently delete your account and all associated data
                            </p>
                            <button class="btn btn-secondary" style="border-color: var(--error); color: var(--error);">
                                <i class="fas fa-trash"></i>
                                <span>Delete Account</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </main>
</div>

<style>
    /* Navigation Link Styles */
    .nav-link {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        margin-bottom: 0.25rem;
        color: var(--text-secondary);
        text-decoration: none;
        border-radius: var(--radius-md);
        transition: all var(--transition-base);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .nav-link:hover {
        background: var(--bg-card);
        color: var(--text-primary);
        transform: translateX(4px);
    }
    
    .nav-link.active {
        background: linear-gradient(135deg, rgba(250, 204, 21, 0.1), rgba(245, 158, 11, 0.05));
        color: var(--primary);
        border-left: 3px solid var(--primary);
        padding-left: calc(1rem - 3px);
    }
    
    .nav-link i {
        width: 20px;
        text-align: center;
    }
    
    /* Page Content */
    .page-content {
        animation: fadeIn 0.4s ease-out;
    }
    
    .page-content.active {
        display: block;
    }
</style>

<script>
    // Page Navigation
    function switchPage(event, pageName) {
        if (event) event.preventDefault();
        
        // Hide all pages
        document.querySelectorAll('.page-content').forEach(page => {
            page.style.display = 'none';
            page.classList.remove('active');
        });
        
        // Show selected page
        const targetPage = document.getElementById('page-' + pageName);
        if (targetPage) {
            targetPage.style.display = 'block';
            targetPage.classList.add('active');
        }
        
        // Update nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        const activeLink = document.querySelector(`[data-page="${pageName}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
        
        // Update page title
        const titles = {
            'overview': 'Dashboard Overview',
            'scripts': 'Script Library',
            'activity': 'Activity Log',
            'profile': 'User Profile',
            'settings': 'Account Settings'
        };
        document.getElementById('pageTitle').textContent = titles[pageName] || 'Dashboard';
        
        // Update URL without reload
        history.pushState({page: pageName}, '', '/dashboard/' + (pageName === 'overview' ? '' : pageName));
    }
    
    // Copy functions
    async function copyKey() {
        const keyText = '{{ user.get("key", "") }}';
        await navigator.clipboard.writeText(keyText);
        alert('✅ License key copied to clipboard!');
    }
    
    async function copyLoader() {
        const script = document.getElementById('loaderScript').value;
        await navigator.clipboard.writeText(script);
        alert('✅ Loader script copied to clipboard!');
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
        if (!confirm('Reset your HWID? You can only do this once every 5 minutes.')) return;
        
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
    
    // Handle browser back/forward
    window.addEventListener('popstate', function(event) {
        if (event.state && event.state.page) {
            switchPage(null, event.state.page);
        }
    });
</script>
""")
# ==============================================================================
# 🛡️ ADMIN PANEL - Multi-Page Layout with Advanced Management
# ==============================================================================

ADMIN_PAGE = BASE_HTML.replace('{BODY_CONTENT}', """
<!-- Admin Layout -->
<div style="display: flex; min-height: 100vh;">
    
    <!-- Admin Sidebar Navigation -->
    <aside style="width: 280px; background: var(--bg-darker); border-right: 1px solid var(--border); position: fixed; height: 100vh; overflow-y: auto; z-index: 100;">
        <!-- Logo -->
        <div style="padding: 2rem 1.5rem; border-bottom: 1px solid var(--border);">
            <a href="/admin" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none;">
                <span style="font-size: 2rem;">🍌</span>
                <span style="font-size: 1.25rem; font-weight: 800; color: var(--primary);">Admin Panel</span>
            </a>
        </div>
        
        <!-- Admin Profile Card -->
        <div style="padding: 1.5rem; border-bottom: 1px solid var(--border);">
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05)); border-radius: var(--radius-lg); border: 1px solid rgba(239, 68, 68, 0.2);">
                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--error), #DC2626); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 800; color: white;">
                    A
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 600; font-size: 0.875rem; color: var(--text-primary);">
                        Administrator
                    </div>
                    <div style="font-size: 0.75rem; color: var(--error);">Full Access</div>
                </div>
            </div>
        </div>
        
        <!-- Admin Navigation Menu -->
        <nav style="padding: 1.5rem 1rem;">
            <!-- Dashboard Section -->
            <div style="margin-bottom: 2rem;">
                <div style="padding: 0 0.75rem; margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">
                    Overview
                </div>
                
                <a href="/admin" class="nav-link active" data-page="dashboard" onclick="switchAdminPage(event, 'dashboard')">
                    <i class="fas fa-chart-pie"></i>
                    <span>Dashboard</span>
                </a>
                
                <a href="/admin/analytics" class="nav-link" data-page="analytics" onclick="switchAdminPage(event, 'analytics')">
                    <i class="fas fa-chart-line"></i>
                    <span>Analytics</span>
                </a>
            </div>
            
            <!-- Management Section -->
            <div style="margin-bottom: 2rem;">
                <div style="padding: 0 0.75rem; margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">
                    Management
                </div>
                
                <a href="/admin/users" class="nav-link" data-page="users" onclick="switchAdminPage(event, 'users')">
                    <i class="fas fa-users"></i>
                    <span>Users</span>
                </a>
                
                <a href="/admin/keys" class="nav-link" data-page="keys" onclick="switchAdminPage(event, 'keys')">
                    <i class="fas fa-key"></i>
                    <span>License Keys</span>
                </a>
                
                <a href="/admin/logs" class="nav-link" data-page="logs" onclick="switchAdminPage(event, 'logs')">
                    <i class="fas fa-clipboard-list"></i>
                    <span>Activity Logs</span>
                </a>
            </div>
            
            <!-- System Section -->
            <div style="margin-bottom: 2rem;">
                <div style="padding: 0 0.75rem; margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">
                    System
                </div>
                
                <a href="/admin/settings" class="nav-link" data-page="settings" onclick="switchAdminPage(event, 'settings')">
                    <i class="fas fa-cog"></i>
                    <span>Settings</span>
                </a>
                
                <a href="#" onclick="createBackup(); return false;" class="nav-link">
                    <i class="fas fa-database"></i>
                    <span>Backup</span>
                </a>
            </div>
            
            <!-- Quick Actions -->
            <div>
                <div style="padding: 0 0.75rem; margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">
                    Quick Actions
                </div>
                
                <a href="/dashboard" class="nav-link">
                    <i class="fas fa-user"></i>
                    <span>User View</span>
                </a>
                
                <a href="/logout" class="nav-link" style="color: var(--error);">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </div>
        </nav>
    </aside>
    
    <!-- Admin Main Content Area -->
    <main style="margin-left: 280px; flex: 1; min-height: 100vh; background: var(--bg-dark);">
        
        <!-- Admin Top Bar -->
        <header style="background: var(--bg-card); border-bottom: 1px solid var(--border); padding: 1.5rem 2rem; position: sticky; top: 0; z-index: 50;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h1 id="adminPageTitle" style="font-size: 1.75rem; margin-bottom: 0.25rem;">Admin Dashboard</h1>
                    <p style="color: var(--text-muted); font-size: 0.875rem;">System overview and management</p>
                </div>
                
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span class="badge badge-error">
                        <i class="fas fa-shield-alt"></i>
                        <span>Admin Access</span>
                    </span>
                    <button onclick="generateKeys()" class="btn btn-primary btn-sm">
                        <i class="fas fa-plus"></i>
                        <span>Generate Keys</span>
                    </button>
                </div>
            </div>
        </header>
        
        <!-- Admin Page Content Container -->
        <div id="adminPageContent" style="padding: 2rem;">
            
            <!-- ===== DASHBOARD PAGE ===== -->
            <div id="admin-page-dashboard" class="page-content active">
                
                <!-- System Stats Grid -->
                <div class="grid grid-4" style="margin-bottom: 2rem;">
                    <div class="stat-card fade-in">
                        <div class="stat-label">Total Users</div>
                        <div class="stat-value">{{ stats.get('total_users', 0) }}</div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i>
                            <span>+{{ stats.get('total_users', 0) // 10 }} this week</span>
                        </div>
                    </div>
                    
                    <div class="stat-card fade-in" style="animation-delay: 0.1s;">
                        <div class="stat-label">Active Keys</div>
                        <div class="stat-value">{{ stats.get('total_keys', 0) - stats.get('available_keys', 0) }}</div>
                        <div class="stat-change">
                            <i class="fas fa-key"></i>
                            <span>{{ stats.get('available_keys', 0) }} available</span>
                        </div>
                    </div>
                    
                    <div class="stat-card fade-in" style="animation-delay: 0.2s;">
                        <div class="stat-label">Total Logins</div>
                        <div class="stat-value">{{ stats.get('total_logins', 0) }}</div>
                        <div class="stat-change positive">
                            <i class="fas fa-chart-line"></i>
                            <span>All time</span>
                        </div>
                    </div>
                    
                    <div class="stat-card fade-in" style="animation-delay: 0.3s;">
                        <div class="stat-label">Banned Users</div>
                        <div class="stat-value" style="color: var(--error);">{{ stats.get('total_blacklisted', 0) }}</div>
                        <div class="stat-change negative">
                            <i class="fas fa-ban"></i>
                            <span>Blacklisted</span>
                        </div>
                    </div>
                </div>
                
                <!-- Main Dashboard Grid -->
                <div class="grid grid-2">
                    
                    <!-- Quick Actions Card -->
                    <div class="card fade-in">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-bolt"></i>
                            </div>
                            <div>
                                <div class="card-title">Quick Actions</div>
                                <div class="card-subtitle">Common administrative tasks</div>
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 1.5rem;">
                            <button onclick="generateKeys()" class="btn btn-primary" style="justify-content: flex-start;">
                                <i class="fas fa-key"></i>
                                <span>Generate Keys</span>
                            </button>
                            
                            <button onclick="whitelistUser()" class="btn btn-primary" style="justify-content: flex-start;">
                                <i class="fas fa-user-plus"></i>
                                <span>Whitelist User</span>
                            </button>
                            
                            <button onclick="switchAdminPage(null, 'users')" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fas fa-users"></i>
                                <span>Manage Users</span>
                            </button>
                            
                            <button onclick="switchAdminPage(null, 'keys')" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fas fa-list"></i>
                                <span>View Keys</span>
                            </button>
                            
                            <button onclick="createBackup()" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fas fa-database"></i>
                                <span>Backup DB</span>
                            </button>
                            
                            <button onclick="switchAdminPage(null, 'logs')" class="btn btn-secondary" style="justify-content: flex-start;">
                                <i class="fas fa-clipboard-list"></i>
                                <span>View Logs</span>
                            </button>
                        </div>
                    </div>
                    
                    <!-- System Status Card -->
                    <div class="card fade-in" style="animation-delay: 0.1s;">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-server"></i>
                            </div>
                            <div>
                                <div class="card-title">System Status</div>
                                <div class="card-subtitle">Service health monitoring</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1.5rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: var(--bg-darker); border-radius: var(--radius-md);">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <i class="fas fa-database" style="color: var(--primary); font-size: 1.25rem;"></i>
                                    <div>
                                        <div style="font-weight: 600; font-size: 0.875rem;">Database</div>
                                        <div style="font-size: 0.75rem; color: var(--text-muted);">SQLite Connection</div>
                                    </div>
                                </div>
                                <span class="badge badge-success">Online</span>
                            </div>
                            
                            <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: var(--bg-darker); border-radius: var(--radius-md);">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <i class="fas fa-cloud" style="color: var(--primary); font-size: 1.25rem;"></i>
                                    <div>
                                        <div style="font-weight: 600; font-size: 0.875rem;">API Server</div>
                                        <div style="font-size: 0.75rem; color: var(--text-muted);">Flask Backend</div>
                                    </div>
                                </div>
                                <span class="badge badge-success">Running</span>
                            </div>
                            
                            <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: var(--bg-darker); border-radius: var(--radius-md);">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <i class="fas fa-shield-alt" style="color: var(--primary); font-size: 1.25rem;"></i>
                                    <div>
                                        <div style="font-weight: 600; font-size: 0.875rem;">Security</div>
                                        <div style="font-size: 0.75rem; color: var(--text-muted);">HWID Protection</div>
                                    </div>
                                </div>
                                <span class="badge badge-success">Active</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Recent Users Card -->
                    <div class="card fade-in" style="animation-delay: 0.2s;">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-user-clock"></i>
                            </div>
                            <div>
                                <div class="card-title">Recent Users</div>
                                <div class="card-subtitle">Latest registrations</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1.5rem;">
                            {% for user in users[:5] %}
                            <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem; background: var(--bg-darker); border-radius: var(--radius-md);">
                                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, var(--primary), var(--accent)); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-weight: 800; color: var(--bg-dark);">
                                    {{ user.get('discord_id', 'U')[0]|upper }}
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <div style="font-weight: 600; font-size: 0.875rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                        {{ user.get('discord_id', 'Unknown')[:20] }}
                                    </div>
                                    <div style="font-size: 0.75rem; color: var(--text-muted);">
                                        {{ user.get('joined_at', 'Unknown')[:10] }}
                                    </div>
                                </div>
                                <button onclick="manageUser('{{ user.get('discord_id', '') }}')" class="btn btn-ghost btn-icon btn-sm">
                                    <i class="fas fa-cog"></i>
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    
                    <!-- Recent Activity Card -->
                    <div class="card fade-in" style="animation-delay: 0.3s;">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-history"></i>
                            </div>
                            <div>
                                <div class="card-title">Recent Activity</div>
                                <div class="card-subtitle">Latest system events</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1.5rem;">
                            <div style="padding: 0.75rem; background: var(--bg-darker); border-radius: var(--radius-md); border-left: 3px solid var(--success);">
                                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                                    <span class="badge badge-success" style="font-size: 0.625rem;"><i class="fas fa-sign-in-alt"></i> Login</span>
                                    <span style="font-size: 0.75rem; color: var(--text-muted);">2 minutes ago</span>
                                </div>
                                <div style="font-size: 0.875rem;">User logged in via web panel</div>
                            </div>
                            
                            <div style="padding: 0.75rem; background: var(--bg-darker); border-radius: var(--radius-md); border-left: 3px solid var(--primary);">
                                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                                    <span class="badge badge-primary" style="font-size: 0.625rem;"><i class="fas fa-key"></i> Key</span>
                                    <span style="font-size: 0.75rem; color: var(--text-muted);">15 minutes ago</span>
                                </div>
                                <div style="font-size: 0.875rem;">New license key generated</div>
                            </div>
                            
                            <div style="padding: 0.75rem; background: var(--bg-darker); border-radius: var(--radius-md); border-left: 3px solid var(--warning);">
                                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                                    <span class="badge badge-warning" style="font-size: 0.625rem;"><i class="fas fa-desktop"></i> HWID</span>
                                    <span style="font-size: 0.75rem; color: var(--text-muted);">1 hour ago</span>
                                </div>
                                <div style="font-size: 0.875rem;">HWID reset requested</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- ===== ANALYTICS PAGE ===== -->
            <div id="admin-page-analytics" class="page-content" style="display: none;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <div>
                            <div class="card-title">System Analytics</div>
                            <div class="card-subtitle">Performance and usage metrics</div>
                        </div>
                    </div>
                    
                    <div class="grid grid-3" style="margin-top: 2rem;">
                        <div class="stat-card">
                            <div class="stat-label">Total Revenue</div>
                            <div class="stat-value" style="font-size: 2rem;">$0</div>
                            <div class="stat-change">
                                <i class="fas fa-dollar-sign"></i>
                                <span>Coming soon</span>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-label">Avg. Session Time</div>
                            <div class="stat-value" style="font-size: 2rem;">24m</div>
                            <div class="stat-change positive">
                                <i class="fas fa-clock"></i>
                                <span>+5m from last week</span>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-label">Server Uptime</div>
                            <div class="stat-value" style="font-size: 2rem;">99.9%</div>
                            <div class="stat-change positive">
                                <i class="fas fa-server"></i>
                                <span>Excellent</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- ===== USERS MANAGEMENT PAGE ===== -->
            <div id="admin-page-users" class="page-content" style="display: none;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <div style="flex: 1;">
                            <div class="card-title">Users Management</div>
                            <div class="card-subtitle">{{ users|length }} total users</div>
                        </div>
                        <div style="display: flex; gap: 1rem;">
                            <input type="text" id="userSearchAdmin" onkeyup="searchUsersAdmin()" placeholder="Search users..." class="form-input" style="width: 300px; padding: 0.625rem 1rem;">
                            <button onclick="whitelistUser()" class="btn btn-primary btn-sm">
                                <i class="fas fa-user-plus"></i>
                                <span>Add User</span>
                            </button>
                        </div>
                    </div>
                    
                    <div class="table-container" style="margin-top: 1.5rem;">
                        <table>
                            <thead>
                                <tr>
                                    <th>User</th>
                                    <th>License Key</th>
                                    <th>HWID</th>
                                    <th>Joined</th>
                                    <th>Logins</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="usersTableAdmin">
                                {% for user in users[:50] %}
                                <tr data-user-id="{{ user.get('discord_id', '') }}">
                                    <td>
                                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                                            <div style="width: 32px; height: 32px; background: linear-gradient(135deg, var(--primary), var(--accent)); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.875rem; color: var(--bg-dark);">
                                                {{ user.get('discord_id', 'U')[0]|upper }}
                                            </div>
                                            <div>
                                                <div style="font-weight: 600; font-size: 0.875rem;">{{ user.get('discord_id', 'Unknown')[:20] }}</div>
                                                <div style="font-size: 0.75rem; color: var(--text-muted);">Discord ID</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <code style="background: rgba(16, 185, 129, 0.1); padding: 0.375rem 0.625rem; border-radius: var(--radius-sm); color: var(--success); font-size: 0.75rem;">
                                            {{ user.get('key', 'None')[:12] }}...
                                        </code>
                                    </td>
                                    <td>
                                        <code style="font-size: 0.75rem; color: var(--text-muted);">
                                            {% if user.get('hwid') %}
                                                {% if user.get('hwid')|length > 12 %}
                                                    {{ user.get('hwid')[:12] }}...
                                                {% else %}
                                                    {{ user.get('hwid') }}
                                                {% endif %}
                                            {% else %}
                                                Not set
                                            {% endif %}
                                        </code>
                                    </td>
                                    <td style="font-size: 0.875rem; color: var(--text-muted);">{{ user.get('joined_at', 'Unknown')[:10] }}</td>
                                    <td>
                                        <span class="badge badge-primary" style="font-size: 0.75rem;">
                                            {{ user.get('login_count', 0) }}
                                        </span>
                                    </td>
                                    <td>
                                        <span class="badge badge-success user-status-admin"><i class="fas fa-check"></i> Active</span>
                                    </td>
                                    <td>
                                        <button onclick="manageUser('{{ user.get('discord_id', '') }}')" class="btn btn-secondary btn-sm">
                                            <i class="fas fa-cog"></i>
                                        </button>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- ===== KEYS MANAGEMENT PAGE ===== -->
            <div id="admin-page-keys" class="page-content" style="display: none;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">
                            <i class="fas fa-key"></i>
                        </div>
                        <div style="flex: 1;">
                            <div class="card-title">License Keys</div>
                            <div class="card-subtitle">{{ unused_keys|length }} available keys</div>
                        </div>
                        <button onclick="generateKeys()" class="btn btn-primary btn-sm">
                            <i class="fas fa-plus"></i>
                            <span>Generate Keys</span>
                        </button>
                    </div>
                    
                    <div class="grid grid-3" style="margin-top: 2rem; margin-bottom: 2rem;">
                        <div class="stat-card">
                            <div class="stat-label">Total Keys</div>
                            <div class="stat-value">{{ all_keys|length }}</div>
                            <div class="stat-change">
                                <i class="fas fa-key"></i>
                                <span>Generated</span>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-label">Available</div>
                            <div class="stat-value" style="color: var(--success);">{{ unused_keys|length }}</div>
                            <div class="stat-change positive">
                                <i class="fas fa-check"></i>
                                <span>Ready to use</span>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-label">Used Keys</div>
                            <div class="stat-value">{{ all_keys|length - unused_keys|length }}</div>
                            <div class="stat-change">
                                <i class="fas fa-user-check"></i>
                                <span>Redeemed</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>License Key</th>
                                    <th>Created</th>
                                    <th>Created By</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for key in unused_keys[:30] %}
                                <tr>
                                    <td>
                                        <code style="background: rgba(16, 185, 129, 0.1); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); color: var(--success); font-weight: 600;">
                                            {{ key.get('key', '') }}
                                        </code>
                                    </td>
                                    <td style="font-size: 0.875rem; color: var(--text-muted);">{{ key.get('created_at', 'Unknown')[:10] }}</td>
                                    <td style="font-size: 0.875rem;">{{ key.get('created_by', 'System')[:20] }}</td>
                                    <td><span class="badge badge-success">Available</span></td>
                                    <td>
                                        <div style="display: flex; gap: 0.5rem;">
                                            <button onclick="copyText('{{ key.get('key', '') }}')" class="btn btn-primary btn-sm">
                                                <i class="fas fa-copy"></i>
                                            </button>
                                            <button onclick="deleteKey('{{ key.get('key', '') }}')" class="btn btn-secondary btn-sm">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- ===== ACTIVITY LOGS PAGE ===== -->
            <div id="admin-page-logs" class="page-content" style="display: none;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">
                            <i class="fas fa-clipboard-list"></i>
                        </div>
                        <div style="flex: 1;">
                            <div class="card-title">Activity Logs</div>
                            <div class="card-subtitle">System-wide activity tracking</div>
                        </div>
                        <select class="form-input" style="width: 200px; padding: 0.5rem;">
                            <option value="all">All Events</option>
                            <option value="login">Logins</option>
                            <option value="hwid_reset">HWID Resets</option>
                            <option value="key_generated">Key Generation</option>
                            <option value="blacklist">Bans</option>
                        </select>
                    </div>
                    
                    <div class="table-container" style="margin-top: 1.5rem;">
                        <table>
                            <thead>
                                <tr>
                                    <th>Event Type</th>
                                    <th>User</th>
                                    <th>Description</th>
                                    <th>IP Address</th>
                                    <th>Timestamp</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><span class="badge badge-success"><i class="fas fa-sign-in-alt"></i> Login</span></td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">User#12345</td>
                                    <td>Successful web login</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">5 mins ago</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-primary"><i class="fas fa-key"></i> Key Gen</span></td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">Admin</td>
                                    <td>Generated 5 new keys</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">1 hour ago</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-warning"><i class="fas fa-desktop"></i> HWID</span></td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">User#67890</td>
                                    <td>HWID reset performed</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">3 hours ago</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-error"><i class="fas fa-ban"></i> Ban</span></td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">User#11111</td>
                                    <td>User blacklisted for ToS violation</td>
                                    <td style="font-family: monospace; font-size: 0.875rem;">xxx.xxx.xxx.xxx</td>
                                    <td style="color: var(--text-muted); font-size: 0.875rem;">1 day ago</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- ===== SETTINGS PAGE ===== -->
            <div id="admin-page-settings" class="page-content" style="display: none;">
                <div class="grid grid-2">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-cog"></i>
                            </div>
                            <div>
                                <div class="card-title">System Settings</div>
                                <div class="card-subtitle">Configure system behavior</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 1.5rem; margin-top: 1.5rem;">
                            <div>
                                <label class="form-label">System Name</label>
                                <input type="text" class="form-input" value="Banana Hub Enterprise" readonly>
                            </div>
                            
                            <div>
                                <label class="form-label">Website URL</label>
                                <input type="text" class="form-input" value="{{ website_url }}" readonly>
                            </div>
                            
                            <div>
                                <label class="form-label">Max HWID Resets</label>
                                <input type="number" class="form-input" value="1" readonly>
                                <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">Per 5 minutes</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-icon">
                                <i class="fas fa-database"></i>
                            </div>
                            <div>
                                <div class="card-title">Database Management</div>
                                <div class="card-subtitle">Backup and maintenance</div>
                            </div>
                        </div>
                        
                        <div style="margin-top: 1.5rem;">
                            <button onclick="createBackup()" class="btn btn-primary" style="width: 100%; margin-bottom: 1rem;">
                                <i class="fas fa-download"></i>
                                <span>Create Backup</span>
                            </button>
                            
                            <div style="padding: 1rem; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: var(--radius-md);">
                                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                                    <i class="fas fa-info-circle" style="color: var(--warning);"></i>
                                    <span style="font-weight: 600; font-size: 0.875rem;">Backup Info</span>
                                </div>
                                <p style="font-size: 0.75rem; color: var(--text-muted);">
                                    Regular backups are recommended to prevent data loss. Backups are saved to the backups/ directory.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </main>
</div>

<script>
    // Admin Page Navigation
    function switchAdminPage(event, pageName) {
        if (event) event.preventDefault();
        
        document.querySelectorAll('.page-content').forEach(page => {
            page.style.display = 'none';
            page.classList.remove('active');
        });
        
        const targetPage = document.getElementById('admin-page-' + pageName);
        if (targetPage) {
            targetPage.style.display = 'block';
            targetPage.classList.add('active');
        }
        
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        const activeLink = document.querySelector(`[data-page="${pageName}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
        
        const titles = {
            'dashboard': 'Admin Dashboard',
            'analytics': 'System Analytics',
            'users': 'Users Management',
            'keys': 'License Keys',
            'logs': 'Activity Logs',
            'settings': 'System Settings'
        };
        document.getElementById('adminPageTitle').textContent = titles[pageName] || 'Admin Panel';
        
        history.pushState({page: pageName}, '', '/admin/' + (pageName === 'dashboard' ? '' : pageName));
    }
    
    // Mark banned users
    document.addEventListener('DOMContentLoaded', function() {
        const blacklistedIds = {{ blacklisted|map(attribute='discord_id')|list|tojson }};
        
        document.querySelectorAll('[data-user-id]').forEach(row => {
            const userId = row.getAttribute('data-user-id');
            const statusBadge = row.querySelector('.user-status-admin');
            
            if (statusBadge && blacklistedIds.includes(userId)) {
                statusBadge.className = 'badge badge-error user-status-admin';
                statusBadge.innerHTML = '<i class="fas fa-ban"></i> Banned';
            }
        });
    });
    
    // Search users
    function searchUsersAdmin() {
        const input = document.getElementById('userSearchAdmin');
        const filter = input.value.toUpperCase();
        const table = document.getElementById('usersTableAdmin');
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
    
    // Generate keys
    async function generateKeys() {
        const count = prompt('How many keys to generate? (1-25):', '5');
        if (!count) return;
        
        const num = parseInt(count);
        if (isNaN(num) || num < 1 || num > 25) {
            alert('❌ Invalid count (must be 1-25)');
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
            alert('❌ Connection error');
        }
    }
    
    // Whitelist user
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
                alert(`✅ User whitelisted!\\nDiscord ID: ${discordId}\\nLicense Key: ${data.key}`);
                location.reload();
            } else {
                alert('❌ ' + data.error);
            }
        } catch (error) {
            alert('❌ Failed to whitelist user');
        }
    }
    
    // Manage user
    async function manageUser(discordId) {
        const action = prompt(`Manage user: ${discordId}\\n\\n1 - Reset HWID\\n2 - Ban User\\n3 - Unban User\\n4 - Remove User\\n\\nEnter choice:`);
        
        if (action === '1') {
            if (!confirm(`Reset HWID for ${discordId}?`)) return;
            
            try {
                const response = await fetch('/api/admin/reset-hwid', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({discord_id: discordId})
                });
                
                const data = await response.json();
                alert(data.success ? '✅ HWID reset successfully!' : '❌ Failed to reset HWID');
                if (data.success) location.reload();
            } catch (error) {
                alert('❌ Error resetting HWID');
            }
        } else if (action === '2' || action === '3') {
            const reason = action === '2' ? (prompt('Ban reason:') || 'No reason provided') : 'Unbanned by admin';
            
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
                alert('❌ Error updating user status');
            }
        } else if (action === '4') {
            if (!confirm(`Permanently remove ${discordId}? This cannot be undone!`)) return;
            
            try {
                const response = await fetch('/api/admin/unwhitelist', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({discord_id: discordId})
                });
                
                const data = await response.json();
                alert(data.success ? '✅ User removed!' : '❌ Failed to remove user');
                if (data.success) location.reload();
            } catch (error) {
                alert('❌ Error removing user');
            }
        }
    }
    
    // Create backup
    async function createBackup() {
        if (!confirm('Create database backup?')) return;
        
        try {
            const response = await fetch('/api/admin/backup', {
                method: 'POST'
            });
            
            const data = await response.json();
            alert(data.success ? `✅ Backup created successfully!\\nPath: ${data.path}` : '❌ ' + data.error);
        } catch (error) {
            alert('❌ Failed to create backup');
        }
    }
    
    // Copy text
    async function copyText(text) {
        await navigator.clipboard.writeText(text);
        alert('✅ Copied to clipboard!');
    }
    
    // Delete key
    async function deleteKey(key) {
        if (!confirm(`Delete key: ${key}?`)) return;
        alert('⚠️ Key deletion feature coming soon!');
    }
    
    // Handle browser navigation
    window.addEventListener('popstate', function(event) {
        if (event.state && event.state.page) {
            switchAdminPage(null, event.state.page);
        }
    });
</script>
""")

# ==============================================================================
# 📦 COMPLETE TEMPLATES DICTIONARY
# ==============================================================================

TEMPLATES = {
    'landing': LANDING_PAGE,
    'login': LOGIN_PAGE,
    'dashboard': DASHBOARD_PAGE,
    'admin': ADMIN_PAGE,
}

# Export all templates
__all__ = ['TEMPLATES', 'LANDING_PAGE', 'LOGIN_PAGE', 'DASHBOARD_PAGE', 'ADMIN_PAGE']
