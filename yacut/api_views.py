from flask import jsonify, request, url_for

from . import app, db
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Отсутствует тело запроса"}), 400

    url = data.get('url')
    custom_id = data.get('custom_id')

    if custom_id is None:
        custom_id = ''

    if len(custom_id) > 16:
        return jsonify({"message": "Указано недопустимое имя для короткой ссылки"}), 400

    if not url:
        return jsonify({"message": '"url" является обязательным полем!'}), 400

    if custom_id:
        if not URLMap.is_valid_custom_link(custom_id):
            return jsonify({"message": "Указано недопустимое имя для короткой ссылки"}), 400
        elif URLMap.query.filter_by(short=custom_id).first():
            return jsonify({"message": "Предложенный вариант короткой ссылки уже существует."}), 400
    else:
        custom_id = URLMap.get_unique_short_id(url)

    new_url_map = URLMap(original=url, short=custom_id)
    db.session.add(new_url_map)
    db.session.commit()
    full_short_link = url_for('short_link_url', short=custom_id, _external=True)
    return jsonify({"url": url, "short_link": full_short_link}), 201


@app.route('/api/id/<short_id>/', methods=['GET', ])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({"message": "Указанный id не найден"}), 404
    return jsonify({"url": url_map.original}), 200
