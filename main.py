from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

db = []


class City(BaseModel):
    name: str
    timezone: str


@app.get('/')
def index():
    return {'Key': 25}


@app.get('/cities')
def get_cities():
    res = []
    for city in db:
        r = requests.get(
            f"http://worldtimeapi.org/api/timezone/{city['timezone']}")
        current_time = r.json()['datetime']
        res.append(
            {'name': city['name'], 'timezone': city['timezone'], 'current_time': current_time})
    return res


@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id-1]
    # return city
    r = requests.get(
        f"http://worldtimeapi.org/api/timezone/{city['timezone']}")
    current_time = r.json()['datetime']
    return {'name': city['name'], 'timezone': city['timezone'], 'current_time': current_time}


@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    print(db)
    json_object = json.dumps(city.dict(), indent=4)
    print(json_object)
    with open('db.json', 'w') as outfile:
        outfile.write(json_object)
    return db[-1]


@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {f'deleted city {(city_id)}'}
