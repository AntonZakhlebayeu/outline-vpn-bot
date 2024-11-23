import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, PicklePersistence, filters)

from config.config import config
from telegram_bot.bot_methods import (about_the_project, main_menu,
                                      main_menu_nested, reset_connection,
                                      selection_vpn, selection_vpn_nested,
                                      start, vpn)
from telegram_bot.constants import (ABOUT_PROJECT, BACK_TO_MAIN_MENU,
                                    BACK_TO_SELECTION, ESTONIA, GEORGIA,
                                    GET_VPN_CLIENT, MAIN_MENU, POLAND,
                                    SELECTING_ACTION, SELECTING_VPN,
                                    SEND_NEW_VPN_CONNECTION, WELCOME_MESSAGE)
from telegram_bot.conversation_handler_factory import \
    ConversationHandlerFactory


class TelegramBot:
    """This is a telegram client for communicating with ChatGPT using the telegram client"""

    def __init__(self) -> None:
        persistence = PicklePersistence(
            filepath="outline_vpn_manager.pkl", update_interval=1
        )
        self.__application = (
            Application.builder()
            .token(config.get("TELEGRAM_TOKEN"))
            .read_timeout(30)
            .write_timeout(30)
            .persistence(persistence)
            .build()
        )
        self.__conversation_handler_factory = ConversationHandlerFactory(
            persistent=True
        )

    def __configure_telegram_client(self):
        """Configure telegram client using ConversationHandlerFactory"""
        vpn_handler = self.__conversation_handler_factory.create(
            entry_points=[
                CallbackQueryHandler(
                    vpn, pattern=f"^{str(POLAND)}$|{str(ESTONIA)}$|{str(GEORGIA)}$"
                ),
            ],
            states={},
            fallbacks=[
                CallbackQueryHandler(
                    selection_vpn_nested,
                    pattern=f"^{str(BACK_TO_SELECTION)}$",
                ),
                CallbackQueryHandler(
                    reset_connection,
                    pattern=f"^{str(SEND_NEW_VPN_CONNECTION)}$",
                ),
            ],
            map_to_parent={BACK_TO_SELECTION: SELECTING_VPN},
            name="chat_gpt_conv",
        )

        get_vpn_handler = self.__conversation_handler_factory.create(
            entry_points=[
                CallbackQueryHandler(selection_vpn, pattern=f"^{str(GET_VPN_CLIENT)}$"),
            ],
            states={
                SELECTING_VPN: [
                    vpn_handler,
                ],
            },
            fallbacks=[
                CallbackQueryHandler(
                    main_menu_nested,
                    pattern=f"^{str(BACK_TO_MAIN_MENU)}$",
                ),
                CallbackQueryHandler(
                    selection_vpn, pattern=f"^{str(BACK_TO_SELECTION)}$"
                ),
            ],
            map_to_parent={BACK_TO_MAIN_MENU: SELECTING_ACTION},
            name="ask_gpt_conv",
        )

        main_menu_handler = self.__conversation_handler_factory.create(
            entry_points=[
                CallbackQueryHandler(main_menu, pattern=f"^{str(MAIN_MENU)}$"),
            ],
            states={
                SELECTING_ACTION: [
                    get_vpn_handler,
                ],
            },
            fallbacks=[
                CallbackQueryHandler(
                    main_menu,
                    pattern=f"^{str(BACK_TO_MAIN_MENU)}$",
                ),
                CallbackQueryHandler(
                    about_the_project, pattern=f"^{str(ABOUT_PROJECT)}$"
                ),
            ],
            name="main_menu_conv",
        )

        start_handler = self.__conversation_handler_factory.create(
            entry_points=[CommandHandler("start", start)],
            states={
                WELCOME_MESSAGE: [
                    main_menu_handler,
                ],
            },
            fallbacks=[],
            name="start_conv_handler",
        )

        self.__application.add_handler(start_handler)

    def run_telegram_client(self) -> None:
        """Start up the telegram client"""
        self.__configure_telegram_client()

        self.__application.run_polling(timeout=1000, allowed_updates=Update.ALL_TYPES)
