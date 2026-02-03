from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import io
import asyncio
import logging
import re
import secrets
import string
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from contextlib import asynccontextmanager
from datetime import datetime, UTC
from typing import List, Optional, Dict, Any

import discord
from discord.ext import commands
from discord import app_commands

from config import Config
from database import db
from website_server import run_server
from bot_api_client import BananaAPI
from components_v2 import patch_components_v2, ComponentsV2Config

# Enable Components v2 for modern UI
patch_components_v2()
ComponentsV2Config.enable()

logging.basicConfig(
    level=logging.DEBUG if getattr(Config, "DEBUG", True) else logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("banana_hub_bot")
START_TIME = time.time()

DEV_MODE = getattr(Config, "DEBUG", "localhost" in getattr(Config, "WEBSITE_URL", ""))
IS_LOCALHOST = "localhost" in getattr(Config, "WEBSITE_URL", "")

if DEV_MODE:
    log.info("🔧 Running in DEVELOPMENT mode")
    log.info(f"📍 Website: {Config.WEBSITE_URL}")
else:
    log.info("🚀 Running in PRODUCTION mode")

bot_api = BananaAPI(Config.WEBSITE_URL, Config.ADMIN_API_KEY)

# ==============================================================================
# 🔑 REDEMPTION SESSION TRACKING
# ==============================================================================

# Active redemption sessions: {discord_id: {step, key, email, verified_email, username}}
# Steps: 1=waiting_key, 2=waiting_email, 3=waiting_code, 4=waiting_username, 5=waiting_password
redemption_sessions: Dict[int, Dict[str, Any]] = {}


def generate_verification_code() -> str:
    """Generate a 6-digit verification code."""
    return ''.join(secrets.choice(string.digits) for _ in range(6))


async def send_verification_email(email: str, code: str) -> bool:
    """Send verification email with code. Returns True if successful."""
    smtp_host = getattr(Config, 'SMTP_HOST', '')
    smtp_port = getattr(Config, 'SMTP_PORT', 587)
    smtp_user = getattr(Config, 'SMTP_USER', '')
    # Handle spaces in app passwords (common copy-paste issue)
    smtp_pass = getattr(Config, 'SMTP_PASSWORD', '').replace(' ', '')
    smtp_from = getattr(Config, 'SMTP_FROM', 'noreply@bananahub.com')
    
    # In DEV mode without SMTP, log code and return success
    if DEV_MODE and not smtp_pass:
        log.info(f"📧 [DEV] Email verification code for {email}: {code}")
        return True
    
    if not smtp_pass:
        log.warning("📧 SMTP password not configured, skipping email send")
        return False

    # Ensure we have a user, default to from address if user is missing
    if not smtp_user:
        # Extract email if format is "Name <email@domain.com>"
        match = re.search(r'<(.+?)>', smtp_from)
        smtp_user = match.group(1) if match else smtp_from
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🍌 Banana Hub - Email Verification Code'
        msg['From'] = smtp_from
        msg['To'] = email
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #0A0E1A; color: white; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background: #141824; padding: 30px; border-radius: 12px;">
                <h1 style="color: #FACC15; text-align: center;">🍌 Banana Hub</h1>
                <h2 style="text-align: center;">Email Verification</h2>
                <p style="text-align: center; font-size: 18px;">Your verification code is:</p>
                <div style="background: #1F2937; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                    <span style="font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #FACC15;">{code}</span>
                </div>
                <p style="text-align: center; color: #9CA3AF;">This code expires in 10 minutes.</p>
                <p style="text-align: center; color: #6B7280; font-size: 12px;">If you didn't request this, please ignore this email.</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Run SMTP in thread to not block
        def send_email():
            try:
                # Extract pure email for envelope sender
                envelope_from = smtp_from
                match = re.search(r'<(.+?)>', smtp_from)
                if match:
                    envelope_from = match.group(1)

                # 10 second timeout for SMTP
                if smtp_port == 465:
                    # Use SSL for port 465
                    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                        server.login(smtp_user, smtp_pass)
                        server.sendmail(envelope_from, email, msg.as_string())
                else:
                    # Use STARTTLS for port 587
                    with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                        server.starttls()
                        server.login(smtp_user, smtp_pass)
                        server.sendmail(envelope_from, email, msg.as_string())

                log.info(f"📧 Verification email sent to: {email}")
                return True
            except Exception as e:
                log.error(f"📧 Failed to send email: {e}")
                return False
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, send_email)
        
    except Exception as e:
        log.error(f"📧 Email error: {e}")
        return False


def validate_email(email: str) -> bool:
    """Basic email validation."""
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()))


def validate_username(username: str) -> bool:
    """Validate username: 3-20 chars, alphanumeric and underscore only."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username.strip()))


def validate_password(password: str) -> bool:
    """Validate password: at least 6 characters."""
    return len(password) >= 6


def generate_key(length: int = 12) -> str:
    alphabet = string.ascii_uppercase + string.digits
    part1 = "".join(secrets.choice(alphabet) for _ in range(3))
    part2 = "".join(secrets.choice(alphabet) for _ in range(3))
    part3 = "".join(secrets.choice(alphabet) for _ in range(3))
    return f"BANANA-{part1}-{part2}-{part3}"


def validate_discord_id(discord_id: str) -> bool:
    return bool(re.match(r'^\d{17,20}$', str(discord_id)))


def validate_key_format(key: str) -> bool:
    return bool(re.match(r'^BANANA-[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{3}$', key.strip().upper()))


def chunk_text(text: str, size: int = 1900) -> List[str]:
    return [text[i:i + size] for i in range(0, len(text), size)]


def create_embed(
    title: str,
    description: str = "",
    color: discord.Color = None,
    **kwargs
) -> discord.Embed:
    color = color or getattr(Config, "EMBED_COLOR", discord.Color.gold())
    embed = discord.Embed(
        title=f"🍌 {title}",
        description=description,
        color=color,
        timestamp=datetime.now(UTC)
    )
    
    footer_text = "Banana Hub Enterprise"
    if DEV_MODE:
        footer_text += " [DEV]"
    
    icon_url = getattr(Config, "ICON_URL", None)
    embed.set_footer(
        text=footer_text,
        icon_url=icon_url if icon_url and not DEV_MODE else None
    )
    
    return embed


async def is_admin(interaction: discord.Interaction, bot: commands.Bot) -> bool:
    try:
        app_info = await bot.application_info()
        if interaction.user.id == app_info.owner.id:
            return True
        
        if hasattr(Config, "OWNER_ID") and interaction.user.id == Config.OWNER_ID:
            return True
        
        if hasattr(Config, "ADMIN_IDS") and interaction.user.id in Config.ADMIN_IDS:
            return True
        
        if interaction.guild:
            member = interaction.guild.get_member(interaction.user.id)
            if member:
                if member.guild_permissions.administrator:
                    return True
                
                admin_role = discord.utils.get(member.roles, name="Banana Hub Admin")
                if admin_role:
                    return True
                
    except Exception as e:
        log.error(f"Error checking admin permissions: {e}")
    
    return False


@asynccontextmanager
async def safe_db_operation(operation_name: str):
    try:
        log.debug(f"Starting DB operation: {operation_name}")
        yield
        log.debug(f"Completed DB operation: {operation_name}")
    except Exception as e:
        log.error(f"DB operation '{operation_name}' failed: {e}", exc_info=True)
        raise


def format_uptime(seconds: int) -> str:
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    
    return " ".join(parts)


class UserPanelView(discord.ui.View):
    def __init__(self, user_id: int, has_key: bool):
        super().__init__(timeout=300)
        self.user_id = user_id
        
        if not IS_LOCALHOST or "ngrok" in Config.WEBSITE_URL:
            web_btn = discord.ui.Button(
                label="Web Panel",
                style=discord.ButtonStyle.link,
                url=f"{Config.WEBSITE_URL}/login",
                emoji="🌐"
            )
            self.add_item(web_btn)
        
        script_btn = discord.ui.Button(
            label="Script URL",
            style=discord.ButtonStyle.link,
            url=f"{Config.BASE_URL}/script.lua",
            emoji="📜"
        )
        self.add_item(script_btn)
    
    @discord.ui.button(label="Get Loader", style=discord.ButtonStyle.primary, emoji="📋", row=1)
    async def get_loader(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This button is not for you!", ephemeral=True)
            return
        
        user_data = db.get_user(interaction.user.id)
        if not user_data or not user_data.get("key"):
            embed = create_embed("❌ No License", "You don't have an active license.", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        key = user_data["key"]
        uid = str(interaction.user.id)
        
        loader = (
            f'local USER_ID = "{uid}"\n'
            f'local KEY = "{key}"\n'
            f'local BASE_URL = "{Config.BASE_URL}"\n\n'
            f'local function auth()\n'
            f'    local s, r = pcall(function()\n'
            f'        return game:HttpGet(BASE_URL .. "/api/auth?user_id=" .. USER_ID .. "&key=" .. KEY)\n'
            f'    end)\n'
            f'    \n'
            f'    if s then\n'
            f'        local d = game:GetService("HttpService"):JSONDecode(r)\n'
            f'        if d.success and d.authenticated then\n'
            f'            loadstring(game:HttpGet(BASE_URL .. "/main.lua?user_id=" .. USER_ID .. "&key=" .. KEY))()\n'
            f'        else\n'
            f'            warn("Auth failed: " .. (d.message or "Unknown"))\n'
            f'        end\n'
            f'    end\n'
            f'end\n\n'
            f'auth()'
        )
        
        try:
            dm_embed = create_embed("Your Loader Script", "Copy and paste this into your executor:")
            dm_embed.add_field(name="📋 Loader Code", value=f"``````", inline=False)
            dm_embed.add_field(name="⚠️ Security", value="Keep your key private!", inline=False)
            
            await interaction.user.send(embed=dm_embed)
            await interaction.response.send_message("✅ Loader sent to your DMs!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"``````\n⚠️ Enable DMs for future requests.", ephemeral=True)
    
    @discord.ui.button(label="Reset HWID", style=discord.ButtonStyle.danger, emoji="🔄", row=1)
    async def reset_hwid_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This button is not for you!", ephemeral=True)
            return
        
        success = db.reset_hwid(interaction.user.id)
        if success:
            db.log_event("hwid_reset", str(interaction.user.id), None, "Button reset")
            embed = create_embed("✅ HWID Reset", "Your hardware ID has been reset!", discord.Color.green())
        else:
            embed = create_embed("❌ Failed", "Could not reset HWID.", discord.Color.red())
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="My Info", style=discord.ButtonStyle.secondary, emoji="ℹ️", row=2)
    async def my_info_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This button is not for you!", ephemeral=True)
            return
        
        user = db.get_user(interaction.user.id)
        is_banned = db.is_blacklisted(interaction.user.id)
        
        embed_color = discord.Color.red() if is_banned else discord.Color.green()
        embed = create_embed("Your Account Info", "", embed_color)
        
        if user:
            embed.add_field(name="🔑 Key", value=f"||`{user.get('key', 'None')}`||", inline=False)
            embed.add_field(name="💻 HWID", value=user.get("hwid") or "Not set", inline=True)
            embed.add_field(name="📅 Joined", value=user.get("joined_at") or "Unknown", inline=True)
            embed.add_field(name="🕒 Last Login", value=user.get("last_login") or "Never", inline=True)
        
        status = "🔴 BLACKLISTED" if is_banned else "🟢 Active"
        embed.add_field(name="Status", value=status, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.secondary, emoji="🔄", row=2)
    async def refresh_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This button is not for you!", ephemeral=True)
            return
        
        await interaction.response.send_message("🔄 Refreshing panel...", ephemeral=True)


class AdminPanelView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=300)
        self.bot = bot
    
    @discord.ui.button(label="Generate Key", style=discord.ButtonStyle.success, emoji="🔑", row=0)
    async def gen_key_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        key = generate_key()
        if db.generate_key_entry(key, interaction.user.id):
            embed = create_embed("✅ Key Generated", f"``````", discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("❌ Failed to generate key!", ephemeral=True)
    
    @discord.ui.button(label="View Stats", style=discord.ButtonStyle.primary, emoji="📊", row=0)
    async def view_stats_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            result = await bot_api.get_stats()
            if result.get('success'):
                stats = result['stats']
                uptime = format_uptime(int(time.time() - self.bot.start_time))
                
                embed = create_embed("System Statistics")
                embed.add_field(name="⏱️ Uptime", value=f"`{uptime}`", inline=False)
                embed.add_field(name="👥 Users", value=f"`{stats.get('total_users', 0)}`", inline=True)
                embed.add_field(name="🔑 Keys", value=f"`{stats.get('available_keys', 0)}`", inline=True)
                embed.add_field(name="📈 Logins", value=f"`{stats.get('total_logins', 0)}`", inline=True)
                
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(f"❌ {result.get('error')}", ephemeral=True)
        except Exception as e:
            log.error(f"Stats error: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error loading stats: {str(e)[:100]}", ephemeral=True)
    
    @discord.ui.button(label="Backup DB", style=discord.ButtonStyle.secondary, emoji="💾", row=1)
    async def backup_db_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            backup_path = db.create_backup()
            embed = create_embed("✅ Backup Created", f"Database backed up to:\n`{backup_path}`", discord.Color.green())
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Backup failed: {e}", ephemeral=True)
    
    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.secondary, emoji="🔄", row=1)
    async def refresh_admin_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.send_message("🔄 Admin panel refreshed!", ephemeral=True)


class BananaBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = False
        
        super().__init__(
            command_prefix=getattr(Config, "PREFIX", "!"),
            intents=intents,
            help_command=None,
        )
        
        self.start_time = START_TIME
        self.synced = False
        self.version = "2.1.0"
        self.admin_role_name = "Banana Hub Admin"
        self.hwid_reset_cooldown = 300

    async def setup_hook(self) -> None:
        log.info("⚙️ Running setup hook...")
        
        self.tree.error(self.on_app_command_error)
        
        try:
            await self.add_cog(UserCog(self))
            log.info("✅ Loaded UserCog")
            
            await self.add_cog(AdminCog(self))
            log.info("✅ Loaded AdminCog")
            
            await self.add_cog(UtilityCog(self))
            log.info("✅ Loaded UtilityCog")
            
        except Exception as e:
            log.error(f"❌ Failed to load cogs: {e}", exc_info=True)
            raise
        
        await self.sync_commands()

    async def sync_commands(self) -> None:
        if self.synced:
            return
        
        try:
            if hasattr(Config, "GUILD_ID") and Config.GUILD_ID:
                guild = discord.Object(id=int(Config.GUILD_ID))
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                log.info(f"✅ Synced {len(synced)} commands to guild {Config.GUILD_ID}")
            else:
                synced = await self.tree.sync()
                log.info(f"✅ Synced {len(synced)} commands globally")
            
            log.info(f"Commands: {', '.join([cmd.name for cmd in synced])}")
            self.synced = True
            
        except Exception as e:
            log.error(f"❌ Command sync failed: {e}", exc_info=True)

    async def on_ready(self) -> None:
        assert self.user is not None
        
        log.info("=" * 60)
        log.info(f"🍌 BOT READY")
        log.info(f"Username: {self.user} (ID: {self.user.id})")
        log.info(f"Guilds: {len(self.guilds)}")
        log.info(f"Version: {self.version}")
        log.info("=" * 60)
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | /panel"
            ),
            status=discord.Status.online
        )
        
        for guild in self.guilds:
            await self.setup_admin_role(guild)

    async def on_guild_join(self, guild: discord.Guild) -> None:
        log.info(f"📥 Joined guild: {guild.name} (ID: {guild.id})")
        await self.setup_admin_role(guild)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | /panel"
            )
        )

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        log.info(f"📤 Left guild: {guild.name}")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | /panel"
            )
        )

    async def on_message(self, message: discord.Message) -> None:
        """Handle DM messages for redemption flow."""
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Only handle DMs
        if not isinstance(message.channel, discord.DMChannel):
            return
        
        user_id = message.author.id
        
        # Check if user has an active redemption session
        if user_id not in redemption_sessions:
            return
        
        session = redemption_sessions[user_id]
        content = message.content.strip()
        
        # Check for timeout (30 minutes)
        if time.time() - session.get('started_at', 0) > 1800:
            del redemption_sessions[user_id]
            embed = create_embed(
                "⏰ Session Expired",
                "Your redemption session expired. Use `/redeem` to start again.",
                discord.Color.red()
            )
            await message.channel.send(embed=embed)
            return
        
        # Handle cancel
        if content.lower() == 'cancel':
            del redemption_sessions[user_id]
            embed = create_embed(
                "❌ Cancelled",
                "Redemption process cancelled. Use `/redeem` to start again.",
                discord.Color.red()
            )
            await message.channel.send(embed=embed)
            return
        
        step = session.get('step', 1)
        
        try:
            if step == 1:
                # Waiting for key
                key_value = content.upper()
                
                if not validate_key_format(key_value):
                    embed = create_embed(
                        "❌ Invalid Format",
                        "That doesn't look right. Keys must be: `BANANA-XXX-XXX-XXX`\n\n**Please try again:**",
                        discord.Color.red()
                    )
                    await message.channel.send(embed=embed)
                    return
                
                # Check key availability
                if not db.check_key_available(key_value):
                    embed = create_embed(
                        "❌ Key Unavailable",
                        "This key is invalid, already used, or expired.\n\n**Please try a different key:**",
                        discord.Color.red()
                    )
                    await message.channel.send(embed=embed)
                    return
                
                # Key is valid! Move to step 4 (Skip email)
                session['key'] = key_value
                session['step'] = 4
                session['verified_email'] = f"{user_id}@no-email.local"
                
                embed = create_embed(
                    "✅ Key Verified!",
                    f"Key `{key_value}` is valid!\n\n**👤 Step 2/3: Choose Username**\n\nPick a username for your account.\n\n*3-20 characters, letters, numbers, and underscores only.*",
                    discord.Color.green()
                )
                await message.channel.send(embed=embed)
            
            elif step == 2:
                # Waiting for email
                email = content.lower().strip()
                
                if not validate_email(email):
                    embed = create_embed(
                        "❌ Invalid Email",
                        "That doesn't look like a valid email address.\n\n**Please try again:**",
                        discord.Color.red()
                    )
                    await message.channel.send(embed=embed)
                    return
                
                # Generate and send verification code
                code = generate_verification_code()
                
                # Store in database
                db.store_email_code(user_id, email, code)
                
                # Send email
                email_sent = await send_verification_email(email, code)
                
                session['email'] = email
                session['step'] = 3
                
                if email_sent:
                    embed = create_embed(
                        "📧 Verification Code Sent!",
                        f"We've sent a **6-digit code** to `{email}`\n\n**🔢 Step 3/5: Verify Email**\n\nPlease send the code now.\n\n*Check your spam folder if you don't see it!*",
                        discord.Color.blue()
                    )
                    if DEV_MODE and not getattr(Config, 'SMTP_USER', ''):
                        embed.add_field(
                            name="🔧 Dev Mode",
                            value=f"Check console for code (SMTP not configured)",
                            inline=False
                        )
                else:
                    # Email failed but we can continue in dev mode
                    if DEV_MODE:
                        embed = create_embed(
                            "📧 Verification Code",
                            f"**🔢 Step 3/5: Verify Email**\n\nCheck the console for your code (email not configured).",
                            discord.Color.orange()
                        )
                    else:
                        embed = create_embed(
                            "❌ Email Failed",
                            "Couldn't send verification email. Please try again or use a different email.",
                            discord.Color.red()
                        )
                        session['step'] = 2
                
                await message.channel.send(embed=embed)
            
            elif step == 3:
                # Waiting for verification code
                code = content.strip()
                
                # Verify code
                verified_email = db.verify_email_code(user_id, code)
                
                if not verified_email:
                    embed = create_embed(
                        "❌ Invalid Code",
                        "That code is incorrect or expired.\n\n**Please try again:**",
                        discord.Color.red()
                    )
                    await message.channel.send(embed=embed)
                    return
                
                # Email verified!
                session['verified_email'] = verified_email
                session['step'] = 4
                
                embed = create_embed(
                    "✅ Email Verified!",
                    f"Email `{verified_email}` confirmed!\n\n**👤 Step 4/5: Choose Username**\n\nPick a username for your account.\n\n*3-20 characters, letters, numbers, and underscores only.*",
                    discord.Color.green()
                )
                await message.channel.send(embed=embed)
            
            elif step == 4:
                # Waiting for username
                username = content.strip()
                
                if not validate_username(username):
                    embed = create_embed(
                        "❌ Invalid Username",
                        "Username must be 3-20 characters.\nOnly letters, numbers, and underscores allowed.\n\n**Please try again:**",
                        discord.Color.red()
                    )
                    await message.channel.send(embed=embed)
                    return
                
                # Check availability
                if not db.check_username_available(username):
                    embed = create_embed(
                        "❌ Username Taken",
                        f"`{username}` is already taken.\n\n**Please choose a different username:**",
                        discord.Color.red()
                    )
                    await message.channel.send(embed=embed)
                    return
                
                # Username is good!
                session['username'] = username
                session['step'] = 5
                
                embed = create_embed(
                    "✅ Username Available!",
                    f"Username `{username}` is yours!\n\n**🔒 Step 3/3: Set Password**\n\nChoose a secure password.\n\n*Minimum 6 characters.*",
                    discord.Color.green()
                )
                await message.channel.send(embed=embed)
            
            elif step == 5:
                # Waiting for password
                password = content  # Don't strip, preserve spaces
                
                if not validate_password(password):
                    embed = create_embed(
                        "❌ Password Too Short",
                        "Password must be at least 6 characters.\n\n**Please try again:**",
                        discord.Color.red()
                    )
                    await message.channel.send(embed=embed)
                    return
                
                # All steps complete! Create the account
                key = session['key']
                email = session['verified_email']
                username = session['username']
                
                # Register user with key (if new user)
                existing_user = db.get_user(user_id)
                if not existing_user or not existing_user.get('key'):
                    db.register_user(user_id, key)
                    db.mark_key_redeemed(key, user_id)
                
                # Create account
                success = db.create_account(user_id, email, username, password)
                
                if success:
                    db.log_event("account_created", str(user_id), None, f"Username: {username}")
                    
                    embed = create_embed(
                        "🎉 Account Created!",
                        f"Welcome to Banana Hub!\n\n"
                        f"**Username:** `{username}`\n"
                        f"**Email:** `{email}`\n\n"
                        f"You can now login at:\n{Config.WEBSITE_URL}/login\n\n"
                        f"Use your **username** and **password** to login.",
                        discord.Color.green()
                    )
                    embed.add_field(
                        name="🚀 Next Steps",
                        value="• Use `/panel` to access dashboard\n• Get your loader script\n• Start using Banana Hub!",
                        inline=False
                    )
                    
                    log.info(f"✅ Account created: {username} (Discord: {user_id})")
                else:
                    embed = create_embed(
                        "❌ Account Creation Failed",
                        "Something went wrong. Please try `/redeem` again.",
                        discord.Color.red()
                    )
                
                # Clean up session
                del redemption_sessions[user_id]
                await message.channel.send(embed=embed)
        
        except Exception as e:
            log.error(f"Redemption flow error for {user_id}: {e}", exc_info=True)
            embed = create_embed(
                "❌ Error",
                "Something went wrong. Please try `/redeem` again.",
                discord.Color.red()
            )
            if user_id in redemption_sessions:
                del redemption_sessions[user_id]
            await message.channel.send(embed=embed)

    async def setup_admin_role(self, guild: discord.Guild) -> Optional[discord.Role]:
        try:
            existing_role = discord.utils.get(guild.roles, name=self.admin_role_name)
            if existing_role:
                return existing_role
            
            admin_role = await guild.create_role(
                name=self.admin_role_name,
                color=discord.Color.gold(),
                permissions=discord.Permissions(administrator=True),
                hoist=True,
                mentionable=True,
                reason="Banana Hub Admin Role"
            )
            
            log.info(f"✅ Created admin role in {guild.name}")
            
            try:
                owner = guild.get_member(Config.OWNER_ID)
                if owner:
                    await owner.add_roles(admin_role)
            except:
                pass
            
            if guild.system_channel:
                try:
                    embed = discord.Embed(
                        title="🍌 Banana Hub Setup!",
                        description=f"Admin role created: {admin_role.mention}\n\nUse `/help` to get started!",
                        color=discord.Color.gold()
                    )
                    await guild.system_channel.send(embed=embed)
                except:
                    pass
            
            return admin_role
            
        except Exception as e:
            log.error(f"Error setting up admin role: {e}")
            return None

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = create_embed(
                "⏱️ Cooldown",
                f"Wait **{error.retry_after:.1f}s** before using this again.",
                discord.Color.orange()
            )
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                pass
        elif isinstance(error, app_commands.MissingPermissions):
            embed = create_embed("❌ No Permission", "You can't use this command.", discord.Color.red())
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                pass
        else:
            log.error(f"Command error: {error}", exc_info=True)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"❌ **An error occurred:** `{str(error)}`", ephemeral=True)
                else:
                    await interaction.followup.send(f"❌ **An error occurred:** `{str(error)}`", ephemeral=True)
            except:
                pass


class UserCog(commands.Cog, name="User"):
    def __init__(self, bot: BananaBot) -> None:
        self.bot = bot

    @app_commands.command(name="redeem", description="Redeem your Banana Hub license key (starts DM flow)")
    async def redeem(self, interaction: discord.Interaction):
        """Start the 5-step redemption process via DM."""
        try:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
        except:
            pass
        
        user_id = interaction.user.id
        
        # Check if already has an account
        existing_account = db.get_account_by_discord(user_id)
        if existing_account:
            embed = create_embed(
                "⚠️ Already Registered",
                f"You already have an account!\n\n**Username:** `{existing_account['username']}`\n\nUse the web panel to login with your username and password.",
                discord.Color.orange()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Check if already has a key (legacy user)
        existing_user = db.get_user(user_id)
        if existing_user and existing_user.get("key"):
            # Legacy user - they need to complete account setup
            embed = create_embed(
                "🔄 Account Setup Required",
                "You have a key but need to set up your account with username/password.\n\n**Check your DMs to continue!**",
                discord.Color.blue()
            )
            # Start them at step 4 (username) since they already have a key
            redemption_sessions[user_id] = {
                'step': 4,
                'key': existing_user['key'],
                'email': None,
                'verified_email': f"{user_id}@no-email.local",
                'username': None,
                'started_at': time.time()
            }
        else:
            # New user - start from step 1
            embed = create_embed(
                "🍌 Key Redemption",
                "Let's set up your Banana Hub account!\n\n**Check your DMs to continue!**\n\nI'll walk you through a quick 3-step process.",
                discord.Color.gold()
            )
            redemption_sessions[user_id] = {
                'step': 1,
                'key': None,
                'email': None,
                'verified_email': None,
                'username': None,
                'started_at': time.time()
            }
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Send DM to start the flow
        try:
            dm_channel = await interaction.user.create_dm()
            
            session = redemption_sessions[user_id]
            if session['step'] == 1:
                dm_embed = create_embed(
                    "🔑 Step 1/3: License Key",
                    "Welcome! Let's get you set up.\n\n**Please send your license key now.**\n\nFormat: `BANANA-XXX-XXX-XXX`",
                    discord.Color.gold()
                )
            elif session['step'] == 4:
                dm_embed = create_embed(
                    "👤 Step 2/3: Choose Username",
                    f"Your key: `{session['key']}`\n\n**Please send your desired username.**\n\n*3-20 characters, letters, numbers, and underscores only.*",
                    discord.Color.gold()
                )
            else:
                # Fallback for unexpected state
                dm_embed = create_embed(
                    "❓ Continue Setup",
                     "Please continue your setup.",
                     discord.Color.blue()
                )
            
            dm_embed.set_footer(text="Type 'cancel' to stop the process.")
            await dm_channel.send(embed=dm_embed)
            
        except discord.Forbidden:
            # Can't DM user
            if user_id in redemption_sessions:
                del redemption_sessions[user_id]
            
            error_embed = create_embed(
                "❌ Can't Send DM",
                "Please enable DMs from server members and try again!",
                discord.Color.red()
            )
            try:
                await interaction.followup.send(embed=error_embed, ephemeral=True)
            except:
                pass


    @app_commands.command(name="panel", description="Access your Banana Hub dashboard")
    async def panel(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        user = db.get_user(interaction.user.id)
        
        embed = create_embed("Your Dashboard")
        
        has_key = user and user.get("key")
        has_hwid = user and user.get("hwid")
        is_banned = db.is_blacklisted(interaction.user.id)
        
        status_emoji = "🔴" if is_banned else ("🟢" if has_key else "🟡")
        
        embed.add_field(
            name=f"{status_emoji} Status",
            value=(
                f"**License:** {'✅ Active' if has_key else '❌ None'}\n"
                f"**HWID:** {'✅ Set' if has_hwid else '⚠️ Not Set'}\n"
                f"**Access:** {'🔴 BANNED' if is_banned else '🟢 Active'}"
            ),
            inline=False
        )
        
        if has_key:
            embed.add_field(name="🔑 License", value=f"||`{user['key']}`||", inline=False)
            
            try:
                analytics = db.get_user_analytics(interaction.user.id)
                embed.add_field(name="📊 Logins", value=f"`{analytics['login_count']}`", inline=True)
            except:
                pass
        else:
            embed.add_field(
                name="⚠️ No License",
                value="Use `/redeem <key>` to activate your license.",
                inline=False
            )
        
        if not IS_LOCALHOST:
            embed.add_field(
                name="🌐 Web Access",
                value=f"[Login to Web Panel]({Config.WEBSITE_URL}/login)",
                inline=False
            )
        
        view = UserPanelView(interaction.user.id, has_key)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="getkey", description="Get your license key via DM")
    @app_commands.checks.cooldown(1, 30, key=lambda i: i.user.id)
    async def getkey(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user = db.get_user(interaction.user.id)
        
        if not user or not user.get("key"):
            embed = create_embed("❌ No License", "Use `/redeem <key>` first.", discord.Color.red())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        key = user["key"]
        
        try:
            dm_embed = create_embed("Your License Key", f"**Key:** `{key}`\n\n⚠️ Keep this secret!")
            if not IS_LOCALHOST:
                dm_embed.add_field(name="🌐 Login", value=f"[Web Panel]({Config.WEBSITE_URL}/login)", inline=False)
            
            await interaction.user.send(embed=dm_embed)
            await interaction.followup.send("✅ Key sent to your DMs!", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(f"❌ FAILED: Please enable DMs!\n**Your Key:** ||`{key}`||", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to send DM: {str(e)}", ephemeral=True)

    @app_commands.command(name="reset-hwid", description="Reset your hardware ID")
    @app_commands.checks.cooldown(1, 300, key=lambda i: i.user.id)
    async def reset_hwid(self, interaction: discord.Interaction):
        success = db.reset_hwid(interaction.user.id)
        
        if success:
            db.log_event("hwid_reset", str(interaction.user.id), None, "User reset")
            embed = create_embed("✅ HWID Reset", "Successfully reset your hardware ID!", discord.Color.green())
        else:
            embed = create_embed("❌ Failed", "No license found.", discord.Color.red())
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="myinfo", description="View your account information")
    async def myinfo(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user = db.get_user(interaction.user.id)
        is_banned = db.is_blacklisted(interaction.user.id)
        
        embed_color = discord.Color.red() if is_banned else (discord.Color.green() if user else discord.Color.orange())
        embed = create_embed("Your Account", "", embed_color)
        
        embed.add_field(name="👤 User", value=f"{interaction.user.mention}\nID: `{interaction.user.id}`", inline=False)
        
        if user:
            embed.add_field(name="🔑 Key", value=f"||`{user.get('key', 'None')}`||", inline=False)
            embed.add_field(name="💻 HWID", value=user.get("hwid") or "Not set", inline=True)
            embed.add_field(name="📅 Joined", value=user.get("joined_at") or "Unknown", inline=True)
            embed.add_field(name="🕒 Last Login", value=user.get("last_login") or "Never", inline=True)
            
            try:
                analytics = db.get_user_analytics(interaction.user.id)
                embed.add_field(
                    name="📊 Stats", 
                    value=f"Logins: `{analytics['login_count']}`\nResets: `{analytics['reset_count']}`", 
                    inline=False
                )
            except:
                pass
        else:
            embed.add_field(name="⚠️ No License", value="Use `/redeem` to activate.", inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="profile", description="View your Banana Hub profile card")
    async def profile(self, interaction: discord.Interaction):
        """Show a beautiful profile card with user stats and buttons."""
        user_data = db.get_user(interaction.user.id)
        is_banned = db.is_blacklisted(interaction.user.id)
        
        if is_banned:
            embed = create_embed("🚫 Account Suspended", "Your account has been blacklisted.", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = create_embed("Your Profile", "", discord.Color.blurple())
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        if user_data:
            status = "✅ Licensed"
            embed.add_field(name="🎫 License Status", value=status, inline=True)
            embed.add_field(name="🔑 Key", value=f"||`{user_data.get('key', 'N/A')}`||", inline=True)
            embed.add_field(name="💻 HWID", value=f"`{user_data.get('hwid', 'Not set')[:20]}...`" if user_data.get('hwid') else "Not set", inline=False)
            
            try:
                analytics = db.get_user_analytics(interaction.user.id)
                embed.add_field(name="📊 Activity", value=f"Logins: **{analytics.get('login_count', 0)}** | Resets: **{analytics.get('reset_count', 0)}**", inline=False)
            except:
                pass
        else:
            embed.add_field(name="⚠️ Not Licensed", value="Use `/redeem` to activate your account!", inline=False)
        
        # Add interactive buttons
        view = discord.ui.View(timeout=300)
        view.add_item(discord.ui.Button(label="🔄 Reset HWID", style=discord.ButtonStyle.secondary, custom_id="quick_reset_hwid"))
        view.add_item(discord.ui.Button(label="🔑 Get Key", style=discord.ButtonStyle.primary, custom_id="quick_get_key"))
        view.add_item(discord.ui.Button(label="🌐 Web Panel", style=discord.ButtonStyle.link, url=Config.WEBSITE_URL))
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="invite", description="Get the bot invite link")
    async def invite(self, interaction: discord.Interaction):
        """Generate bot invite link."""
        bot_id = self.bot.user.id if self.bot.user else "UNKNOWN"
        invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_id}&permissions=8&scope=bot%20applications.commands"
        
        embed = create_embed("Invite Banana Hub", "Add Banana Hub to your server!", discord.Color.green())
        embed.add_field(name="🔗 Invite Link", value=f"[Click Here]({invite_url})", inline=False)
        embed.add_field(name="📋 Required Permissions", value="Administrator (for full functionality)", inline=False)
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="🚀 Add to Server", style=discord.ButtonStyle.link, url=invite_url))
        view.add_item(discord.ui.Button(label="🌐 Website", style=discord.ButtonStyle.link, url=Config.WEBSITE_URL))
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="changelog", description="View recent updates and changes")
    async def changelog(self, interaction: discord.Interaction):
        """Show changelog with latest updates."""
        embed = create_embed("📝 Changelog", "Recent updates to Banana Hub")
        
        embed.add_field(
            name="🆕 v2.2.0 - Components v2 Update",
            value="• Modern UI with buttons and menus\n• Interactive profile cards\n• Enhanced admin dashboard\n• New utility commands",
            inline=False
        )
        embed.add_field(
            name="🔧 v2.1.0 - Stability Update",
            value="• Improved HWID handling\n• Better error messages\n• Fixed key redemption bugs\n• Performance optimizations",
            inline=False
        )
        embed.add_field(
            name="🚀 v2.0.0 - Major Release",
            value="• Web dashboard integration\n• API-based authentication\n• New admin commands\n• Enhanced security",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="status", description="Check Banana Hub service status")
    async def status(self, interaction: discord.Interaction):
        """Show service status."""
        await interaction.response.defer(ephemeral=True)
        
        # Check various services
        bot_latency = round(self.bot.latency * 1000)
        bot_status = "🟢 Online" if bot_latency < 500 else "🟡 Slow"
        
        try:
            result = await bot_api.get_stats()
            api_status = "🟢 Online" if result.get('success') else "🔴 Offline"
        except:
            api_status = "🔴 Offline"
        
        try:
            db.get_user(0)
            db_status = "🟢 Online"
        except:
            db_status = "🔴 Offline"
        
        embed = create_embed("🔍 Service Status", "Current status of all Banana Hub services")
        embed.add_field(name="🤖 Bot", value=f"{bot_status} ({bot_latency}ms)", inline=True)
        embed.add_field(name="🌐 API", value=api_status, inline=True)
        embed.add_field(name="💾 Database", value=db_status, inline=True)
        embed.add_field(name="🔗 Website", value=f"[{Config.WEBSITE_URL}]({Config.WEBSITE_URL})", inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="script", description="Get your personalized executor script")
    async def script(self, interaction: discord.Interaction):
        """Get the Roblox script for the user."""
        user_data = db.get_user(interaction.user.id)
        
        if not user_data:
            embed = create_embed("❌ Not Licensed", "You need to redeem a key first!\nUse `/redeem` to activate.", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if db.is_blacklisted(interaction.user.id):
            embed = create_embed("🚫 Blacklisted", "Your account has been suspended.", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        script_code = f'loadstring(game:HttpGet("{Config.WEBSITE_URL}/script.lua?user_id={interaction.user.id}&key={user_data.get("key", "")}"))()'
        
        embed = create_embed("📜 Your Script", "Copy and paste this into your executor:")
        embed.add_field(name="Script", value=f"```lua\n{script_code}\n```", inline=False)
        embed.add_field(name="⚠️ Important", value="• Never share your script\n• Script is linked to your HWID\n• Contact support if issues arise", inline=False)
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="🌐 Web Dashboard", style=discord.ButtonStyle.link, url=Config.WEBSITE_URL))
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="support", description="Get help and support information")
    async def support(self, interaction: discord.Interaction):
        """Show support information."""
        await interaction.response.defer(ephemeral=True)
        
        embed = create_embed("🆘 Support Center", "Need help? We've got you covered!")
        
        embed.add_field(name="📖 Common Issues", value="• **HWID Locked**: Use `/reset-hwid` (5min cooldown)\n• **Invalid Key**: Check format `BANANA-XXX-XXX-XXX`\n• **Script Error**: Make sure you're whitelisted", inline=False)
        embed.add_field(name="📬 Contact", value="• Use `/report` for bug reports\n• Use `/feedback` for suggestions\n• Visit our website for FAQ", inline=False)
        embed.add_field(name="🔗 Quick Links", value=f"[Website]({Config.WEBSITE_URL}) • [Dashboard]({Config.WEBSITE_URL})", inline=False)
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="📖 FAQ", style=discord.ButtonStyle.link, url=f"{Config.WEBSITE_URL}"))
        view.add_item(discord.ui.Button(label="🎫 Open Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket", disabled=True))
        
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="report", description="Report a bug or issue")
    @app_commands.describe(issue="Describe the bug or issue you encountered")
    async def report(self, interaction: discord.Interaction, issue: str):
        """Submit a bug report."""
        await interaction.response.defer(ephemeral=True)
        
        db.log_event("bug_report", str(interaction.user.id), None, issue[:500])
        
        embed = create_embed("🐛 Bug Report Submitted", "Thank you for your report!", discord.Color.green())
        embed.add_field(name="📝 Your Report", value=f"```{issue[:200]}{'...' if len(issue) > 200 else ''}```", inline=False)
        embed.add_field(name="ℹ️ Next Steps", value="Our team will review your report. Major issues may result in a fix in future updates.", inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Log to console for admins
        log.info(f"📝 Bug Report from {interaction.user} ({interaction.user.id}): {issue[:100]}")

    @app_commands.command(name="feedback", description="Send feedback or suggestions")
    @app_commands.describe(feedback="Your feedback or suggestion")
    async def feedback(self, interaction: discord.Interaction, feedback: str):
        """Submit feedback."""
        await interaction.response.defer(ephemeral=True)
        
        db.log_event("feedback", str(interaction.user.id), None, feedback[:500])
        
        embed = create_embed("💡 Feedback Received", "Thank you for your input!", discord.Color.green())
        embed.add_field(name="📝 Your Feedback", value=f"```{feedback[:200]}{'...' if len(feedback) > 200 else ''}```", inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        log.info(f"💡 Feedback from {interaction.user} ({interaction.user.id}): {feedback[:100]}")


class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot: BananaBot) -> None:
        self.bot = bot

    @app_commands.command(name="adminpanel", description="🔧 [ADMIN] Open admin control panel")
    async def adminpanel(self, interaction: discord.Interaction):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            result = await bot_api.get_stats()
            
            if result.get('success'):
                stats = result['stats']
                uptime = format_uptime(int(time.time() - self.bot.start_time))
                
                embed = create_embed("Admin Control Panel")
                embed.add_field(name="⏱️ Uptime", value=f"`{uptime}`", inline=False)
                embed.add_field(name="👥 Total Users", value=f"`{stats.get('total_users', 0)}`", inline=True)
                embed.add_field(name="🔑 Available Keys", value=f"`{stats.get('available_keys', 0)}`", inline=True)
                embed.add_field(name="📈 Total Logins", value=f"`{stats.get('total_logins', 0)}`", inline=True)
                embed.add_field(name="🚫 Blacklisted", value=f"`{stats.get('total_blacklisted', 0)}`", inline=True)
                embed.add_field(
                    name="🎛️ Quick Actions",
                    value="Use the buttons below for quick admin tasks",
                    inline=False
                )
                
                view = AdminPanelView(self.bot)
                await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            else:
                error_msg = result.get('error') or 'Server returned unknown error'
                if str(error_msg).lower() == 'none': error_msg = 'Server returned no error details'
                await interaction.followup.send(f"❌ {error_msg}", ephemeral=True)
            
        except Exception as e:
            log.error(f"Admin panel error: {e}", exc_info=True)
            embed = create_embed(
                "❌ Error Loading Admin Panel",
                f"Failed to load admin panel.\n\n**Error:** {str(e)[:200]}",
                discord.Color.red()
            )
            try:
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                pass

    @app_commands.command(name="whitelist", description="🔧 [ADMIN] Whitelist a user with auto key")
    @app_commands.describe(member="User to whitelist", send_dm="Send instructions via DM")
    async def whitelist(self, interaction: discord.Interaction, member: discord.Member, send_dm: bool = True):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        if member.bot:
            await interaction.response.send_message("❌ Can't whitelist bots!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        result = await bot_api.whitelist_user(str(member.id))
        
        if result.get('success'):
            key = result['key']
            
            dm_status = "Not sent"
            if send_dm:
                try:
                    dm_embed = create_embed(
                        "Welcome to Banana Hub!",
                        f"You've been whitelisted by **{interaction.user.name}** in **{interaction.guild.name}**!"
                    )
                    dm_embed.add_field(name="🔑 Your Key", value=f"`{key}`\n⚠️ Keep this secret!", inline=False)
                    dm_embed.add_field(
                        name="🚀 Getting Started",
                        value=(
                            "**Step 1:** Use `/panel` in the server\n"
                            "**Step 2:** Click 'Get Loader' button\n"
                            "**Step 3:** Paste into your executor\n"
                            "**Step 4:** Enjoy Banana Hub!"
                        ),
                        inline=False
                    )
                    
                    if not IS_LOCALHOST:
                        dm_embed.add_field(
                            name="🌐 Web Login",
                            value=(
                                f"[Login Here]({Config.WEBSITE_URL}/login)\n\n"
                                f"**Your User ID:** `{member.id}`\n"
                                f"**Your Key:** `{key}`"
                            ),
                            inline=False
                        )
                    
                    await member.send(embed=dm_embed)
                    dm_status = "✅ Sent"
                except discord.Forbidden:
                    dm_status = "⚠️ DMs disabled"

            embed = create_embed("✅ User Whitelisted", f"Successfully whitelisted {member.mention}")
            embed.add_field(name="🔑 Generated Key", value=f"`{key}`", inline=False)
            embed.add_field(name="📨 DM Status", value=dm_status, inline=False)
            embed.add_field(name="👤 User Info", value=f"**Name:** {member.name}\n**ID:** `{member.id}`", inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            log.info(f"✅ Whitelisted {member.id} with key {key}")
        else:
            await interaction.followup.send(f"❌ {result.get('error')}", ephemeral=True)

    @app_commands.command(name="unwhitelist", description="🔧 [ADMIN] Remove user from whitelist")
    @app_commands.describe(member="User to remove")
    async def unwhitelist(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        result = await bot_api.unwhitelist_user(str(member.id))
        
        if result.get('success'):
            embed = create_embed("✅ Removed", f"{member.mention} removed from whitelist.", discord.Color.green())
        else:
            embed = create_embed("❌ Not Found", f"{member.mention} not whitelisted.", discord.Color.red())
        
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="lookup", description="🔧 [ADMIN] Look up user information")
    @app_commands.describe(user="User to lookup (mention or ID)")
    async def lookup(self, interaction: discord.Interaction, user: str):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        discord_id = user.strip("<@!>")
        
        if not validate_discord_id(discord_id):
            await interaction.response.send_message("❌ Invalid Discord ID!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        result = await bot_api.get_user(discord_id)
        
        if result.get('success'):
            user_data = result['user']
            
            embed_color = discord.Color.red() if user_data['banned'] else discord.Color.blue()
            embed = create_embed(f"User Lookup: {discord_id}", "", embed_color)
            
            try:
                discord_user = await self.bot.fetch_user(int(discord_id))
                embed.set_thumbnail(url=discord_user.display_avatar.url)
                embed.description = f"**{discord_user.name}** ({discord_user.display_name})"
            except:
                pass
            
            embed.add_field(name="🔑 Key", value=f"`{user_data.get('key')}`", inline=False)
            embed.add_field(name="💻 HWID", value=user_data.get("hwid") or "Not set", inline=True)
            embed.add_field(name="📅 Joined", value=user_data.get("joined_at") or "Unknown", inline=True)
            embed.add_field(name="🕒 Last Login", value=user_data.get("last_login") or "Never", inline=True)
            embed.add_field(
                name="📊 Stats", 
                value=f"Logins: `{user_data['login_count']}`", 
                inline=False
            )
            
            status = "🔴 BLACKLISTED" if user_data['banned'] else "🟢 Active"
            embed.add_field(name="Status", value=status, inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = create_embed("❌ Not Found", result.get('error', 'User not found'), discord.Color.red())
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="genkey", description="🔧 [ADMIN] Generate license keys")
    @app_commands.describe(amount="Number of keys (1-25)")
    async def genkey(self, interaction: discord.Interaction, amount: int = 1):
        if not await is_admin(interaction, self.bot):
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            except:
                pass
            return

        if amount < 1 or amount > 25:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("❌ Amount must be 1-25!", ephemeral=True)
            except:
                pass
            return

        try:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
        except:
            pass
        
        result = await bot_api.generate_keys(amount)
        
        if result.get('success'):
            keys = result['keys']
            
            if len(keys) <= 5:
                keys_display = '\n'.join(f'`{k}`' for k in keys)
                embed = create_embed(
                    "✅ Keys Generated",
                    f"Created **{len(keys)}** key(s):",
                    discord.Color.green()
                )
                embed.add_field(name="Keys", value=keys_display, inline=False)
            else:
                embed = create_embed(
                    "✅ Keys Generated",
                    f"Successfully created **{len(keys)}** keys!\n\n📨 Check your DMs for the full list.",
                    discord.Color.green()
                )
            
            try:
                dm_embed = create_embed(
                    f"🔑 Generated Keys ({len(keys)})",
                    "Here are your newly generated license keys:"
                )
                
                key_chunks = [keys[i:i+10] for i in range(0, len(keys), 10)]
                
                for idx, chunk in enumerate(key_chunks):
                    chunk_text = '\n'.join(f'`{k}`' for k in chunk)
                    
                    if len(key_chunks) == 1:
                        dm_embed.add_field(name="Keys", value=chunk_text, inline=False)
                        await interaction.user.send(embed=dm_embed)
                    else:
                        chunk_embed = create_embed(
                            f"🔑 Keys (Part {idx+1}/{len(key_chunks)})",
                            chunk_text
                        )
                        await interaction.user.send(embed=chunk_embed)
                
                if len(keys) > 10:
                    key_file = io.StringIO()
                    key_file.write(f"Banana Hub License Keys - Generated by {interaction.user.name}\n")
                    key_file.write(f"Date: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
                    key_file.write(f"Total: {len(keys)} keys\n")
                    key_file.write("=" * 50 + "\n\n")
                    for i, key in enumerate(keys, 1):
                        key_file.write(f"{i}. {key}\n")
                    
                    key_file.seek(0)
                    file = discord.File(
                        fp=io.BytesIO(key_file.read().encode()),
                        filename=f"banana_keys_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.txt"
                    )
                    await interaction.user.send("📁 Keys also attached as file:", file=file)
                
                dm_sent = True
            except discord.Forbidden:
                dm_sent = False
                embed.add_field(
                    name="⚠️ DMs Disabled",
                    value="Enable DMs to receive keys privately!",
                    inline=False
                )
            except Exception as e:
                log.error(f"Error sending keys via DM: {e}")
                dm_sent = False
            
            if dm_sent and len(keys) > 5:
                embed.add_field(
                    name="📬 Keys Sent",
                    value="Full list sent to your DMs!",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            log.info(f"Generated {len(keys)} keys by admin {interaction.user.id}")
        else:
            await interaction.followup.send(f"❌ {result.get('error') or 'Unknown error'}", ephemeral=True)

    @app_commands.command(name="blacklist", description="🔧 [ADMIN] Blacklist a user")
    @app_commands.describe(member="User to blacklist", reason="Reason")
    async def blacklist(self, interaction: discord.Interaction, member: Optional[discord.Member] = None, reason: str = "No reason"):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        if not member:
            blacklist_data = db.get_blacklisted_users()
            count = len(blacklist_data)
            
            embed = create_embed("Blacklist Stats", f"**Total:** `{count}` users")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if member.bot or member.id == interaction.user.id:
            await interaction.response.send_message("❌ Invalid target!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        result = await bot_api.ban_user(str(member.id), reason)

        if result.get('success'):
            if result['banned']:
                embed = create_embed("✅ Blacklisted", f"{member.mention} blacklisted.\n**Reason:** {reason}", discord.Color.red())
            else:
                embed = create_embed("✅ Unblacklisted", f"{member.mention} removed from blacklist.", discord.Color.green())
        else:
            embed = create_embed("❌ Error", result.get('error', 'Unknown error'), discord.Color.red())
        
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="unblacklist", description="🔧 [ADMIN] Remove user from blacklist")
    @app_commands.describe(member="User to unblacklist")
    async def unblacklist(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        result = await bot_api.ban_user(str(member.id), "Unbanned by admin")
        
        if result.get('success'):
            if not result['banned']:
                embed = create_embed("✅ Unblacklisted", f"{member.mention} removed from blacklist.", discord.Color.green())
                log.info(f"✅ Unblacklisted {member.id}")
            else:
                embed = create_embed("⚠️ Already Active", f"{member.mention} is not blacklisted.", discord.Color.orange())
        else:
            embed = create_embed("❌ Error", result.get('error', 'Unknown error'), discord.Color.red())
        
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="forceresethwid", description="🔧 [ADMIN] Force reset user's HWID")
    @app_commands.describe(member="User to reset HWID for")
    async def forceresethwid(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        result = await bot_api.reset_hwid(str(member.id))
        
        if result.get('success'):
            embed = create_embed("✅ HWID Reset", f"Force reset HWID for {member.mention}", discord.Color.green())
            log.info(f"🔄 Admin {interaction.user.id} force reset HWID for {member.id}")
        else:
            embed = create_embed("❌ Failed", result.get('error', 'User not found'), discord.Color.red())
        
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="stats", description="🔧 [ADMIN] View system statistics")
    async def stats(self, interaction: discord.Interaction):
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            result = await bot_api.get_stats()
            
            if result.get('success'):
                stats = result['stats']
                uptime = format_uptime(int(time.time() - self.bot.start_time))
                latency = round(self.bot.latency * 1000)
                
                embed = create_embed("System Statistics")
                embed.add_field(name="🤖 Bot", value=f"Uptime: `{uptime}`\nGuilds: `{len(self.bot.guilds)}`\nLatency: `{latency}ms`", inline=False)
                embed.add_field(name="💾 Database", value=f"Users: `{stats.get('total_users', 0)}`\nKeys: `{stats.get('available_keys', 0)}`\nLogins: `{stats.get('total_logins', 0)}`", inline=True)
                embed.add_field(name="🚫 Security", value=f"Blacklisted: `{stats.get('total_blacklisted', 0)}`", inline=True)
                
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(f"❌ {result.get('error') or 'Unknown error'}", ephemeral=True)
        except Exception as e:
            log.error(f"Stats error: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="broadcast", description="🔧 [ADMIN] Send a message to all whitelisted users")
    @app_commands.describe(message="The message to broadcast")
    async def broadcast(self, interaction: discord.Interaction, message: str):
        """Broadcast a message to all users (logs it)."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        db.log_event("broadcast", str(interaction.user.id), None, message[:500])
        
        embed = create_embed("📢 Broadcast Sent", f"Message logged for delivery.", discord.Color.green())
        embed.add_field(name="📝 Message", value=f"```{message[:500]}```", inline=False)
        embed.add_field(name="📊 Status", value="Broadcast recorded. Users will see this on next login.", inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        log.info(f"📢 Broadcast by {interaction.user}: {message[:100]}")

    @app_commands.command(name="userlist", description="🔧 [ADMIN] View paginated user list")
    @app_commands.describe(page="Page number (default: 1)")
    async def userlist(self, interaction: discord.Interaction, page: int = 1):
        """Show paginated list of all users."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            result = await bot_api.get_all_users()
            
            if result.get('success'):
                users = result.get('users', [])
                per_page = 10
                total_pages = max(1, (len(users) + per_page - 1) // per_page)
                page = max(1, min(page, total_pages))
                
                start = (page - 1) * per_page
                end = start + per_page
                page_users = users[start:end]
                
                embed = create_embed(f"👥 User List (Page {page}/{total_pages})", f"Total: **{len(users)}** users")
                
                for i, user in enumerate(page_users, start=start+1):
                    discord_id = user.get('discord_id', 'Unknown')
                    key = user.get('key', 'N/A')[:8] + '...'
                    status = "🟢" if user.get('hwid') else "🟡"
                    embed.add_field(name=f"{i}. {status} ID: {discord_id}", value=f"Key: `{key}`", inline=True)
                
                view = discord.ui.View()
                if page > 1:
                    view.add_item(discord.ui.Button(label="⬅️ Previous", style=discord.ButtonStyle.secondary, custom_id=f"userlist_prev_{page}"))
                if page < total_pages:
                    view.add_item(discord.ui.Button(label="➡️ Next", style=discord.ButtonStyle.secondary, custom_id=f"userlist_next_{page}"))
                
                await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            else:
                await interaction.followup.send(f"❌ {result.get('error') or 'Unknown error'}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="keylist", description="🔧 [ADMIN] View available keys")
    @app_commands.describe(show_used="Also show used keys")
    async def keylist(self, interaction: discord.Interaction, show_used: bool = False):
        """Show list of available keys."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            result = await bot_api.get_stats()
            
            if result.get('success'):
                stats = result['stats']
                
                embed = create_embed("🔑 Key Statistics", "License key overview")
                embed.add_field(name="📊 Available", value=f"`{stats.get('available_keys', 0)}`", inline=True)
                embed.add_field(name="✅ Used", value=f"`{stats.get('total_users', 0)}`", inline=True)
                embed.add_field(name="📈 Total Generated", value=f"`{stats.get('available_keys', 0) + stats.get('total_users', 0)}`", inline=True)
                
                view = discord.ui.View()
                view.add_item(discord.ui.Button(label="🔑 Generate Keys", style=discord.ButtonStyle.primary, custom_id="quick_genkey"))
                view.add_item(discord.ui.Button(label="📋 Export", style=discord.ButtonStyle.secondary, custom_id="export_keys"))
                
                await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            else:
                error_msg = result.get('error') or 'Server returned unknown error'
                if str(error_msg).lower() == 'none': error_msg = 'Server returned no error details'
                await interaction.followup.send(f"❌ {error_msg}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="exportdata", description="🔧 [ADMIN] Export all data as JSON")
    async def exportdata(self, interaction: discord.Interaction):
        """Export all data as a downloadable file."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            result = await bot_api.get_stats()
            users_result = await bot_api.get_all_users()
            
            import json
            export_data = {
                "exported_at": datetime.now(UTC).isoformat(),
                "exported_by": str(interaction.user.id),
                "stats": result.get('stats', {}),
                "users": users_result.get('users', [])
            }
            
            json_str = json.dumps(export_data, indent=2)
            file = discord.File(io.BytesIO(json_str.encode()), filename=f"banana_hub_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            embed = create_embed("📦 Data Export", "Your data export is ready!", discord.Color.green())
            embed.add_field(name="📊 Stats", value=f"Users: `{len(users_result.get('users', []))}`", inline=True)
            
            await interaction.followup.send(embed=embed, file=file, ephemeral=True)
            db.log_event("data_export", str(interaction.user.id), None, "Admin exported data")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="purgekeys", description="🔧 [ADMIN] Delete unused keys")
    @app_commands.describe(confirm="Type 'CONFIRM' to proceed")
    async def purgekeys(self, interaction: discord.Interaction, confirm: str = ""):
        """Purge unused keys."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        if confirm != "CONFIRM":
            embed = create_embed("⚠️ Confirmation Required", "This will delete ALL unused keys!\n\nRe-run with `confirm: CONFIRM` to proceed.", discord.Color.orange())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            count = db.purge_unused_keys() if hasattr(db, 'purge_unused_keys') else 0
            
            embed = create_embed("🗑️ Keys Purged", f"Deleted **{count}** unused keys.", discord.Color.green())
            db.log_event("purge_keys", str(interaction.user.id), None, f"Purged {count} keys")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}", ephemeral=True)

    @app_commands.command(name="announce", description="🔧 [ADMIN] Send an announcement embed to a channel")
    @app_commands.describe(channel="Channel to send to", title="Announcement title", message="Announcement message")
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel, title: str, message: str):
        """Send a fancy announcement."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        embed = create_embed(f"📢 {title}", message, discord.Color.gold())
        embed.set_author(name="Banana Hub Announcement", icon_url=self.bot.user.display_avatar.url if self.bot.user else None)
        
        try:
            await channel.send(embed=embed)
            await interaction.response.send_message(f"✅ Announcement sent to {channel.mention}!", ephemeral=True)
            db.log_event("announcement", str(interaction.user.id), None, f"Sent to {channel.id}: {title}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ No permission to send to that channel!", ephemeral=True)

    @app_commands.command(name="masskey", description="🔧 [ADMIN] Generate multiple keys at once")
    @app_commands.describe(count="Number of keys to generate (1-50)")
    async def masskey(self, interaction: discord.Interaction, count: int = 5):
        """Generate multiple keys."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        count = max(1, min(count, 50))
        
        await interaction.response.defer(ephemeral=True)
        
        keys = []
        for _ in range(count):
            key = generate_key()
            db.generate_key_entry(key, interaction.user.id)
            keys.append(key)
        
        keys_text = "\n".join([f"`{k}`" for k in keys])
        
        embed = create_embed(f"🔑 Generated {count} Keys", "Keys have been added to the database.")
        
        # Send keys as a file if too many
        if count > 10:
            file_content = "\n".join(keys)
            file = discord.File(io.BytesIO(file_content.encode()), filename=f"keys_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            await interaction.followup.send(embed=embed, file=file, ephemeral=True)
        else:
            embed.add_field(name="🔑 Keys", value=keys_text, inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
        
        db.log_event("mass_keygen", str(interaction.user.id), None, f"Generated {count} keys")


class UtilityCog(commands.Cog, name="Utility"):
    def __init__(self, bot: BananaBot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        status = "🟢" if latency < 100 else ("🟡" if latency < 200 else "🔴")
        
        embed = create_embed("🏓 Pong!", f"{status} **{latency}ms**")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="uptime", description="Show bot uptime")
    async def uptime(self, interaction: discord.Interaction):
        uptime_str = format_uptime(int(time.time() - self.bot.start_time))
        
        embed = create_embed("⏱️ Uptime", f"`{uptime_str}`")
        embed.add_field(name="Servers", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="Version", value=f"`{self.bot.version}`", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="help", description="Get help with commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = create_embed("Command Help")
        
        embed.add_field(
            name="👤 User Commands",
            value=(
                "`/redeem` - Redeem license key\n"
                "`/panel` - Dashboard with buttons\n"
                "`/profile` - View profile card\n"
                "`/getkey` - Get key via DM\n"
                "`/reset-hwid` - Reset HWID\n"
                "`/myinfo` - Account info\n"
                "`/script` - Get executor script\n"
                "`/status` - Check service status"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📬 Feedback",
            value=(
                "`/support` - Get help\n"
                "`/report` - Report a bug\n"
                "`/feedback` - Send suggestions\n"
                "`/changelog` - View updates\n"
                "`/invite` - Bot invite link"
            ),
            inline=False
        )
        
        if await is_admin(interaction, self.bot):
            embed.add_field(
                name="🛡️ Admin Commands",
                value=(
                    "`/adminpanel` - Admin control panel\n"
                    "`/whitelist` - Auto-whitelist user\n"
                    "`/unwhitelist` - Remove user\n"
                    "`/lookup` - User lookup\n"
                    "`/genkey` - Generate keys\n"
                    "`/masskey` - Generate multiple keys\n"
                    "`/blacklist` - Ban user\n"
                    "`/unblacklist` - Remove from blacklist\n"
                    "`/forceresethwid` - Force HWID reset\n"
                    "`/stats` - System stats"
                ),
                inline=False
            )
            embed.add_field(
                name="📊 Admin Tools",
                value=(
                    "`/userlist` - View all users\n"
                    "`/keylist` - View key stats\n"
                    "`/broadcast` - Send broadcast\n"
                    "`/announce` - Channel announcement\n"
                    "`/exportdata` - Export data as JSON\n"
                    "`/purgekeys` - Delete unused keys"
                ),
                inline=False
            )
        
        embed.add_field(
            name="🧰 Utility",
            value="`/ping` `/uptime` `/help`",
            inline=False
        )
        
        if not IS_LOCALHOST:
            embed.add_field(name="🌐 Web", value=f"[Panel]({Config.WEBSITE_URL})", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


def main() -> None:
    try:
        if not Config.BOT_TOKEN or Config.BOT_TOKEN == "YOUR_NEW_TOKEN_HERE":
            log.error("❌ BOT_TOKEN not set!")
            return
        
        log.info("=" * 60)
        log.info("🍌 BANANA HUB ENTERPRISE BOT v2.1 + API")
        log.info("=" * 60)
        log.info(f"Mode: {'DEV' if DEV_MODE else 'PROD'}")
        log.info(f"Website: {Config.WEBSITE_URL}")
        log.info("=" * 60)
        
        log.info("🌐 Starting web server...")
        server_thread = threading.Thread(target=run_server, daemon=True, name="WebServer")
        server_thread.start()
        log.info("✅ Web server started")
        
        time.sleep(1)
        
        log.info("🤖 Starting bot...")
        bot = BananaBot()
        bot.run(Config.BOT_TOKEN, log_handler=None)
        
    except discord.LoginFailure:
        log.error("❌ INVALID BOT TOKEN")
    except KeyboardInterrupt:
        log.info("👋 Shutdown")
    except Exception as e:
        log.exception(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    main()
