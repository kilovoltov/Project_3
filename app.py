import json
import os
from random import shuffle

from flask import Flask, render_template, abort
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, HiddenField
from wtforms.validators import InputRequired
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)

SECRET_KEY = os.urandom(43)
app.config['SECRET_KEY'] = SECRET_KEY


class RequestForm(FlaskForm):
    with open('goals.json', 'r') as f:
        goals = json.load(f)
    name = StringField('Вас зовут', validators=[InputRequired(message='Нужно ввести свое имя')])
    phone = StringField('Ваш телефон', validators=[InputRequired(message='Введите номер телефона')])
    goal = RadioField('Какая цель занятий?', choices=[(key, value) for key, value in goals.items()])
    time = RadioField('Сколько времени есть?', choices=[("1-2 часа в неделю", "1-2 часа в неделю"),
                                                        ("3-5 часов в неделю", "3-5 часов в неделю"),
                                                        ("5-7 часов в неделю", "5-7 часов в неделю"),
                                                        ("7-10 часов в неделю", "7-10 часов в неделю")])
    submit = SubmitField('Найдите мне преподавателя')


class BookingForm(FlaskForm):
    with open('teachers.json') as f:
        teachers = json.load(f)
    client_name = StringField('Вас зовут', validators=[InputRequired(message='Нужно ввести свое имя')])
    client_phone = StringField('Ваш телефон', validators=[InputRequired(message='Введите номер телефона')])
    client_teacher = HiddenField('clientTeacher')
    client_time = HiddenField('clientTime')
    client_weekday = HiddenField('clientWeekday')
    submit = SubmitField('Записаться')


@app.route('/')
def render_main():
    with open('teachers.json') as f:
        teachers = json.load(f)
        shuffle(teachers)

    with open('goals.json', 'r') as f:
        goals = json.load(f)

    return render_template('index.html',
                           teachers=teachers[:6],
                           goals=goals)


@app.route('/goals/<goal>/')
def render_goal(goal):
    with open('teachers.json') as f:
        teachers = [item for item in json.load(f) if goal in item.get('goals')]
    return render_template('goal.html',
                           teachers=teachers)


@app.route('/profiles/all/')
def render_all_teachers():
    with open('teachers.json') as f:
        teachers = json.load(f)
        for teacher in teachers:
            del teacher['free']

    with open('goals.json', 'r') as f:
        goals = json.load(f)

    return render_template('all.html',
                           teachers=teachers,
                           goals=goals)


@app.route('/profiles/<int:id>/')
def render_profile(id):
    with open('teachers.json', 'r') as f:
        teacher = [item for item in json.load(f) if item.get('id') == id]
    if not teacher:
        abort(404)

    with open('goals.json', 'r') as f:
        goals = json.load(f)

    with open('days.json', 'r') as f:
        days = json.load(f)

    return render_template('profile.html',
                           teacher=teacher[0],
                           goals=goals,
                           days=days)


@app.route('/booking/<int:id>/<day>/<int:time>/')
def render_booking(id, day, time):
    with open('teachers.json', 'r') as f:
        teacher = [item for item in json.load(f) if item.get('id') == id]
    if not teacher:
        abort(404)
    with open('days.json', 'r') as f:
        days = json.load(f)
    form = BookingForm(client_time=str(time) + ':00', client_weekday=day, client_teacher=id)
    return render_template('booking.html',
                           teacher=teacher[0],
                           days=days,
                           day=day,
                           time=time,
                           form=form)


@app.route('/booking_done/', methods=['GET', 'POST'])
def render_booking_done():
    with open('days.json', 'r') as f:
        days = json.load(f)
    form = BookingForm()
    client_name = form.client_name.data
    client_phone = form.client_phone.data
    client_teacher = form.client_teacher.data
    client_time = form.client_time.data
    client_weekday = form.client_weekday.data

    return render_template('booking_done.html',
                           name=client_name,
                           phone=client_phone,
                           days=days,
                           day=client_weekday,
                           time=client_time,
                           teacher=client_teacher)


@app.route('/request/')
def render_request():
    form = RequestForm()
    with open('goals.json', 'r') as f:
        goals = json.load(f)
    return render_template('request.html',
                           form=form,
                           goals=goals)


@app.route('/request_done/', methods=['GET', 'POST'])
def render_request_done():
    with open('goals.json', 'r') as f:
        goals = json.load(f)
    form = RequestForm()
    name = form.name.data
    phone = form.phone.data
    goal = form.goal.data
    time = form.time.data
    return render_template('request_done.html',
                           name=name,
                           phone=phone,
                           goals=goals,
                           goal=goal,
                           time=time)


if __name__ == '__main__':
    app.run()
