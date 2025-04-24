from app import db  # Используем db из app.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import ForeignKey

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False)

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(255), nullable=False)  # Сохраняем через запятую
    file_path = db.Column(db.String(255), nullable=False)  # Путь к файлу

    def get_tags(self):
        return self.tags.split(',')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'))
    reviewer_name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    publication = db.relationship('Publication', backref=db.backref('reviews', lazy=True))

class MembershipApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    approved = db.Column(db.Boolean, default=False)

class EventAccreditation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    approved = db.Column(db.Boolean, default=False)


## for pacients
class CertifiedSpecialist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=True)
    certification_date = db.Column(db.Date, nullable=True)

class EthicsDecision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    decision_date = db.Column(db.Date, nullable=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Implant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    manufacturer = db.Column(db.String(200), nullable=False)
    certification_number = db.Column(db.String(100), nullable=False)

#flask-login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=True)  # Для отображения имени пользователя
    first_name = db.Column(db.String(150))
    avatar = db.Column(db.String(100), nullable=True, default='default_avatar.png')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)


class NewsItem(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)  # будет использоваться в ссылке
    content = db.Column(db.Text)
    file_path = db.Column(db.String(200))  # путь к изображению

    def __repr__(self):
        return self.title or f'News #{self.id}'


# Обновим SliderItem, добавив связь с новостью
class SliderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200))

    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    news = db.relationship('NewsItem', backref='sliders')

    def __repr__(self):
        return self.title or f'Slider #{self.id}'
