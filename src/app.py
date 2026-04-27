import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
from sqlalchemy import select

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# [GET] /users Listar todos los usuarios del blog
@app.route('/users', methods=['GET']) 
def get_all_users():

    query = select(User)
    all_users = db.session.execute(query).scalars().all()

    character_list = [c.serialize() for c in all_users]
    return jsonify(character_list), 200


# [GET] /planets Listar todos los registros de planets en la base de datos 
@app.route('/planets', methods=['GET']) 
def get_all_planets():

    query = select(Planet)
    all_planets = db.session.execute(query).scalars().all()

    planet_list = [p.serialize() for p in all_planets]
    return jsonify(planet_list), 200


# [GET] /people/<int:people_id> Muestra la información de un solo personaje según su id
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):

    one_user = db.session.get(User, user_id)

    if one_user is None:
        return jsonify({"msg": "Planet not found"}), 404
    
    return jsonify(one_user.serialize()), 200


# [GET] /planets Listar todos los registros de planets en la base de datos 
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):

    single_planet = db.session.get(Planet, planet_id)

    if single_planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    
    return jsonify(single_planet.serialize()), 200


# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual 

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_favorites(user_id):

    query = select(Favorite).where(Favorite.user_id == user_id)
    all_favorites = db.session.execute(query).scalars().all()

    serialized_favorites = [f.serialize() for f in all_favorites]
    return jsonify(serialized_favorites), 200 

# [POST] /users agregar usuarios
@app.route('/user/', methods=['POST']) 

def adding_a_user():
 
 body = request.get_json()

 email = body.get("email")

 password = body.get("password")

 username = body.get("username")

 is_active = body.get("is_active")
 
 new_user = User(email=email, password=password, username = username, is_active = is_active)

 db.session.add(new_user)
 db.session.commit()
 
 return jsonify({"msg": "user created"}), 201

 

# [POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id 

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])

def adding_a_planet(planet_id): 

  planet = db.session.get(Planet, planet_id)

  if planet is None:
      return jsonify ({"msg": "planet not found"}), 404
  
  planet_favorite = Favorite (user_id=1, planet_id=planet_id)

  db.session.add(planet_favorite)
  db.session.commit()

  return jsonify({"msg": "Planet added at fav"}), 201

# [POST] /favorite/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.

@app.route('/favorite/people/<int:people_id>', methods=['POST'])

def adding_a_people_fav(people_id): 

  people = db.session.get(Character, people_id)

  if people is None:
      return jsonify ({"msg": "people not found"}), 404
  
  people_favorite = Favorite (user_id=1, character_id=people_id)

  db.session.add(people_favorite)
  db.session.commit()

  return jsonify({"msg": "People added at fav"}), 201

#   [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_a_planet(planet_id): 
    
    consult_favorito = select(Favorite).where(Favorite.user_id == 1, Favorite.planet_id == planet_id)
    delete_favorito = db.session.execute(consult_favorito).scalar_one_or_none()
    
    
    if delete_favorito is None:
        return jsonify({"msg": "Favorite not found"}), 404
    
    
    db.session.delete(delete_favorito)
    db.session.commit()
    
    
    return jsonify({"msg": "favorite deleted"}), 200

# LOGIN 

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if body is None:
        return jsonify({"msg": "Body is missing"}), 400
    
    email = body.get("email")
    password = body.get("password")

    query = select(User).where(User.email == email)
    user = db.session.execute(query).scalar_one_or_none()

    if user is None or user.password != password:
        return jsonify({"msg": "Invalid email or password"}), 401
    
    return jsonify({"msg": "Login successful", "user_id": user.id}), 200


# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):



 if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)