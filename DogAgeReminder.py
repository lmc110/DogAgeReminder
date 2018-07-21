import flask
from datetime import datetime, date
from dateutil import relativedelta
import math
import flask_sqlalchemy

app = flask.Flask(__name__)
app.config.from_pyfile('settings.py')
db = flask_sqlalchemy.SQLAlchemy(app)




@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    form_date = flask.request.form['pet-age']
    pet_age = form_date.replace('-', ' ')
    date_of_birth = datetime.strptime(pet_age, "%Y %m %d")
    total_age = calculate_total(date_of_birth)
    total_days = calculate_days(date_of_birth)
    total_weeks = calculate_weeks(date_of_birth)
    return flask.render_template('age.html', total_age=total_age, total_days=total_days, total_weeks=total_weeks)


def calculate_total(born):
    today = date.today()
    r = relativedelta.relativedelta(today, born)
    #print("Total age: " + str(r.years) + " years " + str(r.months) + " months " + str(r.days) + " days")
    return r


def calculate_days(born):
    # Calculate total number of days born
    days = date.today()-date(born.year, born.month, born.day)
    #print("Days: " + str(days.days))
    return days


def calculate_weeks(born):
    # Calculate total number of weeks
    days = date.today() - date(born.year, born.month, born.day)
    weeks = math.floor(days.days / 7)
    #print("Weeks: " + str(weeks))
    return weeks


if __name__ == '__main__':
    app.run()
