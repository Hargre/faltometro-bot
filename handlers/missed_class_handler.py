import logging

from peewee import DoesNotExist

from telegram import ParseMode
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from flavor.missed_class_responses import choose_missed_class_response
from handlers.shared import cancel_handler
from handlers.shared import select_class_keyboard
from models.class_model import ClassModel

logger = logging.getLogger(__name__)

SELECTING_CLASS = range(1)

def ask_for_class(bot, update):
    select_class_keyboard(update)
    return SELECTING_CLASS

def missed_class(bot, update):
    class_name = update.message.text
    chat_id = update.message.chat_id

    try:
        missed_class = ClassModel.get((ClassModel.chat_id == chat_id) & (ClassModel.class_name == class_name))

        missed_class.skipped_classes += 1
        missed_class.save()

        response = choose_missed_class_response(missed_class.skipped_classes, missed_class.skipped_classes_limit)
        response += (
            '\n\nVocê já faltou *%s* vezes, de um limite de *%s* faltas.'
            % (missed_class.skipped_classes, missed_class.skipped_classes_limit)
        )

        update.message.reply_text(
            response,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardRemove()
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
        fallbacks=[cancel_handler()]
    )

    return handler


def remove_missed_class(bot, update):
    class_name = update.message.text
    chat_id = update.message.chat_id

    try:
        missed_class = ClassModel.get((ClassModel.chat_id == chat_id) & (ClassModel.class_name == class_name))

        if not missed_class.skipped_classes:
            update.message.reply_text(
                'Não há faltas para remover!',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        missed_class.skipped_classes -= 1
        missed_class.save()

        update.message.reply_text(
            'Falta removida! Você agora tem *%s* falta(s), de um limite de *%s*.'
            % (missed_class.skipped_classes, missed_class.skipped_classes_limit),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END
    except DoesNotExist:
        update.message.reply_text(
            'Não conheço essa matéria! Tente novamente.'
        )

def remove_missed_class_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('tirar_falta', ask_for_class)],
        states={
            SELECTING_CLASS: [MessageHandler(Filters.text, remove_missed_class)]
        },
        fallbacks=[cancel_handler()]
    )

    return handler