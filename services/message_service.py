import json
from pathlib import Path

from utils.logger import logger

DATA_FILE = Path(__file__).parent.parent / "data" / "daily_texts.json"

try:
    with open(DATA_FILE, encoding="utf-8") as f:
        DAILY_TEXTS = json.load(f)
    logger.info(f"Данные ежедневных сообщений загружены из {DATA_FILE}")
except FileNotFoundError:
    logger.warning(f"Файл с ежедневными сообщениями не найден: {DATA_FILE}")
    DAILY_TEXTS = []
except json.JSONDecodeError as e:
    logger.warning(f"Ошибка декодирования JSON из файла {DATA_FILE}: {e}")
    DAILY_TEXTS = []
except Exception as e:
    logger.warning(
        f"Неожиданная ошибка при загрузке файла {DATA_FILE}: {e}",
        exc_info=True
    )
    DAILY_TEXTS = []


def get_daily_message_pair(day: int):
    """
    Возвращает tuple из (reminder_text, thank_you_text) по номеру дня.
    """
    try:
        if not DAILY_TEXTS:
            logger.warning("Список ежедневных сообщений пуст")
            return None, None
        index = (day - 1) % len(DAILY_TEXTS)
        item = DAILY_TEXTS[index]
        return item["reminder"], item["thank_you"]
    except Exception as e:
        logger.warning(
            f"Ошибка получения сообщения для дня {day}: {e}",
            exc_info=True)
        return None, None
