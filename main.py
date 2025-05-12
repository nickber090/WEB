from flask import Flask, render_template, request


app = Flask(__name__)

# Пример данных об автомобилях
cars_data = [
    {
        "id": 1,
        "title": "Toyota Camry 2021",
        "price": 2450000,
        "image": "https://via.placeholder.com/350x220?text=Toyota+Camry",
        "mileage": 45000,
        "fuel": "Бензин",
        "transmission": "Автомат",
        "body": "Седан",
        "location": "Москва",
        "year": 2021,
        "seller": {
            "name": "Автосалон 'Премиум'",
            "avatar": "https://via.placeholder.com/40x40?text=AV",
            "rating": 4.5,
            "reviews": 24
        },
        "badge": "Топ"
    },
    {
        "id": 2,
        "title": "Mercedes-Benz E-Class 2019",
        "price": 3800000,
        "image": "https://via.placeholder.com/350x220?text=Mercedes+E-Class",
        "mileage": 60000,
        "fuel": "Дизель",
        "transmission": "Автомат",
        "body": "Седан",
        "location": "Санкт-Петербург",
        "year": 2019,
        "seller": {
            "name": "Мерседес Центр",
            "avatar": "https://via.placeholder.com/40x40?text=MB",
            "rating": 4.8,
            "reviews": 42
        },
        "badge": "Премиум"
    },
    {
        "id": 3,
        "title": "BMW X5 2020",
        "price": 4200000,
        "image": "https://via.placeholder.com/350x220?text=BMW+X5",
        "mileage": 35000,
        "fuel": "Бензин",
        "transmission": "Автомат",
        "body": "Внедорожник",
        "location": "Казань",
        "year": 2020,
        "seller": {
            "name": "Автоцентр 'БМВ'",
            "avatar": "https://via.placeholder.com/40x40?text=BMW",
            "rating": 4.7,
            "reviews": 36
        },
        "badge": "Новинка"
    },
    {
        "id": 4,
        "title": "Kia Rio 2022",
        "price": 1500000,
        "image": "https://via.placeholder.com/350x220?text=Kia+Rio",
        "mileage": 10000,
        "fuel": "Бензин",
        "transmission": "Механика",
        "body": "Седан",
        "location": "Москва",
        "year": 2022,
        "seller": {
            "name": "Киа Авто",
            "avatar": "https://via.placeholder.com/40x40?text=KIA",
            "rating": 4.3,
            "reviews": 18
        },
        "badge": "Выгодно"
    }
]


@app.route('/')
@app.route('/index.html')
def main_window():
    # Получаем параметры фильтрации из URL
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    fuel_type = request.args.get('fuel_type')
    transmission = request.args.get('transmission')
    location = request.args.get('location')
    search_query = request.args.get('search', '').lower()

    # Фильтрация автомобилей
    filtered_cars = cars_data

    if search_query:
        filtered_cars = [car for car in filtered_cars if search_query in car['title'].lower()]

    if min_price is not None:
        filtered_cars = [car for car in filtered_cars if car['price'] >= min_price]

    if max_price is not None:
        filtered_cars = [car for car in filtered_cars if car['price'] <= max_price]

    if fuel_type:
        filtered_cars = [car for car in filtered_cars if car['fuel'] == fuel_type]

    if transmission:
        filtered_cars = [car for car in filtered_cars if car['transmission'] == transmission]

    if location:
        filtered_cars = [car for car in filtered_cars if car['location'] == location]

    # Получаем уникальные значения для фильтров
    fuel_types = sorted(list(set(car['fuel'] for car in cars_data)))
    transmissions = sorted(list(set(car['transmission'] for car in cars_data)))
    locations = sorted(list(set(car['location'] for car in cars_data)))

    return render_template(
        'index.html',
        title='Главная страница',
        cars=filtered_cars,
        fuel_types=fuel_types,
        transmissions=transmissions,
        locations=locations,
        search_query=search_query,
        min_price=min_price,
        max_price=max_price,
        selected_fuel=fuel_type,
        selected_transmission=transmission,
        selected_location=location
    )


if __name__ == 'main':
    app.run(port=8080, host='127.0.0.1')

