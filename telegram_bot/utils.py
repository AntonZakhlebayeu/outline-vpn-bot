from telegram import InlineKeyboardButton, User

from outline_manager.constants import VPNType
from outline_manager.managers import (georgia_manager,
                                      poland_manager)
from telegram_bot.constants import POLAND, ESTONIA, GEORGIA


def return_user_selection(selection: int) -> VPNType:
    if selection == POLAND:
        return VPNType.POLAND
    elif selection == ESTONIA:
        return VPNType.ESTONIA
    elif selection == GEORGIA:
        return VPNType.GEORGIA


def return_key(vpn_type: VPNType, user_id: str, user: User) -> str:
    if vpn_type == VPNType.POLAND:
        return poland_manager.create_a_new_free_key(vpn_type, user_id, user)
    elif vpn_type == VPNType.ESTONIA:
        pass
    elif vpn_type == VPNType.GEORGIA:
        return georgia_manager.create_a_new_free_key(vpn_type, user_id, user)
    else:
        raise ValueError("Unsupported VPN type.")


def delete_key(vpn_type: VPNType, user_id: str) -> None:
    if vpn_type == VPNType.POLAND:
        poland_manager.remove_key(user_id, vpn_type)
    elif vpn_type == VPNType.ESTONIA:
        pass
    elif vpn_type == VPNType.GEORGIA:
        georgia_manager.remove_key(user_id, vpn_type)
    else:
        raise ValueError("Unsupported VPN type.")


def send_vpn_text(vpn_type: VPNType, user_id: str, user: User) -> str:
    key = return_key(vpn_type, user_id, user)
    return f"""You are currently connected via {vpn_type} VPN. Feel free to use the VPN service as long as you need.
If you'd like to reset your connection data, just click the "Retrieve new VPN connection" button. This will allow you to start a new session from the beginning.

<code>{key}</code>"""


def generate_keyboard_buttons(
    options: list, callback_data: list = None, urls: list = None
) -> list:
    if not callback_data:
        callback_data = [None] * len(options)

    if not urls:
        urls = [None] * len(options)

    if len(options) != len(callback_data) or len(options) != len(urls):
        raise ValueError(
            "Length of options should be equal to the length of callback_data and urls."
        )

    button_list = []

    for option, cb_data, url in zip(options, callback_data, urls):
        if cb_data and url:
            raise ValueError(
                "Each option should have either callback_data or a URL, not both."
            )

        if url:
            button = [InlineKeyboardButton(text=option, url=url)]
        else:
            button = [InlineKeyboardButton(text=option, callback_data=str(cb_data))]

        button_list.append(button)

    return button_list


def generate_column_oriented_buttons(
    options: list, callback_data: list = None, urls: list = None, columns: int = 2
) -> list:
    if not callback_data:
        callback_data = [None] * len(options)

    if not urls:
        urls = [None] * len(options)

    if len(options) != len(callback_data) or len(options) != len(urls):
        raise ValueError(
            "Length of options should be equal to the length of callback_data and urls."
        )

    button_list = []

    for option, cb_data, url in zip(options, callback_data, urls):
        if cb_data and url:
            raise ValueError(
                "Each option should have either callback_data or a URL, not both."
            )

        if url:
            button = InlineKeyboardButton(text=option, url=url)
        else:
            button = InlineKeyboardButton(text=option, callback_data=str(cb_data))

        button_list.append(button)

    return [button_list[n : n + columns] for n in range(0, len(button_list), columns)]
