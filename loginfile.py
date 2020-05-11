from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from data import db_session
from data.users import User


class RegistrationForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    age = StringField('Возраст')

    email = StringField('Почта',
                         validators=[DataRequired(), Email(), Length(min=4, max=25)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField('Подтвердите Пароль', 
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Почта', 
                         validators=[DataRequired(), Email(), Length(min=4, max=25)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class NewsForm(FlaskForm):
    news_tittle = StringField('Заголовок', validators=[DataRequired()]) 
    news = TextAreaField("Запись", validators=[DataRequired()])

    submit = SubmitField('Создать')


class UpdateForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    age = StringField('Возраст')

    email = StringField('Почта',
                         validators=[DataRequired(), Email(), Length(min=4, max=25)])
    submit = SubmitField('Изменить')

    image = FileField('Новая аватарка', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])


class ResetPasswordForm(FlaskForm):
    email = StringField('Введите почту', 
                         validators=[DataRequired(), Email(), Length(min=4, max=25)])
    submit = SubmitField('Восстанвить пароль')


class NewPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField('Подтвердите Пароль', 
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сменить пароль')