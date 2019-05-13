import json
from typing import List  # used to add type check to list output in definitions

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


# helpers

def _load_ips_data():
    with open('ip.json') as f:
        ips = json.loads(f.read())
        return {ip["id"]: ip for ip in ips}
        # dictionary of ips with key 'id' and value ip dictionary
        # e.g. {1: {'id': 1, 'manufacturer': 'Mercedes-Benz', ...}
        # this allows retrieval by ip id and faster processing / lookup


ips = _load_ips_data()  # one time task

# now we can get unique manufacturers to help with validation
VALID_GENDERS = set([ip["gender"]
                     for ip in ips.values()])
IP_NOT_FOUND = 'IP not found'
# definition


class Ip(types.Type):
    # validators comes from apistar
    id = validators.Integer(allow_null=True)  # assign in POST
    gender = validators.String(enum=list(VALID_GENDERS))
    first_name = validators.String(max_length=50)
    last_name = validators.String(max_length=50)
    email = validators.String(max_length=50, default='')
    ip = validators.String(max_length=15, default="0.0.0.0")


# API methods

def list_ips() -> List[Ip]:
    return [Ip(ip[1]) for ip in sorted(ips.items())]
    # Need .items() to sort because The method items() returns a list of dict's (key, value) tuple pairs
    # So, we have list of id:dictionary pairs : (1, {'id':1, 'model': 'Corsa', ...}), (2, {'id:2', 'model...})
    # We only need the dictionary part so ip[1] to get second element
    # Car(ip[1]) now creates a Car object from the ip item
    # Finally the list comprehension does this for each entry in cars


def create_ip(ip: Ip) -> JSONResponse:
    car_id = len(cars) + 1  # ids are sequential
    ip.id = car_id
    cars[car_id] = ip  # car is a dictionary containing the car info
    return JSONResponse(Ip(ip), status_code=201)  # 201 code is created


def get_car(car_id: int) -> JSONResponse:
    car = cars.get(car_id)
    if not car:
        error = {'error': CAR_NOT_FOUND} # best practice is to return error as a dictionary
        return JSONResponse(error, status_code=404)  # status 404 is not found

    return JSONResponse(Ip(car), status_code=200)
    # 200 is OK
    # Car(car) creates a Car object from the car with id = car_id


def update_car(car_id: int, car: Ip) -> JSONResponse:
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
    return JSONResponse(Ip(car), status_code=200)


def delete_car(car_id: int) -> JSONResponse:
    # similar to update_car
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del cars[car_id]
    return JSONResponse({}, status_code=204)


routes = [
    # Routes require end point, method and handler
    Route('/', method='GET', handler=list_ips),
    Route('/', method='POST', handler=create_ip),
    Route('/{car_id}/', method='GET', handler=get_car),
    Route('/{car_id}/', method='PUT', handler=update_car),
    Route('/{car_id}/', method='DELETE', handler=delete_car),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
