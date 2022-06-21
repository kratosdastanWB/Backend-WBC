from cmath import log
import time 
from datetime import datetime, timedelta
import redis
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import logging
from jwt import encode,decode
from jwt import exceptions

#Models

from models.ModelUser import ModelUser

#Entities

from models.entities.User import  User

app = Flask(__name__)
app.config['SECRET_KEY'] = '637bxrO9mEZ7NhTkSqgCMmWzYIGJaKNy'

logging.basicConfig(level=logging.DEBUG)

logging.debug("Se incio esto")

cache = redis.Redis(host='redis', port=6379)

db_name = 'WBC'
db_user = 'postgres'
db_pass = 'example'
db_host = 'db'
db_port = '5432'
db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
db = create_engine(db_string)
con = db.raw_connection()

def execute_queries(query):
    logging.debug("se inicia la DB")
    # db_name = 'WBC'
    # db_user = 'postgres'
    # db_pass = 'example'
    # db_host = 'db'
    # db_port = '5432'
    # db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    # db = create_engine(db_string)
    try:
        data = db.execute(query)
        for item in data:
            logging.debug(item)
    except Exception as ex:
        logging.debug(ex)  

@app.route('/log', methods=['POST'])
def log():
    if request.method=='POST':
        user =User(0,request.form['email'],request.form['password'])
        logging.debug("voy a intentar entrar a login")
        logged_user=ModelUser.login(con,user)
        if logged_user != None:
            if logged_user.password:
                return jsonify({"message": "Usuario loggeado con exito"})
            else:
                return jsonify({"message": "Error al iniciar sesion"})    
        else:
            return jsonify({"message": "Error al iniciar sesion"})
        # return jsonify({"message": "Resultado exitoso",
        # "username": request.form['username'],
        # "password": request.form['password']})
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


def expire_date(days: int):
    now= datetime.now()
    new_date = now + timedelta(days)
    return new_date


def write_token(data):
    token = encode(payload={**data, "exp": expire_date(2)} , 
                    key="637bxrO9mEZ7NhTkSqgCMmWzYIGJaKNy", algorithm="HS256")
    return token.encode("UTF-8")

def validate_token(token, output=False):
    try:
        if output:
            return decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        decode(token, app.config['SECRET_KEY'], algorithms="HS256")

    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    logging.debug(data['username'])
    if data['username'] == "Nelson Hernandez":
        return write_token(data=request.get_json())
    else:
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response

@app.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)
@app.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

@app.route('/home')
def hello():
    # execute_queries("""CREATE TABLE Users 
    # ( ID SERIAL PRIMARY KEY, 
    # name varchar(50),
    # lastname varchar(50),
    # email varchar(50),
    # phone varchar(15),
    # photo_profile varchar(150),
    # role integer,
    # roleTag varchar(150),
    # password varchar(102),
    # created_at timestamp,
    # updated_at timestamp,
    # deleted_at timestamp);""")
    count = get_hit_count()
    return 'Hello World! haz visitado {} veces este sitio.\n'.format(count)
