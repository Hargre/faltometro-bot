import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater

from handlers.start import start_handler
from handlers.class_handler import add_class_handler
from handlers.class_handler import delete_class_handler
from handlers.class_handler import list_classes_handler
from handlers.help import help_handler
from handlers.missed_class_handler import missed_class_handler

def __setup_logger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def main():
    __setup_logger()
    logger = logging.getLogger(__name__)

    load_dotenv()
    token = os.getenv('BOT_API_TOKEN')

    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Add handlers to dispatcher here
    dispatcher.add_handler(start_handler())
    dispatcher.add_handler(add_class_handler())
    dispatcher.add_handler(delete_class_handler())
    dispatcher.add_handler(list_classes_handler())
    dispatcher.add_handler(missed_class_handler())
    dispatcher.add_handler(help_handler())
    
    updater.start_polling()
    logger.info("Polling started...")
    updater.idle()

if __name__ == '__main__':
    main()