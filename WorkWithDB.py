import sqlite3
import os
import datetime


def date_translator(date):
    day, month = date.split('.')
    new_date = month + day
    if int(new_date) < 121:
        new_date = str(int(new_date) + 1200)
    return new_date


def check_date(date):
    day, month = date.split('.')
    year = '2024'  # високосный год, в котором есть 29.02
    try:
        birth_date = datetime.datetime(int(year), int(month), int(day)).date()
        return True
    except ValueError:
        return False


def get_information(id_for_sign):
    Fullname = os.path.join('data', 'Zodiac_Signs.db')
    con = sqlite3.connect(Fullname)
    cur = con.cursor()
    query = f'SELECT Sign, Sign_Eng, Date, Element, Planet FROM Zodiac_Signs WHERE id=={id_for_sign}'
    result = cur.execute(query).fetchone()
    con.close()

    return result


def make_id_from_date(date):
    Fullname = os.path.join('data', 'Zodiac_Signs.db')
    con = sqlite3.connect(Fullname)
    cur = con.cursor()
    query = f'SELECT Begin, Finish, id_date FROM For_search'
    result = cur.execute(query).fetchall()
    con.close()

    for cor in result:
        num_1 = cor[0]
        num_2 = cor[1]
        if int(num_1) <= int(date) <= int(num_2):
            id_for_sign = cor[2]
    return id_for_sign


date = '27.12'  # дата рождения в формате "день.месяц"
if check_date(date):
    information = get_information(make_id_from_date(date_translator(date)))
    print(information)
else:
    print("Несуществующая дата")
