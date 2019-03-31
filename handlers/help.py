from telegram import ParseMode
from telegram.ext import CommandHandler

def help(bot, update):
    update.message.reply_text(
        '/add\_materia - Adiciona uma nova matéria à sua lista.\n\n'
        '/tirar\_materia - Retira uma matéria de sua lista.\n\n'
        '/resumo - Exibe sua situação de faltas em todas as matérias.\n\n'
        '/faltei - Adiciona uma falta a uma de suas matérias.\n\n'
        '/tirar\_falta - Retira uma falta de uma de suas matérias.\n\n'
        '/cancelar - Cancela qualquer ação em andamento.\n\n',
        parse_mode=ParseMode.MARKDOWN
    )

def help_handler():
    return CommandHandler('ajuda', help)