from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .models import URLMap
from .constans import MAX_LENGTH_LONG, MAX_LENGTH_SHORT, LONG_URL, SHORT_URL, DATA_REQUIRED, CREATE, SHORT_EXIST


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
