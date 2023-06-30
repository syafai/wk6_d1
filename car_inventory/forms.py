from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()

class CarForm(FlaskForm):
    make = StringField('make')
    model = StringField('model')
    year = StringField('year')
    description = StringField('description')
    price = DecimalField('price', places=2)
    max_speed = StringField('max speed')
    horse_power = StringField('horsepower')
    weight = StringField('weight')
    cost_of_production = DecimalField('cost of production', places = 2)
    series = StringField('series')
    random_fact = StringField('snapple fact')
    submit_button = SubmitField()