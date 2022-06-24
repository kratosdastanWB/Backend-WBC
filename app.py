from cmath import log
import time
from datetime import datetime, timedelta
import redis
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
from jwt import encode, decode
from jwt import exceptions
from flask_migrate import Migrate
# Models

#from models.ModelUser import ModelUser

# Entities

#from models.entities.User import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '637bxrO9mEZ7NhTkSqgCMmWzYIGJaKNy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db_name = 'WBC'
db_user = 'postgres'
db_pass = 'example'
db_host = 'db'
db_port = '5432'
db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_string


logging.basicConfig(level=logging.DEBUG)

logging.debug("Se incio esto")

cache = redis.Redis(host='redis', port=6379)


# db = create_engine(db_string)
# con = db.raw_connection()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# MODELS


class User(db.Model):
    
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	lastname = db.Column(db.String(50))
	email = db.Column(db.String(30))
	phone = db.Column(db.String(15))
	photo_profile = db.Column(db.String(150))
	role = db.Column(db.Integer)
	roleTag = db.Column(db.String(50))
	password = db.Column(db.String(102))    
    created_at = db.Column(db.Timestamp)
    updated_at = db.Column(db.Timestamp)
    deleted_at = db.Column(db.Timestamp)



    def __init__(self,name):
            self.name = name


    def __repr__(self):
            return f'<name {self.name}>'

# Test de login flask-login
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
# test redis
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

# Ruta test de redis
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

# Inicia implementacion JWT

# Expiarar token
def expire_date(days: int):
    now= datetime.now()
    new_date = now + timedelta(days)
    return new_date

# crear token
def write_token(data):
    token = encode(payload={**data, "exp": expire_date(2)} , 
                    key=app.config['SECRET_KEY'], algorithm="HS256")
    return token.encode("UTF-8")
# validar token
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
# ruta de API para pedir un token
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
# Verificar token via API
@app.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)

 # Codigo para restringir rutas con JWT   
# @app.before_request
# def verify_token_middleware():
#     token = request.headers['Authorization'].split(" ")[1]
#     return validate_token(token, output=False)


