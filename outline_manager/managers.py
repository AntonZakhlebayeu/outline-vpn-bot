from config.config import config
from outline_manager.outline_manager import OutlineManager

poland_manager = OutlineManager(
    url=config.get("POLAND_URL"), server_name="Poland VPN Server"
)
estonia_manager = OutlineManager(
    url=config.get("ESTONIA_URL"), server_name="Estonia VPN Server"
)
georgia_manager = OutlineManager(
    url=config.get("GEORGIA_URL"), server_name="Georgia VPN Server"
)
