import telebot

#import logging

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
#Call the Telebot created in telegrm thanks to its TOKEN
bot = telebot.TeleBot("791446971:AAEDuNxuEQU67jbScnjLwcrOCVG57lBD5oY")

bot.send_message(chat_id = "-1001386026536", text = "hi from ilyass" )

@bot.message_handler(commands = ['start', 'go'])
def start_handler(message):
    print(message.chat)
    bot.send_message(message.chat.id, "Hey mate")
bot.polling()

