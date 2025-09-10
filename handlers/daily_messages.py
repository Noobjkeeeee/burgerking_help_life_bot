from datetime import datetime, timezone, timedelta
from keyboards.voting_kb import voting_keyboard
from services.user_service import get_all_users_with_reminders
from services.message_service import get_daily_message_pair
from utils.logger import logger


moscow_tz = timezone(timedelta(hours=3))


async def send_reminder(user_id: int, day: int):
    from bot import bot

    try:
        users = await get_all_users_with_reminders()
        user_data = dict(users).get(user_id)
        if not user_data:
            return

        first_interaction_date = user_data["first_interaction_date"]
        reminders_enabled = user_data["reminders_enabled"]

        now_dt = datetime.now(timezone.utc).astimezone(moscow_tz)
        today_date = now_dt.date()

        if not reminders_enabled or first_interaction_date == today_date:
            logger.info(
                f"Не отправляем напоминания пользователю {user_id}"
                f" в первый день или если напоминания не включены"
            )
            return

        day_num = (today_date - first_interaction_date).days + 1
        msg_1, msg_2 = get_daily_message_pair(day_num)

        logger.info(
            f"Отправка первого напоминания пользователю {user_id}"
            f" за день {day_num}"
        )
        await bot.send_message(user_id, msg_1, reply_markup=voting_keyboard())

        logger.info(
            f"Отправка второго напоминания пользователю {user_id}"
            f" за день {day_num}"
        )
        await bot.send_message(user_id, msg_2)

    except Exception as e:
        logger.warning(
            f"Ошибка при отправке напоминания пользователю {user_id} за день {day}: {e}",
            exc_info=True,
        )


async def send_daily_messages():
    try:
        users = await get_all_users_with_reminders()
        day_of_campaign = (datetime.now(timezone.utc).day % 30) or 1
        for user_id, _ in users:
            await send_reminder(user_id, day_of_campaign)
        logger.info(
            f"Отправлены ежедневные напоминания для {len(users)} пользователей за день {day_of_campaign}"
        )
    except Exception as e:
        logger.warning(
            f"Ошибка при отправке ежедневных напоминаний: {e}", exc_info=True
        )