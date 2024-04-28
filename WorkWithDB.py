import sqlite3
import os
import datetime

date = '1227'  # дата рождения в формате "день.месяц"
# Sign, Sighn_Eng, Element, Planet FROM Zodiac Signs

Fullname = os.path.join('data', 'Zodiac_Signs.db')
con = sqlite3.connect(Fullname)
cur = con.cursor()
query = f'SELECT id, Begin, Finish FROM id_date'

result = cur.execute(query).fetchall()
con.close()
for cor in result:
    d1, m1 = cor[1].split('.')
    d2, m2 = cor[2].split('.')
    print(cor, m1 + d1, m2 + d2)

