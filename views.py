from __future__ import print_function

import os

from flask import Flask, render_template, request

import do_analysis

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    artist = request.form['artist']
    song = request.form['song']
    root = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.join(root, 'static')
    comp = do_analysis.do_comparison(static_path, artist, song).split(",")
    diff = str(float(comp[1]) * 100)
    return render_template('result.html', artist=artist, song=song, diff=diff, result=comp[0])


if __name__ == '__main__':
    app.run()
