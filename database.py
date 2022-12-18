from aiogram.types import message
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from aiogram import types


engine = create_engine('sqlite:///translabot.db', echo=False)
Base = declarative_base()

session = Session(bind=engine)

class User(Base):
    """
    Модель User
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(String)
    lang = Column(String)

    def __init__(self,
        user_id:int=0,
        name: str='',
        lang: str='ru'
    ):
        self.user_id = user_id
        self.name = name
        self.lang = lang

    def __repr__(self):
        return f"<User('{self.user_id}', '{self.name}')>"


class DB:
    def __init__(self, message: types.Message):
        self.message = message

    def create_tables(self):
        """Создание БД и таблиц"""
        Base.metadata.create_all(engine)
        return "Успешно создано"

    def reg(self):
        """Регистрация пользователя"""
        try:
            user = User(
                user_id=self.message.from_user.id,
                name=self.message.from_user.first_name,
                lang="ru"
            )
            session.add(user)
            session.commit()
            return self.get()
        except:
            session.rollback()
        finally:
            session.close()

    def get(self, **kw):
        """Чтение данных пользователя из таблицы"""
        if kw:
            if "is_all" in kw.keys():
                result = [user for user in session.query(User).distinct()]
            else:
                result = session.query(User).filter_by(**kw).first()
        else:
            result = session.query(User).filter_by(user_id=self.message.from_user.id).first()
        return result

    def update(self, instance):
        """Обновление данных пользователя"""
        try:
            session.add(instance)
            session.commit()
            return instance
        except Exception as e:
            print(e)

