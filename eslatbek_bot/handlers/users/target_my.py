from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.defoult_btn import menu_btn, phone_btn, get_my_targets_btn
from keyboards.inline.inline_btn import target_delete_btn, view_progress_target_btn
from loader import dp, bot
from data.api import get_my_targets, delete_target, get_weekdays


@dp.message_handler(text="📝 Mening maqsadlarim")
async def View_My_Targets(message: types.Message, state=FSMContext):
    targets = await get_my_targets(message.from_user.id)
    if targets:
        await message.answer("Sizning Maqsadlaringiz: ", reply_markup=get_my_targets_btn(targets['user_targets']))
        await state.update_data(targets=targets['user_targets'])
        await state.set_state("get_my_targets")
    else:
        await message.answer("Sizning Maqsadlaringiz yo'q 😢.", reply_markup=menu_btn)

@dp.message_handler(text="🔙 Ortga", state="get_my_targets")
async def my_targets(message: types.Message, state=FSMContext):
    await message.answer("Menu", reply_markup=menu_btn)
    await state.finish()

@dp.message_handler(state="get_my_targets")
async def my_targets(message: types.Message, state=FSMContext):
    targets_ = await get_my_targets(message.from_user.id)
    targets = targets_['user_targets']
    if not targets:
        await message.answer("Sizda hali maqsadlar yo'q 🥲.")
        return


    selected_target = message.text
    tar = ""
    for i in targets:
        if selected_target == i['name']:
            weekdays = await get_weekdays()
            hafta_kunlari = ", ".join(a['weekday'] for a in weekdays if a['id'] in i['weekday'])
            # print(hafta_kunlari)
            # print(i['weekday'])

            tar += f"⚙️ <b>Nomi: </b> {i['name']}\n"
            tar += f"🔘 <b>Tavsifi: </b>{i['description']}\n"
            tar += f"📆 <b>Hafta kunlari:</b> {hafta_kunlari}\n"
            tar += f"🕔 <b>Boshlanish: </b>{i['start_date']}\n"
            tar += f"🕠 <b>Tugash: </b>{i['end_date']}\n"
            tar += f"⏳ <b>Vaqt: </b>{i['time']}\n"
            if i['status'] == "new":
                tar += f"🟢 <b>Status: </b>Hali boshlanmagan\n\n"
                await message.answer(tar, reply_markup=target_delete_btn(i['id']))
            elif i['status'] == "process":
                tar += f"🟡 <b>Status: </b>Jarayonda\n\n"
                await message.answer(tar, reply_markup=view_progress_target_btn(i['id']))
            else:
                tar += f"🔴 <b>Status:</b> Tugagan\n\n"
                await message.answer(tar)
            break


    await state.set_state("get_my_targets")


@dp.callback_query_handler(text_contains="delete", state="get_my_targets")
async def delete_target_func(call: types.CallbackQuery, state=FSMContext):
    target_id = call.data.split("_")[1]
    await delete_target(target_id)
    await call.message.delete()
    await call.message.answer("Target o'chirildi ✅")

    targets = await get_my_targets(call.from_user.id)
    if targets:
        await call.message.answer("Sizning Targetlariz: ", reply_markup=get_my_targets_btn(targets['user_targets']))
        await state.update_data(targets=targets['user_targets'])
        await state.set_state("get_my_targets")
    else:
        await call.message.answer("Sizning Targetlariz yo'q", reply_markup=menu_btn)
        await state.finish()



