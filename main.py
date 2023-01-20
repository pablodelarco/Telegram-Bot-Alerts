import os
import telebot
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")
bot = telebot.TeleBot(API_KEY)

alert_words = {}


@bot.message_handler(commands=["set_alert"])
def set_alert(message):
    user_id = message.from_user.id
    alert_word = message.text.split(" ")[1]
    alert_words[user_id] = alert_word
    print(alert_wordsalert_words[user_id])
    bot.send_message(user_id, f"Alert word set to: {alert_word}")


@bot.message_handler(commands=["add_group"])
def add_group(message):
    group_id = message.text.split(" ")[1]
    bot.join_chat(group_id)
    bot.send_message(message.from_user.id, f"Added group with ID: {group_id}")


@bot.message_handler(commands=["greet"])
def greet(message):
    bot.send_message(message.from_user.id, "Hey! Hows it going?")


@bot.message_handler(func=lambda message: True)
def check_word(message):
    for user_id, alert_word in alert_words.items():
        if alert_word in message.text:
            bot.send_message(
                user_id, f'The word "{alert_word}" has appeared in the chat.'
            )


bot.polling()
