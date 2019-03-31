import logging

from telegram.ext import CommandHandler

logger = logging.getLogger(__name__)

ADD_CLASS_QUESTION = range(1)

def start(bot, update):
    update.message.reply_text(
        'Bem-vindo! Em dúvida se ainda dá pra faltar ou não naquela matéria insuportável? '
        'Estou aqui para evitar isso!\n\n'
        'Comece a adicionar matérias com /add_materia\n\n'
        'Para informações sobre os comandos, digite /ajuda'
    )


def start_handler():
    handler = CommandHandler('start', start)
    return handler