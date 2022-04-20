from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from geopy import geocoders
from data import db_session
import requests
import json
from data.geolocation import User

TOKEN = '5146192395:AAFuwm-__5uK-tG7tfirvAWXCfo97idma54'
WEATHER_TOKEN = ''
current_area = ''
new_name = ''
WEATHER_TOKEN = 'a911cb6b-7f4b-4b40-99b4-a1a8f235ad78'
current_name = ''
user_markup = ReplyKeyboardMarkup([['/registration', '/enter']], one_time_keyboard=False)
functional_markup = ReplyKeyboardMarkup([['/temperature', '/weather_conditions', '/weather', '/map'], ['change_city']])
user_keyboard = [['/registration', '/enter']]
functions_keyboard = [['/weather', '/conditions', '/advice'], ['/help', '/change', '/link'], ['/quit']]
user_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)
functional_markup = ReplyKeyboardMarkup(functions_keyboard)
main_flag = True


def registration(update, context):
    update.message.reply_text('''Вы активировали процесс регистрации. Чтобы прервать последующий диалог,
используйте команду /stop. Пожалуйста, введите свой никнейм''')
    return 1
    global main_flag
    if main_flag:
        update.message.reply_text('Вы активировали процесс регистрации. Чтобы прервать последующий диалог,'
                                  'используйте команду /stop. Пожалуйста, введите свой никнейм')
        main_flag = False
        return 1
    else:
        update.message.reply_text('Сначала завершите предыдущую задачу')


def registration_name(update, context):
    global new_name
    new_name = update.message.text
    context.user_data['name'] = update.message.text
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    if context.user_data['name'] == '---':
        update.message.reply_text('Пожалуйста, придумайте другое имя')
        return 1
    for user in db_sess.query(User).all():
        if user.name == context.user_data['new_name']:
            update.message.reply_text('Пользователь с таким именем уже существет. '
                                      'Пожалуйста, придумайте другое')
            return 1
    update.message.reply_text('Теперь придумайте пароль')
    return 2


def geolocation(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude


def registration_password(update, context):
    password = update.message.text
    db_session.global_init("db/cities.db")
    db_sess = db_session.create_session()
    context.user_data['password'] = password
    user = User()
    user.name = new_name
    user.password = password
    user.name = context.user_data['new_name']
    user.password = context.user_data['password']
    db_sess.add(user)
    db_sess.commit()
    functional(update, context)
    update.message.reply_text('Регистрация успешно пройдена!')
    return ConversationHandler.END





def help(update, context):
    update.message.reply_text('Вы используете бот-метеоролог. Чтобы получить доступ ко всем функциям вам необходимо'
                              'пройти регистрацию или выполнить вход, если вы использовали бота ранее. После '
                              'этого вам будут доступны следующие функции: выбор города проживания (/change_city),'
                              'вывод температуры в городе проживания (/temperature), вывод погодных условий, а'
                              'именно влажности, скорости и направления ветра, атмосферного давления '
                              '(/weather_conditions), вывод всей информации о погоде (/weather), вывод метеокарты'
                              '(/map)')
    if main_flag:
        update.message.reply_text('Вы используете бот-метеоролог. Чтобы получить доступ ко всем функциям вам необходимо'
                                  'пройти регистрацию или выполнить вход, если вы использовали бота ранее. После '
                                  'этого вам будут доступны следующие функции: выбор города (/change_city),'
                                  'вывод краткой информации о погоде в выбранном городе (/weather),'
                                  'вывод подробной информации о погоде (/conditions),'
                                  'совет о том, что надеть в такую погоду (/advice),'
                                  'ссылка на сайт Яндекс.Погоды, где можно найти более'
                                  'подробную информацию и метеокарту (/link).'
                                  'Для отмены действия воспользуйтесь командой /stop')
    else:
        update.message.reply_text('Сначала завершите предыдущую задачу')


def stop(update, context):
    global main_flag
    main_flag = True
    update.message.reply_text('Действие отменено')
    return ConversationHandler.END

def enter_name(update, context):
    global current_name
    current_name = update.message.text
    f = False
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.name == current_name:
            f = True
    if f:
        update.message.reply_text('Введите ваш пароль')
        return 2
    else:
        update.message.reply_text('Пользователь с таким именем не найден')
        current_name = ''
        return ConversationHandler.END

def start(update, context):
    global main_flag
    main_flag = True
    context.user_data['name'] = '---'
    update.message.reply_text('Добро пожаловать в бот-метеоролог! Чтобы начать '
                              'пройдите регистрацию или выполните вход', reply_markup=user_markup)


def functional(update, context):
    update.message.reply_text('Добро пожаловать!'
                              'Вам доступны следующие функции:', reply_markup=functional_markup)
    db_session.global_init("db/cities.db")
    db_sess = db_session.create_session()
    city = ''
    for user in db_sess.query(User).all():
        if user.name == context.user_data["name"]:
            city = user.constant_city
            break
    update.message.reply_text(f'Добро пожаловать, {context.user_data["name"]}! ')



def change(update, context):
    if context.user_data['name'] != '---':
        update.message.reply_text('Хотите поменять город проживания?'
                                  'Хорошо, введите новое место:')
        global main_flag
        main_flag = False
        return 1
    else:
        update.message.reply_text('Сначала войдите в систему')
        return ConversationHandler.END


def change_city_handling(update, context):
    global main_flag
    main_flag = True
    new_city = update.message.text
    db_session.global_init("db/cities.db")
    db_sess = db_session.create_session()
    context.user_data['current_area'] = new_city
    for user in db_sess.query(User).all():
        if user.name == context.user_data["name"]:
            user.constant_city = new_city
            db_sess.commit()
    update.message.reply_text('Город проживания успешно изменен')
    return ConversationHandler.END


def enter(update, context):
    update.message.reply_text('''Вы активировали процесс входа. Чтобы прервать последующий диалог,
    используйте команду /stop. Пожалуйста, введите свой никнейм''')
    return 1
    global main_flag
    if main_flag:
        update.message.reply_text('Вы активировали процесс входа. Чтобы прервать последующий диалог, '
                                  'используйте команду /stop. Пожалуйста, введите свой никнейм')
        main_flag = False
        return 1
    else:
        update.message.reply_text('Сначала завершите предыдущую задачу')





def enter_password(update, context):
    global main_flag
    main_flag = True
    global current_name
    password = update.message.text
    f = False
    db_session.global_init("db/blogs.db")

    db_session.global_init("db/cities.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.name == current_name and user.password == password:
            f = True
    if f:
        context.user_data['name'] = current_name
        functional(update, context)
        return ConversationHandler.END
    else:
        update.message.reply_text('Вы ввели неверный пароль. Пожалуйста, войдите в систему заново',
                                  reply_markup=user_markup)
        return ConversationHandler.END




def link(update, context):
    if main_flag:
        if context.user_data['name'] != '---':
            update.message.reply_text('Вот ссылка на подробности:'
                                      f'{context.user_data["link"]}')
        else:
            update.message.reply_text('Сначала войдите в систему')
    else:
        update.message.reply_text('Сначала завершите предыдущую задачу')








def conditions(update, context):
    global main_flag
    if main_flag:
        main_flag = False
        if context.user_data['name'] != '---':
            update.message.reply_text('Введите название города, для которого хотите '
                                      'узнать подробную информацию о погоде')
            return 1
        else:
            update.message.reply_text('Сначала войдите в систему')
            return ConversationHandler.END
    else:
        update.message.reply_text('Сначала завершите предыдущую задачу')




def quit(update, context):
    context.user_data['name'] = '---'
    update.message.reply_text('Вы вышли из системы. Чтобы продолжить работу, пожалуйста, войдите заново.',
                              reply_markup=user_markup)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, registration_name)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('link', link, pass_user_data=True))
    dp.add_handler(CommandHandler('quit', quit, pass_user_data=True))

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('registration', registration)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, registration_name)],
            2: [MessageHandler(Filters.text & ~Filters.command, registration_password)],
            1: [MessageHandler(Filters.text & ~Filters.command, registration_name, pass_user_data=True)],
            2: [MessageHandler(Filters.text & ~Filters.command, registration_password, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('enter', enter)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, enter_name)],
            2: [MessageHandler(Filters.text & ~Filters.command, enter_password)],
            2: [MessageHandler(Filters.text & ~Filters.command, enter_password, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)])



    dp.add_handler(conv_handler1)
    dp.add_handler(conv_handler2)
    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    db_session.global_init("db/cities.db")
    main()