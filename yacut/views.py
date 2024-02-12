from flask import flash, redirect, render_template, url_for
from wtforms.validators import ValidationError

from . import app
from .constans import REDIRECT_FUNC
from .forms import URLForm
from .models import URLMap
from .error_handlers import GenerationException


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        short = URLMap.add_to_db(
            form.original_link.data,
            form.custom_id.data,
        ).short
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                REDIRECT_FUNC,
                short=short,
                _external=True
            )
        )
    except (ValidationError, GenerationException) as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET', ])
def short_link_url(short):
    return redirect(URLMap.get_original_or_404(short))
