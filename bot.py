from auth_data import token
from rembg import remove
from PIL import Image
import os
import telebot
import pillow_heif


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend! Send me an image!")
    
    @bot.message_handler(content_types=['document', 'photo'])
    def remove_image_bg(message):
        is_file_get = 0

        if not os.path.exists(r'.\Images'):
                os.mkdir(r'.\Images')

        if message.content_type == 'photo':
            bot.send_message(message.chat.id, "Starting photo processing...")
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            elems = file_info.file_path.split('/')
            file_name = elems[len(elems) - 1]
            is_file_get = 1
        else:
            file_name = message.document.file_name
            if file_name.lower().endswith(('.jpeg', '.jpg', '.png', 'heic')):
                    bot.send_message(message.chat.id, "Starting image processing...")
                    file_info = bot.get_file(message.document.file_id)
                    is_file_get = 1
            else:
                bot.send_message(message.chat.id, "Whaaat? I don't know what to do about it!?!?")

        if is_file_get:
            try:
                downloaded_file = bot.download_file(file_info.file_path)
                file_name = r'.\\Images\\' + file_name
                with open(file_name, 'wb') as new_file:
                    new_file.write(downloaded_file)
            except:
                bot.send_message(message.chat.id, "Error while file downloading")
            
            try:
                pref, ext = os.path.splitext(file_name)

                if ext.lower() == '.heic':
                    heif_file = pillow_heif.read_heif(file_name)
                    image = Image.frombytes(
                        heif_file.mode,
                        heif_file.size,
                        heif_file.data,
                        "raw",
                    )
                    new_file_png = pref + '.png'
                    image.save(new_file_png, format('png'))
                else:
                    image = Image.open(file_name)
                    new_file_png = pref + '.png'
                    image.save(new_file_png, format('png'))

                new_image = remove(image)
                new_image.save(new_file_png)

                bot.send_document(message.chat.id, open(new_file_png, 'rb'))

                os.remove(file_name)
                os.remove(new_file_png)
            except:
                bot.send_message(message.chat.id, "Ooops! Something went wrong... Try again")
        


    bot.polling()


def main():
    telegram_bot(token)


if __name__ == '__main__':
    main()