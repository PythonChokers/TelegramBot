import telebot
bot = telebot.TeleBot('1377784150:AAHGCgSbk7iyB84ELu9h42QRkDVbg5xMblY')

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Салют! Этот бот нужен для помощи студентам во время обучения на курсе \"Язык Python и анализ данных\". Оставь небольшой отзыв после этого сообщения! ;)')
        bot.register_next_step_handler(message, chat_cool);   
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши мне Привет')
    elif message.text == '/lit':
        bot.send_message(message.from_user.id, '''1)Курс на stepik: https://stepik.org/course/67/syllabus 
2) Pythontutor: https://pythontutor.ru/''')
    else:
        bot.send_message(message.from_user.id, 'Я пока что не понимаю тебя :с. Напиши /help. \n Для доступа к литературе введи /lit')
            

def chat_cool(message):
    if message.text == 'Огонь':
        bot.send_message(message.from_user.id, 'Действительно так ;)')
    elif message.text == 'Херня':
        bot.send_message(message.from_user.id, 'Печально :c')
    else: bot.send_message(message.from_user.id, 'Ты потрясающий')

bot.polling(none_stop = True, interval = 0)