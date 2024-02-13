import random
import re
from datetime import datetime

from wtforms.validators import ValidationError

from . import db
from .constans import (CHARS, LENGTH_SHORT, MAX_LENGTH_LONG, MAX_LENGTH_SHORT,
                       RE_PATTERN, SHORT_EXIST, UNCORRECT)
from .error_handlers import GenerationException


MAX_TRIES = 10
GENERATION_MESSAGE = 'Ошибка генерации короткой ссылки.'
ORIGINAL_MESSAGE = 'Исходная ссылка слишком длинная.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_LONG), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_original_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_TRIES):
            short = ''.join(
                random.choices(CHARS, k=LENGTH_SHORT)
            )
            if not URLMap.get(short):
                return short
        raise GenerationException(GENERATION_MESSAGE)

    @staticmethod
    def validate_short(short):
        if len(short) > MAX_LENGTH_SHORT:
            raise ValidationError(UNCORRECT)
        if not re.match(RE_PATTERN, short):
            raise ValidationError(UNCORRECT)
        if URLMap.get(short):
            raise ValidationError(SHORT_EXIST)
        return short

    @staticmethod
    def add_to_db(original_link, short=None, validate=False):
        if validate:
            if short:
                URLMap.validate_short(short)
            elif len(original_link) > MAX_LENGTH_LONG:
                raise ValidationError(ORIGINAL_MESSAGE)
        if not short:
            short = URLMap.get_unique_short_id()
        url_map = URLMap(
            original=original_link,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
