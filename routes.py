# # routes.py
# from flask import render_template, request, redirect, url_for, send_from_directory, flash
# from werkzeug.utils import secure_filename
# from datetime import datetime
# import os

# from extensions import db
# from models import (
#     Member, Document, Publication, Event, Review,
#     MembershipApplication, EventAccreditationRequest
# )

# def register_routes(app):

#     @app.route('/')
#     def index():
#         return render_template('index.html')

#     @app.route('/about')
#     def about():
#         members = Member.query.all()
#         documents = Document.query.all()
#         return render_template('about.html', members=members, documents=documents)

#     @app.route('/search_members')
#     def search_members():
#         query = request.args.get('query', '')
#         members = Member.query.filter(Member.name.contains(query)).all()
#         return render_template('about.html', members=members, documents=Document.query.all())

#     @app.route('/documents/<filename>')
#     def download_document(filename):
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#     @app.route('/apply_membership', methods=['POST'])
#     def apply_membership():
#         name = request.form.get('name')
#         email = request.form.get('email')
#         if name and email:
#             application = MembershipApplication(name=name, email=email)
#             db.session.add(application)
#             db.session.commit()
#             flash(f'Заявка на вступление от {name} ({email}) отправлена!', 'success')
#         return redirect(url_for('about'))

#     @app.route('/apply_event_accreditation', methods=['POST'])
#     def apply_event_accreditation():
#         event_name = request.form.get('event_name')
#         event_date = request.form.get('event_date')
#         if event_name and event_date:
#             request_ = EventAccreditationRequest(event_name=event_name, event_date=event_date)
#             db.session.add(request_)
#             db.session.commit()
#             flash(f'Заявка на аккредитацию "{event_name}" на {event_date} отправлена!', 'success')
#         return redirect(url_for('about'))

#     @app.route('/upload_publication', methods=['POST'])
#     def upload_publication():
#         title = request.form.get('title')
#         authors = request.form.get('authors')
#         tags = request.form.get('tags')
#         file = request.files['file']
#         if file and title and authors:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join('uploads/publications', filename))
#             new_pub = Publication(title=title, authors=authors, tags=tags, file_path=filename)
#             db.session.add(new_pub)
#             db.session.commit()
#             flash('Публикация успешно загружена!', 'success')
#         return redirect(url_for('publications'))

#     @app.route('/publications')
#     def publications():
#         tag = request.args.get('tag')
#         query = Publication.query
#         if tag:
#             query = query.filter(Publication.tags.like(f"%{tag}%"))
#         publications = query.all()
#         return render_template('publications.html', publications=publications)

#     @app.route('/events')
#     def events():
#         events = Event.query.order_by(Event.date).all()
#         return render_template('events.html', events=events)

#     @app.route('/add_event', methods=['POST'])
#     def add_event():
#         title = request.form.get('title')
#         date = request.form.get('date')
#         description = request.form.get('description')
#         if title and date:
#             event = Event(title=title, date=datetime.strptime(date, '%Y-%m-%d'), description=description)
#             db.session.add(event)
#             db.session.commit()
#             flash('Мероприятие добавлено!', 'success')
#         return redirect(url_for('events'))

#     @app.route('/review/<int:pub_id>', methods=['POST'])
#     def add_review(pub_id):
#         reviewer_name = request.form.get('reviewer_name')
#         comment = request.form.get('comment')
#         if reviewer_name and comment:
#             review = Review(publication_id=pub_id, reviewer_name=reviewer_name, comment=comment)
#             db.session.add(review)
#             db.session.commit()
#             flash('Рецензия добавлена!', 'success')
#         return redirect(url_for('publications'))

#     @app.route('/upload_document', methods=['POST'])
#     def upload_document():
#         title = request.form.get('title')
#         file = request.files['file']
#         if file and title:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join('uploads/documents', filename))
#             doc = Document(title=title, filename=filename)
#             db.session.add(doc)
#             db.session.commit()
#             flash('Документ загружен!', 'success')
#         return redirect(url_for('documents'))

#     @app.route('/documents')
#     def documents():
#         docs = Document.query.all()
#         return render_template('documents.html', docs=docs)

#     @app.route('/surgeons')
#     def surgeons():
#         return render_template('surgeons.html')
