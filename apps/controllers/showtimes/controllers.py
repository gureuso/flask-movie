# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from datetime import datetime, timedelta

from sqlalchemy import and_

from apps.common.auth import signin_required
from apps.database.models import Showtime, Movie

app = Blueprint('showtimes', __name__, url_prefix='/showtimes')


@app.route('', methods=['GET'])
@signin_required
def index():
    week = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
    week_list = []
    now = datetime.now()
    now_weekday = now.weekday()

    args = request.args
    movie_id = args.get('movie_id')
    selected_date = args.get('date', now.strftime('%Y-%m-%d'))
    selected_cinema_id = args.get('cinema_id')

    for i in range(now_weekday, now_weekday + 7):
        day = i - now_weekday
        date = now + timedelta(days=day)
        i %= 7
        week_list.append({'weekday': week[i], 'date': date.strftime('%Y-%m-%d')})

    if selected_cinema_id:
        movies = Movie.query.join(Showtime, and_(Showtime.movie_id == Movie.id, Showtime.cinema_id == selected_cinema_id))
    else:
        movies = Movie.query.join(Showtime, Showtime.movie_id == Movie.id)
    if movie_id:
        movies = movies.filter_by(movie_id=movie_id)
    movies = movies.filter(Showtime.start_time >= now - timedelta(hours=9)).\
        filter(Showtime.end_time < now + timedelta(days=1) - timedelta(hours=9)).all()

    return render_template('showtimes/index.html', date=selected_date, cinema_id=selected_cinema_id, movie_id=movie_id,
                           movies=movies, week_list=week_list, now=datetime.now())
