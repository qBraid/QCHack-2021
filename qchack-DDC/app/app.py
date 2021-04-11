import datetime
import os

import matplotlib.pyplot as plt
from flask import Flask, render_template, request

import adder as ad

app = Flask(__name__)


def remove_old_figs():
    path = './static/assets/UPLOAD_FOLDER/'
    files = os.listdir(path)
    for file in files:
        os.remove(path + file)
    return True


def parser(expression):
    expression = expression.replace(" ", "")
    operator = '+'
    pos = expression.find('+')
    num_1 = expression[:pos]
    operator = expression[pos]
    num_2 = expression[pos + 1:]
    return (num_1, num_2), operator


def result_processing(result):
    plt.hist(result)
    name = "prob_{}.jpg".format(
        datetime.datetime.utcnow().isoformat()[:-7].replace(":", '-'))
    plt.savefig("./static/assets/UPLOAD_FOLDER/{}".format(name))
    return name


@app.route('/', methods=['GET', 'POST'])
def home():
    params = request.form
    expression = params['ex']
    ex = parser(expression)

    qc = ad.adder(int(ex[0][0]), int(ex[0][1]))
    remove_old_figs()
    circuit = "circuit_{}.jpg".format(
        datetime.datetime.utcnow().isoformat()[:-7].replace(":", '-'))
    c_url = './static/assets/UPLOAD_FOLDER/{}'.format(circuit)
    qc.draw(output='mpl', filename=c_url)
    result = ad.simulate(qc)
    prob_url = result_processing(result)
    return render_template('index.html',
                           expression=expression,
                           results=result,
                           c_url=c_url,
                           prob_url=prob_url)


app.run(debug=True)
