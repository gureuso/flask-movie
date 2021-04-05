# -*- coding: utf-8 -*-
from flask import Blueprint, request

from apps.common.auth import signin_required
from apps.common.response import ok, error
from apps.database.models import TheaterTicket, Showtime
from apps.database.session import db

app = Blueprint('theater_tickets', __name__, url_prefix='/theater_tickets')


@app.route('', methods=['POST'])
@signin_required
def create():
    form = request.form
    theater_id = form['theater_id']
    showtime_id = form['showtime_id']
    seat_list = form['seat_list'].split(',')

    showtime = Showtime.query.filter_by(id=showtime_id, theater_id=theater_id).first()
    if not showtime:
        return error(40400)

    for seat in seat_list:
        x, y = seat.split('-')
        if TheaterTicket.query.filter(TheaterTicket.theater_id == theater_id, TheaterTicket.showtime_id == showtime_id,
                                      TheaterTicket.x == x, TheaterTicket.y == y).first():
            return error(40000)
    for seat in seat_list:
        x, y = seat.split('-')
        theater_ticket = TheaterTicket(theater_id=theater_id, showtime_id=showtime_id, x=x, y=y)
        db.session.add(theater_ticket)
    db.session.commit()
    return ok()
