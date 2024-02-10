from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .constans import (CREATE, DATA_REQUIRED, LONG_URL, MAX_LENGTH_LONG,
                       MAX_LENGTH_SHORT, SHORT_EXIST, SHORT_URL)
from .models import URLMap


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
        validators=[Length(max=MAX_LENGTH_SHORT), Optional()]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, short):
        if URLMap.get_link(short.data):
            raise ValidationError(SHORT_EXIST)
