import json
from typing import List

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
breakpoint()
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


def create_car(car: Car) -> JSONResponse:
    car_id = len(cars) + 1
    car.id = car_id
    cars[car_id] = car
    return JSONResponse(Car(car), status_code=201)


def get_car(car_id: int) -> JSONResponse:
    car = cars.get(car_id)
    if not car:
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Car(car), status_code=200)


def update_car(car_id: int, car: Car) -> JSONResponse:
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    car.id = car_id
    cars[car_id] = car
    return JSONResponse(Car(car), status_code=200)


def delete_car(car_id: int) -> JSONResponse:
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
