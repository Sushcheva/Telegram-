from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import time
import datetime


def echo(update, context):
    if update.message.text == "/start":
        update.message.reply_text('Привет, я - книжный бот! Я помогу тебе в поиске нужной книги')
        update.message.reply_text('Для начала введи своё имя')
        update.message.reply_text('Если тебе будет что-то неясно, введи слово: "/help"')
    elif update.message.text == "/help":
        update.message.reply_texе(' чтобы начать общение сначала введите "/start",'
                                  'чтобы закончить диалог введите "/end"')
    elif update.message.text == "/time":
        update.message.reply_text(time.asctime())
    elif update.message.text == "/date":
        update.message.reply_text(time.strftime('%d-%m-%Y'))


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def name(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return


        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text)


def main():
    updater = Updater('5268756137:AAHyoEV3NSDQaQ0K6uszX_qJkL4omYGQtro', use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("name", name))
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()