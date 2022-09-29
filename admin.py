import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def is_admin(login, pwd):
    df = pd.read_csv('admin/login.csv', sep=',', header=None)
    # print(df.values)

    true_login = str(df[0].values[len(df) - 1])
    true_pwd = str(df[1].values[len(df) - 1])
    # Логин и пароль не могут отсутствовать!!!

    if (login == true_login and pwd == true_pwd):
        return True
    else:
        return False

def main_keyboard():
    keyboard = InlineKeyboardMarkup()
    login_edit = InlineKeyboardButton(text="Изменить логин и пароль", callback_data="login_edit")
    faq_edit = InlineKeyboardButton(text="Изменить FAQ", callback_data="faq_edit")
    keyboard.row(login_edit, faq_edit)
    statistic = InlineKeyboardButton(text="Статистика", callback_data="stats")
    msg_to_all = InlineKeyboardButton(text="Написать сообщение ВСЕМ", callback_data="msg_to_all")
    keyboard.row(statistic, msg_to_all)
    admin_exit = InlineKeyboardButton(text="Выход", callback_data="admin_exit")
    keyboard.add(admin_exit)
    return keyboard


def faq_keyboard():
    keyboard = InlineKeyboardMarkup()
    faq_edit = InlineKeyboardButton(text="Изменить", callback_data="faq_1")
    faq_add = InlineKeyboardButton(text="Добавить", callback_data="faq_2")
    keyboard.row(faq_edit, faq_add)
    faq_exit = InlineKeyboardButton(text="Назад", callback_data="faq_exit")
    keyboard.add(faq_exit)
    return keyboard


def stats_keyboard():
    keyboard = InlineKeyboardMarkup()
    faq_exit = InlineKeyboardButton(text="Назад", callback_data="stats_exit")
    keyboard.add(faq_exit)
    return keyboard

def msg_keyboard():
    keyboard = InlineKeyboardMarkup()
    msg_exit = InlineKeyboardButton(text="Назад", callback_data="stats_exit")
    keyboard.add(msg_exit)
    return keyboard

def faq_show():
    df = pd.read_csv('faq/faq.csv', sep=',', header=None)
    # print(df.values)
    faq_dict = {}

    for row in range(0, len(df)):
        faq_dict[df[0].values[row]] = df[1].values[row]

    return faq_dict
    
def faq_data_kb():
    data = faq_show()
    keyboard = InlineKeyboardMarkup()
    for element in data:
        keyboard.add(InlineKeyboardButton(text=str(element), callback_data=str(element)))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="stats_exit"))
    return keyboard

def choice():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text="Вопрос", callback_data="Вопрос__"), InlineKeyboardButton(text="Ответ", callback_data="Ответ__"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="stats_exit"))
    return keyboard

def current_keyboard(name):
    if name == "main":
        return main_keyboard()
    if name == "faq":
        return faq_keyboard()
    if name == "stats":
        return stats_keyboard()
    if name == "msg":
        return msg_keyboard()
    if name == "faq_data":
        return faq_data_kb()
    if name == "faq_e":
        return choice()


def admin_skills(command, data = None):
    if command == "login_edit":
        data = data.replace(" ",",")
        file_upd = open("admin/login.csv","a+",encoding='utf-8')
        file_upd.write(data + "\n")
        file_upd.close()


def read_all_id():
    pass

def faq_add(q,a):
        file_upd = open("faq/faq.csv","a+",encoding='utf-8')
        file_upd.write(str(q) + "," + str(a) + "\n")
        file_upd.close()

def file_rewrite(data):
        file_upd = open("faq/faq.csv","w",encoding='utf-8')
        for element in data:
            file_upd.write(str(element) + "," + str(data[element]) + "\n")
        file_upd.close()

def upd_q(text, current_data):
    data = faq_show()
    data = {v:k for k, v in data.items()}
    data[current_data[1]] = text
    data = {v:k for k, v in data.items()}
    file_rewrite(data)

def upd_a(text, current_data):
    data = faq_show()
    data[current_data[0]] = text
    file_rewrite(data)