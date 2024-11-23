from config.config import config
from outline_manager.outline_manager import OutlineManager
from telegram_bot.telegram_bot import TelegramBot


def main() -> None:
    telegram_client = TelegramBot()
    telegram_client.run_telegram_client()


if __name__ == "__main__":
    main()
