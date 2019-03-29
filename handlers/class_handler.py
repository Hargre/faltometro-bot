import logging

from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler

from models.class_model import ClassModel

ASK_NAME, ASK_LIMIT = range(2)

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

def add_class_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('add-materia', add_class_entry)],
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
        fallbacks=[]
    )

    return handler


def list_classes(bot, update):
    classes = ClassModel.select().where(ClassModel.chat_id == update.message.chat_id)

    response = ''

    for class_model in classes:
        line = class_model.class_name + ':\t' + str(class_model.skipped_classes) + ' faltas\n'
        response += line
    
    update.message.reply_text(response)

def list_classes_handler():
    handler = CommandHandler('resumo', list_classes)
    return handler

def __save(user_data):
    ClassModel.create(
        chat_id = user_data['chat_id'],
        class_name = user_data['class_name'],
        skipped_classes_limit = int(user_data['skipped_classes_limit'])
    )

    