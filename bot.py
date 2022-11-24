from parsehh import *
from graph import *
from dbmigrations import *
from utils import *
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import os.path


def make_image(vacancy):
    if os.path.exists(f'images/{vacancy}.png'):
        logging.info("there is a photo")
    else:
        logging.info("there is no photo")
        get_vacancy_graph(vacancy)



def get_vacancy_graph(vacancy):
    if check_vacancy(vacancy):
        logging.warning("we already have data in bd, just making graph")
        listof_avg_vacancy = get_vacancy_salary(vacancy)
        #return listof_avg_vacancy
        create_graph(listof_avg_vacancy, vacancy)
    else:
        logging.warning("its time to parse")
        parsehh(vacancy)
        logging.warning("we parsed, now make graph")
        listof_avg_vacancy = get_vacancy_salary(vacancy)
        create_graph(listof_avg_vacancy, vacancy)


async def push(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f'bot use echo comand in {update.effective_chat.id} chat')
    vacancy = update.message.text
    make_image(vacancy)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'images/{vacancy}.png', 'rb'))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f'bot use start comand in {update.effective_chat.id} chat')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please tell me what vacancy avg salaries you want to get?")


async def ask_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f'bot use ask_vacancy comand in {update.effective_chat.id} chat')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="what vacancy avg salaries you want to get?")


def start_bot():
    create_db()
    logging.info("starting bot")
    token=str(get_config_args()['BOTOKEN'])
    application = ApplicationBuilder().token(token).build()
    logging.info("bot connected")
    start_handler = CommandHandler('start', start)
    push_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), push)
    application.add_handler(start_handler)
    application.add_handler(push_handler)
    application.run_polling()


