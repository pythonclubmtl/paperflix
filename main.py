#Importing the telebot module
import telebot
import os
import re
from modules import *

#Call the Telebot created in telegrm thanks to its TOKEN
bot = telebot.TeleBot("896532495:AAGNXUeLtWnoS5E8D-uei6Oql27CxWiFF9c")

#This function will accept documents like PDF articles
@bot.message_handler(content_types=['document'])
#The message from telegram is always considered in the variable message
def handle_docs(message):
    #store the informations of the document in the file_info variable. It is a list that contains a file_id, the file_zize and the file_path. The file_path is written like 'document type/.../file extension'
	file_info = bot.get_file(message.document.file_id)
    #Write the document in the hard drive disk, in the foler where the script is running
	downloaded_file = bot.download_file(file_info.file_path)
    #take the extension from the file_info using rsplit function. This will be used for the downloading in the same document type as the original one.
	extension = file_info.file_path.rsplit('.')[1]
#   Define the path where the file will be downloaded
    dummy_dir = "./bib_files/"
    check_folder = os.path.isdir(dummy_dir)
    if not check_folder:
        os.makedirs(dummy_dir)
	src = os.getcwd()+'/bib_files/'
    #Choose the file name as "File_id.extension". If you find a better way to name the file, please feel free to modify the "file_info.file_id" name.
	filename = src + message.chat.first_name + "." + extension
	with open(filename, 'wb') as new_file:
		new_file.write(downloaded_file)
	db = DataManager(message.chat.first_name)
	db.update_user_db()

#This function answer to questions asked in the telegrambot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    #Answer to the question with the description of the purpose of this bot
	bot.reply_to(message, "Up an running.")

@bot.message_handler(commands=['train_classifier'])
def train_classifier(message):
	training = Trainer()
	result_msg = "Finished training, accuracy: " + training.report["test_accuracy"] + " %"
	bot.reply_to(message, result_msg)

@bot.message_handler(commands=['predict'])
def predict_sentence(message):
	sentence = message.text.replace("/predict ", "")
	prediction = Oracle(sentence)
	result_msg = "Prediction: "+str(prediction.category) + "\n with "+str(prediction.proba)+" and "+ str(prediction.classes)
	print(prediction.category, prediction.proba, prediction.classes)
	bot.reply_to(message, result_msg)

bot.polling()