from datetime import datetime


class User_log():
    def __init__(self):
        self.id = None
        self.fname = None
        self.lname = None
        self.nickname = None


    def user_record(self):
        #добавляем лог пользователя
        file_check = open("users/users.txt","r",encoding='utf-8')
        lines = file_check.readlines()
        mark = 0
        for line in lines:
            #проверяем, пользовался ли человек ботом
            line = line.replace("\n","")
            if line == str(self.id) + " | " + str(self.fname) + " | " + str(self.lname) + " | " + str(self.nickname):
                mark = 1
                break
        if mark == 0:
            file_upd = open("users/users.txt","a+",encoding='utf-8')
            file_upd.write(str(self.id) + " | " + str(self.fname) + " | " + str(self.lname) + " | " + str(self.nickname) + "\n")
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