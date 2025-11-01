import json
from datetime import datetime

import requests

from config import TOKEN


TG_BOT_URL = f"https://api.telegram.org/bot{TOKEN}"
USERS_FILE = "users.json"


def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def add_user(user_data):
    users = load_users()
    if not any(u["id"] == user_data["id"] for u in users):
        users.append(user_data)
        save_users(users)


def get_updates(offset=None, limit=100):
    url = f"{TG_BOT_URL}/getUpdates"
    params = {"offset": offset, "limit": limit}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["result"]
    return []


def send_message(chat_id, text):
    url = f"{TG_BOT_URL}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    requests.get(url, params=params)


def send_photo(chat_id, photo_id):
    url = f"{TG_BOT_URL}/sendPhoto"
    params = {"chat_id": chat_id, "photo": photo_id}
    requests.get(url, params=params)


def send_document(chat_id, file_id):
    url = f"{TG_BOT_URL}/sendDocument"
    params = {"chat_id": chat_id, "document": file_id}
    requests.get(url, params=params)


def send_audio(chat_id, file_id):
    url = f"{TG_BOT_URL}/sendAudio"
    params = {"chat_id": chat_id, "audio": file_id}
    requests.get(url, params=params)


def send_voice(chat_id, file_id):
    url = f"{TG_BOT_URL}/sendVoice"
    params = {"chat_id": chat_id, "voice": file_id}
    requests.get(url, params=params)


def send_video(chat_id, file_id):
    url = f"{TG_BOT_URL}/sendVideo"
    params = {"chat_id": chat_id, "video": file_id}
    requests.get(url, params=params)


def send_sticker(chat_id, file_id):
    url = f"{TG_BOT_URL}/sendSticker"
    params = {"chat_id": chat_id, "sticker": file_id}
    requests.get(url, params=params)


def send_contact(chat_id, phone_number, first_name, last_name=None):
    url = f"{TG_BOT_URL}/sendContact"
    params = {
        "chat_id": chat_id,
        "phone_number": phone_number,
        "first_name": first_name,
        "last_name": last_name or "",
    }
    requests.get(url, params=params)


def send_dice(chat_id, emoji="🎲"):
    url = f"{TG_BOT_URL}/sendDice"
    params = {"chat_id": chat_id, "emoji": emoji}
    requests.get(url, params=params)


def main():
    offset = None
    print("Bot ishga tushdi...")

    while True:
        updates = get_updates(offset)
        for update in updates:
            if "message" not in update:
                continue

            message = update["message"]
            chat_id = message["chat"]["id"]
            offset = update["update_id"] + 1

            if "text" in message and message["text"] == "/start":
                user = message["from"]
                user_data = {
                    "id": user["id"],
                    "username": user.get("username"),
                    "first_name": user.get("first_name"),
                    "last_name": user.get("last_name"),
                    "language_code": user.get("language_code"),
                    "joined_at": datetime.utcnow().isoformat(),
                }
                add_user(user_data)
                send_message(chat_id, "Salom! Siz bazaga saqlandingiz. Nima yuborsangiz, shuni qaytaraman.")
                continue

            if "text" in message:
                send_message(chat_id, message["text"])

            elif "photo" in message:
                photo = message["photo"][-1]["file_id"]
                send_photo(chat_id, photo)

            elif "document" in message:
                send_document(chat_id, message["document"]["file_id"])

            elif "audio" in message:
                send_audio(chat_id, message["audio"]["file_id"])

            elif "voice" in message:
                send_voice(chat_id, message["voice"]["file_id"])

            elif "video" in message:
                send_video(chat_id, message["video"]["file_id"])

            elif "sticker" in message:
                send_sticker(chat_id, message["sticker"]["file_id"])

            elif "contact" in message:
                contact = message["contact"]
                send_contact(
                    chat_id,
                    contact["phone_number"],
                    contact["first_name"],
                    contact.get("last_name"),
                )

            elif "dice" in message:
                send_dice(chat_id, message["dice"]["emoji"])

            else:
                send_message(chat_id, "Bu turdagi xabarni hali echo qila olmayman.")


main()
