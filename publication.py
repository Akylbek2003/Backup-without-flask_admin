import os
import uuid
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from markupsafe import Markup
from flask import url_for
from wtforms import fields

file_upload_path = os.path.join(os.path.dirname(__file__), 'static/uploads/publications')

class PublicationAdmin(ModelView):
    form_extra_fields = {
        'file_path': FileUploadField(
            'Файл публикации',
            base_path=file_upload_path,
            allow_overwrite=False,
            namegen=lambda obj, file_data: f"{uuid.uuid4().hex}_{file_data.filename}"
        )
    }

    # Показывать кнопку "Скачать" в списке
    column_formatters = {
        'file_path': lambda v, c, m, p: Markup(
            f'<a href="{url_for("static", filename="uploads/publications/" + m.file_path)}" download>📥 Скачать</a>'
        )
    }
