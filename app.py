from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///organization.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Импортируем маршруты
from views import *

# ✅ ВАЖНО: импорт admin ПЕРЕМЕЩЕН СЮДА
import admin

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
