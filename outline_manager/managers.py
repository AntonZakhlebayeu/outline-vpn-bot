from outline_manager.outline_manager import OutlineManager
from config.config import config


poland_manager = OutlineManager(url=config.get("POLAND_URL"), server_name="Poland VPN Server")
estonia_manager = OutlineManager(url=config.get("ESTONIA_URL"), server_name="Estonia VPN Server")
