import json
import os
from datetime import datetime, date
from asyncio import Lock
from typing import Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/users_data.json")

lock = Lock()
users_data = {}

def load_users():
    global users_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                users_data = json.load(f)
                for user in users_data.values():
                    user['first_interaction_date'] = datetime.strptime(user['first_interaction_date'], "%Y-%m-%d").date()
            except Exception:
                users_data = {}
    else:
        users_data = {}

async def save_users():
    async with lock:
        json_ready = {}
        for k, v in users_data.items():
            json_ready[k] = {
                "first_interaction_date": v["first_interaction_date"].strftime("%Y-%m-%d"),
                "reminder_time": v["reminder_time"],
                "reminders_enabled": v["reminders_enabled"],
            }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(json_ready, f, ensure_ascii=False, indent=2)

async def create_user(user_id: int, reminder_time: str):
    if str(user_id) not in users_data:
        users_data[str(user_id)] = {
            "first_interaction_date": date.today(),
            "reminder_time": reminder_time,
            "reminders_enabled": False,
        }
        await save_users()

async def update_reminder_time(user_id: int, reminder_time: str):
    user = users_data.get(str(user_id))
    if user:
        user["reminder_time"] = reminder_time
        await save_users()

async def enable_reminders(user_id: int):
    user = users_data.get(str(user_id))
    if user:
        user["reminders_enabled"] = True
        await save_users()

async def get_user(user_id: int) -> Optional[dict]:
    return users_data.get(str(user_id))

async def get_all_users_with_reminders():
    return [ (int(uid), u) for uid, u in users_data.items() if u.get("reminders_enabled") ]