from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # Создаём экземпляр, но пока не привязываем к app

app = Flask(__name__)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///organization.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db.init_app(app)  # Теперь привязываем db к app
migrate = Migrate(app, db)  

# Импортируем маршруты ПОСЛЕ создания app
from routes import *
from views import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Теперь должно работать без ошибки
    app.run(debug=True)

