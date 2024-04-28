import telebot
import requests
from bs4 import BeautifulSoup

botTimeWeb = telebot.TeleBot('6837936001:AAHmFPBe6KcU_07bTD4Quhu4C_5F2hurEoQ')

from telebot import types


def get_data_horo(zodiac):
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


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, Привет!\nЧто ты хочешь узнать?"
    markup = types.InlineKeyboardMarkup()
    button_weather = types.InlineKeyboardButton(text='Прогноз погоды на сегодня', callback_data='weather')
    button_quote = types.InlineKeyboardButton(text='Цитата дня', callback_data='quote')
    button_horoscope = types.InlineKeyboardButton(text='Гороскоп', callback_data='horoscope')
    button_dlya_egora = types.InlineKeyboardButton(text='Егорик', callback_data='egor')
    markup.add(button_weather)
    markup.add(button_quote)
    markup.add(button_horoscope)
    markup.add(button_dlya_egora)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@botTimeWeb.callback_query_handler(func=lambda call: True)
def response(function_call):
    if function_call.message:
        if function_call.data == "weather":
            second_mess = "Сегодня отличная погода!"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Подробнее", url="https://yandex.ru/pogoda"))
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            botTimeWeb.answer_callback_query(function_call.id)
        elif function_call.data == "quote":
            second_mess = "Уинстон Черчилль : ледивадавдедвдаведвла"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Подробнее", url="https://en.wikiquote.org/wiki/Winston_Churchill"))
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            botTimeWeb.answer_callback_query(function_call.id)
        elif function_call.data == "horoscope":
            zodiac = 'leo'
            second_mess = f"{get_data_horo(f'{zodiac}')}"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Купить", url="https://market.yandex.ru/"))
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            botTimeWeb.answer_callback_query(function_call.id)
        elif function_call.data == "egor":
            second_mess = "В разработке!"
            botTimeWeb.send_message(function_call.message.chat.id, second_mess)
            botTimeWeb.answer_callback_query(function_call.id)


print((get_data_horo('taurus'))[3:-4])
botTimeWeb.infinity_polling()
