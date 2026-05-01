import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

# === SOZLAMALAR ===
API_ID = 18512808
API_HASH = "3a93474fc8f3c16eb494faeb41a891c2"

TIMEZONE = pytz.timezone("Asia/Tashkent")

ANIMATION = ["꧁", "꧂", "༒", "★", "✦", "❋", "⚡", "🌀"]
EMOJIS = ["🔥", "💫", "⚡", "🌟", "🎯", "🚀", "✨", "🏛️", "📐", "🎨", "💥", "🌈", "🦋", "🎭", "🌙", "☀️", "❄️", "🍀"]

SOAT_STILLER = [
    lambda s, m: f"⏰ {s} ★ {m}",
    lambda s, m: f"⏰ {s} 〜 {m}",
    lambda s, m: f"⏰ {s} ◆ {m}",
    lambda s, m: f"⏰ {s} ━ {m}",
    lambda s, m: f"⏰ {s} » {m}",
    lambda s, m: f"⏰ {s} ● {m}",
    lambda s, m: f"⏰ {s} ▶ {m}",
    lambda s, m: f"🕒 {s}:{m}",
    lambda s, m: f"⌚ 『{s}:{m}』",
    lambda s, m: f"⏰ ⟨{s}:{m}⟩",
    lambda s, m: f"⏰ [{s}:{m}]",
    lambda s, m: f"⏰ {s} ➤ {m}",
    lambda s, m: f"⏰ {s}•{m}",
    lambda s, m: f"⏰ {s[0]} {s[1]} : {m[0]} {m[1]}",
]

anim_index = 0
emoji_index = 0
stil_index = 0

def get_soz(soat):
    if 6 <= soat < 8:
        return "Hayrli tong 🌅"
    elif 8 <= soat < 10:
        return "Hayrli kun ☀️"
    elif 10 <= soat < 11:
        import random
        return random.choice(["Havo yaxshimi? 🌤", "Kun isiyabdi 🌡"])
    elif soat == 11:
        return "Obet yaqin 🍽"
    elif 12 <= soat < 13:
        return "Obet vaqti 🍛"
    elif 13 <= soat < 17:
        return "Isib ketdi 🥵"
    elif 17 <= soat < 19:
        return "Shom bo'lyapti 🌆"
    elif soat == 19:
        return "Shom tushdi 🌇"
    elif soat == 20:
        return "Yoqimli ishtaxa 🍽️"
    elif soat == 22:
        return "Hayrli kech 🌙"
    elif soat >= 23 or soat < 3:
        return "Hayrli tun 😴"
    else:
        return "Online 💻"

def get_bio():
    global anim_index, emoji_index, stil_index
    now = datetime.now(TIMEZONE)

    left = ANIMATION[anim_index % len(ANIMATION)]
    anim_index += 1

    emoji = EMOJIS[emoji_index % len(EMOJIS)]
    emoji_index += 1

    stil = SOAT_STILLER[stil_index % len(SOAT_STILLER)]
    stil_index += 1

    oylar = {
        1:"Jan",2:"Feb",3:"Mar",4:"Apr",
        5:"May",6:"Jun",7:"Jul",8:"Aug",
        9:"Sep",10:"Oct",11:"Nov",12:"Dec"
    }

    kun = now.day
    oy = oylar[now.month]
    yil = now.year
    soat = now.strftime("%H")
    daqiqa = now.strftime("%M")
    soat_int = now.hour
    yil_kuni = now.timetuple().tm_yday
    yil_uzunligi = 366 if (yil % 4 == 0) else 365

    soz = get_soz(soat_int)
    soat_str = stil(soat, daqiqa)

    bio = (
        f"{left} UBS | Arxitektura\n"
        f"📅 {kun} {oy} {yil} | {soat_str}\n"
        f"💬 {soz}\n"
        f"📆 {yil_uzunligi} dan {yil_kuni}-kun {emoji}"
    )
    return bio

async def main():
    print("⏰ Bio boti ishga tushmoqda...")
    async with TelegramClient("bio_session", API_ID, API_HASH) as client:
        print("✅ Ulandi!")
        while True:
            bio = get_bio()
            print(f"Bio ({len(bio)} belgi):\n{bio}\n")
            try:
                await client(UpdateProfileRequest(about=bio))
                print("✅ Yangilandi!\n")
            except Exception as e:
                print(f"❌ Xato: {e}\n")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
