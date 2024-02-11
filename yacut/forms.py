from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .constans import (MAX_LENGTH_LONG, MAX_LENGTH_SHORT, RE_PATTERN,
                       SHORT_EXIST, UNCORRECT)
from .models import URLMap


LONG_URL = 'Длинная ссылка'
SHORT_URL = 'Ваш вариант короткой ссылки'
DATA_REQUIRED = 'Обязательное поле'
CREATE = 'Создать'


class URLForm(FlaskForm):
    original_link = StringField(
        LONG_URL,
        validators=[
            DataRequired(message=DATA_REQUIRED),
            Length(max=MAX_LENGTH_LONG)
        ]
    )

    custom_id = StringField(
        SHORT_URL,
        validators=[
            Length(max=MAX_LENGTH_SHORT),
            Optional(),
            Regexp(RE_PATTERN, message=UNCORRECT)
        ]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, short):
        if URLMap.get(short.data):
            raise ValidationError(SHORT_EXIST)
