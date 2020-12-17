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
               InlineKeyboardButton("Услуга", callback_data="cd_service"),
               InlineKeyboardButton("Время", callback_data="cd_date"))
    return markup


barbers = {"Меиржан": "cd_Meirjan", "Самира": "cd_Samira", "Сергей": "cd_Sergey", "Чингиз": "cd_Chingiz",
           "Самат": "cd_Samat"}


def barber_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temporary = ''
    for barber in barbers:
        if temporary:
            markup.add(InlineKeyboardButton(temporary, callback_data=barbers[temporary]),
                       InlineKeyboardButton(barber, callback_data=barbers[barber]))
            temporary = ''
        else:
            temporary = barber
    markup.add(InlineKeyboardButton(temporary, callback_data=barbers[temporary]))
    return markup


price_services = {"Стрижка": 1000, "Моделирование": 1500, "Детская стрижка": 800, "Стрижка машинкой": 600,
                  "Стрижка + бритье": 1500, "Коррекция бороды": 900, "Стрижка Папы и Сына": 1000}
services = {"Стрижка": "cd_haircut", "Моделирование": "cd_model", "Детская стрижка": "cd_kids_haircut",
            "Стрижка машинкой": "cd_machine", "Стрижка + бритье": "cd_Haircut_shaving", "Коррекция бороды": "cd_beard",
            "Стрижка Папы и Сына": "cd_Dad_Son"}


def service_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    temporary = ''
    for service in services:
        if temporary:
            markup.add(InlineKeyboardButton(temporary, callback_data=services[temporary]),
                       InlineKeyboardButton(service, callback_data=services[service]))
            temporary = ''
        else:
            temporary = service
    markup.add(InlineKeyboardButton(temporary, callback_data=services[temporary]))
    return markup


def date_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3


order = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    order.setdefault(call.from_user.id)
    if not order[call.from_user.id]:
        order[call.from_user.id] = {}

    if call.data == "cd_appointment":
        bot.send_message(call.from_user.id, 'Записаться в Barber KPFU')
        bot.send_message(call.from_user.id, 'Выберите сценарий:',
                         reply_markup=appointment_markup())
    elif call.data == "cd_exit":
        pass
    elif call.data == "cd_price":
        pass
    elif call.data == "cd_call":
        pass
    elif call.data == "cd_master":
        bot.send_message(call.from_user.id, 'Barber:',
                         reply_markup=barber_markup())
    elif call.data == "cd_service":
        pass
    elif call.data == "cd_date":
        pass
    elif call.data in barbers.values():
        barber_name = ''
        for name, id in barbers.items():
            if call.data in id:
                barber_name = name
        bot.send_message(call.from_user.id, f'Услуги ({barber_name})',
                         reply_markup=service_markup())
        order[call.from_user.id].setdefault('Мастер')
        order[call.from_user.id]['Мастер'] = call.data
    elif call.data in services.values():
        service_name = ''
        for name, id in services.items():
            if call.data in id:
                service_name = name
        bot.send_message(call.from_user.id, f'''Вы выбрали - {service_name}
Стоимость данной услуги составляет - {price_services[service_name]}''', reply_markup=date_markup())
        order[call.from_user.id].setdefault('Услуга')
        order[call.from_user.id]['Услуга'] = call.data


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Чтобы записаться в Barbershop, нажмите кнопку <<Записаться>>.',
                     reply_markup=start_markup())


bot.polling(none_stop=True, interval=0)
