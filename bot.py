import os
import tornado.ioloop
import tornado.web
import telebot
from telebot import types
from content import content_list

bot = telebot.TeleBot("662604211:AAEHx4zRD5FS23XuiKIR0i7rM_jS-Jn85Ww")

def get_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Yes', callback_data='yes'), types.InlineKeyboardButton('No', callback_data='no'))
    return kb

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "Hello {}! {}".format(message.chat.first_name, content_list["start"])
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def send_help(message):
    text = content_list["help"]
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['add'])
def add_place(message):
    text = content_list["add"]
    # TODO add a row to DB
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['list'])
def list_places(message):
    text = content_list["list"]
    # TODO get all rows in DB
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['remove'])
def remove_list(message):
    text = content_list["remove"]
    bot.send_message(message.chat.id, text, reply_markup=get_keyboard())


@bot.message_handler()
def handle_message(message):
    bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda x: True)
def callback_handler(callback):
    message = callback.message
    response = callback.data
    if response == 'yes':
        # TODO remove all rows in DB
        bot.send_message(message.chat.id, content_list["removed"])
    else:
        bot.send_message(message.chat.id, content_list["cancel_remove"])


bot.polling()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


application = tornado.web.Application([(r"/", MainHandler)])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()



