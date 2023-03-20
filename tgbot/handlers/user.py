from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

from tgbot.db.db_api import *
from tgbot.filters.back import BackFilter
from tgbot.keyboards.inline import main_menu_btn, sector_btns, row_btns, place_btns, pay_btn, back_kb, buy_kb
from tgbot.keyboards.reply import contact_btn, remove_btn
from tgbot.misc.send_code import send_code
from tgbot.misc.states import UserStartState, UserMenuState, UserBuyState, UserQuesState


async def user_start(m: Message, status):
    if status:
        await m.answer("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇",
                       reply_markup=main_menu_btn)
        await UserMenuState.get_menu.set()
    else:
        await m.reply("Assalomu alaykum 👋\nUmma Forum botiga xush kelibsiz 😃\nIltimos ismingizni kiriting!")
        await UserStartState.get_name.set()


async def about(c: CallbackQuery, state: FSMContext, config):
    res = await get_about(config)
    await c.message.edit_text(res["text"], reply_markup=back_kb)


async def calls(c: CallbackQuery, state: FSMContext, config):
    res = await get_contacts(config)
    text = "Aloqa raqamlar:\n"
    for i in res:
        text += f"{i['phone']}\n"
    await c.message.edit_text(text, reply_markup=back_kb)


async def req_ques(c: CallbackQuery):
    await c.message.edit_text("Iltimos savolingizni qoldiring 📨\ntez orada mutaxassislarimiz siz\nbilan bog'lanishadi! 👨‍💻", reply_markup=back_kb)
    await UserQuesState.get_ques.set()


async def get_ques(m: Message, config, user):
    await m.bot.send_message(chat_id=config.tg_bot.group_ids, text=f"👤 Ism: {user['user_name']}\n"
                                                                   f"📱 Raqam: {user['user_phone']}\n"
                                                                   f"📋 Savol: {m.text}")
    await m.answer("Qabul qilindi ✅", reply_markup=main_menu_btn)
    await UserMenuState.get_menu.set()


async def get_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer("Iltimos telefon raqamingizni yuboring 📲",
                   reply_markup=contact_btn)
    await UserStartState.next()


async def get_contact(m: Message, state: FSMContext, config):
    phone = m.contact.phone_number
    code = await send_code(phone, config)
    await state.update_data(code=code, phone=phone)
    await m.answer(f"Iltimos telefon raqamingizga kelgan sms kodni kiriting 📲\n"
                   f"{code}", reply_markup=remove_btn)
    await UserStartState.next()


async def get_code(m: Message, state: FSMContext, config):
    code = m.text
    data = await state.get_data()
    if code == str(data['code']):
        await create_user(m.from_user.id, data["name"], data["phone"], config)
        await m.answer("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇",
                       reply_markup=main_menu_btn)
        await UserMenuState.get_menu.set()
    else:
        await m.answer("Notog'ri kod yuborildi ❌\nIltimos qayta urinib ko'ring! 🔄")


async def send_sec(c: CallbackQuery, config):
    sectors = await get_sector(config)
    if len(sectors) == 0:
        return await c.answer("Sektorlar qo'shilmagan")
    await c.message.delete()
    await c.message.answer_photo(photo="https://myday.uz/images/gallery/382.jpg", caption="Iltimos Sektorni tanlang 👇",
                                 reply_markup=await sector_btns(sectors))
    await UserBuyState.get_sec.set()


async def get_sec(c: CallbackQuery, state: FSMContext, config):
    debug = c.bot.get("debug")
    await state.update_data(sector=c.data)
    rows = await get_rows(c.data, config)
    if len(rows) == 0:
        return await c.answer("Qatorlar qo'shilmagan")
    await c.message.delete()
    await c.message.answer_photo(caption=f"{rows[0]['sector']['name']}: {rows[0]['sector']['quantity']} ta qator\nIltimos"
                                 f" qatorlardan birini tanlang\nNarxi {rows[0]['sector']['beg_price']}$ dan"
                                 f" {rows[0]['sector']['end_price']}$ gacha  👇", photo="https://myday.uz/images/gallery/382.jpg" if debug else rows[0]['sector']['image'],
                                 reply_markup=await row_btns(rows))
    await UserBuyState.next()


async def get_row(c: CallbackQuery, state: FSMContext, config):
    await state.update_data(row=c.data)
    places = await get_places(c.data, config)
    if len(places) == 0:
        return await c.answer("Joylar qo'shilmagan")
    await c.message.delete()
    await c.message.answer(f"Bu qatorda {places[0]['row']['quantity']} ta o'riniq mavjud\n"
                           f"Iltimos o'rindiqlardan birini tanlang  👇", reply_markup=await place_btns(places))
    await UserBuyState.next()


async def get_place_us(c: CallbackQuery, state: FSMContext, config):
    if c.data == "wrong":
        return await c.answer("Kechirasiz ammo bu joy band 😔")
    else:
        place = await get_place(c.data, config)
        await state.update_data(place=c.data, price=place['price'])
        await c.message.edit_text(f"Sektor: {place['row']['sector']['name']}\nQator: {place['row']['name']}\nO'rindiq: "
                                  f"{place['name']}\nnarxi: {place['price']} so\'m\nXarid qilishni istaysizm?",
                                  reply_markup=buy_kb)
    await UserBuyState.next()


async def get_conf(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text("To'lov usulini tanlang  👇", reply_markup=pay_btn)
    await UserBuyState.next()


async def get_pay_type(c: CallbackQuery, state: FSMContext, config):
    data = await state.get_data()
    price = LabeledPrice(label="Joy uchun to'lov", amount=int(data["price"]) * 100)
    if c.data == "click":
        photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgWGCXrpS2g54YYm0eTzAHHFzY7Kj3ZXEcbg&usqp=CAU"
        token = config.misc.click
    elif c.data == "payme":
        photo = "https://synthesis.uz/wp-content/uploads/2022/01/payme-1920x1080-1.jpg"
        token = config.misc.payme
    await state.update_data(pay_type=c.data)
    await c.bot.send_invoice(chat_id=c.from_user.id, photo_url=photo, currency="uzs", title="Joy", description="Joy uchun tolov",
                             payload="test-invoice-payload", provider_token=token,
                             prices=[price])
    await UserBuyState.next()
    await c.message.delete()


async def pre_checkout_query(query: PreCheckoutQuery):
    await query.bot.answer_pre_checkout_query(query.id, ok=True)


async def success_payment(m: Message):
    await m.answer("zbs")


async def back(c: CallbackQuery, state: FSMContext):
    await c.message.delete()
    await c.message.answer("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇",
                              reply_markup=main_menu_btn)
    await UserMenuState.get_menu.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_name, state=UserStartState.get_name)
    dp.register_message_handler(get_contact, content_types="contact", state=UserStartState.get_contact)
    dp.register_message_handler(get_code, state=UserStartState.get_code)
    dp.register_callback_query_handler(send_sec, Text(equals="ticket"), state=UserMenuState.get_menu)
    dp.register_callback_query_handler(get_sec, BackFilter(), state=UserBuyState.get_sec)
    dp.register_callback_query_handler(get_row, BackFilter(), state=UserBuyState.get_row)
    dp.register_callback_query_handler(get_place_us, BackFilter(), state=UserBuyState.get_place)
    dp.register_callback_query_handler(get_conf, BackFilter(), state=UserBuyState.get_conf)
    dp.register_callback_query_handler(get_pay_type, BackFilter(), state=UserBuyState.get_pay_type)
    dp.register_callback_query_handler(about, Text(equals="about"), state=UserMenuState.get_menu)
    dp.register_callback_query_handler(calls, Text(equals="call"), state=UserMenuState.get_menu)
    dp.register_callback_query_handler(req_ques, Text(equals="question"), state=UserMenuState.get_menu)
    dp.register_message_handler(get_ques, state=UserQuesState.get_ques)
    dp.register_message_handler(success_payment, state=UserBuyState.get_success)
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True, state=UserBuyState.get_query)
    dp.register_callback_query_handler(back, state="*")


