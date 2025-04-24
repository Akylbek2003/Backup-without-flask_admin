from flask import session, render_template, request, redirect, url_for, send_from_directory, flash
from app import app, db
from models import Member, Document, Publication, Event, Review  # Импортируем модели
from datetime import datetime  # уже импортирован, если нет — добавь
from models import MembershipApplication, EventAccreditation, CertifiedSpecialist, Implant, Article, EthicsDecision, User, SliderItem, NewsItem
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
# Путь для сохранения аватарок
AVATAR_FOLDER = os.path.join('static', 'uploads', 'avatars')
app.config['AVATAR_FOLDER'] = AVATAR_FOLDER
os.makedirs(AVATAR_FOLDER, exist_ok=True)


@app.route('/')
def index():
    slider_items = SliderItem.query.all()
    return render_template('index.html', slider_items=slider_items)

    
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

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Почта уже используется', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
            
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')    
            
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
           
        else:
            new_user = User(email=email, first_name=first_name, password_hash=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash('Регистрация прошла успешно', category='success')
            return redirect(url_for('index'))

    return render_template("sign_up.html", user=current_user)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if user.check_password(password):
                flash('Login in successfully!', category='success') 
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                flash('Неправильный пароль, попробуйте еще раз', category='error')
    
        print(f"Пробуем войти с email={email} и password={password}")
        if user:
            print(f"Пользователь найден: {user.email}")
            if user.check_password(password):
                print("Пароль верный, логиним пользователя")
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                print("Неверный пароль")

    return render_template("login.html", user=current_user)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


# Контекстный процессор — добавляет переменные во все шаблоны
@app.context_processor
def inject_user():
    return dict(current_user=current_user)


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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        avatar_file = request.files.get('avatar')
        if avatar_file:
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(app.config['AVATAR_FOLDER'], filename)
            avatar_file.save(avatar_path)

            current_user.avatar = filename
            db.session.commit()
            flash("Аватар обновлён!", "success")
            return redirect(url_for('profile'))

    return render_template('profile.html', user=current_user)

@app.route('/upload_signed_form', methods=['POST'])
def upload_signed_form():
    file = request.files.get('signed_form')
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join('uploads', 'signed_forms', filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        flash('Файл успешно загружен!', 'success')
    else:
        flash('Файл не был выбран', 'danger')
    return redirect(url_for('about'))

@app.route('/news/<slug>')
def news_detail(slug):
    news = NewsItem.query.filter_by(slug=slug).first_or_404()
    return render_template('news_detail.html', news=news)
    