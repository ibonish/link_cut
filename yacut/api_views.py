from http import HTTPStatus

from flask import jsonify, request, url_for
from wtforms.validators import ValidationError

from . import app
from .constans import REDIRECT_FUNC
from .error_handlers import InvalidApiUsage, GenerationException
from .models import URLMap


NO_BODY = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
NOT_FOUD = "Указанный id не найден"


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidApiUsage(NO_BODY, HTTPStatus.BAD_REQUEST)
    url = data.get('url')
    if not url:
        raise InvalidApiUsage(NO_URL, HTTPStatus.BAD_REQUEST)

    try:
        short = URLMap.add_to_db(
            original_link=url,
            short=data.get('custom_id'),
            validate=True
        ).short
        return jsonify(
            {
                'url': url,
                'short_link': url_for(
                    REDIRECT_FUNC,
                    short=short,
                    _external=True
                )
            }
        ), HTTPStatus.CREATED
    except (ValidationError, GenerationException) as error:
        raise InvalidApiUsage(str(error))


@app.route('/api/id/<short>/', methods=['GET', ])
def get_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidApiUsage(NOT_FOUD, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
