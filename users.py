import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def read_s():
    data = []
    for number in range (1,5):
        df = pd.read_excel('4services/4serv.xlsx', sheet_name=f'Услуга {number}', header=None)
        for i in range(0, df.shape[0]):
            data.append({'header' : df[0][i], 'q' : df[1][i], 'a' : df[2][i]})
    return data

def encoding(text):
    data = read_s()
    for el in data:
        if el['header'][:20] == text:
            return el['header']

def encoding_mark(text):
    if text == '✅':
        return True
    else:
         return False

def u_start_keyboard():
    data = read_s()
    headers = []
    for el in data:
        if not el['header'] in headers:
            headers.append(el['header'])

    keyboard = InlineKeyboardMarkup()
    for element in headers:
        keyboard.add(InlineKeyboardButton(text=str(element), callback_data=str(element[:20])))
    keyboard.add(InlineKeyboardButton(text='FAQ', callback_data='show_faq'))
    return keyboard

def u_q_keyboard(header):
    data = read_s()
    q = []
    for el in data:
        if el['header'][:20] == header:
            q.append(el['q'])

    keyboard = InlineKeyboardMarkup()
    for element in q:
        keyboard.add(InlineKeyboardButton(text=str(element), callback_data=str(element[:20])))
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="stats_exit"), InlineKeyboardButton(text="Оценить", callback_data="set_mark"))
    return keyboard

def u_a_keyboard(category, q):
    data = read_s()
    a = []

    for el in data:
        if el['header'][:20] == category and el['q'][:20] == q:
            a.append(el['a'])

    if len(a) != 0:
        return a[0]
    else:
        return 'Ответ не найден'

def mark_btns():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text='✅', callback_data='✅'), InlineKeyboardButton(text='❌', callback_data='❌'))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="stats_exit"))
    return keyboard


def stats_record(category, mark):

    main_stats = False
    mark = encoding_mark(mark)

    try:
        file_check = open("stats/stats.csv","r",encoding='utf-8')
        lines = file_check.readlines()

        main_stats = []

        for line in lines:
            arr = []
            line = line.replace("\n","")
            line = line.split(",")
            arr = [line[0], line[1], line[2]]
            main_stats.append(arr)

        file_check.close()
    except Exception as ex:
        pass

    if not main_stats or len(main_stats) == 0:
        file_upd = open("stats/stats.csv","a+",encoding='utf-8')
        if mark:
            file_upd.write(category + "," + str(1) + "," + str(0) + "\n")
        else: 
            file_upd.write(category + "," + str(0) + "," + str(1) + "\n")
        file_upd.close()
    else:
        exists = False
        for element in main_stats:
            if element[0] == category:
                exists = True
                if mark:
                    element[1] = int(element[1]) + 1
                else:
                    element[2] = int(element[2]) + 1
        
        if not exists:
            arr = []
            arr.append(category)
            if mark:
                arr.append(1)
                arr.append(0)
            else:
                arr.append(0)
                arr.append(1)
            main_stats.append(arr)

        file_upd = open("stats/stats.csv","w+",encoding='utf-8')
        for element in main_stats:
            file_upd.write(element[0] + "," + str(element[1]) + "," + str(element[2]) + "\n")
        file_upd.close()