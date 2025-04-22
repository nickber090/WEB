from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main_window():
    return render_template('static/templates/index.html', title='job well done')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
