import os
import telebot
from dotenv import load_dotenv
from telebot import types
load_dotenv()

API_KEY = os.environ.get("API_KEY")
bot = telebot.TeleBot(API_KEY)
alert_words = {}


@bot.message_handler(commands=["start"])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    set_alert_button = telebot.types.KeyboardButton("/set_alert")
    remove_alert_button = telebot.types.KeyboardButton("/remove_alert")
    alert_words_button = telebot.types.KeyboardButton("/alert_words")
    start_button = telebot.types.KeyboardButton("/start")
    markup.add(set_alert_button, remove_alert_button, alert_words_button, start_button)
    bot.send_message(chat_id=message.chat.id, text="Hello, I am a Telegram bot that can search for a specific word in a group's messages.", reply_markup=markup)
    bot.send_message(message.chat.id, "Here is a list of commands you can use:")
    bot.send_message(message.chat.id, "/set_alert - Set an alert word")
    bot.send_message(message.chat.id, "/remove_alert - Remove an alert word")
    bot.send_message(message.chat.id, "/alert_words - Show all the alert words set")



@bot.message_handler(commands=["alert_words"])
def show_alert_words(message):
    if message.chat.type != "private":
        return
    user_id = message.from_user.id
    alert_words_list = alert_words.get(user_id, [])
    if alert_words_list:
        bot.send_message(
            user_id, f"Your alert words are: {', '.join(alert_words_list)}"
        )
    else:
        bot.send_message(user_id, "You have no alert words set.")


# Add a new command "/remove_alert" to remove a specific alert word
@bot.message_handler(commands=["remove_alert"])
def remove_alert(message):
    if message.chat.type != "private":
        return
    user_id = message.from_user.id
    words = message.text.split(" ")
    if len(words) < 2:
        bot.send_message(user_id, "Please provide an alert word to remove.")
        return
    alert_word = words[1]
    if user_id in alert_words:
        if alert_word in alert_words[user_id]:
            alert_words[user_id].remove(alert_word)
            bot.send_message(user_id, f"Alert word '{alert_word}' removed.")
        else:
            bot.send_message(user_id, f"Alert word '{alert_word}' not found.")
    else:
        bot.send_message(user_id, "You have no alert words set.")


# Add a new command "/set_alert" to set a new alert word
@bot.message_handler(commands=["set_alert"])
def set_alert(message):
    if message.chat.type != "private":
        return
    bot.send_message(message.from_user.id, "Which word do you want me to look for?")
    bot.register_next_step_handler(message, handle_alert_word)

def handle_alert_word(message):
    alert_word = message.text
    user_id = message.from_user.id
    if user_id in alert_words:
        alert_words[user_id].append(alert_word)
    else:
        alert_words[user_id] = [alert_word]
    bot.send_message(user_id, f"Alert word set to: {alert_word}")


@bot.message_handler(commands=["add_group"])
def add_group(message):
    if message.chat.type != "private":
        return
    group_id = message.text.split(" ")[1]
    try:
        chat = bot.get_chat(group_id)
        bot.join_chat(chat.id)
        bot.send_message(message.from_user.id, f"Added group with ID: {group_id}")
    except Exception as e:
        bot.send_message(
            message.from_user.id, f"Error occured while joining group, {str(e)}"
        )


@bot.message_handler(commands=["greet"])
def greet(message):
    if message.chat.type != "private":
        return
    bot.send_message(message.from_user.id, "Hey! Hows it going?")


@bot.message_handler(func=lambda message: True)
def check_word(message):
    message_text = message.text.casefold()
    for user_id, alert_words_list in alert_words.items():
        for alert_word in alert_words_list:
            if alert_word in message_text:
                limpio_chat = str(message.chat.id)
                new_number_str = limpio_chat[3:]
                new_number = int(new_number_str)
                bot.send_message(
                    user_id,
                    f'The word "{alert_word}" has appeared in the chat: "{message.text}". Link to the message: t.me/c/{new_number}/{message.message_id}',
                )


@bot.message_handler(content_types=["photo"])
def check_word_photo(message):
    if message.caption:
        message_text = message.caption.casefold()
    else:
        message_text = ""
    for user_id, alert_words_list in alert_words.items():
        for alert_word in alert_words_list:
            if alert_word in message_text:
                limpio_chat = str(message.chat.id)
                new_number_str = limpio_chat[3:]
                new_number = int(new_number_str)
                bot.send_photo(
                    user_id,
                    message.photo[-1].file_id,
                    caption=f'The word "{alert_word}" has appeared in the chat: "{message_text}". Link to the message: t.me/c/{new_number}/{message.message_id}',
                )


@bot.message_handler(content_types=["video"])
def check_word_video(message):
    for user_id, alert_words_list in alert_words.items():
        for alert_word in alert_words_list:
            if message.caption and alert_word.casefold() in message.caption.casefold():
                limpio_chat = str(message.chat.id)
                new_number_str = limpio_chat[3:]
                new_number = int(new_number_str)
                bot.send_video(
                    user_id,
                    message.video.file_id,
                    caption=f'The word "{alert_word}" has appeared in the chat: "{message.caption}". Link to the message: t.me/c/{new_number}/{message.message_id}',
                )


bot.polling()
