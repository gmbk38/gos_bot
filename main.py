import logging
from admin import faq_data_kb, is_admin, current_keyboard, admin_skills, faq_add, faq_show, upd_q, upd_a, get_stats, get_users
from user_conf import mark_btns, u_start_keyboard, u_q_keyboard, u_a_keyboard, stats_record
from extra_func import chat_type as ct
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
msg_to_all_status = False
faq_add_status = False
faq_edit_status = False

q_add = False
q_edit = False
a_edit = False

user_check_faq = False
user_category = False

current_data = []
user = ul() #объявляем пользователя
keyboards = {
    0: "main",
    1: "faq",
    2: "stats",
    3: "msg",
    400: "faq_data", 
    401: "faq_e"
}
selected_keyboard = None


@dp.message_handler(commands=['start', 'help'])
async def start_ans(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}\nЧем я могу помочь?\n\nКоманды:\n\nПроверить статус - /whoami\nПанель администратора - /access", reply_markup=u_start_keyboard())

    if not ct(message):
        return False

    global user_category
    user_category = False

    user.id = message.chat.id
    user.fname = message.from_user.first_name
    user.lname = message.from_user.last_name
    user.nickname = message.from_user.username
    user.user_record()

# @dp.message_handler(commands=['chat'])
# async def send_welcome(message: types.Message):
#     await message.answer(f"Всё украл")
#     element = await bot.get_chat(message.chat.id) #Вся инфа о чате
#     element2 = await bot.get_chat_members_count(message.chat.id)
#     # bot.ban_chat_member(chat_id, user_id, datetime.now() + timedelta(days=1))
#     # element3 = await bot.get_chat_member(message.from_user.id)
#     # async for member in bot.get_chat_members(message.chat.id):
#     #     print(member)
#     print(element)
#     print(element2)
#     print(message.chat.id)
#     print(message.from_user.id, message.from_user.full_name, message.from_user.last_name, message.from_user.first_name, message.from_user.username)
#     await message.answer(f"{message.from_user.id} , {message.from_user.full_name} , {message.from_user.last_name} , {message.from_user.first_name} , {message.from_user.username}")
#     # print(element3)
#     print(message.chat.type) #private supergroup

@dp.message_handler(commands=['access'])
async def access_ans(message: types.Message):

    global auto_status

    if not ct(message):
        return False

    if admin and ct(message):
        await message.answer("Вы уже администратор", reply_markup=current_keyboard(keyboards[0]))
        return False
    else:
        await message.answer("Введите данные для входа\nПример сообщения для авторизации: 'admin 1234'\nПишите логин и пароль СТРОГО в одном сообщении")
        auto_status = True


@dp.message_handler(commands=['whoami'])
async def whoami_ans(message: types.Message):
    if admin and ct(message):
        await message.reply("Admin")
    elif ct(message):
        await message.reply("User")
    else:
        return False


@dp.message_handler()
async def common_answer(message: types.Message):

    global auto_status
    global login_edit_status
    global msg_to_all_status
    global faq_add_status
    global faq_edit_status
    global q_add
    global q_edit
    global a_edit
    global current_data
    global selected_keyboard
    global admin

    if not ct(message):

        group = await bot.get_chat(message.chat.id)
        user.id = message.chat.id
        user.fname = group["title"]
        user.lname = group["title"]
        user.nickname = group["title"]
        user.user_record()

        user.id = message.from_user.id
        user.fname = message.from_user.first_name
        user.lname = message.from_user.last_name
        user.nickname = message.from_user.username
        # group = await bot.get_chat(message.chat.id)
        user.user_group_record(group["title"])

    #Заметка
    if auto_status and ct(message):
        auto_status = False
        login_data = message.text.split(" ")
        if len(login_data) != 2:
            await message.answer('Неправильный ввод')
            return False
        else:
        # print(login_data)
            admin = is_admin(login_data[0],login_data[1])
        if admin:
            selected_keyboard = keyboards[0]
            await message.answer("Панель администратора:\n\nЗдесь представлен набор функций для управления ботом. Приятной работы!", reply_markup=current_keyboard(keyboards[0]))
            # await message.delete()
        else:
            await message.answer("Вход не выполнен. Проверьте корректность введённых данных")


    if faq_edit_status and ct(message) and admin:
        faq_edit_status = False
        if q_edit:
            upd_q(message.text , current_data)
            q_edit = False
            current_data = []
        else:
            upd_a(message.text , current_data)
            a_edit = False
            current_data = []
        await message.answer("Данные успешно обновлены", reply_markup=current_keyboard(keyboards[0]))


    if login_edit_status and ct(message) and admin:
        login_edit_status = False
        new_login_and_pwd = message.text.split(" ")
        if len(new_login_and_pwd) == 2:
            admin_skills("login_edit", message.text)
            selected_keyboard = keyboards[0]
            await message.answer("Логин и пароль успешно изменён!", reply_markup=current_keyboard(keyboards[0]))
        else:
            selected_keyboard = keyboards[0]
            await message.answer("Некорректные данные!", reply_markup=current_keyboard(keyboards[0]))


    if msg_to_all_status and ct(message) and admin:
        all_users = get_users()
        for i in all_users:
            await bot.send_message(i,message.text)
        await message.answer("Рассылка выполнена успешно", reply_markup=current_keyboard(keyboards[0]))


    if faq_add_status and ct(message) and admin:
        if q_add:
            faq_add(q_add, message.text)
            q_add = False
            faq_add_status = False
            selected_keyboard = keyboards[0]
            await message.answer("Раздел FAQ успешно обновлён!", reply_markup=current_keyboard(keyboards[0]))
        else:
            q_add = message.text


# Изменение логина и пароля
@dp.callback_query_handler(text="login_edit")
async def login_edit_ans(callback: types.CallbackQuery):

    global login_edit_status
    global selected_keyboard

    if admin and ct(callback.message):
        login_edit_status = True
        selected_keyboard = None
        await callback.message.edit_text("Редактирование данных:\nПожалуйста, отправьте новый логин и пароль ОДНИМ сообщением", reply_markup=current_keyboard(keyboards[2]))


@dp.callback_query_handler(text="admin_exit")
async def admin_exit_ans(callback: types.CallbackQuery):

    global admin

    admin = False
    await callback.message.edit_text("Вы вышли из панели администратора", reply_markup=u_start_keyboard())


@dp.callback_query_handler(text="faq_edit")
async def faq_ans(callback: types.CallbackQuery):

    global selected_keyboard
    
    if admin and ct(callback.message):
        selected_keyboard = keyboards[1]
        await callback.message.edit_text("Выберите опцию:", reply_markup=current_keyboard(keyboards[1]))


@dp.callback_query_handler(text="faq_1")
async def faq_1_ans(callback: types.CallbackQuery):

    global selected_keyboard
    global faq_edit_status
    
    if admin and ct(callback.message):
        faq_edit_status = True
        selected_keyboard = keyboards[400]
        await callback.message.edit_text("Актуальные данные раздела FAQ:" , reply_markup=current_keyboard(keyboards[400]))


@dp.callback_query_handler(text="faq_2")
async def faq_2_ans(callback: types.CallbackQuery):

    global selected_keyboard
    global faq_add_status
    
    if admin and ct(callback.message):
        faq_add_status = True
        selected_keyboard = keyboards[2]
        await callback.message.edit_text("Отправьте вопрос и ответ строго ДВУМЯ сообщениями\nПервое сообщение должно содержать вопрос, второе - ответ", reply_markup=current_keyboard(keyboards[2]))


@dp.callback_query_handler(text="faq_exit")
async def faq_exit_ans(callback: types.CallbackQuery):

    global selected_keyboard
    
    if admin and ct(callback.message):
        selected_keyboard = keyboards[0]
        await callback.message.edit_text("Панель администратора:\n\nЗдесь представлен набор функций для управления ботом. Приятной работы!", reply_markup=current_keyboard(keyboards[0]))


@dp.callback_query_handler(text="msg_to_all")
async def msg_to_all_ans(callback: types.CallbackQuery):

    global selected_keyboard
    global msg_to_all_status
    
    if admin and ct(callback.message):
        msg_to_all_status = True
        selected_keyboard = keyboards[3]
        await callback.message.edit_text("Отправьте сообщение для рассылки в чаты", reply_markup=current_keyboard(keyboards[3]))


@dp.callback_query_handler(text="stats")
async def stats_ans(callback: types.CallbackQuery):

    global selected_keyboard
    
    if admin and ct(callback.message):
        selected_keyboard = keyboards[2]
        await callback.message.edit_text(get_stats(), reply_markup=current_keyboard(keyboards[2]))


@dp.callback_query_handler(text="stats_exit")
async def stats_exit_ans(callback: types.CallbackQuery):

    global selected_keyboard
    global faq_add_status
    global faq_edit_status
    global login_edit_status
    global msg_to_all_status
    global user_category

    user_category = False
    faq_add_status = False
    faq_edit_status = False
    login_edit_status = False
    msg_to_all_status = False
    
    if admin and ct(callback.message):
        selected_keyboard = keyboards[0]
        await callback.message.edit_text("Панель администратора:\n\nЗдесь представлен набор функций для управления ботом. Приятной работы!", reply_markup=current_keyboard(keyboards[0]))
    
    if not admin and ct(callback.message):
        await callback.message.edit_text('Выберите опцию', reply_markup=u_start_keyboard())


@dp.callback_query_handler(text="Вопрос__")
@dp.callback_query_handler(text="Ответ__")
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):

    global q_edit
    global a_edit

    answer_data = query.data

    if answer_data == "Вопрос__":
        q_edit = True
    else:
        a_edit = True

    await query.message.edit_text(f"Введите новые данные", reply_markup=current_keyboard(keyboards[2]))


@dp.callback_query_handler()
async def faq_edit_ans(callback: types.CallbackQuery):
    global faq_edit_status
    global current_data
    global selected_keyboard
    global user_category

    global user_check_faq

    if not admin and callback.data == 'show_faq' and ct(callback.message):
        user_check_faq = True
        await callback.message.edit_text('Выберите интересующий вас вопрос', reply_markup=faq_data_kb())

    elif not admin and ct(callback.message) and user_check_faq:
        user_check_faq = False
        await callback.message.edit_text(f'{faq_show()[callback.data]}', reply_markup=current_keyboard(keyboards[2]))



    elif not admin and not user_category and ct(callback.message):
        user_category = callback.data
        await callback.message.edit_text(f"Выберите вопрос по категории:", reply_markup=u_q_keyboard(callback.data))

    elif not admin and ct(callback.message):

        if callback.data == 'set_mark':
            await callback.message.edit_text('Оцените, помог ли вам этот раздел', reply_markup=mark_btns())

        elif callback.data == '✅' or callback.data == '❌' and ct(callback.message):
            stats_record(user_category, callback.data)
            user_category = False
            await callback.message.edit_text(f'Ваша оценка успешно выставлена. Спасибо, что помогаете нам!', reply_markup=u_start_keyboard())

        elif ct(callback.message):
            await callback.message.answer(u_a_keyboard(user_category, callback.data))

    if not faq_edit_status:
        return False
    elif admin:
        selected_keyboard = keyboards[401]
        await callback.message.edit_text(f"Вопрос:\n\n{callback.data}\n\nОтвет\n\n{faq_show()[callback.data]}", reply_markup=current_keyboard(keyboards[401]))
        current_data = [callback.data, faq_show()[callback.data]]


# if __name__ == '__main__':
executor.start_polling(dp, skip_updates=True)