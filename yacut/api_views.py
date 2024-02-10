from flask import jsonify, request, url_for
from http import HTTPStatus

from . import app, db
from .models import URLMap
from .error_handlers import BadRequest
from wtforms.validators import ValidationError


NO_BODY = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
NOT_FOUD = "Указанный id не найден"


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise BadRequest(NO_BODY, HTTPStatus.BAD_REQUEST)
    url = data.get('url')
    custom_id = data.get('custom_id')
    if not url:
        raise BadRequest(NO_URL, HTTPStatus.BAD_REQUEST)
    
    try:
        custom_id = URLMap.save(original_link=url, short=custom_id).short
        return jsonify(
            {
                'url': url,
                'short_link': url_for(
                    'short_link_url',
                    short=custom_id,
                    _external=True
                )
            }
        ), HTTPStatus.CREATED
    except ValidationError as error:
        raise BadRequest(str(error))

    # if custom_id is None:
    #     custom_id = ''

    # if len(custom_id) > 16:
    #     return jsonify({"message": "Указано недопустимое имя для короткой ссылки"}), 400

    # if custom_id:
    #     if not URLMap.is_valid_custom_link(custom_id):
    #         return jsonify({"message": "Указано недопустимое имя для короткой ссылки"}), 400
    #     elif URLMap.query.filter_by(short=custom_id).first():
    #         return jsonify({"message": "Предложенный вариант короткой ссылки уже существует."}), 400
    # else:
    #     custom_id = URLMap.get_unique_short_id()

    # new_url_map = URLMap(original=url, short=custom_id)
    # db.session.add(new_url_map)
    # db.session.commit()
    # full_short_link = url_for('short_link_url', short=custom_id, _external=True)
    # return jsonify({"url": url, "short_link": full_short_link}), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET', ])
def get_url(short_id):
    url_map = URLMap.get_link(short_id)
    if not url_map:
        raise BadRequest(NOT_FOUD, HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
