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

if os.environ['DB_URL'] == 'sqlite:///test.db':
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    username = db.Column(db.String())
    codewars_username = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)

class UserListResource(Resource):
    def post(self):
        new_user = User(
                email=request.json['email'],
                username=request.json['username']
            )
        db.session.add(new_user)
        db.session.commit()
        user = User.query.order_by(User.id.desc()).first()
        json = {
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
