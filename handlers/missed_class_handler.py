import logging

from peewee import DoesNotExist

from telegram import ParseMode
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from models.class_model import ClassModel

logger = logging.getLogger(__name__)

SELECTING_CLASS = range(1)

def ask_for_class(bot, update):
    classes = ClassModel.select().where(ClassModel.chat_id == update.message.chat_id)

    reply_keyboard = [[class_model.class_name for class_model in classes]]

    update.message.reply_text(
        'Qual a matéria?\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return SELECTING_CLASS

def missed_class(bot, update):
    class_name = update.message.text
    chat_id = update.message.chat_id

    try:
        missed_class = ClassModel.get((ClassModel.chat_id == chat_id) & (ClassModel.class_name == class_name))
        logger.info("User %s skipped class: %s", update.message.from_user.first_name, missed_class.class_name)

        missed_class.skipped_classes += 1
        missed_class.save()

        update.message.reply_text(
            'Falta salva! Você já faltou *%s* vezes, e seu limite é de *%s* faltas.'
            % (missed_class.skipped_classes, missed_class.skipped_classes_limit),
            parse_mode=ParseMode.MARKDOWN
        )

        return ConversationHandler.END
    except DoesNotExist:
        update.message.reply_text(
            'Não conheço essa matéria! Tente novamente.'
        )


def missed_class_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('faltei', ask_for_class)],
        states={
            SELECTING_CLASS: [MessageHandler(Filters.text, missed_class)]
        },
        fallbacks=[]
    )

    return handler