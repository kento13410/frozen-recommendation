from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 追加

app = Flask(__name__)
app.config.from_object('py.config')

db = SQLAlchemy(app)  # 追加
# インスタンス化され、db.~とすることでクラスSQLAlchemyのメソッドが使用できる
from .models import sql

