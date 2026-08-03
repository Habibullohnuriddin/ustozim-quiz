#!/usr/bin/env python3
"""
Ustozim Nurim community — kunlik viktorina e'loni.

Guruhga BITTA xabar joylashtiradi: bugungi mavzu, savollar soni va
"▶️ HOZIR BOSHLASH" tugmasi. Tugma viktorina sahifasini ochadi —
savollar u yerda birma-bir beriladi, chat uzayib ketmaydi.

Muhit o'zgaruvchilari (GitHub Secrets / Variables):
  BOT_TOKEN  — Telegram bot tokeni            (secret)
  CHAT_ID    — guruh chat_id                  (secret)
  QUIZ_URL   — viktorina sahifasi manzili     (variable)
  TOPIC_ID   — (ixtiyoriy) forum mavzusi ID   (variable)
  PIN        — (ixtiyoriy) "1" bo'lsa pin qilinadi. DIQQAT: oldingi pinni almashtiradi.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date

API = "https://api.telegram.org/bot{token}/{method}"

# ——— Sozlamalar (index.html dagi qiymatlar bilan BIR XIL bo'lishi shart) ———
START_DATE = date(2026, 8, 4)
WEEKLY_COUNTS = [7, 9, 11, 13, 15]   # 1-, 2-, 3-, 4-hafta va undan keyin
IT_SHARE = 2 / 3

WEEKDAYS_UZ = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba",
               "Juma", "Shanba", "Yakshanba"]
MONTHS_UZ = ["yanvar", "fevral", "mart", "aprel", "may", "iyun",
             "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"]


def call(token, method, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API.format(token=token, method=method),
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": e.read().decode("utf-8", "replace")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def day_index(today=None):
    return max(((today or date.today()) - START_DATE).days, 0)


def today_count(today=None):
    week = day_index(today) // 7
    return WEEKLY_COUNTS[min(week, len(WEEKLY_COUNTS) - 1)]


def build_text(today):
    day = day_index(today)
    total = today_count(today)
    it_count = round(total * IT_SHARE)
    ld_count = total - it_count

    nxt = WEEKLY_COUNTS[min(day // 7 + 1, len(WEEKLY_COUNTS) - 1)]
    growth = ""
    if nxt > total:
        growth = (f"\n📈 <i>{7 - (day % 7)} kundan keyin savollar soni "
                  f"{nxt} taga oshadi.</i>\n")

    return (
        f"🧠 <b>KUNLIK BILIM SINOVI</b>\n"
        f"<i>{today.day}-{MONTHS_UZ[today.month - 1]}, "
        f"{WEEKDAYS_UZ[today.weekday()]}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"Bugun sizni <b>{total} ta savol</b> kutmoqda:\n\n"
        f"💻 IT va dasturlash — <b>{it_count} ta</b>\n"
        f"🌟 Fazilatli liderlik — <b>{ld_count} ta</b>\n\n"
        f"⏱ Taxminan {max(2, round(total / 2))}–{total} daqiqa.\n"
        f"📊 Natijangiz darhol ko'rsatiladi.\n"
        f"{growth}\n"
        f"Tugmani bosing va boshlang 👇"
    )


def main():
    token = os.environ.get("BOT_TOKEN", "").strip()
    chat_id = os.environ.get("CHAT_ID", "").strip()
    quiz_url = os.environ.get("QUIZ_URL", "").strip()

    if not token or not chat_id or not quiz_url:
        print("XATO: BOT_TOKEN, CHAT_ID yoki QUIZ_URL berilmagan.", file=sys.stderr)
        sys.exit(1)

    today = date.today()
    day = day_index(today)
    total = today_count(today)

    payload = {
        "chat_id": chat_id,
        "text": build_text(today),
        "parse_mode": "HTML",
        "link_preview_options": {"is_disabled": True},
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "▶️  HOZIR BOSHLASH", "url": quiz_url}
            ]]
        },
    }

    topic_id = os.environ.get("TOPIC_ID", "").strip()
    if topic_id:
        payload["message_thread_id"] = int(topic_id)

    res = call(token, "sendMessage", payload)
    if not res.get("ok"):
        print("XATO:", res, file=sys.stderr)
        sys.exit(1)

    msg_id = res["result"]["message_id"]
    print(f"E'lon joylashtirildi (message_id={msg_id}). "
          f"Kun #{day + 1}, {day // 7 + 1}-hafta, {total} ta savol.")

    if os.environ.get("PIN", "").strip() == "1":
        pin = call(token, "pinChatMessage", {
            "chat_id": chat_id,
            "message_id": msg_id,
            "disable_notification": True,
        })
        if not pin.get("ok"):
            print("Eslatma: pin qilinmadi:", pin.get("error", pin), file=sys.stderr)


if __name__ == "__main__":
    main()
