from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


back_btn = InlineKeyboardButton("🔙 Orqaga", callback_data="back")

pay_btn = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Click", callback_data='click'),
                                                InlineKeyboardButton("Payme", callback_data='payme'),
                                                back_btn)

back_kb = InlineKeyboardMarkup(row_width=1).add(back_btn)


main_menu_btn = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Bilet xarid qilish 🛒", callback_data="ticket"),
        InlineKeyboardButton("QR code ni olish 📋", callback_data="qr"),
        InlineKeyboardButton("Umma forum haqida 👥", callback_data="about"),
        InlineKeyboardButton("Savol qoldirish 📩", callback_data="question"),
        InlineKeyboardButton("Aloqa 👨‍💻", callback_data="call"))

buy_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("✅ Xarid", callback_data="buy"),
                                                back_btn)


async def sector_btns(sectors):
    sector_btn = InlineKeyboardMarkup(row_width=3)
    for sector in sectors:
        sector_btn.insert(InlineKeyboardButton(text=sector["name"], callback_data=sector["id"]))
    sector_btn.add(back_btn)
    return sector_btn


async def row_btns(rows):
    row_btn = InlineKeyboardMarkup(row_width=4)
    for row in rows:
        row_btn.insert(InlineKeyboardButton(row["name"], callback_data=row["id"]))
    row_btn.add(back_btn)
    return row_btn


async def place_btns(places):
    place_btn = InlineKeyboardMarkup(row_width=3)
    for place in places:
        if place["status"]:
            place_btn.insert(InlineKeyboardButton(place["name"], callback_data=place["id"]))
        else:
            place_btn.add(InlineKeyboardButton(f'🚫 {place["name"]}', callback_data="wrong"))
    place_btn.add(back_btn)
    return place_btn

