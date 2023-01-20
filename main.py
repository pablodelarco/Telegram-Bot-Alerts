import os
import telebot
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
bot = telebot.TeleBot(API_KEY)

alert_word = None
alert_user_id = None


@bot.message_handler(commands=["set_alert"])
def set_alert(message):
    global alert_word, alert_user_id
    alert_word = message.text.split(" ")[1]
    alert_user_id = message.from_user.id
    # print(alert_user_id)
    bot.send_message(alert_user_id, f"Alert word set to: {alert_word}")


@bot.message_handler(commands=["add_group"])
def add_group(message):
    group_id = message.text.split(" ")[1]
    bot.join_chat(group_id)
    bot.send_message(message.from_user.id, f"Added group with ID: {group_id}")


@bot.message_handler(commands=["Greet"])
def greet(message):
    bot.send_message(message.from_user.id, "Hey! Hows it going?")


@bot.message_handler(func=lambda message: True)
def check_word(message):
    global alert_word, alert_user_id
    if alert_word and alert_word in message.text and alert_user_id:
        bot.send_message(
            alert_user_id, f'The word "{alert_word}" has appeared in the chat.'
        )


bot.polling()
