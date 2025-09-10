import asyncio
from datetime import datetime, timezone, timedelta

from handlers.daily_messages import send_reminder
from services.user_service import get_all_users_with_reminders
from utils.logger import logger

sent_reminders = set()
last_logged_user_count = None

moscow_tz = timezone(timedelta(hours=3))

sent_reminders = set()
last_logged_user_count = None


async def schedule_daily_jobs():
    global last_logged_user_count
    while True:
        try:
            now_dt_utc = datetime.now(timezone.utc)
            now_dt = now_dt_utc.astimezone(moscow_tz)
            now_str = now_dt.strftime("%H.%M")
            users = await get_all_users_with_reminders()
            today = now_dt.date()

            current_user_count = len(users)
            if current_user_count != last_logged_user_count:
                last_logged_user_count = current_user_count
                logger.info(f"Количество пользователей с напоминаниями: {current_user_count}")

            for user_id, user_info in users:
                key = (user_id, user_info["reminder_time"], today)
                if user_info["reminder_time"] == now_str:
                    if key not in sent_reminders:
                        logger.info(f"Текущее московское время: {now_str}")
                        logger.info(
                            f"Отправка напоминания пользователю {user_id} в {user_info['reminder_time']}"
                        )
                        await send_reminder(user_id, now_dt.day)
                        sent_reminders.add(key)
                else:
                    sent_reminders.discard(key)

        except Exception as e:
            logger.warning(f"Ошибка в планировщике: {e}", exc_info=True)

        await asyncio.sleep(10)