import logging

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from telegram_bot.constants import (CONNECTION_RESET_TEXT, BACK_TO_SELECTION_BUTTON_TEXT, SEND_NEW_VPN_CONNECTION, SENDING_VPN_CLIENT, VPN_BUTTON_TEXT, BACK_TO_SELECTION, CHOOSE_VPN_BUTTON_TEXT, CHOOSE_VPN_TEXT, ESTONIA, POLAND, SELECTING_VPN, MAIN_MENU_BUTTON_TEXT, GET_VPN_CLIENT, ABOUT_PROJECT, BACK_TO_MAIN_MENU_BUTTON_TEXT, ABOUT_PROJECT_TEXT, MAIN_MENU_TEXT, BACK_TO_MAIN_MENU, WELCOME_MESSAGE_BUTTON_TEXT, WELCOME_MESSAGE_TEXT, WELCOME_MESSAGE, SELECTING_ACTION, MAIN_MENU)
from telegram_bot.utils import (generate_keyboard_buttons, return_user_selection, send_vpn_text, delete_key)
from db_client.client import db_client


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

    text = send_vpn_text(context.user_data["vpn"], update.effective_user.id, update.callback_query.from_user)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""{CONNECTION_RESET_TEXT}

{text}""",
        reply_markup=keyboard,
        parse_mode="HTML"
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

    text = send_vpn_text(vpn_type, update.effective_user.id, update.callback_query.from_user)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    return SEND_NEW_VPN_CONNECTION


async def selection_vpn_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["vpn"] = None
    keyboard = InlineKeyboardMarkup(
        generate_keyboard_buttons(
            CHOOSE_VPN_BUTTON_TEXT,
            callback_data=[POLAND, ESTONIA, BACK_TO_MAIN_MENU],
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
            callback_data=[POLAND, ESTONIA, BACK_TO_MAIN_MENU],
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