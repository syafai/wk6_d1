from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid 
from datetime import datetime 


# Adding Flask Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets Module
import secrets

# Import for LoginManager & UserMixin 
# help us login our users & store their credentials 
from flask_login import UserMixin, LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)
    # create relationship between User table & Car table 

    def __init__(self, email, username, password, first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username 


    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    

    def __repr__(self):
        return f"User {self.email} has been added to the database! Woohoo!"
    

class Car(db.Model): 
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(100))
    model = db.Column(db.String(150))
    year = db.Column(db.String(20))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    max_speed = db.Column(db.String(100))
    horse_power = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    series = db.Column(db.String(150))
    snapple_fact = db.Column(db.String, nullable=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, make, model, year, description, price, max_speed, horse_power, weight,
                 cost_of_production, series, snapple_fact, user_token):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.description = description
        self.price = price
        self.max_speed = max_speed
        self.horse_power = horse_power
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.series = series
        self.snapple_fact = snapple_fact
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Car {self.make} has been added to the database! Woohoo!"
    

class CarSchema(ma.Schema): 
    class Meta:
        fields = ['id', 'make', 'model', 'year', 'description', 'price', 'max_speed', 'horse_power', 
                'weight', 'cost_of_production', 'series', 'snapple_joke']
        
car_schema = CarSchema()
cars_schema = CarSchema(many = True)


