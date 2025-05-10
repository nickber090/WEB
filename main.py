from flask import Flask, render_template


app = Flask(__name__)


cars_data = [
    {
        "title": "Toyota Camry 2021",
        "price": "2 450 000 ₽",
        "image": "https://via.placeholder.com/350x220?text=Toyota+Camry",
        "mileage": "45 000 км",
        "fuel": "Бензин",
        "transmission": "Автомат",
        "body": "Седан",
        "location": "Москва",
        "seller": {
            "name": "Автосалон 'Премиум'",
            "avatar": "https://via.placeholder.com/40x40?text=AV",
            "rating": 4.5,
            "reviews": 24
        },
        "badge": "Топ"
    },
    {
        "title": "Mercedes-Benz E-Class 2019",
        "price": "3 800 000 ₽",
        "image": "https://via.placeholder.com/350x220?text=Mercedes+E-Class",
        "mileage": "60 000 км",
        "fuel": "Дизель",
        "transmission": "Автомат",
        "body": "Седан",
        "location": "Санкт-Петербург",
        "seller": {
            "name": "Мерседес Центр",
            "avatar": "https://via.placeholder.com/40x40?text=MB",
            "rating": 4.8,
            "reviews": 42
        },
        "badge": "Премиум"
    },
    {
        "title": "BMW X5 2020",
        "price": "4 200 000 ₽",
        "image": "https://via.placeholder.com/350x220?text=BMW+X5",
        "mileage": "35 000 км",
        "fuel": "Бензин",
        "transmission": "Автомат",
        "body": "Внедорожник",
        "location": "Казань",
        "seller": {
            "name": "Автоцентр 'БМВ'",
            "avatar": "https://via.placeholder.com/40x40?text=BMW",
            "rating": 4.7,
            "reviews": 36
        },
        "badge": "Новинка"
    }
]

@app.route('/')
@app.route('/index.html')
def main_window():
    return render_template('index.html', title='Главная страница', cars=cars_data)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
