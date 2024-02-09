from flask import flash, redirect, render_template, url_for

from yacut import db
from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        original_link = form.original_link.data
        if not custom_id:
            custom_id = URLMap.get_unique_short_id(original_link)

        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.', 'short')
            return render_template('index.html', form=form)

        if not URLMap.is_valid_custom_link(custom_id):
            flash('Введены недопустимые символы.', 'short')
            return render_template('index.html', form=form)

        url = URLMap(
            original=original_link,
            short=custom_id,
        )
        db.session.add(url)
        db.session.commit()
        flash(url_for('short_link_url', short=custom_id, _external=True), 'link')
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET', ])
def short_link_url(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
