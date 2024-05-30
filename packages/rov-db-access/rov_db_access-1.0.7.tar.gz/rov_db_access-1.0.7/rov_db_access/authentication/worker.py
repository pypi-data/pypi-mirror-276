from sqlalchemy import select

from rov_db_access.config.db_utils import init_db_engine
from rov_db_access.config.settings import Settings
from sqlalchemy.orm import Session
from rov_db_access.authentication.models import User

settings = Settings()

class AuthenticationWorker:

    def __init__(self) -> None:

        self.engine = init_db_engine(
            settings.db_rov_gis_user,
            settings.db_rov_gis_password,
            settings.db_rov_gis_host,
            settings.db_rov_gis_port,
            settings.db_rov_gis_database
        )

    def get_user_by_username(self, username: str):
        with Session(self.engine) as session:
            user_query = (
                select(User)
                .where(User.username == username)
                .limit(1)
            )
            user = session.scalar(user_query)
            roles = user.roles
            return {"user": user, "user_roles": roles}

    def create_user(self, username: str, password: str):
        with Session(self.engine) as session:
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()
            return new_user
