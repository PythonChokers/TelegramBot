# cd C:\Users\User\PycharmProjects\pythonBOT\venv\Scripts\
# .\activate
# cd ..\
# python.exe bot.py

import time
import telebotdb
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "1487154008:AAGTL5lUFwaUUwZ_Vdn2xiXdwJNY83_JsiQ"

bot = telebot.TeleBot(TOKEN)


def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Записаться", callback_data="cd_appointment"),
               InlineKeyboardButton("Отменить запись", callback_data="cd_exit"),
               InlineKeyboardButton("Прайс-лист", callback_data="cd_price"),
               InlineKeyboardButton("Позвонить", callback_data="cd_call"))
    return markup


def appointment_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Мастер", callback_data="cd_master"),
               InlineKeyboardButton("Услуга", callback_data="cd_service"))
    return markup


def barber_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temp_name = ''
    for barber in telebotdb.get_master():
        barber_name = barber.name
        if temp_name:
            markup.add(InlineKeyboardButton(temp_name, callback_data=temp_name),
                       InlineKeyboardButton(barber_name, callback_data=barber_name))
            temp_name = ''
        else:
            temp_name = barber_name
    if temp_name:
        markup.add(InlineKeyboardButton(temp_name, callback_data=temp_name))
    return markup


def service_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temp_serv = ''
    for service in telebotdb.get_service():
        service_name = service.name
        if temp_serv:
            markup.add(InlineKeyboardButton(temp_serv, callback_data=temp_serv),
                       InlineKeyboardButton(service_name, callback_data=service_name))
            temp_serv = ''
        else:
            temp_serv = service_name
    if temp_serv:
        markup.add(InlineKeyboardButton(temp_serv, callback_data=temp_serv))
    return markup


day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


def day_markup(id):
    days = telebotdb.get_date_having_master(id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temp_day = ''
    for day in days:
        day_num = int(day.day)
        if temp_day and temp_day != day_num:
            markup.add(InlineKeyboardButton(day_names[temp_day - 1],
                                            callback_data=day_names[temp_day - 1]),
                       InlineKeyboardButton(day_names[day_num - 1], callback_data=day_names[day_num - 1]))
            temp_day = ''
        else:
            temp_day = day_num
    if temp_day:
        markup.add(
            InlineKeyboardButton(day_names[temp_day - 1], callback_data=day_names[temp_day - 1]))
    return markup


def time_markup(id):
    days = telebotdb.get_date_having_master(id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temporary_hour = ''
    for day in days:
        hour = str(day.hour)
        mins = str(day.mins)
        if temporary_hour:
            markup.add(
                InlineKeyboardButton(temporary_hour + ' : ' + ("00" if temporary_mins == '0' else temporary_mins),
                                     callback_data=temporary_hour + ' : ' + (
                                         "00" if temporary_mins == '0' else temporary_mins)),
                InlineKeyboardButton(hour + ' : ' + mins,
                                     callback_data=hour + ' : ' + mins))
            temporary_hour = ''
        else:
            temporary_hour = hour
            temporary_mins = mins
    if temporary_hour:
        markup.add(
            InlineKeyboardButton(temporary_hour + ' : ' + ("00" if temporary_mins == '0' else temporary_mins),
                                 callback_data=temporary_hour + ' : ' + (
                                     "00" if temporary_mins == '0' else temporary_mins)))
    return markup


def do_order():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Подтвердить заказ', callback_data='confirm_order'),
               InlineKeyboardButton('Вернуться к началу', callback_data='back_to_start'))
    return markup


order = {}

barbers = {}
for barber in telebotdb.get_master():
    barbers[barber.id] = str(barber.name)

services = {}
service_price = {}
for service in telebotdb.get_service():
    services[service.id] = str(service.name)
    service_price[service.id] = service.price

days = {1: 'Пн', 2: 'Вт', 3: 'Ср', 4: 'Чт', 5: 'Пт', 6: 'Сб', 7: 'Вс'}

times = {}
hour = 8
for time in range(1, 26, 2):
    times[time] = str(hour) + ' : 00'
    times[time + 1] = str(hour) + ' : 30'
    hour += 1


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    order.setdefault(call.from_user.id)
    if not order[call.from_user.id]:
        order[call.from_user.id] = {}

    if call.data == "cd_appointment":
        bot.send_message(call.from_user.id, 'Записаться в Barber KPFU')
        bot.send_message(call.from_user.id, 'Выберите сценарий:',
                         reply_markup=appointment_markup())
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data == "cd_exit":
        pass
    elif call.data == "back_to_start":
        bot.send_message(call.from_user.id, 'Чтобы записаться в Barbershop, нажмите кнопку <<Записаться>>.',
                     reply_markup=start_markup())
        order[call.from_user.id] = {}
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data == "cd_price":
        for service in telebotdb.get_service():
            bot.send_message(call.from_user.id, str(service.name) + ' - ' + str(service.price) + ' рублей')
    elif call.data == "cd_call":
        bot.send_message(call.from_user.id, '88005553535')
    elif call.data == "cd_master":
        bot.send_message(call.from_user.id, 'Barber:',
                         reply_markup=barber_markup())
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data == "cd_service":
        bot.send_message(call.from_user.id, f'Услуги: ',
                         reply_markup=service_markup())
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data in day_names:
        bot.send_message(call.from_user.id, f'Время ({call.data}) ',
                         reply_markup=time_markup(order[call.from_user.id]['Мастер']))
        for id, name in days.items():
            if call.data == name:
                order[call.from_user.id]['День'] = id
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data in times.values():
        for id, name in times.items():
            if call.data == name:
                order[call.from_user.id]['Время'] = id

        master_name = barbers[order[call.from_user.id]['Мастер']]
        service_name = services[order[call.from_user.id]['Услуга']]
        time = str(days[order[call.from_user.id]['День']]) + f' ({times[order[call.from_user.id]["Время"]]})'
        price = service_price[order[call.from_user.id]['Услуга']]

        bot.send_message(call.from_user.id, f'''Ваш заказ: 
Мастер - {master_name}
Услуга - {service_name}
Время - {time}
Цена - {price}
''', reply_markup=do_order())

        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data in barbers.values():
        order[call.from_user.id].setdefault('Мастер')
        service_field = order[call.from_user.id].get('Услуга')
        id_m = ''
        for id, name in barbers.items():
            if name == call.data:
                order[call.from_user.id]['Мастер'] = id
                id_m = id
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
        if not service_field:
            bot.send_message(call.from_user.id, f'Услуги ({call.data})',
                             reply_markup=service_markup())
        else:
            bot.send_message(call.from_user.id, 'День',
                             reply_markup=day_markup(id_m))
    elif call.data in services.values():
        order[call.from_user.id].setdefault('Услуга')
        master_field = order[call.from_user.id].get('Мастер')
        for id, name in services.items():
            if call.data == name:
                order[call.from_user.id]['Услуга'] = id
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
        if not master_field:
            bot.send_message(call.from_user.id, 'Barber:',
                             reply_markup=barber_markup())
        else:
            bot.send_message(call.from_user.id, 'День',
                             reply_markup=day_markup(order[call.from_user.id]['Мастер']))

    print(order)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Чтобы записаться в Barbershop, нажмите кнопку <<Записаться>>.',
                     reply_markup=start_markup())


@bot.message_handler(commands=['admin'])
def log_admin(message):
    bot.send_message(message.from_user.id, 'Введите пароль админа!')


@bot.message_handler(func=lambda m: True)
def password(message):
    if message.text == '12345678':
        bot.send_message(message.from_user.id, 'Добро пожаловать, админ!')
    else:
        bot.send_message(message.from_user.id, 'Хорошая попытка, Олег))))0)0)')


bot.polling(none_stop=True, interval=0)
