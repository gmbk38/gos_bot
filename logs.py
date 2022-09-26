from datetime import datetime
import pandas as pd

class User_log():
    def __init__(self):
        self.id = None
        self.fname = None
        self.lname = None
        self.nickname = None


def user_record(self):

    file_check = open("users/users.csv","r",encoding='utf-8')
    lines = file_check.readlines()
    new_client = True

    for line in lines:
        line = line.replace("\n","")
        line = line.split(",")
        if line[0] == str(self.id) and line[1] == str(self.fname) and line[2] == str(self.lname) and line[3] == str(self.nickname):
            new_client = False
            # print("old")

    file_check.close()

    if new_client:
        # print("new")
        file_upd = open("users/users.csv","a+",encoding='utf-8')
        file_upd.write(str(self.id) + "," + str(self.fname) + "," + str(self.lname) + "," + str(self.nickname) + "\n")
        file_upd.close()


def user_group_record(self, title):
    new_client = True
    try:
        file_check = open("users/" + str(title) + ".csv","r",encoding='utf-8')
        lines = file_check.readlines()

        for line in lines:
            line = line.replace("\n","")
            line = line.split(",")
            if line[0] == str(self.id) and line[1] == str(self.fname) and line[2] == str(self.lname) and line[3] == str(self.nickname):
                new_client = False
                # print("old")

        file_check.close()
    except Exception as ex:
        pass

    if new_client:
        # print("new")
        file_upd = open("users/" + str(title) + ".csv","a+",encoding='utf-8')
        file_upd.write(str(self.id) + "," + str(self.fname) + "," + str(self.lname) + "," + str(self.nickname) + "\n")
        file_upd.close()


def chat_record(self,msg):
    #записываем сообщения пользователя
    file_upd = open("chats/" + str(self.id) + ".txt","a+",encoding='utf-8')
    date = str(datetime.now()).split(".")[0]
    file_upd.write(date + " " + msg + "\n")
    file_upd.close()


def err_record(self,ex):
    #записываем ошибки
    file_upd = open("err/err.txt","a+",encoding='utf-8')
    date = str(datetime.now()).split(".")[0]
    file_upd.write(date + " " + str(self.id) + "\n")
    file_upd.write(str(ex) + "\n")
    file_upd.write("\n")
    file_upd.close()