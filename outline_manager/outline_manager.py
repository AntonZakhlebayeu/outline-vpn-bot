from outline.client import OutlineClient
from db_client.client import db_client
from outline_manager.constants import VPNType
from telegram import User


class OutlineManager:
    def __init__(self, url: str, server_name: str = "Outline Server") -> None:
        self.client = OutlineClient(url)
        if self.client:
            self.client.rename(server_name)
            print(self.client.metrics.total)

    def create_a_new_free_key(self, vpn_type: VPNType, user_id: int, user: User) -> str:
        key = self.client.new(name=str(user_id))
        key.change_data_limit(10000000)
        db_client.add_key_id(user_id, vpn_type, key.id)
        last_name = f" {user.last_name}" if user.last_name else ""
        return key.url(f"{user.first_name}{last_name} {vpn_type}")
    
    def remove_key(self, user_id: int, vpn_type: VPNType) -> None:
        key_id = db_client.get_key_id(user_id, vpn_type)
        self.client.delete_key(key_id)
        db_client.remove_key_id(vpn_type, user_id)
