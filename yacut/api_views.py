from http import HTTPStatus

from flask import jsonify, request, url_for
from wtforms.validators import ValidationError

from . import app
from .error_handlers import BadRequest
from .models import URLMap

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


@app.route('/api/id/<short_id>/', methods=['GET', ])
def get_url(short_id):
    url_map = URLMap.get_link(short_id)
    if not url_map:
        raise BadRequest(NOT_FOUD, HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
