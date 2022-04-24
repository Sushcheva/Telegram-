from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from geopy import geocoders
from data import db_session
import requests as req
import csv
import logging
from telegram.ext import Updater, ConversationHandler, \
    MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove

import requests
import json
from data.geolocation import User

TOKEN = '5146192395:AAFuwm-__5uK-tG7tfirvAWXCfo97idma54'
WEATHER_TOKEN = ''
current_area = ''
new_name = ''
current_name = ''
user_markup = ReplyKeyboardMarkup([['/registration', '/enter']], one_time_keyboard=False)
functional_markup = ReplyKeyboardMarkup([['/temperature', '/weather_conditions', '/weather', '/map'], ['change_city']])
user_keyboard = [['/registration', '/enter']]
user_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)
main_flag = True

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def registration(update, context):
    global main_flag, variant
    update.message.reply_text('''Вы активировали процесс регистрации. Чтобы прервать последующий диалог,
используйте команду /stop. Пожалуйста, введите свой никнейм''')
    variant = 'reg1'
    return 11
    global main_flag
    if main_flag:
        update.message.reply_text('Вы активировали процесс регистрации. Чтобы прервать последующий диалог,'
                                  'используйте команду /stop. Пожалуйста, введите свой никнейм')
        main_flag = False
        return 11
    else:
        update.message.reply_text('Сначала завершите предыдущую задачу')


def geolocation(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude


def registration_password(update, context):
    global variant
    variant = ''
    password = update.message.text
    db_session.global_init("db/cities.db")
    db_sess = db_session.create_session()
    context.user_data['password'] = password
    user = User()
    user.name = new_name
    user.password = password
    user.name = context.user_data['name']
    user.password = context.user_data['password']
    db_sess.add(user)
    db_sess.commit()
    functional(update, context)
    update.message.reply_text('Регистрация успешно пройдена!')
    return ConversationHandler.END


def stop(update, context):
    global main_flag
    main_flag = True
    update.message.reply_text('Действие отменено')
    return ConversationHandler.END


def enter_name(update, context):
    global current_name
    variant = 'ent2'
    current_name = update.message.text
    f = False
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.name == current_name:
            f = True
    if f:
        update.message.reply_text('Введите ваш пароль')
        return 22
    else:
        update.message.reply_text('Пользователь с таким именем не найден')
        current_name = ''
        return ConversationHandler.END


def start(update, context):
    global main_flag
    main_flag = True
    context.user_data['name'] = '---'
    update.message.reply_text('Добро пожаловать в бот-библиотекарь! Чтобы начать поиск '
                              'пройдите регистрацию или выполните вход', reply_markup=user_markup)


def functional(update, context):
    update.message.reply_text('Добро пожаловать!'
                              'Вам доступны следующие функции:')
    db_session.global_init("db/cities.db")
    db_sess = db_session.create_session()
    city = ''


    update.message.reply_text(f'Добро пожаловать, {context.user_data["name"]}! ')

    reply_keyboard = [['/search_book', '/test'],
                      ['/site', '/work_time'],
                      ['/phone', '/address']
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Я бот-справочник. Что вы хотите получить?",
        reply_markup=markup
    )


# Запускаем логгирование


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def help(update, context):
    update.message.reply_text(
        "Я бот справочник.")


def test(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop."
    )
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='det'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='fen'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='thril'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='lub'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1


def address(update, context):
    update.message.reply_text(
        "Адрес: г. Санкт-Петербург, штаб квартира чат-бота книг Гимназия 116, 4 этаж")


def phone(update, context):
    update.message.reply_text("Телефон Марии Егоровны: +7(911)004-1574")


def site(update, context):
    update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")

def registration_name(update, context):
    global new_name
    variant = 'reg2'
    new_name = update.message.text
    context.user_data['name'] = update.message.text
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    if context.user_data['name'] == '---':
        update.message.reply_text('Пожалуйста, придумайте другое имя')
        return 11
    for user in db_sess.query(User).all():
        if user.name == context.user_data['name']:
            update.message.reply_text('Пользователь с таким именем уже существет. '
                                      'Пожалуйста, придумайте другое')
            return 11

    update.message.reply_text('Теперь придумайте пароль')
    return 12

def param(update, context):
    global variant
    global new_name
    print(update.message.text)
    print(variant)
    if variant == 'Введите название':
        context.user_data['dan'] = update.message.text
        search_by_name(update, context)
    elif variant == 'Введите автора':
        context.user_data['dan'] = update.message.text
        search_by_author(update, context)
    elif variant == 'reg1':
        x = registration_name(update, context)
        if x != 11:
            variant = 'reg2'
    elif variant == 'reg2':
        return registration_password(update, context)
    elif variant == 'ent1':
        x = enter_name(update, context)
        if x != 21:
            variant = 'ent2'
    elif variant == 'ent2':
        return enter_password(update, context)


def button(update, _):
    global variant
    global choose
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    with open('Толстой.txt', 'w') as f:
        if variant == 'Введите название' or variant == 'Введите автора':
            query.edit_message_text(text=variant)
        else:
            f.write(variant)
            query.edit_message_text(text='Уверены?')


def first_response(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Удивляться фантазии автора и полностью погружаться в новые миры",
                                 callback_data='fen'),
            InlineKeyboardButton("Мне нравится разбираться в запутанных сюжетных линиях", callback_data='det'),
            InlineKeyboardButton("Мне нравится переживать эмоции персонажей. Радоваться и скорбить вместе с ними",
                                 callback_data='lub'),
            InlineKeyboardButton("Нравится когда книга немного пугает и заставляет копаться в себе",
                                 callback_data='thril'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Что вам больше всего нравится в процессе чтения?", reply_markup=reply_markup)
    # обработчиком states[2]
    return 2


def second_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопроc
    keyboard = [
        [
            InlineKeyboardButton(
                "Во время перерыва, чтобы не только прекрасно провести время, но и пораскинуть мозгами",
                callback_data='det'),
            InlineKeyboardButton("Везде, чтобы избежать рутины", callback_data='fen'),
            InlineKeyboardButton("Ночью, когда вы остаетесь наедине со своими страхами",
                                 callback_data='thril'),
            InlineKeyboardButton("В уютном пледе и чашечкой кове, захлебываясь в слезах", callback_data='lub'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вы читаете...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 3


def third_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    keyboard = [
        [
            InlineKeyboardButton("Опытный следователь, расследующий самые загадочные преступления",
                                 callback_data='det'),
            InlineKeyboardButton("Простой парень, который влюбился по уши, но весь мир против него",
                                 callback_data='lub'),
            InlineKeyboardButton("Сын маньяка, который добрый в душе, но на него давит отец",
                                 callback_data='thril'),
            InlineKeyboardButton(
                "Капитан звездолета, который каждый день отправляется в космос за новыми приключениями",
                callback_data='fen'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Главный герой вашей мечты...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 4


def fourth_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопрос
    keyboard = [
        [
            InlineKeyboardButton("способ развлечения", callback_data='fen'),
            InlineKeyboardButton("способ отдыха", callback_data='lub'),
            InlineKeyboardButton("способ познания мира",
                                 callback_data='det'),
            InlineKeyboardButton("учебник", callback_data='thril'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Книга для вас - это в первую очередь…", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 5


def fifth_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе
    keyboard = [
        [
            InlineKeyboardButton("Эх, вот б мне так", callback_data='lub'),
            InlineKeyboardButton("Да… интересно, но хорошо, что у меня не так", callback_data='thril'),
            InlineKeyboardButton("Так вот оно что!",
                                 callback_data='det'),
            InlineKeyboardButton(" Как такое вообще выдумать можно?!", callback_data='fen'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("С какой фразой вы хотите закрывать книгу?", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 6


def sixth_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    keyboard = [
        [
            InlineKeyboardButton("Агата Кристи", callback_data='det'),
            InlineKeyboardButton("Стивен Кинг", callback_data='thril'),
            InlineKeyboardButton("Терри Пратчетт",
                                 callback_data='fen'),
            InlineKeyboardButton("Джейн Остин", callback_data='lub'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите автора, который вам больше по душе.", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 7


def seventh_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    update.message.reply_text('Подсчет результатов...')
    x = []
    with open('test.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            x.append(row)
    f = open("Толстой.txt", encoding="utf8")
    lines = f.readlines()
    f.close()
    fen = 0
    lub = 0
    thril = 0
    det = 0
    for el in lines:
        if 'fen' in el:
            fen += 1
        elif 'lub' in el:
            lub += 1
        elif 'thril' in el:
            thril += 1
        elif 'det' in el:
            det += 1
    z = max(fen, lub, thril, det)
    if fen == z:
        n = 3
    elif z == lub:
        n = 2
    elif z == det:
        n = 1
    elif z == thril:
        n = 4
    print(x[n])
    update.message.reply_text(x[n][0])
    update.message.reply_text(x[n][2])
    context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        x[n][3],
        caption="Нашёл:"
    )
    update.message.reply_text(f'Рекомендуем к прочтению из этого жанра: {x[n][1]} (лучшая по мнениям опроса 2021)')

    return ConversationHandler.END


def search_by_name(update, context):
    d = context.user_data['dan']
    resp = req.get(
        f"https://www.googleapis.com/books/v1/volumes?q=intitle+{d}:keyes&key=AIzaSyBW1ihw2fnM8jpQg1C-r77bAUYm-WhjJ20")
    z = resp.json()['items']
    print(resp.json())
    f = 0
    for el in z:
        d = []
        f = 0
        x = el['volumeInfo']
        print(x)
        for k, v in x.items():
            f += 1
            if f <= 5:
                d.append(str(str(k) + ': ' + str(v)))
        update.message.reply_text('\n'.join(d))
        context.bot.send_photo(
            update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
            # Ссылка на static API, по сути, ссылка на картинку.
            # Телеграму можно передать прямо её, не скачивая предварительно карту.
            x['imageLinks']['smallThumbnail'],
            caption="Нашёл:"
        )



def search_by_author(update, context):
    d = context.user_data['dan']
    resp = req.get(
        f"https://www.googleapis.com/books/v1/volumes?q=inauthor+{d}:keyes&key=AIzaSyBW1ihw2fnM8jpQg1C-r77bAUYm-WhjJ20")
    z = resp.json()['items']
    print(resp.json())
    f = 0
    for el in z:
        d = []
        f = 0
        x = el['volumeInfo']
        print(x)
        for k, v in x.items():
            f += 1
            if f <= 5:
                d.append(str(str(k) + ': ' + str(v)))
        update.message.reply_text('\n'.join(d))
        context.bot.send_photo(
            update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
            # Ссылка на static API, по сути, ссылка на картинку.
            # Телеграму можно передать прямо её, не скачивая предварительно карту.
            x['imageLinks']['smallThumbnail'],
            caption="Нашёл:"
        )



def work_time(update, context):
    update.message.reply_text(
        "Время работы: круглосуточно.")


def search_book(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Искать по названию", callback_data='Введите название'),
            InlineKeyboardButton("Искать по автору", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('как будем проводить поиск?', reply_markup=reply_markup)


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


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
    global variant
    update.message.reply_text('''Вы активировали процесс входа. Чтобы прервать последующий диалог,
    используйте команду /stop. Пожалуйста, введите свой никнейм''')
    variant = 'ent1'
    return 21
    global main_flag
    if main_flag:
        update.message.reply_text('Вы активировали процесс входа. Чтобы прервать последующий диалог, '
                                  'используйте команду /stop. Пожалуйста, введите свой никнейм')
        main_flag = False
        return 21
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
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    conv_handler4 = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('test', test)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, first_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text & ~Filters.command, second_response)],
            3: [MessageHandler(Filters.text & ~Filters.command, third_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            4: [MessageHandler(Filters.text & ~Filters.command, fourth_response)],
            5: [MessageHandler(Filters.text & ~Filters.command, fifth_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            6: [MessageHandler(Filters.text & ~Filters.command, sixth_response)],
            7: [MessageHandler(Filters.text & ~Filters.command, seventh_response)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler4)
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("search_book", search_book))
    dp.add_handler(CommandHandler("search_by_author", search_by_author))
    dp.add_handler(CommandHandler("search_by_name", search_by_name))
    dp.add_handler(CommandHandler("work_time", work_time))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, param, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))

    text_handler = MessageHandler(Filters.text, param)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('link', link, pass_user_data=True))
    dp.add_handler(CommandHandler('quit', quit, pass_user_data=True))

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('registration', registration)],
        states={
            11: [MessageHandler(Filters.text & ~Filters.command, param, pass_user_data=True)],
            12: [MessageHandler(Filters.text & ~Filters.command, param, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('enter', enter)],
        states={
            21: [MessageHandler(Filters.text & ~Filters.command, param, pass_user_data=True)],
            22: [MessageHandler(Filters.text & ~Filters.command, param, pass_user_data=True)]
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
