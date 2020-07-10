from flask import Flask, render_template
import random
import csv
from datetime import datetime

"%b %d %Y"

def getFirstDate(a,b):
    if datetime.strptime(a, '%Y-%m-%d %H:%M') > datetime.strptime(b,'%Y-%m-%d %H:%M'):
        return b
    else:
        return a

def getLastDate(a,b):
    if datetime.strptime(a, '%Y-%m-%d %H:%M') > datetime.strptime(b,'%Y-%m-%d %H:%M'):
        return a
    else:
        return b

class code_violation:
    def __init__(self, category, first_date, last_date):
        self.category = category
        self.first_date = first_date
        self.last_date = last_date
        self.count = 1


def csv_processor():
    with open('C4C-dev-challenge-2018.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        list_of_unique_violations = []
        for i, row in enumerate(reader):
            if i == 0:
                continue
            else:
                found_flag = False
                for violation in list_of_unique_violations:
                    if row[2] == violation.category:
                        found_flag = True
                        violation.count += 1
                        violation.first_date = getFirstDate(row[3], violation.first_date)
                        violation.last_date = getLastDate(row[3], violation.last_date)
                        break
                if found_flag is False:
                    new_violation = code_violation(row[2], row[3], row[3])
                    list_of_unique_violations.append(new_violation)

    return list_of_unique_violations

app = Flask(__name__)


@app.route('/')
def hello_world():
    labels, values, data = [[], [], []]
    colour = []
    r = lambda: random.randint(0, 255)
    for violation in csv_processor():
        labels.append(violation.category)
        values.append(violation.count)
        data.append([violation.category, violation.first_date, violation.last_date, violation.count])
        colour.append('#%02X%02X%02X' % (r(), r(), r()))
    return render_template('hello_world.html', set=zip(values, labels, colour),tableList=data)

