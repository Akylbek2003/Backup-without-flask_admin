from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import MembershipApplication, EventAccreditation
from models import CertifiedSpecialist, EthicsDecision, Article, Publication, Implant, Document

import publication 
from publication import PublicationAdmin
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

# Модель для заявок на вступление
class MembershipApplicationView(ModelView):
    column_list = ('id', 'name', 'email', 'approved')
    form_columns = ('name', 'email', 'approved')

# Модель для заявок на аккредитацию
class EventAccreditationView(ModelView):
    column_list = ('id', 'event_name', 'event_date', 'approved')
    form_columns = ('event_name', 'event_date', 'approved')

# Добавляем модели в админку
admin.add_view(MembershipApplicationView(MembershipApplication, db.session))
admin.add_view(EventAccreditationView(EventAccreditation, db.session))
admin.add_view(ModelView(CertifiedSpecialist, db.session))
admin.add_view(ModelView(EthicsDecision, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Implant, db.session))
admin.add_view(PublicationAdmin(Publication, db.session))
admin.add_view(ModelView(Document, db.session))
