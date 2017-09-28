# OF Bot

"""
Version - 4.5
With this bot you can fast and easly order food.
Based on SQLite base.
"""

import telebot
import constains
import sqlite3
state = 0
bot = telebot.TeleBot(constains.token)
message_id = 0

print("------------------------------------------------------------------")
print(bot.get_me())
print("------------------------------------------------------------------")


def log(log_answer, message):
    from datetime import datetime
    print("Мой вопрос - " + log_answer)
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nСообщение пользователя - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   message.from_user.id,
                                                                      message.text))
    print("------------------------------------------------------------------")


@bot.message_handler(commands=['start', 'help', 'stop'])
def handle_start_help(message):
    global state
    log_answer = """Что бы произвести заказ продукции вы должны ввести название продукта, который вы хотите преобрести.
Если Бот отвечает ??? - это значит, что такого товара нет в базе данных.
Введите вид товара!"""
    log(log_answer, message)

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/help', '/stop')
    user_markup.row('Пицца', 'Вода')
    user_markup.row('Суши', 'Кола')
    user_markup.row('Карзина')
    if message.text == '/start' or message.text == '/help':
        bot.send_message(message.chat.id, """Что бы произвести заказ продукции вы должны ввести название продукта, который вы хотите преобрести.
Если Бот отвечает ??? - это значит, что такого товара нет в базе данных.""")
    bot.send_message(message.chat.id, "Что вы хотите?", reply_markup=user_markup)
    state = 0


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global state
    global message_id
    if state == 0:
        conn = sqlite3.connect('baza.sqlite')
        c = conn.cursor()

        if message.text == 'Пицца' or message.text == 'пицца':
            message_id = 1
        if message.text == 'Суши' or message.text == 'суши':
            message_id = 2
        if message.text == 'Вода' or message.text == 'вода':
            message_id = 3


        if message_id == 1:
            c.execute('SELECT * FROM pizza')
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('/help', '/stop')
            row = c.fetchone()
            while row is not None:
                row_a = str(row[0])
                row = c.fetchone()
                if row is not None:
                    row_b = str(row[0])
                    user_markup.row(row_a, row_b)
                    row = c.fetchone()
                else:
                    user_markup.row(row_a)
            bot.send_message(message.chat.id, "Введите название пиццы, которую вы хотите приобрести.",
                             reply_markup=user_markup)

        if message_id == 2:
            c.execute('SELECT * FROM sushi')
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('/help', '/stop')
            row = c.fetchone()
            while row is not None:
                row_a = str(row[0])
                row = c.fetchone()
                if row is not None:
                    row_b = str(row[0])
                    user_markup.row(row_a, row_b)
                else:
                    user_markup.row(row_a)
            bot.send_message(message.chat.id, "Введите вид суши, который вы хотите приобрести.",
                             reply_markup=user_markup)
        if message_id == 3:
            c.execute('SELECT * FROM wather')
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('/help', '/stop')
            row = c.fetchone()
            while row is not None:
                row_a = str(row[0])
                row = c.fetchone()
                if row is not None:
                    row_b = str(row[0])
                    user_markup.row(row_a, row_b)
                else:
                    user_markup.row(row_a)
            bot.send_message(message.chat.id, "Введите марку воды, которую вы хотите приобрести.",
                             reply_markup=user_markup)

        if message_id == 0:
            bot.send_message(message.chat.id, "Что вы хотите?")
        else:
            log("Введите название товара!", message)
            state = 1
        c.close()
        conn.close()
        return 0

    if state == 1:
        conn = sqlite3.connect('baza.sqlite')
        c = conn.cursor()
        input_name = message.text
        log("Введите марку товара!", message)

        if message_id == 1:
            c.execute('SELECT * FROM pizza')
        if message_id == 2:
            c.execute('SELECT * FROM sushi')
        if message_id == 3:
            c.execute('SELECT * FROM wather')
        row = c.fetchone()
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('/help', '/stop')
        user_markup.row('Да', 'Нет')

        while row is not None:
            if row[0] == input_name:
                bot.send_message(message.chat.id, "Наименование: " + row[0] + " | Стоимость: " + str(row[1]) +
                                 " | Вес: " + str(row[2]))
                bot.send_message(message.chat.id, "Устраивает ли вас этот товар? ", reply_markup=user_markup)
                state = 2
            row = c.fetchone()
            if state == 2:
                c.close()
                conn.close()
                return 0
        bot.send_message(message.chat.id, "#EROR 404 || Товар не найден!")

    if state == 2:
        user_message = message.text
        arc = 0
        if user_message == 'Нет' or user_message == 'нет':
            log("Устраивает ли вас этот товар? ", message)
            arc = 1
            bot.send_message(message.chat.id, "Введите вид товара!")
        if user_message == 'Да' or user_message == 'да':
            log("Устраивает ли вас этот товар? ", message)
            arc = 1
            bot.send_message(message.chat.id, "Успешно!")
        if arc == 0:
            log("Устраивает ли вас этот товар? ", message)
            bot.send_message(message.chat.id, "Устраивает ли вас этот товар?")
        if arc == 1:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('/help', '/stop')
            user_markup.row('Пицца', 'Вода')
            user_markup.row('Суши', 'Кола')
            bot.send_message(message.chat.id, "#REFRESH", reply_markup=user_markup)
            state = 0
        return 0


@bot.message_handler(content_types=['document', 'audio', 'photo', 'video', 'voice'])
def handle_docs_audio_photo_video_voice(message):
    log_answer = "???"
    log(log_answer, message)
    bot.send_message(message.chat.id, log_answer)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    log_answer = ")))"
    log(log_answer, message)
    bot.send_message(message.chat.id, log_answer)

bot.polling(none_stop=True, interval=0)