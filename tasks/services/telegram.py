import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_task_telegram(user, task):
    if not user.telegram_id:
        return

    full_name = user.first_name or user.username or "Team member"

    text = (
        f"👋 Salom, <b>{full_name}</b>!\n\n"
        f"Sizga <b>yangi task</b> biriktirildi.\n\n"
        f"📝 <b>Task nomi:</b> {task.title}\n"
        f"🏢 <b>Department:</b> {task.department.name}\n"
        f"📌 <b>Status:</b> {task.status}\n"
        f"🔥 <b>Priority:</b> {task.priority}\n"
    )

    if task.deadline:
        text += f"⏰ <b>Deadline:</b> {task.deadline:%d.%m.%Y %H:%M}\n"

    if task.description:
        text += f"\n📄 <b>Tavsif:</b>\n{task.description}\n"

    text += (
        "\n⚠️ Iltimos, taskni belgilangan muddatda bajarishni unutmang.\n"
        "Agar savollar bo‘lsa, team lead bilan bog‘laning."
    )

    payload = {
        "chat_id": user.telegram_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    response = requests.post(TELEGRAM_API, json=payload, timeout=10)

    if response.status_code != 200:
        raise Exception(response.text)

