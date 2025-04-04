from app import db  # Используем db из app.py

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