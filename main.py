import os
import telebot
from PIL import Image

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))



@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id,
                     'Hi, there!\n'
                     'Please, send me a picture and I will resize it to a sticker format.',
                     parse_mode='markdown')

@bot.message_handler(content_types=["text"])
def help_(message):
    bot.send_message(message.chat.id, "Please, send an image.")

@bot.message_handler(content_types=["photo"])
def resize(message):
    photo_id = message.photo[-1].file_id

    photo_file = bot.get_file(photo_id)
    photo_bytes = bot.download_file(photo_file.file_path)
    name = '/tmp/image.png'

    with open(name, 'wb') as new_file:
        new_file.write(photo_bytes)

    image = Image.open(name)
    image.thumbnail((512, 512))

    image.save(name, 'PNG')
    with open(name, 'rb') as result:
        bot.send_document(message.chat.id, result)

if __name__ == '__main__':
    bot.infinity_polling()
