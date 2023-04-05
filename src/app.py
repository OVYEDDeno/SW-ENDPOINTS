"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people=People.query.all()
    if people is None:
        return jsonify(message="Where Did Everybody GOOO?")
    else:
        return jsonify([person.serialize()for person in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(id):
    person=People.query.get(id)
    if person is None:
        return jsonify(message="Where Did can't assume gender GOOO?")
    else:
        return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets=Planets.query.all()
    if planets is None:
        return jsonify(message="The Death Star Destroyed them all!!")
    else:
        return jsonify([planet.serialize()for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(id):
    planet=Planets.query.get(id)
    if planet is None:
        return jsonify(message="Death Star Got here Before us!")
    else:
        return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users=Users.query.all()
    if users is None:
        return jsonify(message="Where Did Everybody GOOO?")
    else:
        return jsonify([user.serialize()for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def all_users_favs():
    users=Users.query.all()
    if users is None:
        return jsonify(message="Where Did Everybody GOOO?")
    else:
        return jsonify([user.serialize()for user in users]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def fav_planet():

    response_body = {
        "msg": "Hello, this is everybody"
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet():

    response_body = {
        "msg": "Hello, this is everybody"
    }

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def fav_people():

    response_body = {
        "msg": "Hello, this is everybody"
    }

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people():

    response_body = {
        "msg": "Hello, this is everybody"
    }

    return jsonify(response_body), 200 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
