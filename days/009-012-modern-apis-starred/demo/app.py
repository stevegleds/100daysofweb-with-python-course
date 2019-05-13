import json
from typing import List  # used to add type check to list output in definitions

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


# helpers

def _load_cars_data():
    with open('cars.json') as f:
        cars = json.loads(f.read())
        return {car["id"]: car for car in cars}
        # dictionary of cars with key 'id' and value car dictionary
        # e.g. {1: {'id': 1, 'manufacturer': 'Mercedes-Benz', ...}
        # this allows retrieval by car id and faster processing / lookup


cars = _load_cars_data()  # one time task
# now we can get unique manufacturers to help with validation
VALID_MANUFACTURERS = set([car["manufacturer"]
                          for car in cars.values()])
CAR_NOT_FOUND = 'Car not found'
# definition


class Car(types.Type):
    # validators comes from apistar
    id = validators.Integer(allow_null=True)  # assign in POST
    manufacturer = validators.String(enum=list(VALID_MANUFACTURERS))
    model = validators.String(max_length=50)
    year = validators.Integer(minimum=1900, maximum=2050)
    vin = validators.String(max_length=50, default='')


# API methods

def list_cars() -> List[Car]:
    return [Car(car[1]) for car in sorted(cars.items())]
    # Need .items() to sort because The method items() returns a list of dict's (key, value) tuple pairs
    # So, we have list of id:dictionary pairs : (1, {'id':1, 'model': 'Corsa', ...}), (2, {'id:2', 'model...})
    # We only need the dictionary part so car[1] to get second element
    # Car(car[1]) now creates a Car object from the car item
    # Finally the list comprehension does this for each entry in cars


def create_car(car: Car) -> JSONResponse:
    car_id = len(cars) + 1  # ids are sequential
    car.id = car_id
    cars[car_id] = car  # car is a dictionary containing the car info
    return JSONResponse(Car(car), status_code=201)  # 201 code is created


def get_car(car_id: int) -> JSONResponse:
    car = cars.get(car_id)
    if not car:
        error = {'error': CAR_NOT_FOUND} # best practice is to return error as a dictionary
        return JSONResponse(error, status_code=404)  # status 404 is not found

    return JSONResponse(Car(car), status_code=200)
    # 200 is OK
    # Car(car) creates a Car object from the car with id = car_id


def update_car(car_id: int, car: Car) -> JSONResponse:
    #  update_car is the method when routed with car_id in the url and method is 'put'
    #  car_id is the integer from the url
    #  car is the car object with updated mandatory fields and optional vin. for this demo this information is added
    #  using Postman
    #  check if cars dictionary has key = equal to car_id
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    car.id = car_id
    cars[car_id] = car
    return JSONResponse(Car(car), status_code=200)


def delete_car(car_id: int) -> JSONResponse:
    # similar to update_car
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del cars[car_id]
    return JSONResponse({}, status_code=204)


routes = [
    # Routes require end point, method and handler
    Route('/', method='GET', handler=list_cars),
    Route('/', method='POST', handler=create_car),
    Route('/{car_id}/', method='GET', handler=get_car),
    Route('/{car_id}/', method='PUT', handler=update_car),
    Route('/{car_id}/', method='DELETE', handler=delete_car),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
