import pandas as pd

def is_admin(login, pwd):
    df = pd.read_csv('admin/login.csv', sep=',', header=None)
    # print(df.values)

    true_login = str(df[0].values[0])
    true_pwd = str(df[1].values[0])

    if (login == true_login and pwd == true_pwd):
        return True
    else:
        return False