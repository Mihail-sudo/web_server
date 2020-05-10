from flask import Flask, render_template, url_for, redirect, abort, request
import secrets
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from data import db_session
from loginfile import LoginForm, RegistrationForm, NewsForm, UpdateForm
from data.users import User
from data.news import News
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)


def save_picture(picture):
    rnd_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = rnd_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    picture.save(picture_path)
    return picture_fn


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(news_api.blueprint)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/home')
def index():
    session = db_session.create_session()
    news = session.query(News)
    return render_template("index.html", news=news)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.email = form.email.data
        user.hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        session.add(user)
        session.commit()
        return redirect('login')
    return render_template('register.html', title='регистрация', 
                            form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and bcrypt.check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News()
        news.news_tittle = form.news_tittle.data
        news.news = form.news.data
        news.usered = f'{current_user.name} {current_user.surname}'
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('news.html', title='Новая запись', 
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id).first()
        if news:
            form.news_tittle.data = news.news_tittle
            form.news.data = news.news
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id).first()
        if news:
            form.news_tittle.data = news.news_tittle
            form.news.data = news.news
            session.commit()
            return redirect('')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        message = ''
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if form.image.data:
            user.image = save_picture(form.image.data)
        user.name = form.name.data
        user.surname = form.surname.data
        mail = session.query(User).filter(User.email == form.email.data).first()
        if mail.id == user.id:
            user.email = form.email.data
        else:
            message = 'мыло занято'
            return render_template('my_account.html', tittle='Account', image=user.image, form=form, message=message)
        user.email = form.email.data
        user.age = form.age.data
        session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        message = ''
        session = db_session.create_session()
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
        form.age.data = current_user.age
        session.commit()
    image = url_for('static', filename='img/' + current_user.image)
    return render_template('my_account.html', tittle='Account', image=image, form=form, message=message)


@app.route('/user_account/<int:id>')
def user_account(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user:
        news = session.query(News).filter(News.user_id == id)
    else:
        abort(404)
    return render_template("index.html", news=news)


if __name__ == '__main__':
    main()

