import requests as req
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5146192395:AAFuwm-__5uK-tG7tfirvAWXCfo97idma54'


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def start(update, context):
    reply_keyboard = [['/search_book', '/test'],
                      ['/site', '/work_time'],
                      ['/phone', '/address']
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Я бот-справочник. Что вы хотите получить?",
        reply_markup=markup
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
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
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


def param(update, context):
    global variant
    print(update.message.text)
    context.user_data['dan'] = update.message.text
    if variant == 'Введите название':
        search_by_name(update, context)
    else:
        search_by_author(update, context)


def button(update, _):
    global variant
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    with open('files/Толстой.txt', 'w') as f:
        if variant == 'Введите название' or variant == 'Введите автора':
            query.edit_message_text(text=variant)
        else:
            f.write(choose)
    query.edit_message_text(text=variant)


def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    # Следующее текстовое сообщение будет обработано
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # обработчиком states[2]
    return 2


def second_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 3


def third_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 4


def fourth_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 5


def fifth_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 6


def sixth_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 7


def seventh_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 8


def eith_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    keyboard = [
        [
            InlineKeyboardButton("Дворецкий", callback_data='Введите название'),
            InlineKeyboardButton("Пришелец, который захватывает миры", callback_data='Введите автора'),
            InlineKeyboardButton("На самом деле и есть жертва, и все действие происходит в голове автора",
                                 callback_data='Введите автора'),
            InlineKeyboardButton("Никого не убил, а главные герои вместе и счастливы", callback_data='Введите автора'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вaм нравится, когда убийца...", reply_markup=reply_markup)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
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

        update.message.reply_text(x['averageRating'])


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

        update.message.reply_text(x['averageRating'])


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


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('test', start)],

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
            7: [MessageHandler(Filters.text & ~Filters.command, seventh_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            8: [MessageHandler(Filters.text & ~Filters.command, eith_response)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("search_book", search_book))
    dp.add_handler(CommandHandler("search_by_author", search_by_author))
    dp.add_handler(CommandHandler("search_by_name", search_by_name))
    dp.add_handler(CommandHandler("work_time", work_time))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, param, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
