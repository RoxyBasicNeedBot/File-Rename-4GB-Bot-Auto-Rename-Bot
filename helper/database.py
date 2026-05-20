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

# Special Thanks To (https://github.com/JayMahakal98)

# database imports
import motor.motor_asyncio, datetime, pytz

# bots imports
from config import Config
from helper.utils import send_log

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
        self.premium = self.db.premium
        self.auto_delete = self.db.auto_delete
        self.bot_messages = self.db.bot_messages

    def new_user(self, id):
        return dict(
            _id=int(id),
            join_date=datetime.date.today().isoformat(),
            file_id=None,
            caption=None,
            prefix=None,
            suffix=None,
            autorename_template=None,
            media_type=None,  # Default media output type: document, video, audio
            dump_channel=None,  # Target channel ID for sending renamed files
            screenshot_mode=False,  # Generate screenshots from video every 5 seconds
            convert_mkv_to_mp4=False,  # Auto-convert MKV files to MP4 using FFmpeg remux
            compress_video=False,  # Compress video to 720p, 480p, 360p (Premium only)
            trim_mode=False,  # Enable video trimming before upload
            auto_delete=False,  # Auto-delete processing messages after upload
            watermark_text=None,  # Text watermark to overlay on videos
            watermark_position='bottom_right',  # Watermark position on video
            used_limit=0,
            usertype="Free",
            uploadlimit=Config.FREE_UPLOAD_LIMIT,
            daily=0,
            metadata_mode=False,
            metadata_code="--change-title @roxybasicneedbot1\n--change-video-title @roxybasicneedbot1\n--change-audio-title @roxybasicneedbot1\n--change-subtitle-title @roxybasicneedbot1\n--change-author @roxybasicneedbot1",
            expiry_time=None,
            has_free_trial=False,
            # TMDb settings
            tmdb_auto_mode=False,   # Auto-detect and search TMDb on file upload
            tmdb_auto_thumb=False,  # Use TMDb poster as video thumbnail
            tmdb_language="en-US",  # Preferred TMDb metadata language
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)            
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

    async def set_prefix(self, id, prefix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'prefix': prefix}})

    async def get_prefix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('prefix', None)

    async def set_suffix(self, id, suffix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'suffix': suffix}})

    async def get_suffix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('suffix', None)

    async def set_autorename(self, id, template):
        await self.col.update_one({'_id': int(id)}, {'$set': {'autorename_template': template}})

    async def get_autorename(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('autorename_template', None)

    async def set_media_type(self, id, media_type):
        await self.col.update_one({'_id': int(id)}, {'$set': {'media_type': media_type}})

    async def get_media_type(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('media_type', None)

    async def set_dump_channel(self, id, channel_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'dump_channel': channel_id}})

    async def get_dump_channel(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('dump_channel', None)

    async def set_screenshot_mode(self, id, mode):
        await self.col.update_one({'_id': int(id)}, {'$set': {'screenshot_mode': mode}})

    async def get_screenshot_mode(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('screenshot_mode', False)

    async def set_convert_mkv_to_mp4(self, id, mode):
        await self.col.update_one({'_id': int(id)}, {'$set': {'convert_mkv_to_mp4': mode}})

    async def get_convert_mkv_to_mp4(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('convert_mkv_to_mp4', False)

    async def set_compress_video(self, id, mode):
        await self.col.update_one({'_id': int(id)}, {'$set': {'compress_video': mode}})

    async def get_compress_video(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('compress_video', False)

    async def set_trim_mode(self, id, mode):
        await self.col.update_one({'_id': int(id)}, {'$set': {'trim_mode': mode}})

    async def get_trim_mode(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('trim_mode', False)

    async def set_auto_delete(self, id, mode):
        await self.col.update_one({'_id': int(id)}, {'$set': {'auto_delete': mode}})

    async def get_auto_delete(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('auto_delete', False)

    async def set_watermark(self, id, text):
        await self.col.update_one({'_id': int(id)}, {'$set': {'watermark_text': text}})

    async def get_watermark(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('watermark_text', None)

    async def set_watermark_position(self, id, position):
        await self.col.update_one({'_id': int(id)}, {'$set': {'watermark_position': position}})

    async def get_watermark_position(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('watermark_position', 'bottom_right')

    # ===== TMDb Settings =====
    async def set_tmdb_auto_mode(self, id, mode):
        await self.col.update_one({'_id': int(id)}, {'$set': {'tmdb_auto_mode': mode}})

    async def get_tmdb_auto_mode(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('tmdb_auto_mode', False)

    async def set_tmdb_auto_thumb(self, id, mode):
        await self.col.update_one({'_id': int(id)}, {'$set': {'tmdb_auto_thumb': mode}})

    async def get_tmdb_auto_thumb(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('tmdb_auto_thumb', False)

    async def set_tmdb_language(self, id, lang):
        await self.col.update_one({'_id': int(id)}, {'$set': {'tmdb_language': lang}})

    async def get_tmdb_language(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('tmdb_language', 'en-US')

    async def set_metadata_mode(self, id, bool_meta):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_mode': bool_meta}})

    async def get_metadata_mode(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_mode', None)

    async def set_metadata_code(self, id, metadata_code):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_code': metadata_code}})

    async def get_metadata_code(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_code', None)

    async def set_used_limit(self, id, used):
        await self.col.update_one({'_id': int(id)}, {'$set': {'used_limit': used}})
      
    async def set_usertype(self, id, type):
        await self.col.update_one({'_id': int(id)}, {'$set': {'usertype': type}})

    async def set_uploadlimit(self, id, limit):
        await self.col.update_one({'_id': int(id)}, {'$set': {'uploadlimit': limit}})
  
    async def set_reset_dailylimit(self, id, date):
        await self.col.update_one({'_id': int(id)}, {'$set': {'daily': date}})
        
    async def reset_uploadlimit_access(self, user_id):
        seconds = 1440 * 60
        reset_date = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        zero_usage = 0
        
        user_data = await self.get_user_data(user_id)
        if user_data:
            expiry_time = user_data.get("daily")
            current_time = datetime.datetime.now()
            
            needs_reset = (
                expiry_time is None or
                expiry_time == 0 or
                not isinstance(expiry_time, datetime.datetime) or
                current_time > expiry_time
            )
            
            # Also check if the stored uploadlimit needs syncing to current config
            # for non-premium (Free) users — prevents stale high limits
            stored_limit = user_data.get('uploadlimit', 0)
            user_type = user_data.get('usertype', 'Free')
            sync_limit = (user_type == 'Free' and int(stored_limit) != Config.FREE_UPLOAD_LIMIT)
            
            update_fields = {}
            if needs_reset:
                update_fields['daily'] = reset_date
                update_fields['used_limit'] = zero_usage
            if sync_limit:
                update_fields['uploadlimit'] = Config.FREE_UPLOAD_LIMIT
            
            if update_fields:
                await self.col.update_one(
                    {'_id': user_id}, 
                    {'$set': update_fields}
                )
                        
    async def get_user_data(self, id) -> dict:
        user_data = await self.col.find_one({'_id': int(id)})
        return user_data or None
        
    async def get_user(self, user_id):
        user_data = await self.premium.find_one({"id": user_id})
        return user_data

    async def add_premium(self, user_id, user_data, limit=None, type=None):    
        await self.premium.update_one(
            {"id": user_id}, 
            {"$set": user_data}, 
            upsert=True
        )
        

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

        if Config.UPLOAD_LIMIT_MODE and limit and type:
            await self.col.update_one(
                {'_id': user_id}, 
                {'$set': {
                    'usertype': type,
                    'uploadlimit': limit
                }}
            )
    
    async def remove_premium(self, user_id, limit=Config.FREE_UPLOAD_LIMIT, type="Free"):
        await self.premium.update_one(
            {"id": user_id}, 
            {"$set": {
                "expiry_time": None,
                "has_free_trial": False
            }}
        )
        
        # Reset all premium feature flags
        await self.col.update_one(
            {'_id': user_id}, 
            {'$set': {
                'trim_mode': False,
                'compress_video': False,
                'screenshot_mode': False,
                'convert_mkv_to_mp4': False,
                'auto_delete': False,
                'watermark_text': None
            }}
        )
        
        if Config.UPLOAD_LIMIT_MODE and limit and type:
            await self.col.update_one(
                {'_id': user_id}, 
                {'$set': {
                    'usertype': type,
                    'uploadlimit': limit
                }}
            )
          
    async def checking_remaining_time(self, user_id):
        user_data = await self.get_user(user_id)
        expiry_time = user_data.get("expiry_time")
        time_left_str = expiry_time - datetime.datetime.now()
        return time_left_str

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                # User previously used the free trial, but it has ended.
                # Ensure all premium features are OFF
                await self._reset_premium_features(user_id)
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                await self.remove_premium(user_id)
        # No premium data at all — also ensure features are reset
        await self._reset_premium_features(user_id)
        return False

    async def _reset_premium_features(self, user_id):
        """Silently reset ALL premium-only feature flags to OFF.
        Called whenever premium check fails to prevent feature leaks."""
        await self.col.update_one(
            {'_id': int(user_id)},
            {'$set': {
                'trim_mode': False,
                'compress_video': False,
                'auto_delete': False,
                'watermark_text': None,
            }}
        )

    async def has_feature_access(self, user_id, feature_name):
        """Check if user's plan tier includes a specific feature.
        
        Args:
            user_id: User ID
            feature_name: Feature key (e.g. 'compress', 'trim', 'tmdb_auto', 'tmdb_thumb')
        
        Returns:
            True if user's plan includes this feature
        """
        # First check: if user has active premium, grant all premium features
        is_premium = await self.has_premium_access(user_id)
        if is_premium:
            # User has active premium — check their plan tier
            user_data = await self.get_user_data(user_id)
            user_type = user_data.get('usertype', 'Free') if user_data else 'Free'
            
            # If usertype is still "Free" but premium is active (admin gave premium
            # without specifying plan type), grant ALL features
            if user_type == 'Free':
                return True
            
            plan = Config.PREMIUM_PLANS.get(user_type, {})
            features = plan.get('features', [])
            return 'all' in features or feature_name in features
        
        # Not premium — check Free plan features
        plan = Config.PREMIUM_PLANS.get('Free', {})
        features = plan.get('features', [])
        return feature_name in features

    async def total_premium_users_count(self):
        count = await self.premium.count_documents({"expiry_time": {"$gt": datetime.datetime.now()}})
        return count

    async def get_all_premium_users(self):
        all_premium_users = self.premium.find({"expiry_time": {"$gt": datetime.datetime.now()}})
        return all_premium_users

    async def get_free_trial_status(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            return user_data.get("has_free_trial", False)
        return False

    async def give_free_trial(self, user_id):
        seconds = 240 * 60  # 4 hours trial
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {
            "id": user_id, 
            "expiry_time": expiry_time, 
            "has_free_trial": True
        }
        
        if Config.UPLOAD_LIMIT_MODE:
            limit_type = "Trial"
            upload_limit = 32212254720  # 30GB limit
            await self.add_premium(user_id, user_data, upload_limit, limit_type)
        else:
            await self.add_premium(user_id, user_data)
                    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'_id': int(id)}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason)
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason='')
        user = await self.col.find_one({'_id': int(id)})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users
    
    # ===== Maintenance Mode Functions =====
    async def set_maintenance_mode(self, is_enabled, message=None):
        """Set bot maintenance mode on/off with optional custom message"""
        settings = self.db.settings
        await settings.update_one(
            {'_id': 'bot_settings'},
            {'$set': {
                'maintenance_mode': is_enabled,
                'maintenance_message': message or "🔧 Bot is currently under maintenance. Please try again later!"
            }},
            upsert=True
        )
    
    async def get_maintenance_mode(self):
        """Get current maintenance mode status"""
        settings = self.db.settings
        data = await settings.find_one({'_id': 'bot_settings'})
        if data:
            return data.get('maintenance_mode', False), data.get('maintenance_message', '')
        return False, ''
    
    # ===== Activity Tracking Functions =====
    async def log_upload(self, user_id, file_size=0):
        """Log an upload event with timestamp and file size"""
        activity = self.db.activity
        await activity.insert_one({
            'user_id': int(user_id),
            'file_size': int(file_size),
            'timestamp': datetime.datetime.now()
        })
    
    async def get_top_uploaders(self, hours=24, limit=10):
        """Get top uploaders in last X hours with upload count and total size"""
        activity = self.db.activity
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
        
        # Aggregate pipeline: filter by time, group by user, count uploads and sum size
        pipeline = [
            {'$match': {'timestamp': {'$gte': cutoff_time}}},
            {'$group': {
                '_id': '$user_id',
                'upload_count': {'$sum': 1},
                'total_size': {'$sum': '$file_size'}
            }},
            {'$sort': {'upload_count': -1}},
            {'$limit': limit}
        ]
        
        results = []
        async for doc in activity.aggregate(pipeline):
            results.append({
                'user_id': doc['_id'],
                'upload_count': doc['upload_count'],
                'total_size': doc['total_size']
            })
        return results

    async def get_user_uploads(self, user_id, hours=12):
        """Get a specific user's upload count and total size in last X hours"""
        activity = self.db.activity
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
        
        pipeline = [
            {'$match': {
                'user_id': int(user_id),
                'timestamp': {'$gte': cutoff_time}
            }},
            {'$group': {
                '_id': '$user_id',
                'upload_count': {'$sum': 1},
                'total_size': {'$sum': '$file_size'}
            }}
        ]
        
        async for doc in activity.aggregate(pipeline):
            return {
                'upload_count': doc['upload_count'],
                'total_size': doc['total_size']
            }
        return {'upload_count': 0, 'total_size': 0}

    # ===== Auto-Delete Scheduling Functions =====
    async def schedule_auto_delete(self, chat_id, message_id, delete_at):
        """Schedule a message for auto-deletion at specific time"""
        await self.auto_delete.insert_one({
            'chat_id': int(chat_id),
            'message_id': int(message_id),
            'delete_at': delete_at,
            'created_at': datetime.datetime.now()
        })
    
    async def get_pending_deletions(self):
        """Get all messages due for deletion (past their delete_at time)"""
        return self.auto_delete.find({
            'delete_at': {'$lte': datetime.datetime.now()}
        })
    
    async def remove_scheduled_deletion(self, chat_id, message_id):
        """Remove a deletion record after successful delete"""
        await self.auto_delete.delete_one({
            'chat_id': int(chat_id),
            'message_id': int(message_id)
        })
    
    async def cleanup_expired_deletions(self):
        """Remove deletion records older than 48 hours (Telegram limit)"""
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=48)
        await self.auto_delete.delete_many({
            'created_at': {'$lte': cutoff}
        })
    
    # ===== Bot Message Tracking (for ban cleanup) =====
    async def track_bot_message(self, user_id, chat_id, message_id):
        """Track a message sent by the bot to a user"""
        await self.bot_messages.insert_one({
            'user_id': int(user_id),
            'chat_id': int(chat_id),
            'message_id': int(message_id),
            'timestamp': datetime.datetime.now()
        })
    
    async def get_user_bot_messages(self, user_id, limit=100):
        """Get tracked bot messages for a user (for cleanup on ban)"""
        return self.bot_messages.find(
            {'user_id': int(user_id)}
        ).sort('timestamp', -1).limit(limit)
    
    async def clear_user_bot_messages(self, user_id):
        """Clear all tracked bot messages for a user"""
        await self.bot_messages.delete_many({'user_id': int(user_id)})
        

roxy_bot = Database(Config.DB_URL, Config.DB_NAME)

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
