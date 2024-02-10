from flask import flash, redirect, render_template, url_for

from yacut import db

from . import app
from .constans import REDIRECT_FUNC
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    original_link = form.original_link.data

    try:
        custom_id = URLMap.save(original_link, custom_id).short
        return render_template('index.html',
                               form=form,
                                context={
                                'short': url_for(
                                    REDIRECT_FUNC,
                                    short=custom_id,
                                    _external=True
                                )})
    except Exception as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET', ])
def short_link_url(short):
    return redirect(URLMap.get_original_link(short))
