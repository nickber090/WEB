from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def main_window():
    return render_template('index.html', title='Главная страница')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
