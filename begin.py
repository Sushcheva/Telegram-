from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from data import db_session
from telegram.ext import Updater, MessageHandler, Filters


TOKEN = '5268756137:AAHyoEV3NSDQaQ0K6uszX_qJkL4omYGQtro'
WEATHER_TOKEN = ''
new_name = ''
current_area = ''


def password(update, context):
    password = update.message.text
    db_session.global_init("db/books.db")
    db_sess = db_session.create_session()
    user = User()
    user.name = new_name
    user.password = password
    user.latest_city = ''
    user.constant_city = ''
    db_sess.add(user)
    db_sess.commit()
    update.message.reply_text('Поздравляем! Вы зарегестрировались!')
    return ConversationHandler.END
def new(update, context):
    update.message.reply_text('''Здравствуйте! Это Книжный бот!
    Чтобы начать поиск книг, введите свой никнейм для 
    регистрации. Если хотите закончить - команду /stop. ''')
    return 1


def name(update, context):
    global new_name
    new_name = update.message.text
    update.message.reply_text('Теперь придумайте пароль')
    return 2


def stop(update, context):
    update.message.reply_text('stop')
    return ConversationHandler.END


def start(update, context):
    update.message.reply_text('Здравствуйте! Это Книжный бот!'
                              'Чтобы начать поиск книг, введите свой никнейм для '
                              'регистрации. Если хотите закончить - команду /stop.')


def help(update, context):
    update.message.reply_text('Help')


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, name)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new_person', new)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, name)],
            2: [MessageHandler(Filters.text & ~Filters.command, password)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    db_session.global_init("db/books1.db")
    main()