import logging
import math

from emoji import emojize

from peewee import DoesNotExist

from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler

from handlers.shared import cancel_handler
from handlers.shared import select_class_keyboard
from models.class_model import ClassModel

ASK_NAME, ASK_LIMIT = range(2)
DELETING_CLASS = range(1)

def add_class_entry(bot, update):
    update.message.reply_text(
        'Qual o nome da matéria?'
    )
    
    return ASK_NAME

def add_class_name(bot, update, user_data):
    class_name = update.message.text
    user_data['class_name'] = class_name

    update.message.reply_text(
        'Ok! E qual o limite de faltas?'
    )

    return ASK_LIMIT

def add_skip_limit(bot, update, user_data):
    skipped_classes_limit = update.message.text
    user_data['skipped_classes_limit'] = skipped_classes_limit
    user_data['chat_id'] = update.message.chat_id

    __save(user_data)

    update.message.reply_text(
        'Pronto!'
    )

    return ConversationHandler.END

def add_class_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('add_materia', add_class_entry)],
        states={
            ASK_NAME: [
                MessageHandler(
                    Filters.text,
                    add_class_name,
                    pass_user_data=True
                )
            ],
            ASK_LIMIT: [
                RegexHandler(
                    '^\d+$',
                    add_skip_limit,
                    pass_user_data=True
                )
            ],
        },
        fallbacks=[cancel_handler()]
    )

    return handler


def list_classes(bot, update):
    classes = ClassModel.select().where(ClassModel.chat_id == update.message.chat_id)

    response = ''

    for class_model in classes:
        line = (
            '*%s:*\t\t\t\t```\n%s / %s faltas\t\t\t\t%s```\n\n'
            % (
                class_model.class_name,
                class_model.skipped_classes,
                class_model.skipped_classes_limit,
                __get_status_emoji(class_model.skipped_classes, class_model.skipped_classes_limit)
            )
        )
        response += line
    
    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)



def list_classes_handler():
    handler = CommandHandler('resumo', list_classes)
    return handler


def delete_class_entry(bot, update):
    select_class_keyboard(update)
    return DELETING_CLASS

def delete_class(bot, update):
    class_name = update.message.text
    chat_id = update.message.chat_id

    try:
        missed_class = ClassModel.get((ClassModel.chat_id == chat_id) & (ClassModel.class_name == class_name))
        missed_class.delete_instance()

        update.message.reply_text(
            'Matéria removida!',
            parse_mode=ParseMode.MARKDOWN
        )

        return ConversationHandler.END
    except DoesNotExist:
        update.message.reply_text(
            'Não conheço essa matéria! Tente novamente.'
        )


def delete_class_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('tirar_materia', delete_class_entry)],
        states={
            DELETING_CLASS: [
                MessageHandler(
                    Filters.text,
                    delete_class,
                )
            ],
        },
        fallbacks=[cancel_handler()]
    )

    return handler


def __get_status_emoji(skipped_classes, skipped_classes_limit):
    status_ok = emojize(":white_check_mark:", use_aliases=True)
    status_warning = emojize(":warning:", use_aliases=True)
    status_danger = emojize(":sos:", use_aliases=True)
    status_failed = emojize(":x:", use_aliases=True)

    skipped_percent = (skipped_classes * 100) / skipped_classes_limit
    skipped_percent = math.floor(skipped_percent)

    if skipped_percent < 40:
        return status_ok
    elif skipped_percent >= 40 and skipped_percent < 70:
        return status_warning
    elif skipped_percent >= 70 and skipped_percent < 100:
        return status_danger
    else:
        return status_failed

def __save(user_data):
    ClassModel.create(
        chat_id = user_data['chat_id'],
        class_name = user_data['class_name'],
        skipped_classes_limit = int(user_data['skipped_classes_limit'])
    )

    