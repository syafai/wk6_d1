from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from car_inventory.forms import CarForm
from car_inventory.models import Car, db 
from car_inventory.helpers import snapple_fact_generator

site = Blueprint('site', __name__, template_folder='site_template')

@site.route('/')
def home():
    print('look at this cool project. Would you just look at it')
    return render_template('index.html')


@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    carform = CarForm()

    try:
        if request.method == 'POST' and carform.validate_on_submit():
            make = carform.make.data
            model = carform.model.data
            year = carform.year.data
            description = carform.description.data
            price = carform.price.data
            max_speed = carform.max_speed.data
            horse_power = carform.horse_power.data
            weight = carform.weight.data
            cost_of_production = carform.cost_of_production.data
            series = carform.series.data
            if carform.random_fact.data:
                snapple_fact = carform.random_fact.data
            else:
                snapple_fact = snapple_fact_generator()
            user_token = current_user.token 

            car = Car(make, model, year, description, price, max_speed, 
                          horse_power, weight, cost_of_production, series, snapple_fact, user_token)
            
            db.session.add(car)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Car not created, please check your form and try again.')
    
    user_token = current_user.token 
    cars = Car.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=carform, cars=cars )