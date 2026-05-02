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
SESSION_STRING = "1ApWapzMBu4J8EHPOJvj1-SDQONiR-jNj6Blha9e5MNDViPDUi_GHjyvpwU8LC61xr3iFvcT5e3hhId6Zg7P1QJ4xGVkWkt9sA_7LqgIFA_r0GecMB4gNds8oHAb2PZ_3O8J5DqtjhtHa98iCXbFLXFpYDir6DNm-Hsn9BI7TmKAEf6EbtWOWSw8-_oFBGS94zcY8cX_sIH4GVYP856YjYUP1byp63Drpv5syBMr7LgvKVOdlsQNR5lknkURLdM6OnnewuMdWW4yKXJAYy6XruwZI5xQymsNe9peaPsmgzBo0myOWnyC2nY5T2s1Rhtbicxm1iMkKQNs0K9736B8w1kg2XT9nGfs="

WEATHER_API_KEY = "501c16a296be1c368b4865b05b6a1994"  # openweathermap.org dan oling
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

bio_index = 0

def get_bio():
    global bio_index
    now = datetime.now(TIMEZONE)
    soat = now.hour
    soat_str = now.strftime("%H:%M")
    kun = now.day
    oy = OYLAR[now.month]
    yil = now.year
    hafta = HAFTA_KUNLARI[now.weekday()]
    yil_kuni = now.timetuple().tm_yday

    # Tungi bio (00:00 - 06:00)
    if 0 <= soat < 6:
        return (
            f"🌙 Hayrli tun!\n"
            f"Yaxshi uxlang! 😴\n"
            f"📅 {kun} {oy} {yil} | ⏰ {soat_str}"
        )

    # Ertalabki bio (06:00 - 07:00)
    if 6 <= soat < 7:
        return (
            f"🌅 Hayrli tong!\n"
            f"Yaxshi dam oldingmi?\n"
            f"📅 {kun} {oy} {yil} | ⏰ {soat_str}"
        )

    # Kun davomida — 4 bio almashib turadi
    temp, wind, desc, sunrise, sunset = get_weather()

    bios = [
        # 1 - Universitet
        (
            f"꧁ UBS | Arxitektura ꧂\n"
            f"🖥 AutoCAD•3Ds Max•Corona\n"
            f"📅 {kun} {oy} | ⏰ {soat_str}\n"
            f"📆 {yil_kuni}-kun | Maqsadlar sari! 🎯"
        ),
        # 2 - Ob-havo
        (
            f"📅 {hafta} | {kun} {oy} {yil}\n"
            f"🌤 Buxoro: +{temp}°C {desc}\n"
            f"⏰ {soat_str} | 💨 {wind} m/s\n"
            f"🌅 {sunrise} | 🌇 {sunset}"
        ),
        # 3 - Zerikkanda
        (
            f"😎 Burxon Xayrullayev\n"
            f"zerikkanda qilgan ishi\n"
            f"⏰ {soat_str} | {kun} {oy} {yil}\n"
            f"🔥 Bio bot!"
        ),
    ]

    bio = bios[bio_index % len(bios)]
    bio_index += 1
    return bio

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
            await asyncio.sleep(600)  # 10 daqiqada bir

if __name__ == "__main__":
    asyncio.run(main())
