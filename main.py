import logging
from admin import is_admin
from logs import User_log as ul

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '5683599741:AAEAaqWehHZX9zzDyEvH9q3g0D3tHDaVR-I'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

admin = False
auto_status = False
user = ul() #объявляем пользователя

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

    user.id = message.chat.id
    user.fname = message.from_user.first_name
    user.lname = message.from_user.last_name
    user.nickname = message.from_user.username
    user.user_record()

@dp.message_handler(commands=['access'])
async def send_welcome(message: types.Message):

    global auto_status

    await message.answer("Введите данные для входа\nПример сообщения для авторизации: 'admin 1234'\nПишите логин и пароль СТРОГО в одном сообщении")
    auto_status = True


@dp.message_handler(commands=['whoami'])
async def send_welcome(message: types.Message):
    if admin:
        await message.reply("Admin")
    else:
        await message.reply("User")

@dp.message_handler()
async def echo(message: types.Message):

    global auto_status
    global admin

    if auto_status:
        auto_status = False
        login_data = message.text.split(" ")
        # print(login_data)
        admin = is_admin(login_data[0],login_data[1])
        if admin:
            await message.answer("Успешно")
        else:
            await message.answer("Вход не выполнен. Проверьте корректность введённых данных")

    INKB = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text="++", callback_data="++"))\
        .add(InlineKeyboardButton(text="+-", callback_data="+"))\
        .add(InlineKeyboardButton(text="--", callback_data="--"))   # Эту инлайн-клаву нужно вкарячить в Send_audio

    await message.answer("вот", reply_markup=INKB)  # сюда
    # await message.answer(message.text)

@dp.callback_query_handler(text="++")
async def new_answer(callback: types.CallbackQuery):
    await callback.message.answer("Выбрано ++")
    INKB2 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text="++---", callback_data="++"))\
        .add(InlineKeyboardButton(text="+----", callback_data="+"))\
        .add(InlineKeyboardButton(text="-----", callback_data="--")) 
    await callback.message.edit_text("a ntgth", reply_markup=INKB2)


# if __name__ == '__main__':
executor.start_polling(dp, skip_updates=True)