import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater

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
    
    updater.start_polling()
    logger.info("Polling started...")
    updater.idle()

if __name__ == '__main__':
    main()