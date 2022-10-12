from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, scoped_session


engine_food = create_engine('sqlite:///foodname.sqlite3', echo=True)
engine_user = create_engine('sqlite:///users.sqlite3', echo=True)

db_session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine_food
    )
)

Base = declarative_base()
Base.query = db_session.query_property()

class Food(Base):
    __tablename__ = 'foodnames'

    id = Column(Integer, primary_key=True)
    食品名 = Column(String, unique=False)
    カロリー = Column(Integer, unique=False)
    タンパク質 = Column(Float, unique=False)
    脂質 = Column(Float, unique=False)
    炭水化物 = Column(Float, unique=False)
    値段 = Column(Integer, unique=False)
    画像 = Column(String, unique=False)
    url = Column(String, unique=False)
    カテゴリ = Column(String, unique=False)
    いいね = Column(Integer, unique=False)
    お気に入り = Column(Integer, unique=False)
    商品概要 = Column(String, unique=False)


class Product_liked(Base):
    __tablename__ = 'product_liked'

    id = Column(Integer, primary_key=True)
    product = Column(String, unique=False)
    user_id = Column(Integer, unique=False)


class Ingredient(Base):
    __tablename__ = '食品成分'

    id = Column(Integer, primary_key=True)
    食品名 = Column(String, unique=False)
    エネルギー = Column(Integer, unique=False)
    たんぱく質 = Column(Float, unique=False)
    脂質 = Column(Float, unique=False)
    炭水化物 = Column(Float, unique=False)

Base.metadata.create_all(bind=engine_food)