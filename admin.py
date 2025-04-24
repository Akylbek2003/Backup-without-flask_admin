from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import MembershipApplication, EventAccreditation
from models import CertifiedSpecialist, EthicsDecision, Article, Publication, Implant, Document, SliderItem, NewsItem

from flask_admin.form import ImageUploadField
import os

import publication 
from publication import PublicationAdmin


admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

# Путь к папке загрузки
file_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'slider')

# Убедись, что папка существует
os.makedirs(file_path, exist_ok=True)

# Модель для заявок на вступление
class MembershipApplicationView(ModelView):
    column_list = ('id', 'name', 'email', 'approved')
    form_columns = ('name', 'email', 'approved')

# Модель для заявок на аккредитацию
class EventAccreditationView(ModelView):
    column_list = ('id', 'event_name', 'event_date', 'approved')
    form_columns = ('event_name', 'event_date', 'approved')


from flask_admin.form import ImageUploadField
from wtforms_sqlalchemy.fields import QuerySelectField


class SliderAdmin(ModelView):
    form_columns = ['title', 'description', 'file_path', 'news']

    form_extra_fields = {
        'file_path': ImageUploadField(
            label='Фотография',
            base_path=file_path,
            allow_overwrite=False
        ),
        'news': QuerySelectField(
            label='Новость',
            query_factory=lambda: NewsItem.query.all(),
            get_label='title',
            allow_blank=True
        )
    }




class NewsItemAdmin(ModelView):
    form_columns = ['title', 'slug', 'content', 'file_path']




# Добавляем модели в админку
admin.add_view(MembershipApplicationView(MembershipApplication, db.session))
admin.add_view(EventAccreditationView(EventAccreditation, db.session))
admin.add_view(ModelView(CertifiedSpecialist, db.session))
admin.add_view(ModelView(EthicsDecision, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Implant, db.session))
admin.add_view(PublicationAdmin(Publication, db.session))
admin.add_view(ModelView(Document, db.session))
admin.add_view(SliderAdmin(SliderItem, db.session))
admin.add_view(NewsItemAdmin(NewsItem, db.session))

