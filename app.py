import json

from flask import Flask, render_template, abort, request

app = Flask(__name__)


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


@app.route('/booking_done/')
def render_booking_done():
    clientName = request.form.get('clientName')
    clientPhone = request.form.get('clientPhone')
    clientTeacher = request.form.get('clientTeacher')
    clientTime = request.form.get('clientTime')
    clientWeekday = request.form.get('clientWeekday')

    return render_template('booking_done.html',
                           teacher=teacher[0],
                           days=days,
                           day=day,
                           time=time)


if __name__ == '__main__':
    app.run()
