import logging

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from db_client.client import db_client
from telegram_bot.constants import (ABOUT_PROJECT, ABOUT_PROJECT_TEXT,
                                    BACK_TO_MAIN_MENU,
                                    BACK_TO_MAIN_MENU_BUTTON_TEXT,
                                    BACK_TO_SELECTION, CHOOSE_VPN_BUTTON_TEXT,
                                    CHOOSE_VPN_TEXT, CONNECTION_RESET_TEXT,
                                    ESTONIA, GEORGIA, GET_VPN_CLIENT,
                                    MAIN_MENU, MAIN_MENU_BUTTON_TEXT,
                                    MAIN_MENU_TEXT, OUTLINE_TEXT, POLAND,
                                    SELECTING_ACTION, SELECTING_VPN,
                                    SEND_NEW_VPN_CONNECTION, VPN_BUTTON_TEXT,
                                    WELCOME_MESSAGE,
                                    WELCOME_MESSAGE_BUTTON_TEXT,
                                    WELCOME_MESSAGE_TEXT)
from telegram_bot.utils import (delete_key, generate_keyboard_buttons,
                                return_user_selection, send_vpn_text)

logger = logging.getLogger(__name__)
logging.basicConfig(filename="telegram-bot.log")
logging.getLogger().setLevel(logging.INFO)


async def reset_connection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    delete_key(context.user_data["vpn"], update.effective_user.id)

    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            VPN_BUTTON_TEXT,
            callback_data=[SEND_NEW_VPN_CONNECTION, BACK_TO_SELECTION],
        )
    )

    text = send_vpn_text(
        context.user_data["vpn"],
        update.effective_user.id,
        update.callback_query.from_user,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""{CONNECTION_RESET_TEXT}

{text}""",
        reply_markup=keyboard,
        parse_mode="HTML",
    )

    return SEND_NEW_VPN_CONNECTION


async def vpn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    vpn_type = return_user_selection(int(query.data))

    context.user_data["vpn"] = vpn_type

    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            VPN_BUTTON_TEXT,
            callback_data=[SEND_NEW_VPN_CONNECTION, BACK_TO_SELECTION],
        )
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=OUTLINE_TEXT,
    )

    text = send_vpn_text(
        vpn_type, update.effective_user.id, update.callback_query.from_user
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )

    return SEND_NEW_VPN_CONNECTION


async def selection_vpn_nested(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["vpn"] = None
    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            CHOOSE_VPN_BUTTON_TEXT,
            callback_data=[POLAND, ESTONIA, GEORGIA, BACK_TO_MAIN_MENU],
        )
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOOSE_VPN_TEXT,
        reply_markup=keyboard,
    )

    return BACK_TO_SELECTION


async def selection_vpn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["vpn"] = None
    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            CHOOSE_VPN_BUTTON_TEXT,
            callback_data=[POLAND, ESTONIA, GEORGIA, BACK_TO_MAIN_MENU],
        )
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CHOOSE_VPN_TEXT,
        reply_markup=keyboard,
    )

    return SELECTING_VPN


async def about_the_project(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            BACK_TO_MAIN_MENU_BUTTON_TEXT,
            callback_data=[BACK_TO_MAIN_MENU],
        )
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ABOUT_PROJECT_TEXT,
        reply_markup=keyboard,
    )


async def main_menu_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            MAIN_MENU_BUTTON_TEXT,
            callback_data=[GET_VPN_CLIENT, ABOUT_PROJECT],
        )
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MAIN_MENU_TEXT,
        reply_markup=keyboard,
    )

    return BACK_TO_MAIN_MENU


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            MAIN_MENU_BUTTON_TEXT,
            callback_data=[GET_VPN_CLIENT, ABOUT_PROJECT],
        )
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MAIN_MENU_TEXT,
        reply_markup=keyboard,
    )

    return SELECTING_ACTION


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            WELCOME_MESSAGE_BUTTON_TEXT,
            callback_data=[MAIN_MENU],
        )
    )

    logger.info(
        f"Just started user {update.effective_user.id}, with username {update.message.from_user.username}"
    )
    db_client.add_user(update.effective_user.id)

    await update.message.reply_text(
        text=WELCOME_MESSAGE_TEXT,
        reply_markup=keyboard,
    )

    return WELCOME_MESSAGE
