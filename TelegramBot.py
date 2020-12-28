# cd C:\Users\User\PycharmProjects\pythonBOT\venv\Scripts\
# .\activate
# cd ..\
# python.exe bot.py

import Analytics
from itertools import groupby
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
    check_master_time = False
    for barber in telebotdb.get_master_with_free_time():

        check_master_time = True
        barber_name = barber.name
        if temp_name:
            markup.add(InlineKeyboardButton(temp_name, callback_data=temp_name),
                        InlineKeyboardButton(barber_name, callback_data=barber_name))
            temp_name = ''
        else:
            temp_name = barber_name
    if temp_name:
        markup.add(InlineKeyboardButton(temp_name, callback_data=temp_name))
    if not check_master_time:
        markup.add(InlineKeyboardButton('Извините, все мастера заняты', callback_data='havent_masters'))
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

    days_list = []
    for day in days:
        days_list.append(day.day)

    days_list = [day for day, _ in groupby(days_list)]

    for day in days_list:
        if temp_day:
            markup.add(InlineKeyboardButton(day_names[temp_day - 1],
                                            callback_data=day_names[temp_day - 1]),
                       InlineKeyboardButton(day_names[day - 1], callback_data=day_names[day - 1]))
            temp_day = ''
        else:
            temp_day = day
    if temp_day:
        markup.add(
            InlineKeyboardButton(day_names[temp_day - 1], callback_data=day_names[temp_day - 1]))

    return markup


def time_markup(id, id_day):
    days = telebotdb.get_date_having_master(id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temporary_hour = ''

    correct_days = []
    for day in days:
        if (day.day == id_day):
            correct_days.append(day)

    for day in correct_days:
        hour = str(day.hour)
        mins = str(day.mins)
        if temporary_hour:
            markup.add(
                InlineKeyboardButton(temporary_hour + ' : ' + ("00" if temporary_mins == '0' else temporary_mins),
                                     callback_data=temporary_hour + ' : ' + (
                                         "00" if temporary_mins == '0' else temporary_mins)),
                InlineKeyboardButton(hour + ' : ' + ("00" if mins == '0' else mins),
                                     callback_data=hour + ' : ' + ("00" if mins == '0' else mins)))
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


def analytics():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('Общая прибыль', callback_data='profit'),
               InlineKeyboardButton('Прибыль по услугам', callback_data='service_profit'),
               InlineKeyboardButton('Выработка мастеров', callback_data='master_profit'),
               InlineKeyboardButton('Проценты по услугам', callback_data='percent_services'),
               InlineKeyboardButton('Процента по мастерам', callback_data='percent_masters'))
    return markup


def delete_order(orders_num):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temp_ord = ''
    for order_num in range(orders_num + 1):
        if temp_ord:
            markup.add(InlineKeyboardButton(temp_ord, callback_data=f'del_or_{temp_ord}'),
                       InlineKeyboardButton(order_num, callback_data=f'del_or_{order_num}'))
            temp_ord = ''
        else:
            temp_ord = order_num
    if temp_ord:
        markup.add(InlineKeyboardButton(temp_ord, callback_data=f'del_or_{temp_ord}'))

    markup.add(InlineKeyboardButton('Вернуться', callback_data='back_to_start'))
    return markup


order = {}

del_order = []
for num in range(100):
    del_order.append(f'del_or_{num}')

barbers = {}
for barber in telebotdb.get_master():
    barbers[barber.id] = str(barber.name)

services = {}
service_price = {}
for service in telebotdb.get_service():
    services[service.id] = str(service.name)
    service_price[service.id] = service.price

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
        user_orders = telebotdb.get_order_having_user(call.from_user.id)
        if user_orders:
            bot.send_message(call.from_user.id, 'Ваши записи:')
            orders_num = 0
            for u_order in user_orders:
                bot.send_message(call.from_user.id, f'''
День - {day_names[u_order.id_t // 26]} 
Время - {times[(u_order.id_t - 1) % 26 + 1]}
Услуга - {services[u_order.id_s]} 
Мастер - {barbers[u_order.id_m]}''')
                orders_num += 1
            bot.send_message(call.from_user.id, 'Какую запись вы желаете удалить?',
                             reply_markup=delete_order(orders_num))
        else:
            bot.send_message(call.from_user.id, 'У вас нет записей', reply_markup=start_markup())
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data == "profit":
        profit = Analytics.sumcash()
        bot.send_message(call.from_user.id, f'Общий заработок за все время: {profit} рублей.')
    elif call.data == "service_profit":
        service_profit = Analytics.services_impact()
        for service, profit in service_profit.items():
            bot.send_message(call.from_user.id, f'Услуга "{service}" принесла доход в размере {int(float(profit))} рублей.')
    elif call.data == "master_profit":
        master_profit = Analytics.masters_impact()
        for master, profit in master_profit.items():
            bot.send_message(call.from_user.id, f'Мастер "{master}" принес доход в размере {int(float(profit))} рублей.')
    elif call.data == "percent_services":
        services_percent = Analytics.percent()
        for service, percent in services_percent.items():
            bot.send_message(call.from_user.id, f'Процент услуги "{service}" составляет - {percent}% от всех заказов.')
    elif call.data == "percent_masters":
        masters_percent = Analytics.percent_master()
        for master, percent in masters_percent.items():
            bot.send_message(call.from_user.id, f'Мастер {master} выполнил {percent}% от всех заказов.')
    elif call.data == "havent_masters":
        bot.send_message(call.from_user.id, 'Чтобы записаться в Barbershop, нажмите кнопку <<Записаться>>.',
                         reply_markup=start_markup())
        order[call.from_user.id] = {}
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data == "confirm_order":
        user_id = call.from_user.id
        order_day = order[call.from_user.id]['День']
        order_time = order[call.from_user.id]['Время']
        service_id = order[call.from_user.id]['Услуга']
        master_id = order[call.from_user.id]['Мастер']
        order[call.from_user.id] = {}

        set_order(user_id, order_day, order_time, service_id, master_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
        bot.send_photo(call.from_user.id,
                       'https://coub-anubis-a.akamaized.net/coub_storage/coub/simple/cw_timeline_pic/4ca3f01437d/82972d4812cb9853cfc32/ios_large_1554150210_image.jpg')
        bot.send_message(call.from_user.id, 'Ваш заказ оформлен, ждите уведомлений!')

    elif call.data == "back_to_start":
        bot.send_message(call.from_user.id, 'Чтобы записаться в Barbershop, нажмите кнопку <<Записаться>>.',
                         reply_markup=start_markup())
        order[call.from_user.id] = {}
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data == "cd_price":
        for service in telebotdb.get_service():
            bot.send_message(call.from_user.id, str(service.name) + ' - ' + str(int(float(service.price))) + ' рублей')
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
                         reply_markup=time_markup(order[call.from_user.id]['Мастер'], day_names.index(call.data) + 1))
        order[call.from_user.id]['День'] = day_names.index(call.data) + 1
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    elif call.data in times.values():
        for id, name in times.items():
            if call.data == name:
                order[call.from_user.id]['Время'] = id

        master_name = barbers[order[call.from_user.id]['Мастер']]
        service_name = services[order[call.from_user.id]['Услуга']]
        time = str(day_names[order[call.from_user.id]['День'] - 1]) + f' ({times[order[call.from_user.id]["Время"]]})'
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
    elif call.data in del_order:
        num_order_for_del = int(call.data[7:]) - 1
        user_orders = telebotdb.get_order_having_user(call.from_user.id)
        telebotdb.delete_order(user_orders[num_order_for_del])
        bot.send_message(call.from_user.id, 'Запись отменена успешно!', reply_markup=start_markup())
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=None)
    print(order)


def set_order(user_id, order_day, order_time, service_id, master_id):
    id_time = (order_day - 1) * 26 + order_time
    print(user_id, id_time, service_id, master_id)
    telebotdb.make_order(user_id, id_time, service_id, master_id)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Чтобы записаться в Barbershop, нажмите кнопку <<Записаться>>.',
                     reply_markup=start_markup())


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, """
/start - Начало работы с ботом.
/admin - Доступ к командам админа.
/info - Информация о нашем заведении.""")


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.from_user.id, """
Мы ждем вас в нашем барбершопе '-_-Barbi3Sh0t-_-'
по адресу город Москва, улица Академика Королева, дом 12, вход со стороны двора.
Мы предоставляем большое количество услуг, целых 3.0.
Наши мастера прошли сертификацию на Stepik.org.
Профессионалы со всех уголков Москвы и Московской области, а также стран ближнего востока.
Мы работаем без выходных с 8:00 до 21:00 без обедов и страховок работников.
Если появятся вопросы, обращайтесь к нашему администратору "https://vk.com/vasiliym23".
""")


admins = []


@bot.message_handler(commands=['admin'])
def log_admin(message):
    admins.append(message.from_user.id)
    bot.send_message(message.from_user.id, 'Введите пароль админа:')


@bot.message_handler(func=lambda m: True)
def password(message):
    if message.text == 'Панель админа' and message.from_user.id in admins:
        bot.send_message(message.from_user.id, 'Добро пожаловать, админ!', reply_markup=analytics())
    elif message.from_user.id in admins:
        bot.send_message(message.from_user.id, 'Хорошая попытка, Олег))))0)0)')
        bot.send_message(message.from_user.id, 'Введите пароль админа:')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю, напиши команду "/help"')


bot.polling(none_stop=True, interval=0)
