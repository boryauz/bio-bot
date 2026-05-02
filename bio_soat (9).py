import asyncio
from datetime import datetime
import pytz
import urllib.request
import json
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

# === SOZLAMALAR ===
API_ID = 18512808
API_HASH = "3a93474fc8f3c16eb494faeb41a891c2"
SESSION_STRING = "1ApWapzMBu8Rlxw3XBHxE9Pg6NepFsUx50nY8TTeSH9fTChE8UMn5ExPCEPXSrh1jH7r37do7jofjVxC840OPOV-kr4PkAGBadPolVmMMnmLLl7Zm7APqlYRLsH63bod5OLruCMwjHeApBrRVghnqBXReP6JJQ4AfVMcgJWLuo0rCSHjqfTqmfDlHRKrpyO_481hNfgRCkVzsM-m6xtNxO3dZrEtAcAhYvlIVTW_3OdhbIUOYheFwXQ0YGHiuin7tKcUPzGQBts2Rk6cUjlQq4sWzIbvh0mOKSPVwZScvpO7iBrd2YIv9PwfZCDMbaEqnRIbWIBx1VPSIGfDJrHHWyQ5weUDfKJc="

WEATHER_API_KEY = "501c16a296be1c368b4865b05b6a1994"
CITY = "Bukhara"

TIMEZONE = pytz.timezone("Asia/Tashkent")

HAFTA_KUNLARI = {
    0: "Dushanba", 1: "Seshanba", 2: "Chorshanba",
    3: "Payshanba", 4: "Juma", 5: "Shanba", 6: "Yakshanba"
}
OYLAR = {
    1:"Yanvar",2:"Fevral",3:"Mart",4:"Aprel",
    5:"May",6:"Iyun",7:"Iyul",8:"Avgust",
    9:"Sentabr",10:"Oktabr",11:"Noyabr",12:"Dekabr"
}

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        temp = round(data["main"]["temp"])
        wind = round(data["wind"]["speed"])
        desc = data["weather"][0]["description"].capitalize()
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz=pytz.timezone("Asia/Tashkent")).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz=pytz.timezone("Asia/Tashkent")).strftime("%H:%M")
        return temp, wind, desc, sunrise, sunset
    except:
        return 28, 3, "Quyoshli", "05:12", "19:48"

bio_type = 0
minute_counter = 0

def get_bio():
    global bio_type, minute_counter
    now = datetime.now(TIMEZONE)
    soat = now.hour
    soat_str = now.strftime("%H:%M")
    kun = now.day
    oy = OYLAR[now.month]
    yil = now.year
    hafta = HAFTA_KUNLARI[now.weekday()]
    yil_kuni = now.timetuple().tm_yday

    # 00:00 - 01:00 Hayrli tun
    if soat == 0:
        return (
            f"🌙 Hayrli tun!\n"
            f"Yaxshi uxlang! 😴\n"
            f"📅 {kun} {oy} {yil} | ⏰ {soat_str}"
        )

    # 02:00 - 05:00 Nega uxlamayapsan
    if 2 <= soat < 6:
        return (
            f"😅 Nega uxlamayapsan?\n"
            f"Yarim tun bo'ldi! 🌙\n"
            f"⏰ {soat_str} | Uxla! 😴"
        )

    # 06:00 - 07:00 Hayrli tong
    if soat == 6:
        return (
            f"🌅 Hayrli tong!\n"
            f"Yaxshi dam oldingmi?\n"
            f"📅 {kun} {oy} {yil} | ⏰ {soat_str}"
        )

    # Har 10 daqiqada bio turi o'zgaradi
    if minute_counter % 10 == 0:
        bio_type = (bio_type + 1) % 4
    minute_counter += 1

    # Kun davomida
    temp, wind, desc, sunrise, sunset = get_weather()

    if bio_type == 0:
        return (
            f"꧁ UBS | Arxitektura ꧂\n"
            f"🖥 AutoCAD•3Ds Max•Corona\n"
            f"📅 {kun} {oy} | ⏰ {soat_str}\n"
            f"📆 {yil_kuni}-kun | Maqsadlar sari! 🎯"
        )
    elif bio_type == 1:
        return (
            f"📅 {hafta} | {kun} {oy} {yil}\n"
            f"🌤 Buxoro: +{temp}°C {desc}\n"
            f"⏰ {soat_str} | 💨 {wind} m/s\n"
            f"🌅 {sunrise} | 🌇 {sunset}"
        )
    elif bio_type == 2:
        return (
            f"😎 Burxon Xayrullayev\n"
            f"zerikkanda qilgan ishi\n"
            f"⏰ {soat_str} | {kun} {oy} {yil}\n"
            f"🔥 Bio bot!"
        )
    else:
        return (
            f"📅 Bugun: {hafta} | {kun} {oy}\n"
            f"🌤 Buxoro: +{temp}°C {desc}\n"
            f"✨ Bugungi kun baroqli o'tsin!\n"
            f"⏰ {soat_str}"
        )

async def main():
    print("⏰ Bio boti ishga tushmoqda...")
    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        print("✅ Ulandi!")
        while True:
            bio = get_bio()
            print(f"Bio ({len(bio)} belgi):\n{bio}\n")
            try:
                await client(UpdateProfileRequest(about=bio))
                print("✅ Yangilandi!\n")
            except Exception as e:
                print(f"❌ Xato: {e}\n")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
