import logging

from telegram.ext import CommandHandler

logger = logging.getLogger(__name__)

ADD_CLASS_QUESTION = range(1)

def start(bot, update):
    reply_keyboard = [['Sim', 'Não']]

    update.message.reply_text(
        'Bem-vindo! Medo de reprovar por falta naquela matéria insuportável? '
        'Estou aqui para evitar isso!\n\n'
        'Comece a adicionar matérias com /add-materia',
    )


def start_handler():
    handler = CommandHandler('start', start)
    return handler