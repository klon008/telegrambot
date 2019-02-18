# -*- coding: utf-8 -*-
import os
import re
import sys
import urllib.request as urllib2
import textes.news_vk as news
import telebot
from telebot import apihelper
from telebot import types

import config

path = os.path.dirname(__file__)



apihelper.proxy = config.proxy
bot = telebot.TeleBot(config.token)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


def log(message, answer):
    print("\n --------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \n Текст - {3}".format(
        message.from_user.first_name,
        message.from_user.last_name,
        str(message.from_user.id),
        message.text
    ))
    print(answer)


class CustomFunctions(object):
    @staticmethod
    def generate_start_menu_buttons():
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="🍽 Меню", callback_data="show_menu")
        url_button2 = types.InlineKeyboardButton(text="🛒 Корзина", callback_data="show_cart")
        url_button3 = types.InlineKeyboardButton(text="📢 Новости", callback_data="show_news")
        url_button4 = types.InlineKeyboardButton(text="📩 Контакты", callback_data="show_contacts")
        url_button5 = types.InlineKeyboardButton(text="🚀 Доставка", callback_data="show_delivery")
        keyboard.add(url_button1, url_button2, url_button3, url_button4, url_button5)
        return keyboard

    @staticmethod
    def start_menu(message, *args, **kwargs):
        try:
            keyboard = CustomFunctions.generate_start_menu_buttons()
            result = "Добро пожаловать!\r\nВыберите 🌶️ интересующий вас пункт меню и я незамедлительно отвечу " \
                     "вам 👇"
            if 'custom_text' in kwargs:
                result = kwargs['custom_text']

            bot.send_message(message.chat.id, result,
                             reply_markup=keyboard)
        except Exception as e:
            bot.reply_to(message, 'Извините, произошла непредвиденная ошибка')

    @staticmethod
    def back_start_menu(message):
        try:
            keyboard = CustomFunctions.generate_start_menu_buttons()
            result = "Выберите 🌶️ интересующий вас пункт меню и я незамедлительно отвечу " \
                     "вам 👇"

            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                  text=result, reply_markup=keyboard)
        except Exception as e:
            bot.reply_to(message, 'Извините, произошла непредвиденная ошибка')

    @staticmethod
    def generate_keyboard_menu_selector():
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        url_button1 = types.InlineKeyboardButton(text="Фирменные пиццы", callback_data="pizzas")
        url_button2 = types.InlineKeyboardButton(text="Классические пиццы", callback_data="classic_pizza")
        url_button3 = types.InlineKeyboardButton(text="Закуски", callback_data="snacks")
        url_button4 = types.InlineKeyboardButton(text="Десерты и напитки", callback_data="desert")
        url_button5 = types.InlineKeyboardButton(text="← Назад", callback_data="back_start_menu")
        keyboard.add(url_button1, url_button2, url_button3, url_button4, url_button5)
        return keyboard

    @staticmethod
    def show_menu(message, *args, **kwargs):
        if 'result' in kwargs:
            result = kwargs['result']
        else:
            result = "Что конкретно вас интересует? 👇"

        if 'bot_func' in args:
            bot_func = kwargs['bot_func']
        else:
            bot_func = 'edit_message_text'
        keyboard = CustomFunctions.generate_keyboard_menu_selector()
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text=result, reply_markup=keyboard)

    @staticmethod
    def new_show_menu(message, *args, **kwargs):
        if 'result' in kwargs:
            result = kwargs['result']
        else:
            result = "Что конкретно вас интересует? 👇"
        keyboard = CustomFunctions.generate_keyboard_menu_selector()
        bot.send_message(message.chat.id, result,
                         reply_markup=keyboard)

    @staticmethod
    def draw_menu_from_file(message, file_in, old_message=""):
        try:
            with open(path + "/textes/" + file_in, mode="r", encoding="utf-8") as f:
                file = f.read().split('-----')
            # ReplyKeyboardRemove: скрыть предидущую клавиатурку
            # Takes an optional selective argument (True/False, default False)
            message_id = message.message_id
            markup = types.ReplyKeyboardRemove(selective=False)

            for idx, i in enumerate(file):
                math = re.search(re.escape('![image]') + "(.*?)" + re.escape('[image]!'), str(i))
                if math:
                    url = math.group(0).replace("![image]", "").replace("[image]!", "")
                    image_name = "url_image_{0}.jpg".format(idx)
                    urllib2.urlretrieve(url, image_name)
                    img = open(image_name, 'rb')
                    bot.send_chat_action(message.chat.id, 'upload_photo')
                    result = i.replace(math.group(0), "")
                    bot.send_photo(message.chat.id, img, caption=result)
                    img.close()
                else:
                    bot.send_message(chat_id=message.chat.id, text=i, reply_markup=markup, parse_mode="Markdown")
            if old_message and not old_message.isspace():
                bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                      text=old_message)
            else:
                bot.delete_message(message.chat.id, message_id)
            CustomFunctions.new_show_menu(message, result="Возможно, вас заинтересует что-то еще?")
        except Exception as e:
            print('Извините, произошла непредвиденная ошибка')
            print(e)
            bot.reply_to(message, 'Извините, произошла непредвиденная ошибка')


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    message = call.message
    if call.message:
        if call.data == "show_menu":
            CustomFunctions.show_menu(message)

        elif call.data == "show_cart":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Извините, данный функционал еще не готов")
        elif call.data == "show_news":
            nn = news.generate_news_from_vk()
            bot.edit_message_text(chat_id=message.chat.id, message_id=call.message.message_id,
                                  text="Наши последние новости:")
            for i in nn:
                bot.send_message(chat_id=message.chat.id, text=i)
            CustomFunctions.start_menu(message, custom_text="Возможно, вас заинтересует что-то еще?")
        elif call.data == "back_start_menu":
            CustomFunctions.back_start_menu(message)
        elif call.data == "pizzas":
            CustomFunctions.draw_menu_from_file(message, 'pizzas.txt', 'Предоставляю список наших Фирменных пицц')
        elif call.data == "classic_pizza":
            CustomFunctions.draw_menu_from_file(message, 'classic_pizza.txt', 'Предоставляю список классических пицц')
        elif call.data == "snacks":
            CustomFunctions.draw_menu_from_file(message, 'snacks.txt', 'Предоставляю список закусок')
        elif call.data == "desert":
            CustomFunctions.draw_menu_from_file(message, 'desert.txt', 'Предоставляю Десерты и напитки')
        elif call.data == "show_contacts":
            bot.edit_message_text(chat_id=message.chat.id, message_id=call.message.message_id,
                                  text="Наши контакты:")
            result = """☎ +7 951 577 32 52
📧 chekpointpizza@gmail.com
🌐 www.chekpointpizza.ru
💙 vk.com/chekpointpizza
📷 instagram.com/chekpointpizza
🌏 [2gis.ru](https://2gis.ru/sheregesh/firm/70000001033499892%2C87.979068%2C52.926753?queryState=center%2F87.979487%2C52.926435%2Fzoom%2F18) 
#chekpointpizza
"""
            bot.send_message(chat_id=message.chat.id, text=result, disable_web_page_preview='True', parse_mode="Markdown")
            # sendLocation 52.9254244,87.9768591,17
            bot.send_location(message.chat.id, 52.92675047761759, 87.97900583928678)
            CustomFunctions.start_menu(message, custom_text="Возможно, вас заинтересует что-то еще?")
        elif call.data == "show_delivery":
            bot.edit_message_text(chat_id=message.chat.id, message_id=call.message.message_id,
                                  text="Стоимость и условия доставки:")
            result = """Бесплатная доставка независимо от суммы заказа: 
ПГТ Шерегеш 🏘 г. Зеленая 🏔

Забрать пиццу со скидкой *15%* можно по адресу: _Шерегеш, ул. Советская 13_
Доставка до Таштагола +200 рублей к заказу. 
Режим работы:
*Ежедневно* с 11:00- 22:00            
"""
            bot.send_message(chat_id=message.chat.id, text=result, disable_web_page_preview='True', parse_mode="Markdown")
            CustomFunctions.start_menu(message, custom_text="Возможно, вас заинтересует что-то еще?")
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "show_cart":
            bot.edit_message_text(chat_id=call.message.chat.id, inline_message_id=call.inline_message_id,
                                  text="Извините, данный функционал еще не готов")


@bot.message_handler(commands=['start', 'contacts'])
def handle_text(message):
    command = message.text
    if command == '/start':
        CustomFunctions.start_menu(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    result = "Я вас не понимаю, но мы всегда можем вернуться к началу /start"
    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True, interval=0)
