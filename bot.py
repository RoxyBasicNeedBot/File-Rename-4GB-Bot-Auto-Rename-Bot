# ═══════════════════════════════════════════════════════════════
# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
#
# Portfolio: https://aratt.ai/@roxybasicneedbot
#
# Bot & Website Developer 🤖
# Creator of RoxyBasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
#
# © 2026 RoxyBasicNeedBot. All Rights Reserved.
# ═══════════════════════════════════════════════════════════════

# extra imports
import aiohttp, asyncio, warnings, pytz, datetime
import logging
import logging.config
import glob, sys
import importlib.util
from pathlib import Path

# pyrogram imports
from pyrogram import Client, __version__, errors
from pyrogram.raw.all import layer
from pyrogram import idle

# bots imports
from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app

# Get logging configurations
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'),
             logging.StreamHandler()]
)
#logger = logging.getLogger(__name__)
logging.getLogger("pyrofork").setLevel(logging.WARNING)
logging.getLogger("hachoir").setLevel(logging.ERROR)  # Suppress hachoir warnings
logging.getLogger("hachoir.parser").setLevel(logging.ERROR)

class RoxyRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="RoxyRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=5,
            max_concurrent_transmissions=50
        )
                
         
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE
        Config.BOT = self
        
        # Set bot commands in Telegram menu
        await self.register_bot_commands()
        
        app = aiohttp.web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await aiohttp.web.TCPSite(app, bind_address, Config.PORT).start()
        
        path = "plugins/*.py"
        files = glob.glob(path)
        for name in files:
            with open(name) as a:
                patt = Path(a.name)
                plugin_name = patt.stem.replace(".py", "")
                plugins_path = Path(f"plugins/{plugin_name}.py")
                import_path = "plugins.{}".format(plugin_name)
                spec = importlib.util.spec_from_file_location(import_path, plugins_path)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules["plugins" + plugin_name] = load
                print("Roxy Bot Imported " + plugin_name)
                
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")
        
        # Start auto-delete background scheduler
        asyncio.create_task(self.auto_delete_scheduler())
        print("🗑️ Auto-delete scheduler started")

        
        for id in Config.ADMIN:
            if Config.STRING_SESSION:
                try: await self.send_message(id, f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\nNote: 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐬𝐭𝐫𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐓𝐡𝐞𝐧 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝟐𝐆𝐁+ 𝐟𝐢𝐥𝐞𝐬.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
                except: pass
            else:
                try: await self.send_message(id, f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
                except: pass
                    
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")                                
            except:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def register_bot_commands(self):
        """Register bot commands with Telegram for the menu"""
        from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat
        
        # Commands visible to all users in private chats
        user_commands = [
            BotCommand("start", "🚀 Sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
            BotCommand("free", "💕 Fʀᴇᴇ ꜰᴏʀ 30 ᴅᴀʏs ᴡɪᴛʜ ʟᴏᴠᴇ"),
            BotCommand("set_watermark", "🎨 Sᴇᴛ ᴠɪᴅᴇᴏ ᴡᴀᴛᴇʀᴍᴀʀᴋ"),
            BotCommand("see_watermark", "👁️ Vɪᴇᴡ ᴡᴀᴛᴇʀᴍᴀʀᴋ"),
            BotCommand("del_watermark", "🗑️ Dᴇʟᴇᴛᴇ ᴡᴀᴛᴇʀᴍᴀʀᴋ"),
            BotCommand("extract_audio", "🎵 Exᴛʀᴀᴄᴛ ᴀᴜᴅɪᴏ ꜰʀᴏᴍ ᴠɪᴅᴇᴏ"),
            BotCommand("features", "✨ Aʟʟ Bᴏᴛ Fᴇᴀᴛᴜʀᴇs"),
            BotCommand("settings", "⚙️ Bᴏᴛ sᴇᴛᴛɪɴɢs"),
            BotCommand("stop", "🛑 Sᴛᴏᴘ ᴄᴜʀʀᴇɴᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ"),
            BotCommand("myplan", "📊 Cʜᴇᴄᴋ ʏᴏᴜʀ ᴘʟᴀɴ"),
            BotCommand("plans", "💸 Vɪᴇᴡ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs"),
            BotCommand("merge", "🎬 Sᴛᴀʀᴛ ᴠɪᴅᴇᴏ ᴍᴇʀɢᴇ ᴍᴏᴅᴇ"),
            BotCommand("mergeall", "🔗 Mᴇʀɢᴇ ᴀʟʟ ǫᴜᴇᴜᴇᴅ ᴠɪᴅᴇᴏs"),
            BotCommand("mergestatus", "📋 Vɪᴇᴡ ᴍᴇʀɢᴇ ǫᴜᴇᴜᴇ"),
            BotCommand("clearmerge", "🗑️ Cʟᴇᴀʀ ᴍᴇʀɢᴇ ǫᴜᴇᴜᴇ"),
            BotCommand("exitmerge", "🚪 Exɪᴛ ᴍᴇʀɢᴇ ᴍᴏᴅᴇ"),
            BotCommand("autorename", "📝 Sᴇᴛ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ"),
            BotCommand("see_autorename", "🔎 Vɪᴇᴡ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ"),
            BotCommand("del_autorename", "🗑️ Dᴇʟᴇᴛᴇ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ"),
            BotCommand("setmedia", "🎬 Sᴇᴛ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ"),
            BotCommand("delmedia", "📤 Dᴇʟᴇᴛᴇ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ"),
            BotCommand("set_caption", "📝 Sᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ"),
            BotCommand("see_caption", "📋 Vɪᴇᴡ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ"),
            BotCommand("del_caption", "🧹 Dᴇʟᴇᴛᴇ ᴄᴀᴘᴛɪᴏɴ"),
            BotCommand("set_prefix", "✏️ Sᴇᴛ ғɪʟᴇɴᴀᴍᴇ ᴘʀᴇғɪx"),
            BotCommand("see_prefix", "📄 Vɪᴇᴡ ʏᴏᴜʀ ᴘʀᴇғɪx"),
            BotCommand("del_prefix", "🚮 Dᴇʟᴇᴛᴇ ᴘʀᴇғɪx"),
            BotCommand("set_suffix", "🔖 Sᴇᴛ ғɪʟᴇɴᴀᴍᴇ sᴜғғɪx"),
            BotCommand("see_suffix", "📑 Vɪᴇᴡ ʏᴏᴜʀ sᴜғғɪx"),
            BotCommand("del_suffix", "♻️ Dᴇʟᴇᴛᴇ sᴜғғɪx"),
            BotCommand("view_thumb", "🖼️ Vɪᴇᴡ ᴛʜᴜᴍʙɴᴀɪʟ"),
            BotCommand("del_thumb", "🗑️ Dᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ"),
        ]

# ═══════════════════════════════════════════════════════════════
# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
#
# Portfolio: https://aratt.ai/@roxybasicneedbot
#
# Bot & Website Developer 🤖
# Creator of RoxyBasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
#
# © 2026 RoxyBasicNeedBot. All Rights Reserved.
# ═══════════════════════════════════════════════════════════════

        
        # Additional commands for admins
        admin_commands = user_commands + [
            BotCommand("broadcast", "📢 Broadcast message to all users"),
            BotCommand("stats", "📊 View bot statistics"),
            BotCommand("use", "📊 Tᴏᴘ 10 ᴜᴘʟᴏᴀᴅᴇʀs (24ʜʀ)"),
            BotCommand("current", "👁️ Aᴄᴛɪᴠᴇ ᴜsᴇʀs ɴᴏᴡ"),
            BotCommand("ban", "🚫 Ban a user"),
            BotCommand("unban", "✅ Unban a user"),
            BotCommand("add_premium", "💎 Add premium to user"),
            BotCommand("remove_premium", "❌ Remove premium from user"),
            BotCommand("premium_list", "📋 List all premium users"),
            BotCommand("banned_users", "📋 List all banned users"),
            BotCommand("on_maintenance", "🔧 Eɴᴀʙʟᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ"),
            BotCommand("off_maintenance", "✅ Dɪsᴀʙʟᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ"),
            BotCommand("forcestop", "🛑 Sᴛᴏᴘ ᴀʟʟ ᴘʀᴏᴄᴇssᴇs"),
        ]


        
        try:
            # Register commands with AllPrivateChats scope (using Client.set_bot_commands)
            await Client.set_bot_commands(
                self,
                commands=user_commands,
                scope=BotCommandScopeAllPrivateChats()
            )
            print("✅ User commands registered for all private chats")
            
            # Set admin commands for each admin
            for admin_id in Config.ADMIN:
                try:
                    await Client.set_bot_commands(
                        self,
                        commands=admin_commands,
                        scope=BotCommandScopeChat(chat_id=admin_id)
                    )
                    print(f"✅ Admin commands registered for user {admin_id}")
                except Exception as e:
                    print(f"⚠️ Could not set admin commands for {admin_id}: {e}")
                    
        except Exception as e:
            print(f"❌ Error setting bot commands: {e}")

    async def auto_delete_scheduler(self):
        """Background task: delete scheduled messages every 5 minutes"""
        from helper.database import roxy_bot
        
        while True:
            try:
                pending = await roxy_bot.get_pending_deletions()
                deleted_count = 0
                async for record in pending:
                    try:
                        await self.delete_messages(
                            record['chat_id'], 
                            record['message_id']
                        )
                        deleted_count += 1
                    except Exception:
                        pass  # Message already deleted or expired
                    # Always remove the record after attempting
                    await roxy_bot.remove_scheduled_deletion(
                        record['chat_id'], 
                        record['message_id']
                    )
                
                # Cleanup expired records (older than 48hr Telegram limit)
                await roxy_bot.cleanup_expired_deletions()
                
                if deleted_count > 0:
                    print(f"🗑️ Auto-deleted {deleted_count} message(s)")
                    
            except Exception as e:
                print(f"Auto-delete scheduler error: {e}")
            
            await asyncio.sleep(300)  # Check every 5 minutes

    async def stop(self, *args):
        for id in Config.ADMIN:
            try: await self.send_message(id, f"**Bot Stopped....**")                                
            except: pass
                
        print("Bot Stopped 🙄")
        await super().stop()


roxy_instance = RoxyRenameBot()

def main():
    async def start_services():
        if Config.STRING_SESSION:
            try:
                await asyncio.gather(app.start(), roxy_instance.start())
            except Exception as e:
                print(f"⚠️ Error starting Premium Client: {e}")
                print("⚠️ Falling back to Standard Bot mode (No Premium features)")
                Config.STRING_SESSION = None # Disable premium mode
                # Ensure roxy_instance is started if it wasn't already
                if not roxy_instance.is_connected:
                    await roxy_instance.start()
        else:
            await asyncio.gather(roxy_instance.start())
        
        # Idle mode start karo
        await idle()
        
        # Bot stop karo
        if Config.STRING_SESSION:
            try:
                await asyncio.gather(app.stop(), roxy_instance.stop())
            except:
                await roxy_instance.stop()
        else:
            await asyncio.gather(roxy_instance.stop())

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user!")
    finally:
        loop.close()

if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    try:
        main()
    except errors.FloodWait as ft:
        print(f"⏳ FloodWait: Sleeping for {ft.value} seconds")
        asyncio.run(asyncio.sleep(ft.value))
        print("Now Ready For Deploying!")
        main()

# ═══════════════════════════════════════════════════════════════
# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
#
# Portfolio: https://aratt.ai/@roxybasicneedbot
#
# Bot & Website Developer 🤖
# Creator of RoxyBasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
#
# © 2026 RoxyBasicNeedBot. All Rights Reserved.
# ═══════════════════════════════════════════════════════════════
