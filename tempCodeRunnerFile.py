

# bot = telegram.Bot(token=API_Token)
# last_update_id = None


# async def check_word(word, chat_id):
#     global last_update_id
#     while True:
#         updates = await bot.getUpdates(offset=last_update_id)
#         for update in updates:
#             last_update_id = update.update_id + 1
#             if update.message and word in update.message.text:
#                 await bot.sendMessage(
#                     chat_id=chat_id,
#                     text='The word "' + word + '" has appeared in the chat.',
#                 )
#         await asyncio.sleep(10)  # delay for 10 seconds


# word = "example"  # the word you want to search for
# chat_id = "-603185683"

# asyncio.run(check_word(word, chat_id))
