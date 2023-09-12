#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if not pet:
        return make_response('<h1>404 pet not found</h1>', 404)
    return make_response(f"""
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    """, 200)

@app.route('/owners/<int:id>')
def owner_by_id(id):
    owner =  Owner.query.filter(Pet.id == id).first()

    if not owner:
        return make_response('<h1>404 pet not found</h1>', 404)

    response_body = f'<h1>Information for {owner.name}</h1>'
    pets = [pet for pet in owner.pets]
    if not pets:
        response_body += '<h2>Has no pets at this time.</h2>'
    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    status_code = 200
    return make_response(response_body, status_code)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
