import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
bot = telebot.TeleBot('токен')#Вставьте свой токен
finnn = ''
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!Если хотите быстро просмотреть товары на площадке OLX введите команду /parse')

@bot.message_handler(commands=['parse'])
def parse(message):
    mesg = bot.send_message(message.chat.id, 'Введите какой товар вы хотите просмотреть.')



    bot.register_next_step_handler(message, price_check)

def price_check(message):

    global product
    product = message.text
    bot.send_message(message.chat.id, 'Введите ценовой диапозон,или отправьте N если хотите пропустит.')
    bot.register_next_step_handler(message, where)
    global price
    price = list((message.text.split(' ')))



def where(message):
    global price
    price = list(message.text.split(' '))
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Республика Каракалпакстан', callback_data='karakalpakstan')

    btn2 = types.InlineKeyboardButton('Ташкент', callback_data='toshkent-oblast')
    btn3 = types.InlineKeyboardButton('Бухара', callback_data='buharskaya-oblast')
    btn4 = types.InlineKeyboardButton('Андижан', callback_data='andizhanskaya-oblast')
    btn5= types.InlineKeyboardButton('Джизах', callback_data='dzhizakskaya-oblast')
    btn6 = types.InlineKeyboardButton('Кашкадарья', callback_data='kashkadarinskaya-oblast')
    btn7 = types.InlineKeyboardButton('Наманган', callback_data='namanganskaya-oblast')
    btn8 = types.InlineKeyboardButton('Навои', callback_data='navoijskaya-oblast')
    btn9 = types.InlineKeyboardButton('Самарканд', callback_data='samarkandskaya-oblast')
    btn10 = types.InlineKeyboardButton('Фергана', callback_data='ferganskaya-oblast')
    btn11 = types.InlineKeyboardButton('Хорезм', callback_data='horezmskaya-oblast')
    btn12 = types.InlineKeyboardButton('Сурхандарья', callback_data='surhandarinskaya-oblast')
    btn13 = types.InlineKeyboardButton('Сирдарья', callback_data='syrdarinskaya-oblast')
    btn14 = types.InlineKeyboardButton('Весь Узбекистан', callback_data='UZ')
    markup.row(btn14)
    markup.row(btn1)
    markup.row(btn4, btn5, btn6)
    markup.row(btn7, btn8, btn9)
    markup.row(btn10, btn11, btn12)
    markup.row(btn13, btn2, btn3)

    bot.send_message(message.chat.id, 'Выберите  регион', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    listt = []
    global finnn
    if callback.data == 'UZ' and price == ['N']:
        responce = requests.get(f'https://www.olx.uz/list/q-{product}')
    elif callback.data == 'UZ' and price != ['N']:


        responce = requests.get(f'https://www.olx.uz/list/q-{product}?search%5Bfilter_float_price%3Afrom%5D={price[0]}&search%5Bfilter_float_price%3Ato%5D={price[1]}')

    elif callback.data != 'UZ' and price == ['N']:
        responce = requests.get(
            f'https://www.olx.uz/{callback.data}/q-{product}')

    elif callback.data != 'UZ' and price != ['N']:
        responce = requests.get(
            f'https://www.olx.uz/{callback.data}/q-{product}?search%5Bfilter_float_price%3Afrom%5D={price[0]}&search%5Bfilter_float_price%3Ato%5D={price[1]}')

    bs = BeautifulSoup(responce.text, "html.parser")
    all_titles = bs.find_all("h6", class_='css-16v5mdi er34gjf0')
    all_links = bs.find_all("a", class_='css-rc5s2u')

    all_prices = bs.find_all("p", class_='css-10b0gli er34gjf0')
    all_titles = list(map(lambda x: x.text, all_titles))
    all_links = list(map(lambda x: "https://www.olx.uz/" + x['href'], all_links))
    combined = [x for pair in zip(all_titles, all_links) for x in pair]

    #for el in range(len(all_titles)):
        #finnn = finnn + all_titles[el]
        #print(all_titles[el])

        #bot.send_message(callback.message.chat.id, f"Обьявление:{all_titles[el].text}\nСсылка: https://www.olx.uz/{all_links[el]['href']}")
    new_lists = [combined[i:i + 21] for i in range(0, len(combined), 21)]
    for x in new_lists[0]:
        listt.append(x)
    finn = ' \n'.join(listt)
    bot.send_message(callback.message.chat.id, finn)
bot.polling(none_stop=True)
