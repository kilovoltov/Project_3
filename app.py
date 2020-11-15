import json
import os

from flask import Flask, render_template, abort, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
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


@app.route('/')
def render_main():
    return render_template('index.html')


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
    return render_template('booking.html',
                           teacher=teacher[0],
                           days=days,
                           day=day,
                           time=time)


@app.route('/booking_done/', methods=['GET', 'POST'])
def render_booking_done():
    with open('days.json', 'r') as f:
        days = json.load(f)

    client_name = request.form.get('clientName')
    client_phone = request.form.get('clientPhone')
    client_teacher = request.form.get('clientTeacher')
    client_time = request.form.get('clientTime')
    client_weekday = request.form.get('clientWeekday')

    return render_template('booking_done.html',
                           name=client_name,
                           phone=client_phone,
                           days=days,
                           day=client_weekday,
                           time=client_time,
                           teacher=client_teacher)


@app.route('/request/')
def render_requiest():
    form = RequestForm()
    with open('goals.json', 'r') as f:
        goals = json.load(f)
    return render_template('request.html',
                           form=form,
                           goals=goals)


@app.route('/request_done/', methods=['GET', 'POST'])
def render_requiest_done():
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
