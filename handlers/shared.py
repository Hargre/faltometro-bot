from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler

from models.class_model import ClassModel


def select_class_keyboard(update):
    classes = ClassModel.select().where(ClassModel.chat_id == update.message.chat_id)

    reply_keyboard = [[class_model.class_name for class_model in classes]]

    update.message.reply_text(
        'Qual a matéria?\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

def cancel(bot, update):
    update.message.reply_text(
        'Ação cancelada!',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def cancel_handler():
    return CommandHandler('cancelar', cancel)