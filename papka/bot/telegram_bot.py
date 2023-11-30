import telebot
from telebot import types
from db.DataBase import DataAccessObject
from menu import Menu

class Bot:
    def __init__(self):
        bot = telebot.TeleBot('6926639788:AAHjaj9gKNBWMiFeoCqmxl_pCyrp2mwBD-o')

        @bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Самый дорогой товар")
            button2 = types.KeyboardButton("Отобразить товары из определенной категории")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, '''Привет друг, я pythonreviewbot, здесь ты можешь получить полезную информацию о стоимости кубиков рубика на сайте cubemarket.ru'''.format(message.from_user), reply_markup=markup)
           # menu_buttons(message)



        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            if message.text == 'Самый дорогой товар':
                bot.send_message(message.from_user.id, "Самый дорогой товар на сайте:")
                save = Menu().get_max_cube()
                reply = ''
                for i in save:
                    reply += f"Товар: {i[0]}. Стоимость товара: {i[1]}, URL Фото: {i[2]}, URL: {i[3]}, Скидка: {i[4]} "
                bot.send_message(message.from_user.id, reply)
            if message.text == "Отобразить товары из определенной категории":
                bot.send_message(message.from_user.id, "Укажите минимальную стоимость товара:")
                bot.register_next_step_handler(message, get_text)
                minimum = message.text
                bot.send_message(message.from_user.id, "Укажите максимальную стоимость товара:")
                bot.register_next_step_handler(message, get_text)
                maximum = message.text
                #bot.send_message(message.from_user.id, minimum, maximum)
                

        def get_text(message):
            bot.send_message(message.from_user.id, minimum)
        def stop(message):
            pass
        bot.polling(none_stop=True)

menu = Menu()
bot = Bot()