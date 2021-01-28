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
from models import db, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/contacts', methods=['GET'])
def handle_contact():
    contacts = Contact.query.all()
    response_body = []
    for contact in contacts:
        response_body.append(contact.serialize())
    return jsonify(response_body), 200

@app.route('/contacts', methods=['POST'])
def add_new_contact():
    body = request.get_json()
    print (body)
    new_contact = Contact(
        full_name = body["full_name"],
        email = body["email"],
        address = body["address"],
        phone = body["phone"],
    )
    db.session.add(new_contact)
    try:
        db.session.commit()
        print (new_contact.serialize())
        return jsonify (new_contact.serialize()), 201
    except Exception as error:
        print (error.args)    
        return jsonify("NOT OK"), 500

@app.route('/contacts/<int:id>', methods=['DELETE'])
def remove_contact(id):
    contact = Contact.query.get(id)
    if contact is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(contact)
    db.session.commit()
    return jsonify([]), 204

@app.route('/contacts/<int:id>', methods=['GET','PUT','PATCH'])
def update_contact(id):
    if request.method == 'GET':
        contact = Contact.query.get(id)
        return jsonify (contact.serialize()), 200
    if request.method == 'PUT':
        contact = Contact.query.get(id)
        body = request.get_json()
        contact.full_name = body ['full_name']
        contact.email = body ['email']
        contact.address = body ['address']
        contact.phone = body ['phone']
        db.session.commit()
        return jsonify (contact.serialize()), 200
    if request.method == 'PATCH':
        contact = Contact.query.get(id)
        body = request.get_json()
        if "full_name" in body:
            contact.full_name = body ['full_name']
        if "address" in body:
            contact.address = body ['address']
        if "phone" in body:
            contact.phone = body ['phone']
        db.session.commit()
        return jsonify(contact.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
