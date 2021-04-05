# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from apps.common.auth import signin_required
from apps.database.models import Cinema

app = Blueprint('cinemas', __name__, url_prefix='/cinemas')


@app.route('', methods=['GET'])
@signin_required
def index():
    data = request.args
    movie_id = data.get('movie_id')

    cinemas = Cinema.query.all()
    return render_template('cinemas/index.html', cinemas=cinemas, movie_id=movie_id)
