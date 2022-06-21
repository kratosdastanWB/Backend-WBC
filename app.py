from cmath import log
import string
import time
from venv import create
import redis
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

logging.debug("Se incio esto")

cache = redis.Redis(host='redis', port=6379)

def execute_queries(query):
    logging.debug("se inicia la DB")
    db_name = 'WBC'
    db_user = 'postgres'
    db_pass = 'example'
    db_host = 'db'
    db_port = '5432'
    db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    db = create_engine(db_string)
    try:
        data = db.execute(query)
        for item in data:
            logging.debug(item)
    except Exception as ex:
        logging.debug(ex)  

@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        return jsonify({"message": "Resultado exitoso",
        "username": request.form['username'],
        "password": request.form['password']})
    return ''    

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    execute_queries("CREATE TABLE users ( ID SERIAL PRIMARY KEY, NAME varchar(50));")
    count = get_hit_count()
    return 'Hello World! haz visitado {} veces este sitio.\n'.format(count)