from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..schemas import UserBase
from . import models
from .hash import Hash

class Postgres_DB:
    def __init__(self, user_name, password, host, port, database_name):
        self._user = user_name
        self._password = password
        self._host = host
        self._port = port
        self._database = database_name

        try:
            self._engine = create_engine(url=f"postgresql+psycopg2://{self._user}:{self._password}@{self._host}:{self._port}/{self._database}")
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
            print(f'Connection to the {self._host} for user {self._user} created sucessfully.')
        except Exception as ex:
            print(f'Connection could not be made due to the following error: {ex}.')

    def get_db(self):
        db = self._SessionLocal()
        try:
            return db
        finally:
            db.close()

    def create_user(self, user: UserBase):
        with self.get_db() as db:
            deleted_id = db.query(models.DbDeletedUsers).first()
            if deleted_id:
                new_user = models.DbUser(
                    id=deleted_id.id,
                    username=user.username,
                    email=user.email,
                    password=Hash.bcrypt(user.password)
                )
                db.delete(deleted_id)
            else:
                new_user = models.DbUser(
                    username=user.username,
                    email=user.email,
                    password=Hash.bcrypt(user.password)
                    )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        
    def get_all_users(self):
        with self.get_db() as db:
            return db.query(models.DbUser).all()
    
    def get_user(self, id: int):
        with self.get_db() as db:
            return db.query(models.DbUser).filter(models.DbUser.id == id).first()

    def update_user(self, id: int, new_user: UserBase):
            with self.get_db() as db:
                user = db.query(models.DbUser).filter(models.DbUser.id == id)
                user.update({
                    models.DbUser.username: new_user.username,
                    models.DbUser.email: new_user.email,
                    models.DbUser.password: Hash.bcrypt(new_user.password)
                })
                db.commit()
                return "User was updated sucessfully."

    def delete_user(self, id: int):
        with self.get_db() as db:
            user = db.query(models.DbUser).filter(models.DbUser.id == id).first()
            deleted_user = models.DbDeletedUsers(
                    id=id
                    )
            db.add(deleted_user)
            db.delete(user)
            db.commit()
            return "User was deleted sucessfully."

postgre_db = Postgres_DB('postgres', 000, '127.0.0.1', 5432, 'postgres')