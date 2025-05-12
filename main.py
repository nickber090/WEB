from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm, LoginForm
from data import db_session
from data.users import User


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'your-secret-key-123'

# Пример данных об автомобилях
cars_data = [
    {
        "id": 1,
        "title": "Toyota Camry 2021",
        "price": 2450000,
        "image": "https://avatars.mds.yandex.net/i?id=26a23f81104db5a538953a0c13221b06_l-5221578-images-thumbs&n=13",
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
        "image": "https://avatars.mds.yandex.net/get-autoru-vos/2101859/db43267780a9aa4a9466f96935893f99/1200x900",
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
        "image": "https://avatars.mds.yandex.net/get-autoru-vos/2177499/f2948c098a1b4104c8de17708b93ef44/1200x900",
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
        "image": "https://avatars.mds.yandex.net/i?id=9e1a4ea1b377dfaf6e2f69a0ae573def4b67fc57baac3403-5887733-images-thumbs&n=13",
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

@app.route('/add_to_favorites/<int:car_id>')
def add_to_favorites(car_id):
    if 'favorites' not in session:
        session['favorites'] = []

    if car_id not in session['favorites']:
        session['favorites'].append(car_id)
        session.modified = True

    return redirect(request.referrer or url_for('main_window'))


@app.route('/remove_from_favorites/<int:car_id>')
def remove_from_favorites(car_id):
    if 'favorites' in session and car_id in session['favorites']:
        session['favorites'].remove(car_id)
        session.modified = True

    return redirect(request.referrer or url_for('main_window'))


@app.route('/favorites')
def favorites():
    if 'favorites' not in session:
        session['favorites'] = []

    favorite_cars = [car for car in cars_data if car['id'] in session.get('favorites', [])]

    fuel_types = sorted(list(set(car['fuel'] for car in cars_data)))
    transmissions = sorted(list(set(car['transmission'] for car in cars_data)))
    locations = sorted(list(set(car['location'] for car in cars_data)))

    return render_template(
        'index.html',
        title='Избранное',
        cars=favorite_cars,
        fuel_types=fuel_types,
        transmissions=transmissions,
        locations=locations,
        is_favorites_page=True
    )


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/accounts.db")
    app.run(port=8080, host='127.0.0.1')
