import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def is_admin(login, pwd):
    df = pd.read_csv('admin/login.csv', sep=',', header=None)
    # print(df.values)

    true_login = str(df[0].values[0])
    true_pwd = str(df[1].values[0])

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

def admin_skills(command):
    pass