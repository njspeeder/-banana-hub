# ==============================================================================
# 🍌 BANANA HUB ENTERPRISE - COMPLETE DISCORD BOT v2.1 (FINAL FIXED)
# Enhanced with security, error handling, and automatic admin role setup
# All bugs fixed - Thread-safe database, updated datetime, proper indentation
# ==============================================================================

from __future__ import annotations  # ✅ MUST BE FIRST!

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Now import everything else
import asyncio
import logging
import re
import secrets
import string
import threading
import time
from contextlib import asynccontextmanager
from datetime import datetime, UTC
from typing import List, Optional, Dict, Any

import discord
from discord.ext import commands
from discord import app_commands

from config import Config
from database import db
from website_server import run_server

# ==============================================================================
# 🔧 LOGGING CONFIGURATION
# ==============================================================================

logging.basicConfig(
    level=logging.DEBUG if getattr(Config, "DEBUG", True) else logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("banana_hub_bot")
START_TIME = time.time()

# Development mode detection
DEV_MODE = getattr(Config, "DEBUG", "localhost" in getattr(Config, "WEBSITE_URL", ""))
IS_LOCALHOST = "localhost" in getattr(Config, "WEBSITE_URL", "")

if DEV_MODE:
    log.info("🔧 Running in DEVELOPMENT mode")
    log.info(f"📍 Website: {Config.WEBSITE_URL}")
    log.info(f"📍 Localhost: {IS_LOCALHOST}")
else:
    log.info("🚀 Running in PRODUCTION mode")

# ==============================================================================
# 🔨 HELPER FUNCTIONS
# ==============================================================================

def generate_key(length: int = 12) -> str:
    """Generate a cryptographically secure BANANA-XXXXXXXXXXXX style key."""
    alphabet = string.ascii_uppercase + string.digits
    body = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"BANANA-{body}"


def validate_discord_id(discord_id: str) -> bool:
    """Validate Discord ID format (snowflake: 17-20 digits)."""
    return bool(re.match(r'^\d{17,20}$', str(discord_id)))


def validate_key_format(key: str) -> bool:
    """Validate Banana Hub key format."""
    return bool(re.match(r'^BANANA-[A-Z0-9]{12,}$', key.strip().upper()))


def chunk_text(text: str, size: int = 1900) -> List[str]:
    """Split long text into chunks for Discord message limits."""
    return [text[i:i + size] for i in range(0, len(text), size)]


def create_embed(
    title: str,
    description: str = "",
    color: discord.Color = None,
    **kwargs
) -> discord.Embed:
    """Create a branded Banana Hub embed with consistent styling."""
    color = color or getattr(Config, "EMBED_COLOR", discord.Color.gold())
    embed = discord.Embed(
        title=f"🍌 {title}",
        description=description,
        color=color,
        timestamp=datetime.now(UTC)  # ✅ Fixed: Updated from deprecated utcnow()
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
    """Check if user has administrator permissions."""
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
    """Context manager for safe database operations with logging."""
    try:
        log.debug(f"Starting DB operation: {operation_name}")
        yield
        log.debug(f"Completed DB operation: {operation_name}")
    except Exception as e:
        log.error(f"DB operation '{operation_name}' failed: {e}", exc_info=True)
        raise


def format_uptime(seconds: int) -> str:
    """Format seconds into human-readable uptime string."""
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


# ==============================================================================
# 🎮 INTERACTIVE BUTTON VIEWS
# ==============================================================================

class UserPanelView(discord.ui.View):
    """Interactive button view for user panel."""
    
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
        """Send loader script to user."""
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
            f"-- 🍌 BANANA HUB ENTERPRISE LOADER\n"
            f"-- Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
            f"-- User: {interaction.user.name}\n\n"
            f'getgenv().BananaKey = "{key}"\n'
            f'getgenv().BananaID = "{uid}"\n'
            f'loadstring(game:HttpGet("{Config.BASE_URL}/script.lua"))()\n'
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
        """Reset user's HWID."""
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
        """Show user info."""
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
        """Refresh panel."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This button is not for you!", ephemeral=True)
            return
        
        await interaction.response.send_message("🔄 Refreshing panel...", ephemeral=True)


class AdminPanelView(discord.ui.View):
    """Interactive button view for admin panel."""
    
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=300)
        self.bot = bot
    
    @discord.ui.button(label="Generate Key", style=discord.ButtonStyle.success, emoji="🔑", row=0)
    async def gen_key_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Generate a new key."""
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
        """View system stats."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            stats = db.get_stats()
            uptime = format_uptime(int(time.time() - self.bot.start_time))
            
            embed = create_embed("System Statistics")
            embed.add_field(name="⏱️ Uptime", value=f"`{uptime}`", inline=False)
            embed.add_field(name="👥 Users", value=f"`{stats.get('total_users', 0)}`", inline=True)
            embed.add_field(name="🔑 Keys", value=f"`{stats.get('available_keys', 0)}`", inline=True)
            embed.add_field(name="📈 Logins", value=f"`{stats.get('total_logins', 0)}`", inline=True)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            log.error(f"Stats error: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error loading stats: {str(e)[:100]}", ephemeral=True)
    
    @discord.ui.button(label="Backup DB", style=discord.ButtonStyle.secondary, emoji="💾", row=1)
    async def backup_db_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Create database backup."""
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
        """Refresh admin panel."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.send_message("🔄 Admin panel refreshed!", ephemeral=True)


# ==============================================================================
# 🤖 ENHANCED BOT CLASS
# ==============================================================================

class BananaBot(commands.Bot):
    """Enhanced Discord bot for Banana Hub."""
    
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

    async def setup_admin_role(self, guild: discord.Guild) -> Optional[discord.Role]:
        """Create or get admin role."""
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
        """Global error handler."""
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


# ==============================================================================
# 👤 USER COG
# ==============================================================================

class UserCog(commands.Cog, name="User"):
    """User commands for license management."""

    def __init__(self, bot: BananaBot) -> None:
        self.bot = bot

    @app_commands.command(name="redeem", description="Redeem your Banana Hub license key")
    @app_commands.describe(key="Your BANANA-XXXXXXXXXXXX license key")
    async def redeem(self, interaction: discord.Interaction, key: str):
        """Redeem a license key."""
        key_value = key.strip().upper()
        
        if not validate_key_format(key_value):
            embed = create_embed(
                "❌ Invalid Format",
                "Keys must be: `BANANA-XXXXXXXXXXXX`",
                discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        async with safe_db_operation("redeem_key"):
            try:
                if not db.check_key_available(key_value):
                    embed = create_embed(
                        "❌ Key Unavailable",
                        "This key is invalid, already used, or expired.",
                        discord.Color.red()
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                existing_user = db.get_user(interaction.user.id)
                if existing_user and existing_user.get("key"):
                    embed = create_embed(
                        "⚠️ Already Have Key",
                        f"You already have: `{existing_user['key']}`\n\nContact an admin to change keys.",
                        discord.Color.orange()
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                db.register_user(interaction.user.id, key_value)
                db.mark_key_redeemed(key_value, interaction.user.id)
                db.log_event("key_redeemed", str(interaction.user.id), None, f"Redeemed {key_value}")

                embed = create_embed(
                    "✅ Key Redeemed!",
                    f"Welcome to Banana Hub!\n\n**Your Key:** ||`{key_value}`||",
                    discord.Color.green()
                )
                embed.add_field(
                    name="🚀 Next Steps",
                    value="• Use `/panel` to access dashboard\n• Get your loader script\n• Start using Banana Hub!",
                    inline=False
                )
                
                if not IS_LOCALHOST:
                    embed.add_field(
                        name="🌐 Web Login",
                        value=f"[Login Here]({Config.WEBSITE_URL}/login)\n**User ID:** `{interaction.user.id}`\n**Key:** ||`{key_value}`||",
                        inline=False
                    )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                log.info(f"✅ Key redeemed: {key_value} by {interaction.user.id}")

            except Exception as exc:
                log.exception(f"Error redeeming key")
                embed = create_embed("❌ Error", "Failed to redeem key. Try again.", discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="panel", description="Access your Banana Hub dashboard")
    async def panel(self, interaction: discord.Interaction):
        """Enhanced panel with interactive buttons."""
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
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="getkey", description="Get your license key via DM")
    @app_commands.checks.cooldown(1, 30, key=lambda i: i.user.id)
    async def getkey(self, interaction: discord.Interaction):
        """Send key to DMs."""
        user = db.get_user(interaction.user.id)
        
        if not user or not user.get("key"):
            embed = create_embed("❌ No License", "Use `/redeem <key>` first.", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        key = user["key"]
        
        try:
            dm_embed = create_embed("Your License Key", f"**Key:** `{key}`\n\n⚠️ Keep this secret!")
            if not IS_LOCALHOST:
                dm_embed.add_field(name="🌐 Login", value=f"[Web Panel]({Config.WEBSITE_URL}/login)", inline=False)
            
            await interaction.user.send(embed=dm_embed)
            await interaction.response.send_message("✅ Key sent to your DMs!", ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(f"||`{key}`||\n⚠️ Enable DMs!", ephemeral=True)

    @app_commands.command(name="reset-hwid", description="Reset your hardware ID")
    @app_commands.checks.cooldown(1, 300, key=lambda i: i.user.id)
    async def reset_hwid(self, interaction: discord.Interaction):
        """Reset HWID with cooldown."""
        success = db.reset_hwid(interaction.user.id)
        
        if success:
            db.log_event("hwid_reset", str(interaction.user.id), None, "User reset")
            embed = create_embed("✅ HWID Reset", "Successfully reset your hardware ID!", discord.Color.green())
        else:
            embed = create_embed("❌ Failed", "No license found.", discord.Color.red())
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="myinfo", description="View your account information")
    async def myinfo(self, interaction: discord.Interaction):
        """Display user account info."""
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
        
        status = "🔴 BLACKLISTED" if is_banned else "🟢 Active"
        embed.add_field(name="Status", value=status, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ==============================================================================
# 🛡️ ADMIN COG
# ==============================================================================

class AdminCog(commands.Cog, name="Admin"):
    """Admin commands."""

    def __init__(self, bot: BananaBot) -> None:
        self.bot = bot

    @app_commands.command(name="adminpanel", description="🔧 [ADMIN] Open admin control panel")
    async def adminpanel(self, interaction: discord.Interaction):
        """Interactive admin panel with buttons."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            stats = db.get_stats()
            
            blacklisted = 0
            try:
                blacklist_data = db.get_blacklisted_users()
                blacklisted = len(blacklist_data)
            except Exception as e:
                log.error(f"Error fetching blacklist count: {e}")
            
            uptime = format_uptime(int(time.time() - self.bot.start_time))
            
            embed = create_embed("Admin Control Panel")
            embed.add_field(name="⏱️ Uptime", value=f"`{uptime}`", inline=False)
            embed.add_field(name="👥 Total Users", value=f"`{stats.get('total_users', 0)}`", inline=True)
            embed.add_field(name="🔑 Available Keys", value=f"`{stats.get('available_keys', 0)}`", inline=True)
            embed.add_field(name="📈 Total Logins", value=f"`{stats.get('total_logins', 0)}`", inline=True)
            embed.add_field(name="🚫 Blacklisted", value=f"`{blacklisted}`", inline=True)
            embed.add_field(
                name="🎛️ Quick Actions",
                value="Use the buttons below for quick admin tasks",
                inline=False
            )
            
            view = AdminPanelView(self.bot)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            
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
        """Whitelist user and auto-assign key."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        if member.bot:
            await interaction.response.send_message("❌ Can't whitelist bots!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        existing = db.get_user(member.id)
        if existing and existing.get("key"):
            embed = create_embed("⚠️ Already Whitelisted", f"{member.mention} has key: `{existing['key']}`", discord.Color.orange())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        key = generate_key()
        if not db.generate_key_entry(key, interaction.user.id):
            await interaction.followup.send("❌ Failed to generate key!", ephemeral=True)
            return

        db.register_user(member.id, key)
        db.mark_key_redeemed(key, member.id)
        db.log_event("whitelist", str(member.id), None, f"By admin {interaction.user.id}")

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

    @app_commands.command(name="unwhitelist", description="🔧 [ADMIN] Remove user from whitelist")
    @app_commands.describe(member="User to remove")
    async def unwhitelist(self, interaction: discord.Interaction, member: discord.Member):
        """Remove user from whitelist."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        success = db.unwhitelist(member.id)
        
        if success:
            db.log_event("unwhitelist", str(member.id), None, f"By admin {interaction.user.id}")
            embed = create_embed("✅ Removed", f"{member.mention} removed from whitelist.", discord.Color.green())
        else:
            embed = create_embed("❌ Not Found", f"{member.mention} not whitelisted.", discord.Color.red())
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="lookup", description="🔧 [ADMIN] Look up user information")
    @app_commands.describe(user="User to lookup (mention or ID)")
    async def lookup(self, interaction: discord.Interaction, user: str):
        """Comprehensive user lookup."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        discord_id = user.strip("<@!>")
        
        if not validate_discord_id(discord_id):
            await interaction.response.send_message("❌ Invalid Discord ID!", ephemeral=True)
            return

        user_data = db.get_user(discord_id)
        
        if not user_data:
            embed = create_embed("❌ Not Found", f"No record for ID: `{discord_id}`", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        analytics = db.get_user_analytics(discord_id)
        is_banned = db.is_blacklisted(discord_id)
        
        embed_color = discord.Color.red() if is_banned else discord.Color.blue()
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
            value=f"Logins: `{analytics['login_count']}`\nResets: `{analytics['reset_count']}`", 
            inline=False
        )
        
        status = "🔴 BLACKLISTED" if is_banned else "🟢 Active"
        embed.add_field(name="Status", value=status, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="genkey", description="🔧 [ADMIN] Generate license keys")
    @app_commands.describe(amount="Number of keys (1-25)")
    async def genkey(self, interaction: discord.Interaction, amount: int = 1):
        """Generate multiple keys."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        if amount < 1 or amount > 25:
            await interaction.response.send_message("❌ Amount must be 1-25!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        
        keys = []
        for _ in range(amount):
            key = generate_key()
            if db.generate_key_entry(key, interaction.user.id):
                keys.append(key)

        if keys:
            keys_text = "\n".join([f"`{k}`" for k in keys[:10]])
            if len(keys) > 10:
                keys_text += f"\n\n*...and {len(keys) - 10} more*"
            
            embed = create_embed("✅ Keys Generated", f"Created **{len(keys)}** keys", discord.Color.green())
            embed.add_field(name="🔑 Keys", value=keys_text, inline=False)
            
            try:
                dm_embed = create_embed(f"Generated Keys ({len(keys)})", "\n".join([f"`{k}`" for k in keys]))
                await interaction.user.send(embed=dm_embed)
            except:
                pass
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send("❌ Failed to generate keys!", ephemeral=True)

    @app_commands.command(name="blacklist", description="🔧 [ADMIN] Blacklist a user")
    @app_commands.describe(member="User to blacklist", reason="Reason")
    async def blacklist(self, interaction: discord.Interaction, member: Optional[discord.Member] = None, reason: str = "No reason"):
        """Blacklist user or show count."""
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

        status = db.toggle_blacklist(member.id, reason)

        if status:
            db.log_event("blacklist", str(member.id), None, f"{reason} | By: {interaction.user.id}")
            embed = create_embed("✅ Blacklisted", f"{member.mention} blacklisted.\n**Reason:** {reason}", discord.Color.red())
        else:
            embed = create_embed("✅ Unblacklisted", f"{member.mention} removed from blacklist.", discord.Color.green())
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="unblacklist", description="🔧 [ADMIN] Remove user from blacklist")
    @app_commands.describe(member="User to unblacklist")
    async def unblacklist(self, interaction: discord.Interaction, member: discord.Member):
        """Explicitly unblacklist a user."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        rows = db.unblacklist(member.id)
        
        if rows:
            db.log_event("unblacklist", str(member.id), None, f"By admin {interaction.user.id}")
            embed = create_embed("✅ Unblacklisted", f"{member.mention} removed from blacklist.", discord.Color.green())
            log.info(f"✅ Unblacklisted {member.id}")
        else:
            embed = create_embed("❌ Not Found", f"{member.mention} is not blacklisted.", discord.Color.orange())
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="forceresethwid", description="🔧 [ADMIN] Force reset user's HWID")
    @app_commands.describe(member="User to reset HWID for")
    async def forceresethwid(self, interaction: discord.Interaction, member: discord.Member):
        """Force reset someone's HWID."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        success = db.reset_hwid(member.id)
        
        if success:
            db.log_event("hwid_reset", str(member.id), None, f"Force reset by admin {interaction.user.id}")
            embed = create_embed("✅ HWID Reset", f"Force reset HWID for {member.mention}", discord.Color.green())
            log.info(f"🔄 Admin {interaction.user.id} force reset HWID for {member.id}")
        else:
            embed = create_embed("❌ Failed", f"{member.mention} not found in database.", discord.Color.red())
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="sethwidtime", description="🔧 [ADMIN] Set HWID reset cooldown time")
    @app_commands.describe(seconds="Cooldown in seconds (default: 300)")
    async def sethwidtime(self, interaction: discord.Interaction, seconds: int):
        """Set global HWID reset cooldown."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        if seconds < 0 or seconds > 86400:
            await interaction.response.send_message("❌ Time must be 0-86400 seconds!", ephemeral=True)
            return

        self.bot.hwid_reset_cooldown = seconds
        
        minutes = seconds // 60
        hours = minutes // 60
        
        if hours > 0:
            time_str = f"{hours}h {minutes % 60}m"
        elif minutes > 0:
            time_str = f"{minutes}m"
        else:
            time_str = f"{seconds}s"
        
        embed = create_embed(
            "✅ Cooldown Updated",
            f"HWID reset cooldown set to: **{time_str}** (`{seconds}s`)",
            discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        log.info(f"🕒 Admin {interaction.user.id} set HWID cooldown to {seconds}s")

    @app_commands.command(name="stats", description="🔧 [ADMIN] View system statistics")
    async def stats(self, interaction: discord.Interaction):
        """Display system stats."""
        if not await is_admin(interaction, self.bot):
            await interaction.response.send_message("❌ Admin only!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            stats = db.get_stats()
            uptime = format_uptime(int(time.time() - self.bot.start_time))
            latency = round(self.bot.latency * 1000)
            
            embed = create_embed("System Statistics")
            embed.add_field(name="🤖 Bot", value=f"Uptime: `{uptime}`\nGuilds: `{len(self.bot.guilds)}`\nLatency: `{latency}ms`", inline=False)
            embed.add_field(name="💾 Database", value=f"Users: `{stats.get('total_users', 0)}`\nKeys: `{stats.get('available_keys', 0)}`\nLogins: `{stats.get('total_logins', 0)}`", inline=True)
            
            blacklist_data = db.get_blacklisted_users()
            embed.add_field(name="🚫 Security", value=f"Blacklisted: `{len(blacklist_data)}`", inline=True)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            log.error(f"Stats error: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}", ephemeral=True)


# ==============================================================================
# 🧰 UTILITY COG
# ==============================================================================

class UtilityCog(commands.Cog, name="Utility"):
    """Utility commands."""

    def __init__(self, bot: BananaBot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Ping command."""
        latency = round(self.bot.latency * 1000)
        status = "🟢" if latency < 100 else ("🟡" if latency < 200 else "🔴")
        
        embed = create_embed("🏓 Pong!", f"{status} **{latency}ms**")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="uptime", description="Show bot uptime")
    async def uptime(self, interaction: discord.Interaction):
        """Uptime command."""
        uptime_str = format_uptime(int(time.time() - self.bot.start_time))
        
        embed = create_embed("⏱️ Uptime", f"`{uptime_str}`")
        embed.add_field(name="Servers", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="Version", value=f"`{self.bot.version}`", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="help", description="Get help with commands")
    async def help_command(self, interaction: discord.Interaction):
        """Help command."""
        embed = create_embed("Command Help")
        
        embed.add_field(
            name="👤 User Commands",
            value=(
                "`/redeem` - Redeem license key\n"
                "`/panel` - Dashboard with buttons\n"
                "`/getkey` - Get key via DM\n"
                "`/reset-hwid` - Reset HWID\n"
                "`/myinfo` - Account info"
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
                    "`/blacklist` - Ban user\n"
                    "`/unblacklist` - Remove from blacklist\n"
                    "`/forceresethwid` - Force HWID reset\n"
                    "`/sethwidtime` - Set cooldown\n"
                    "`/stats` - System stats"
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


# ==============================================================================
# 🚀 MAIN
# ==============================================================================

def main() -> None:
    """Run the bot."""
    try:
        if not Config.BOT_TOKEN or Config.BOT_TOKEN == "YOUR_NEW_TOKEN_HERE":
            log.error("❌ BOT_TOKEN not set!")
            return
        
        log.info("=" * 60)
        log.info("🍌 BANANA HUB ENTERPRISE BOT v2.1 FINAL")
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
