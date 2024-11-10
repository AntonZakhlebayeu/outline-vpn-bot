from telegram_bot.telegram_bot import TelegramBot
from outline_manager.outline_manager import OutlineManager
from config.config import config


def main() -> None:
    telegram_client = TelegramBot()
    telegram_client.run_telegram_client()


if __name__ == '__main__':
    main()
