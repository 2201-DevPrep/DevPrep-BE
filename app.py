from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# line 14 creates the database only if DB_URL is set to 'sqlite:///test.db'
# if coding locally, must set DB_URL manually with this command: export DB_URL='sqlite:///test.db'
if os.environ['DB_URL'] == 'sqlite:///test.db':
    db.create_all()

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    username = db.Column(db.String())
    codewars_username = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)

#lines 28-48 define the behavior of a POST request to /api/v1/users
class UserListResource(Resource): 
    def post(self):
        existing_emails = User.query.filter_by(email=request.json['email'])
        existing_usernames = User.query.filter_by(username=request.json['username'])
        if existing_emails or existing_usernames:
            return { "error": "you already have an account." }, 400

        new_user = User(
                email=request.json['email'],
                username=request.json['username']
            ) 
        db.session.add(new_user)
        db.session.commit()
        # line 37 grabs the most recently created user for serialization
        user = User.query.order_by(User.id.desc()).first() 
        json = { # manual serialization
            "data": {
                "id": str(user.id),
                "type": "users",
                "attributes": {
                    "username": user.username
                }
            }
        }
        return json, 201

api.add_resource(UserListResource, '/api/v1/users')

if __name__ == '__main__':
    app.run()
