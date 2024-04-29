import telebot
import requests
from transliterate import translit
import random
from bs4 import BeautifulSoup
from WorkWithDB import get_sign, get_eng_from_rus

botTimeWeb = telebot.TeleBot('6837936001:AAHmFPBe6KcU_07bTD4Quhu4C_5F2hurEoQ')

from telebot import types

KOSTIL = False
KOSTIL2 = False
KOSTIL3 = False


def get_data_horo(data):
    zodiac = get_eng_from_rus(data)
    st_accept = "text/html"
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }
    req = requests.get(f"https://goroskop365.ru/{zodiac}/", headers)
    src = req.text
    soup = BeautifulSoup(src, 'html.parser')
    vava = soup.findAll('p')
    return str(vava[0])[3:-4]


def get_data_quote():
    st_accept = "text/html"
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }
    req = requests.get("https://www.leadertask.ru/blog/150-motiviruyushhix-citat-na-kazhdyj-den", headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    vava = soup.findAll('p')
    res = list(vava)[54:]
    return str(res[random.randint(0, len(res))])[3:-13].replace('<strong>', '')


def get_data_weath(city):
    st_accept = "text/html"
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }
    req = requests.get(f"https://pogoda.mail.ru/prognoz/{city}/14dney/", headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    vava = soup.findAll('span')
    res = list(vava)
    res = str(res).replace('span', '')
    res = str(res).replace('<', '')
    res = str(res).replace('>', '')
    res = str(res).replace('/', '')
    res = str(res).replace('class="icon icon_forecast icon_size_50 margin_bottom_10"', '')
    res = str(res).replace('class="text text_block text_bold_normal text_fixed margin_bottom_10"', '')
    res = str(res).replace('class="text text_block text_bold_medium margin_bottom_10"', '')
    res = str(res).replace('class="link link_block link_icon"', '')
    res = str(res).replace('class="text text_block text_bold_normal text_fixed margin_bottom_10"', '')
    res = str(res).replace('style="background-image: url(imgstatusicon2021ltsvg22.svg)"', '')
    res = str(res).replace('class="text text_block text_light_normal text_fixed"', '')
    res = str(res).replace('class="text text_block text_light_normal text_fixed color_gray"', '')
    res = str(res).replace('class="link__text"', '')
    otvet = (str(res)[res.index('день'):res.index('вечер')].split(', ')[:5][2],
             str(res)[res.index('день'):res.index('вечер')].split(', ')[:5][3],
             str(res)[res.index('день'):res.index('вечер')].split(', ')[:5][4])
    return (otvet[0].strip(), otvet[1].replace('title=', '').strip()[1:], otvet[2][:otvet[2].index('"')])


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, Привет!\nЧто ты хочешь узнать?"
    markup = types.InlineKeyboardMarkup()
    button_weather = types.InlineKeyboardButton(text='Погода днём', callback_data='weather')
    button_quote = types.InlineKeyboardButton(text='Цитата', callback_data='quote')
    button_horoscope = types.InlineKeyboardButton(text='Гороскоп', callback_data='horoscope')
    button_dlya_egora = types.InlineKeyboardButton(text='Мой знак зодиака', callback_data='egor')
    markup.add(button_weather)
    markup.add(button_quote)
    markup.add(button_horoscope)
    markup.add(button_dlya_egora)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@botTimeWeb.callback_query_handler(func=lambda call: True)
def response(function_call):
    global KOSTIL, KOSTIL2, KOSTIL3
    if function_call.message:
        if function_call.data == "weather":
            KOSTIL3 = True
            second_mess = "Введите ваш город"
            botTimeWeb.send_message(function_call.message.chat.id, second_mess)
            botTimeWeb.answer_callback_query(function_call.id)
        elif function_call.data == "quote":
            second_mess = f"{get_data_quote()}"
            botTimeWeb.send_message(function_call.message.chat.id, second_mess)
            botTimeWeb.answer_callback_query(function_call.id)
        elif function_call.data == "horoscope":
            KOSTIL = True
            botTimeWeb.send_message(function_call.message.chat.id,
                                    'Введите свой знак зодиака. Вы можете узнать его в 4 кнопке в главном меню бота.')
            botTimeWeb.answer_callback_query(function_call.id)
        elif function_call.data == "egor":
            KOSTIL2 = True
            second_mess = "Введите свой день и месяц рождения в формате 'День.Месяц'. Без кавычек."
            botTimeWeb.send_message(function_call.message.chat.id, second_mess)
            botTimeWeb.answer_callback_query(function_call.id)

        @botTimeWeb.message_handler(content_types=['text'])
        def handle_text_message(message):
            global KOSTIL, KOSTIL2, KOSTIL3
            date = message.text
            if KOSTIL2:
                res = get_sign(date)
                if res[1]:
                    third_mess = f'Русское название:        {res[0][0]}\nАнглийское название: {res[0][1]}\n' \
                                 f'Стихия знака:                 {res[0][3]}\nПокровитель:                 {res[0][4]}\n' \
                                 f'Даты влияния:               {res[0][2]}'
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("Подробнее:",
                                                          url=f"https://horoscopes.rambler.ru/{res[0][1].lower()}/description/"))
                    botTimeWeb.send_message(message.chat.id, third_mess, reply_markup=markup)
                    botTimeWeb.answer_callback_query(function_call.id)
                    KOSTIL2 = False
                else:
                    third_mess = res[0]
                    botTimeWeb.send_message(message.chat.id, third_mess)
                    botTimeWeb.answer_callback_query(function_call.id)
            elif KOSTIL:
                KOSTIL = False
                data = date.lower()
                second_mess = f"{get_data_horo(f'{data}')}"
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("Подробнее:", url=f"https://goroskop365.ru/{get_eng_from_rus(data)}/"))
                botTimeWeb.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            elif KOSTIL3:
                KOSTIL3 = False
                date.lower()
                cit = translit(date, language_code='ru', reversed=True)
                try:
                    second_mess = ', '.join(get_data_weath(f'{cit}'))
                    markup = types.InlineKeyboardMarkup()
                    markup.add(
                        types.InlineKeyboardButton("Подробнее:", url=f"https://pogoda.mail.ru/prognoz/{cit}/14dney/"))
                    botTimeWeb.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
                except:
                    botTimeWeb.send_message(function_call.message.chat.id, 'Неполадки на сервере!')


botTimeWeb.infinity_polling()
