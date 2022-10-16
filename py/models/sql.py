# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.orm import sessionmaker, scoped_session
from ..__init__ import db


# engine_food = create_engine('sqlite:///foodname.sqlite3', echo=True)
# engine_user = create_engine('sqlite:///users.sqlite3', echo=True)

# db_session = scoped_session(
#     sessionmaker(
#         autocommit = False,
#         autoflush = False,
#         bind = engine_food
#     )
# )

# Base = declarative_base()
# Base.query = db_session.query_property()

class Food(db.Model):
    __tablename__ = 'foodnames'

    id = db.Column(db.Integer, primary_key=True)
    食品名 = db.Column(db.String, unique=False)
    カロリー = db.Column(db.Integer, unique=False)
    タンパク質 = db.Column(db.Float, unique=False)
    脂質 = db.Column(db.Float, unique=False)
    炭水化物 = db.Column(db.Float, unique=False)
    値段 = db.Column(db.Integer, unique=False)
    画像 = db.Column(db.String, unique=False)
    url = db.Column(db.String, unique=False)
    カテゴリ = db.Column(db.String, unique=False)
    いいね = db.Column(db.Integer, unique=False)
    お気に入り = db.Column(db.Integer, unique=False)
    商品概要 = db.Column(db.String, unique=False)


class Product_liked(db.Model):
    __tablename__ = 'product_liked'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String, unique=False)
    user_id = db.Column(db.Integer, unique=False)


class Ingredient(db.Model):
    __tablename__ = '食品成分'

    id = db.Column(db.Integer, primary_key=True)
    食品名 = db.Column(db.String, unique=False)
    エネルギー = db.Column(db.Integer, unique=False)
    たんぱく質 = db.Column(db.Float, unique=False)
    脂質 = db.Column(db.Float, unique=False)
    炭水化物 = db.Column(db.Float, unique=False)

# Base.metadata.create_all(bind=engine_food)