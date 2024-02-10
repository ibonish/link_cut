import re
from datetime import datetime
import random
import string

from wtforms.validators import ValidationError
from yacut import db
from .constans import MAX_LENGTH_SHORT, MAX_LENGTH_LONG, RE_PATTERN, SHORT_EXIST, UNCORRECT, MAX_LENGTH_SHORT, LENGTH_SHORT


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_LONG), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_link(short_link):
        return URLMap.query.filter_by(short=short_link).first()
    
    @staticmethod
    def get_original_link(short_link):
        return URLMap.query.filter_by(short=short_link).first_or_404().original

    @staticmethod
    def get_unique_short_id():
        chars = string.ascii_letters + string.digits
        while True:
            short_link = ''.join(random.choice(chars) for _ in range(LENGTH_SHORT))
            if not URLMap.get_link(short_link):
                return short_link

    @staticmethod
    def is_valid_custom_link(link):
        pattern = RE_PATTERN
        if re.match(pattern, link):
            return True
        return False

    @staticmethod
    def save(original_link, short=None):
        if short is not None and len(short) > MAX_LENGTH_SHORT:
            raise ValidationError(UNCORRECT) 
        if not short:
            short = URLMap.get_unique_short_id()
        if URLMap.get_link(short):
            raise ValidationError(SHORT_EXIST)
        if not URLMap.is_valid_custom_link(short):
            raise ValidationError(UNCORRECT)
        url = URLMap(
            original=original_link,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        return url
