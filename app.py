from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///organization.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

# Настройки Flask-Login
login_manager.login_view = 'login'  # Название view-функции логина
login_manager.login_message_category = 'info'



    
# ✅ Импорт маршрутов и админки после инициализации app и расширений

import admin
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from views import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
