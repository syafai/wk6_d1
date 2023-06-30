from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required, snapple_fact_generator
from car_inventory.models import db, Car, car_schema, cars_schema


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'some': 'value'}

#Create Car Endpoint
@api.route('/cars', methods = ['POST'])
@token_required 
def create_car(our_user):

    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    description = request.json['description']
    price = request.json['price']
    max_speed = request.json['max_speed']
    horse_power = request.json['horse_power']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    series = request.json['series']
    snapple_fact = snapple_fact_generator() #come back and add the snapple fact generator function
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    car = Car(make, model, year, description, price, max_speed, horse_power, weight, 
                  cost_of_production, series, snapple_fact, user_token)
    
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

#Read 1 Single Car Endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):
    if id:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

#Read all the cars
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(our_user):
    token = our_user.token
    cars = Car.query.filter_by(user_token = token).all()
    response = cars_schema.dump(cars)

    return jsonify(response)


#Update 1 Car by ID
@api.route('/cars/<id>', methods = ['PUT'])
@token_required
def update_car(our_user,id):
    car = Car.query.get(id)

    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.description = request.json['description']
    car.price = request.json['price']
    car.max_speed = request.json['max_speed']
    car.horse_power = request.json['horse_power']
    car.weight = request.json['weight']
    car.cost_of_production = request.json['cost_of_production']
    car.series = request.json['series']
    car.snapple_fact = snapple_fact_generator() #come back and add the random joke generator function
    car.user_token = our_user.token

    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


#Delete 1 Car by ID
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(our_user, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)




