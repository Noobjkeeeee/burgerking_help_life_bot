import asyncio
from datetime import datetime

from handlers.daily_messages import send_reminder
from services.user_service import get_all_users_with_reminders
from utils.logger import logger

sent_reminders = set()
last_logged_user_count = None


async def schedule_daily_jobs():
    global last_logged_user_count
    while True:
        try:
            now_dt = datetime.now()
            now_str = now_dt.strftime("%H.%M")
            users = await get_all_users_with_reminders()
            today = now_dt.date()

            current_user_count = len(users)
            if current_user_count != last_logged_user_count:
                last_logged_user_count = current_user_count

            for user in users:
                key = (user.telegram_user_id, user.reminder_time, today)
                if user.reminder_time == now_str:
                    if key not in sent_reminders:
                        logger.info(f"Текущее время: {now_str}")
                        logger.info(
                            f"Отправка напоминания пользователю"
                            f" {user.telegram_user_id} в {user.reminder_time}"
                        )
                        await send_reminder(int(
                            user.telegram_user_id),
                                            day=now_dt.day)
                        sent_reminders.add(key)
                else:
                    sent_reminders.discard(key)

        except Exception as e:
            logger.warning(f"Ошибка в планировщике: {e}", exc_info=True)

        await asyncio.sleep(10)
