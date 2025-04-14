from flask import render_template, request, redirect, url_for, send_from_directory, flash
from app import app, db
from models import Member, Document, Publication, Event, Review  # Импортируем модели

from models import MembershipApplication, EventAccreditation
from datetime import datetime  # уже импортирован, если нет — добавь
from models import CertifiedSpecialist, Implant, Article, EthicsDecision


from models import User
from flask import session

@app.route('/')
def index():
    return render_template('index.html')
    
# Страница "Об организации"
@app.route('/about')
def about():
    members = Member.query.all()
    documents = Document.query.all()
    return render_template('about.html', members=members, documents=documents)

# Поиск членов организации
@app.route('/search_members')
def search_members():
    query = request.args.get('query', '')
    members = Member.query.filter(Member.name.contains(query)).all()
    return render_template('about.html', members=members, documents=Document.query.all())

# Загрузка документов
@app.route('/documents/<filename>')
def download_document(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Обработка заявки на вступление
@app.route('/apply_membership', methods=['POST'])
def apply_membership():
    name = request.form.get('name')
    email = request.form.get('email')
    if name and email:
        application = MembershipApplication(name=name, email=email)
        db.session.add(application)
        db.session.commit()
        flash(f'Заявка на вступление от {name} ({email}) отправлена!', 'success')
    return redirect(url_for('about'))


# Обработка заявки на аккредитацию мероприятия
@app.route('/apply_event_accreditation', methods=['POST'])
def apply_event_accreditation():
    event_name = request.form.get('event_name')
    event_date = request.form.get('event_date')
    if event_name and event_date:
        application = EventAccreditation(event_name=event_name, event_date=datetime.strptime(event_date, '%Y-%m-%d'))
        db.session.add(application)
        db.session.commit()
        flash(f'Заявка на аккредитацию "{event_name}" на {event_date} отправлена!', 'success')
    return redirect(url_for('about'))

@app.route('/upload_publication', methods=['POST'])
def upload_publication():
    title = request.form.get('title')
    authors = request.form.get('authors')
    tags = request.form.get('tags')
    file = request.files['file']

    if file and title and authors:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads/publications', filename))
        new_pub = Publication(title=title, authors=authors, tags=tags, file_path=filename)
        db.session.add(new_pub)
        db.session.commit()
        flash('Публикация успешно загружена!', 'success')

    return redirect(url_for('publications'))

@app.route('/publications')
def publications():
    tag = request.args.get('tag')
    query = Publication.query
    if tag:
        query = query.filter(Publication.tags.like(f"%{tag}%"))
    publications = query.all()
    return render_template('publications.html', publications=publications)

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form.get('title')
    date = request.form.get('date')
    description = request.form.get('description')

    if title and date:
        event = Event(title=title, date=datetime.strptime(date, '%Y-%m-%d'), description=description)
        db.session.add(event)
        db.session.commit()
        flash('Мероприятие добавлено!', 'success')

    return redirect(url_for('events'))

@app.route('/review/<int:pub_id>', methods=['POST'])
def add_review(pub_id):
    reviewer_name = request.form.get('reviewer_name')
    comment = request.form.get('comment')

    if reviewer_name and comment:
        review = Review(publication_id=pub_id, reviewer_name=reviewer_name, comment=comment)
        db.session.add(review)
        db.session.commit()
        flash('Рецензия добавлена!', 'success')

    return redirect(url_for('publications'))

@app.route('/upload_document', methods=['POST'])
def upload_document():
    title = request.form.get('title')
    file = request.files['file']

    if file and title:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads/documents', filename))
        doc = Document(title=title, file_path=filename)
        db.session.add(doc)
        db.session.commit()
        flash('Документ загружен!', 'success')

    return redirect(url_for('documents'))

@app.route('/documents')
def documents():
    docs = Document.query.all()
    return render_template('documents.html', docs=docs)

@app.route('/surgeons')
def surgeons():
    tag = request.args.get('tag')
    query = Publication.query
    if tag:
        query = query.filter(Publication.tags.like(f"%{tag}%"))
    publications = query.all()
    events = Event.query.order_by(Event.date).all()
    return render_template('surgeons.html', events=events, publications=publications)

@app.route('/patients/specialists')
def certified_specialists():
    query = request.args.get('query', '')
    selected_specialty = request.args.get('specialty', '')
    selected_region = request.args.get('region', '')

    specialists_query = CertifiedSpecialist.query

    if query:
        specialists_query = specialists_query.filter(
            CertifiedSpecialist.name.ilike(f'%{query}%') |
            CertifiedSpecialist.specialty.ilike(f'%{query}%')
        )

    if selected_specialty:
        specialists_query = specialists_query.filter(CertifiedSpecialist.specialty == selected_specialty)

    if selected_region:
        specialists_query = specialists_query.filter(CertifiedSpecialist.region == selected_region)

    specialists = specialists_query.all()

    # Получаем уникальные значения из базы
    all_specialties = [s[0] for s in CertifiedSpecialist.query.with_entities(CertifiedSpecialist.specialty).distinct().all() if s[0]]
    all_regions = [r[0] for r in CertifiedSpecialist.query.with_entities(CertifiedSpecialist.region).distinct().all() if r[0]]

    return render_template(
        'patients/specialists.html',
        specialists=specialists,
        all_specialties=all_specialties,
        all_regions=all_regions,
        selected_specialty=selected_specialty,
        selected_region=selected_region,
        query=query
    )



@app.route('/patients/ethics')
def ethics_committee():
    decisions = EthicsDecision.query.order_by(EthicsDecision.decision_date.desc()).all()
    return render_template('patients/ethics.html', decisions=decisions)

@app.route('/patients/articles')
def patient_articles():
    articles = Article.query.all()
    return render_template('patients/articles.html', articles=articles)

@app.route('/patients/implants')
def implants():
    implants = Implant.query.all()
    return render_template('patients/implants.html', implants=implants)

#flask-login

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Пользователь уже существует', 'danger')
        else:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Вы вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


# Контекстный процессор — добавляет переменные во все шаблоны
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return dict(current_user=user)

from flask import jsonify
from models import ContactMessage  # добавим модель

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            msg = ContactMessage(name=name, email=email, message=message)
            db.session.add(msg)
            db.session.commit()
            flash('Сообщение отправлено! Мы свяжемся с вами.', 'success')
            return redirect(url_for('contacts'))
        else:
            flash('Пожалуйста, заполните все поля', 'danger')

    return render_template('contacts.html')
