import logging
from admin import is_admin, current_keyboard, admin_skills
from logs import User_log as ul

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '5683599741:AAEAaqWehHZX9zzDyEvH9q3g0D3tHDaVR-I'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

admin = False
auto_status = False
login_edit_status = False
user = ul() #объявляем пользователя
keyboards = {
    0: "main",
    1: "faq",
    2: "stats",
    3: "msg"
}
selected_keyboard = None

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}\nЧем я могу помочь?\n\nКоманды:\n\nПроверить статус - /whoami\nПанель администратора - /access")

    user.id = message.chat.id
    user.fname = message.from_user.first_name
    user.lname = message.from_user.last_name
    user.nickname = message.from_user.username
    user.user_record()

@dp.message_handler(commands=['access'])
async def access(message: types.Message):

    global auto_status

    if admin:
        await message.answer("Вы уже администратор", reply_markup=current_keyboard(keyboards[0]))
        return False

    await message.answer("Введите данные для входа\nПример сообщения для авторизации: 'admin 1234'\nПишите логин и пароль СТРОГО в одном сообщении")
    auto_status = True


@dp.message_handler(commands=['whoami'])
async def whoami(message: types.Message):
    if admin:
        await message.reply("Admin")
    else:
        await message.reply("User")


@dp.message_handler()
async def common_answer(message: types.Message):

    global auto_status
    global login_edit_status
    global selected_keyboard
    global admin

    if auto_status:
        auto_status = False
        login_data = message.text.split(" ")
        # print(login_data)
        admin = is_admin(login_data[0],login_data[1])
        if admin:
            selected_keyboard = keyboards[0]
            await message.answer("Панель администратора:\n\nЗдесь представлен набор функций для управления ботом. Приятной работы!", reply_markup=current_keyboard(keyboards[0]))
        else:
            await message.answer("Вход не выполнен. Проверьте корректность введённых данных")


    if login_edit_status:
        login_edit_status = False
        new_login_and_pwd = message.text.split(" ")
        if len(new_login_and_pwd) == 2:
            admin_skills("login_edit", message.text)
            selected_keyboard = keyboards[0]
            await message.answer("Логин и пароль успешно изменён!", reply_markup=current_keyboard(keyboards[0]))
        else:
            selected_keyboard = keyboards[0]
            await message.answer("Некорректные данные!", reply_markup=current_keyboard(keyboards[0]))


# Изменение логина и пароля
@dp.callback_query_handler(text="login_edit")
async def new_answer(callback: types.CallbackQuery):

    global login_edit_status
    global selected_keyboard

    if admin:
        login_edit_status = True
        selected_keyboard = None
        await callback.message.edit_text("Редактирование данных:\nПожалуйста, отправьте новый логин и пароль ОДНИМ сообщением", reply_markup=None)


@dp.callback_query_handler(text="admin_exit")
async def new_answer(callback: types.CallbackQuery):

    global admin
    admin = False

    await callback.message.answer("Вы вышли из панели администратора")


@dp.callback_query_handler(text="faq_edit")
async def new_answer(callback: types.CallbackQuery):

    global selected_keyboard
    
    if admin:
        selected_keyboard = keyboards[1]
        await callback.message.edit_text("Выберите опцию:", reply_markup=current_keyboard(keyboards[1]))


@dp.callback_query_handler(text="faq_exit")
async def new_answer(callback: types.CallbackQuery):

    global selected_keyboard
    
    if admin:
        selected_keyboard = keyboards[0]
        await callback.message.edit_text("Панель администратора:\n\nЗдесь представлен набор функций для управления ботом. Приятной работы!", reply_markup=current_keyboard(keyboards[0]))


@dp.callback_query_handler(text="stats")
async def new_answer(callback: types.CallbackQuery):

    global selected_keyboard
    
    if admin:
        selected_keyboard = keyboards[2]
        await callback.message.edit_text("Статистика:\n\n✅Услуга 1: 224 \n✅Услуга 2: 24 \n✅Услуга 3: 1320 \n✅Услуга 4: 2422", reply_markup=current_keyboard(keyboards[2]))


@dp.callback_query_handler(text="stats_exit")
async def new_answer(callback: types.CallbackQuery):

    global selected_keyboard
    
    if admin:
        selected_keyboard = keyboards[0]
        await callback.message.edit_text("Панель администратора:\n\nЗдесь представлен набор функций для управления ботом. Приятной работы!", reply_markup=current_keyboard(keyboards[0]))

# @dp.callback_query_handler(text="++")
# async def new_answer(callback: types.CallbackQuery):
#     await callback.message.answer("Выбрано ++")
#     INKB2 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text="++---", callback_data="++"))\
#         .add(InlineKeyboardButton(text="+----", callback_data="+"))\
#         .add(InlineKeyboardButton(text="-----", callback_data="--")) 
#     await callback.message.edit_text("a ntgth", reply_markup=INKB2)


# if __name__ == '__main__':
executor.start_polling(dp, skip_updates=True)