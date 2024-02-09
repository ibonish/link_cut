import hashlib
import re
from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id(original_url, attempt=1):
        hash_object = hashlib.md5(original_url.encode())
        hex_dig = hash_object.hexdigest()
        short_link = hex_dig[:6] if attempt == 1 else hex_dig[:5] + str(attempt)

        found_object = URLMap.query.filter_by(short=short_link).first()
        if found_object is not None:
            return URLMap.get_unique_short_id(original_url, attempt + 1)
        return short_link

    @staticmethod
    def is_valid_custom_link(link):
        pattern = r'^[A-Za-z0-9]+$'
        if re.match(pattern, link):
            return True
        return False
