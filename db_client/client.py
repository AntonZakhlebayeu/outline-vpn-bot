from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_client.models import Base, User
from outline_manager.constants import VPNType

# TODO: Add logger for this file


class DatabaseClient:
    """Database client for communicating with the sqlite"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseClient, cls).__new__(cls, *args, **kwargs)
            cls._instance._engine = create_engine("sqlite:///outline-vpn-client.db")
            Base.metadata.create_all(cls._instance._engine)
            cls._instance._Session = sessionmaker(bind=cls._instance._engine)
        return cls._instance

    def __init__(self) -> None:
        self.session = self._Session()

    def add_user(self, user_id: int) -> None:
        existing_user = self.session.query(User).filter_by(id=user_id).first()
        if existing_user:
            return

        user = User(id=user_id)
        self.session.add(user)
        self.session.commit()

    def delete_user(self, user_id: int) -> None:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def add_key_id(self, user_id: int, vpn_type: VPNType, key_id: int) -> None:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            if vpn_type == VPNType.POLAND:
                user.poland_key_id = key_id
            elif vpn_type == VPNType.ESTONIA:
                pass
            elif vpn_type == VPNType.GEORGIA:
                user.georgia_key_id = key_id
            else:
                raise ValueError("Invalid VPN type")
            self.session.commit()

    def get_key_id(self, user_id: int, vpn_type: VPNType) -> None:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            if vpn_type == VPNType.POLAND:
                return user.poland_key_id
            elif vpn_type == VPNType.ESTONIA:
                pass
            elif vpn_type == VPNType.GEORGIA:
                return user.georgia_key_id
            else:
                raise ValueError("Invalid VPN type")

    def update_key_id(self, user_id: int, vpn_type: VPNType, new_key_id: int) -> None:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            if vpn_type == VPNType.POLAND:
                user.poland_key_id = new_key_id
            elif vpn_type == VPNType.ESTONIA:
                pass
            elif vpn_type == VPNType.GEORGIA:
                user.georgia_key_id = new_key_id
            else:
                raise ValueError("Invalid VPN type")
            self.session.commit()

    def remove_key_id(self, vpn_type: VPNType, user_id: int) -> None:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            if vpn_type == VPNType.POLAND:
                user.poland_key_id = None
            elif vpn_type == VPNType.ESTONIA:
                pass
            elif vpn_type == VPNType.GEORGIA:
                user.georgia_key_id = None
            else:
                raise ValueError("Invalid VPN type")
            self.session.commit()


db_client = DatabaseClient()
