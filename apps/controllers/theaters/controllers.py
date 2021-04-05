# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

from apps.common.auth import signin_required
from apps.database.models import Showtime, Theater, TheaterTicket

app = Blueprint('theaters', __name__, url_prefix='/theaters')


@app.route('/<int:theater_id>/showtimes/<int:showtime_id>', methods=['GET'])
@signin_required
def detail(theater_id, showtime_id):
    showtime = Showtime.query.filter_by(id=showtime_id, theater_id=theater_id).first()
    if showtime.start_time < datetime.now():
        return redirect(url_for('showtimes.index'))
    if showtime.movie.age_rating > current_user.age:
        return redirect(url_for('showtimes.index'))

    theater = Theater.query.filter_by(id=theater_id).first()
    theater_tickets = TheaterTicket.query.filter_by(theater_id=theater_id, showtime_id=showtime_id).all()
    return render_template('theaters/detail.html', theater=theater, theater_tickets=theater_tickets, showtime=showtime)
