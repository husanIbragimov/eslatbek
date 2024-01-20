import datetime
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from data.api import create_target, get_weekdays
from loader import dp, bot
from keyboards.default.defoult_btn import menu_btn
from keyboards.inline.inline_btn import get_target_btn, choose_weekday_btn, choose_hours_btn, get_calendar


@dp.message_handler(text="💡 Yangi maqsad qo'shish", state=None)
async def add_target(message: types.Message, state=FSMContext):
    await message.answer("Maqsadingiz nomini kiriting", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("add_target")


@dp.message_handler(state="add_target")
async def add_target(message: types.Message, state=FSMContext):
    target_name = message.text
    await state.update_data(target_name=target_name)
    # await message.answer(f"{target_name} tanlandi")
    await message.answer("Maqsadingiz haqida ma'lumot kiriting")
    await state.set_state("target_description")


@dp.message_handler(state="target_description")
async def target_description(message: types.Message, state=FSMContext):
    target_description = message.text
    await state.update_data(target_description=target_description)
    # await message.answer(f"{target_description} tanlandi")
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    await message.answer("Ushbu maqsadga erishish uchun qachondan harakatni boshlamoqchisiz?", reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await state.set_state("start_date")


@dp.callback_query_handler(text="previous_month", state="start_date")
async def previous_month(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    year = data["year"]
    month = data["month"]
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    await call.message.edit_reply_markup(reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await call.answer(cache_time=1)
    await state.set_state("start_date")


@dp.callback_query_handler(text="next_month", state="start_date")
async def next_month(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    year = data["year"]
    month = data["month"]
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    await call.message.edit_reply_markup(reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await call.answer(cache_time=1)
    await state.set_state("start_date")


@dp.callback_query_handler(text="ignore", state="*")
async def ignore(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    await call.answer()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("select_day"), state="start_date")
async def select_day(callback_query: types.CallbackQuery, state=FSMContext):
    await callback_query.message.delete()

    data = callback_query.data.split("_")
    selected_day = int(data[2])
    selected_month = int(data[3])
    selected_year = int(data[4])

    selected_start_date = datetime.date(selected_year, selected_month, selected_day)
    if selected_start_date < datetime.date.today():
        await bot.send_message(callback_query.from_user.id, "Boshlanish sanasi bugundan oldin bo'lishi mumkin emas")
            
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        await callback_query.message.answer("Ushbu maqsadga erishish uchun qachondan harakatni boshlamoqchisiz?", reply_markup=get_calendar(year, month))
        await state.update_data(month=month, year=year)
        await state.set_state("start_date")
        return
    
    await state.update_data(selected_start_date=selected_start_date)

    await bot.send_message(callback_query.from_user.id, f"Harakatni boshlash sanasi: {selected_start_date}")
    # await callback_query.answer()
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    await callback_query.message.answer("Ushbu maqsadingizga qachongacha erishmoqchisiz?", reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await state.set_state("end_date")


@dp.callback_query_handler(text="previous_month", state="end_date")
async def previous_month(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    year = data["year"]
    month = data["month"]
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    await call.message.edit_reply_markup(reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await call.answer(cache_time=1)
    await state.set_state("end_date")


@dp.callback_query_handler(text="next_month", state="end_date")
async def next_month(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    year = data["year"]
    month = data["month"]
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    await call.message.edit_reply_markup(reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await call.answer(cache_time=1)
    await state.set_state("end_date")


# @dp.callback_query_handler(text="ignore", state="*")
# async def ignore(call: types.CallbackQuery, state=FSMContext):
#     await call.answer(cache_time=1)
#     await call.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("select_day"), state="end_date")
async def select_day(callback_query: types.CallbackQuery, state=FSMContext):
    await callback_query.message.delete()

    data = callback_query.data.split("_")
    selected_day = int(data[2])
    selected_month = int(data[3])
    selected_year = int(data[4])
    start_date_data = await state.get_data()
    start_date = start_date_data["selected_start_date"] #2023-11-26
    
    selected_end_date = datetime.date(selected_year, selected_month, selected_day)
    if selected_end_date < start_date + datetime.timedelta(days=7):
        await bot.send_message(callback_query.from_user.id, "Tugatish sanasi kamida 1 hafta bo'lishi kerak !")
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        await callback_query.message.answer("Tugash sanasini tanlang.", reply_markup=get_calendar(year, month))
        await state.update_data(month=month, year=year)
        await state.set_state("end_date")
        return
    
    await state.update_data(selected_end_date=selected_end_date)

    await bot.send_message(callback_query.from_user.id, f"Tugash sanasi: {selected_end_date}")
    # await callback_query.answer()

    checked = {
        "monday": False,
        "tuesday": False,
        "wednesday": False,
        "thursday": False,
        "friday": False,
        "saturday": False,
        "sunday": False,
        "all_weekdays": False,
    }
    await state.update_data(checked=checked)
    await bot.send_message(callback_query.from_user.id, "O'zingizga qulay kunlarni belgilang",
                           reply_markup=await choose_weekday_btn(checked=checked))
    await state.set_state("chose_weekdays")


weeks = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


@dp.callback_query_handler(text=weeks, state="chose_weekdays")
async def weekdays(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    checked = data["checked"]
    checked[call.data] = not checked[call.data]

    await state.update_data(checked=checked)

    await call.message.edit_reply_markup(reply_markup=await choose_weekday_btn(checked=checked))
    await call.answer(f"{call.data} tanlandi")
    await state.set_state("chose_weekdays")


@dp.callback_query_handler(text_contains="all_weekdays", state="chose_weekdays")
async def all_weekdays(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    check = data["checked"]["all_weekdays"]
    if not check:
        checked = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": True,
            "sunday": True,
            "all_weekdays": True,
        }
    else:
        checked = {
            "monday": False,
            "tuesday": False,
            "wednesday": False,
            "thursday": False,
            "friday": False,
            "saturday": False,
            "sunday": False,
            "all_weekdays": False,
        }

    # await call.message.answer("Hafta kunini tanlang", reply_markup=choose_weekday_btn(checked=checked))
    await state.update_data(checked=checked)
    await call.message.edit_reply_markup(reply_markup=await choose_weekday_btn(checked=checked))
    await state.set_state("chose_weekdays")


@dp.callback_query_handler(text="choosen_weekdays", state="chose_weekdays")
async def choosen_weekdays(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    # await call.message.answer(data)
    await call.message.delete()
    await call.answer(cache_time=1)
    await call.message.answer("O'zingizga qulay vaqtni belgilang: ", reply_markup=choose_hours_btn())
    await state.set_state("chose_hours")


@dp.callback_query_handler(state="chose_hours")
async def choosen_hours(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    hours = call.data
    # await state.update_data(hours=hours)

    await call.message.answer(f"Soat: {hours} tanlandi")
    await call.answer(cache_time=1)

    data = await state.get_data()
    target_name = data["target_name"]
    target_description = data["target_description"]
    selected_start_date = data["selected_start_date"]
    selected_end_date = data["selected_end_date"]
    hours = hours
    checked = data["checked"]
    print(checked)
    weekdays = []
    l = list()
    for i in weeks:
        try:
            if checked[i]:
                weekdays.append(i)
        except:
            pass
        
    db_week = await get_weekdays()
    print(weekdays)
    print(db_week)
    
    # weekdays = ", ".join(i for i in weekdays)
    week_days = [i['id'] for i in db_week if i["weekday"] in weekdays]
    print(week_days)
    # print(weekdays)
    is_active = True
    # await call.message.answer("Target qo'shildi")
    # await call.message.answer(f"Target nomi: {target_name}")
    # await call.message.answer(f"Target tavsifi: {target_description}")
    # await call.message.answer(f"Target boshlanish sanasi: {selected_start_date}")
    # await call.message.answer(f"Target tugash sanasi: {selected_end_date}")
    # await call.message.answer(f"Target hafta kunlari: {weekdays}")
    # await call.message.answer(f"Target vaqti: {hours}")
    # await call.message.answer(f"Target statusi: {is_active}")
    
    s = await create_target(telegram_id=call.from_user.id,
                        name=target_name,
                        description=target_description,
                        start_date=selected_start_date,
                        end_date=selected_end_date,
                        weekday=week_days,
                        time=hours,
                        is_active=is_active)
    await state.finish()
    print(s)
    await call.message.answer("Maqsadlar ro'yxatiga qo'shildi ✅", reply_markup=menu_btn)



