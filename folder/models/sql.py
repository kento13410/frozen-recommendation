from app import db

class food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    食品名 = db.Column(db.String, unique=False)
    カロリー = db.Column(db.Integer, unique=False)
    たんぱく質 = db.Column(db.Float, unique=False)
    脂質 = db.Column(db.Float, unique=False)
    炭水化物 = db.Column(db.Float, unique=False)
    値段 = db.Column(db.Integer, unique=False)
    画像 = db.Column(db.String, unique=False)
    url = db.Column(db.String, unique=False)
    カテゴリ = db.Column(db.String, unique=False)
    いいね = db.Column(db.Integer, unique=False)
    お気に入り = db.Column(db.Integer, unique=False)
    商品概要 = db.Column(db.String, unique=False)


class product_liked(db.Model):
    __tablename__ = 'product_liked'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String, unique=False)
    user_id = db.Column(db.Integer, unique=False)


class ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    食品名 = db.Column(db.String, unique=False)
    カロリー = db.Column(db.Integer, unique=False)
    たんぱく質 = db.Column(db.Float, unique=False)
    脂質 = db.Column(db.Float, unique=False)
    炭水化物 = db.Column(db.Float, unique=False)

class personal_data(db.Model):
    __tablename__ = 'personal_data'

    user_id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String, unique=False)
    age = db.Column(db.Integer, unique=False)
    weight = db.Column(db.Integer, unique=False)
    height = db.Column(db.Integer, unique=False)
    purpose = db.Column(db.String, unique=False)

class user(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    hash = db.Column(db.String, unique=False)
