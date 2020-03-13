import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

name = ''
surname = ''
age = 0
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text in ['привіт', 'Привіт', 'ПРИВІТ', '1']:
        bot.send_message(message.from_user.id, "Як тебе звати?")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Я тебе не розумію')

def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Скажи своє прізвище')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id,'Скільки тобі років?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    while age == 0: #проверяем что возраст изменился
        try:
            age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, будь ласка')
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Так', callback_data='yes') #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Ні', callback_data='no')
    keyboard.add(key_no)
    question = 'Тобі '+str(age)+' років, тебе звати '+name+' '+surname+'?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
#call.data это callback_data, которую мы указали при объявлении кнопки
 #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запам\'ятаю : )')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Вибач, я помилився(')

# RUN
bot.polling(none_stop=True, interval=0)


