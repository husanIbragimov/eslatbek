from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Mening maqsadlarim"),
        ],
        [
            KeyboardButton(text="💡 Yangi maqsad qo'shish"),
        ],
        [
            KeyboardButton(text="👤 Ma'lumotlarim"),
        ],
        [
            KeyboardButton(text="Foydali Linklar"),
            KeyboardButton(text="Foydali Kitoblar"),
        ],

    ],
    resize_keyboard=True, input_field_placeholder="Menu")


phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni yuborish", request_contact=True),
        ],

        ],
    resize_keyboard=True, input_field_placeholder="Menu")

phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni yuborish", request_contact=True),
        ],

        ],
    resize_keyboard=True, input_field_placeholder="Menu")

def get_my_targets_btn(targets):
    my_targets_btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, input_field_placeholder="My Targets")

    for i in targets:
        my_targets_btn.insert(KeyboardButton(text=f"{i['name']}"))

    my_targets_btn.add(KeyboardButton(text=f"🔙 Ortga"))

    return my_targets_btn



def get_book_category_btn(books_category):

    books_category_btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, input_field_placeholder="Bo'limlardan birini tanlang")

    for i in books_category:
        books_category_btn.insert(KeyboardButton(text=f"{i['name']}"))

    books_category_btn.add(KeyboardButton(text=f"🔙 Ortga"))

    return books_category_btn
