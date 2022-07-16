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

    def be_avg(self):
        return "null"
    def fe_avg(self):
        return "null"
    def behavioral_avg(self):
        return "null"

#lines 28-48 define the behavior of a POST request to /api/v1/users
class UserListResource(Resource):
    def post(self):
        existing_emails = db.session.query(User).filter_by(email=request.json['email']).all()
        existing_usernames = db.session.query(User).filter_by(username=request.json['username']).all()
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

#user login POST
class LoginResource(Resource):
    def post(self):
        user_check = [
            User.query.filter_by(email=request.json['email']).first(),
            User.query.filter_by(username=request.json['username']).first()
        ]

        if user_check[0] != user_check[1] or None in user_check:
            return { "error": "invalid login credentials" }, 400

        user = user_check[0]

        if user.codewars_username is None:
            json = {
                "data": {
                    "userId": str(user.id),
                    "type": "userDashboard",
                    "attributes": {
                        "username": user.username,
                        "preparednessRating": {
                            "technicalBE": user.be_avg(),
                            "technicalFE": user.fe_avg(),
                            "behavioral": user.behavioral_avg()
                        },
                        "cwAttributes": {
                            "cwLeaderboardPosition": "null",
                            "totalCompleted": "null",
                            "languageRanks": {}
                        }
                    }
                }
            }
        return json, 200

# user show

class UserShowResource(Resource):
    def patch(self, id=None):
        user = User.query.filter_by(id=id)[0]
        if user == None:
            return { "error": "could not find user" }, 404

        for key, value in request.json.items():
            if 'codewarsUsername' in key:
                user.codewars_username = value
            if 'email' in key:
                user.email = value
            if 'username' in key:
                user.username = value        

        db.session.add(user)
        db.session.commit()
        json = {
                "data": {
                    "userId": str(user.id),
                    "type": "userDashboard",
                    "attributes": {
                        "username": user.username,
                        "preparednessRating": {
                            "technicalBE": user.be_avg(),
                            "technicalFE": user.fe_avg(),
                            "behavioral": user.behavioral_avg()
                        },
                        "cwAttributes": {
                            "cwLeaderboardPosition": "null",
                            "totalCompleted": "null",
                            "languageRanks": {}
                        }
                    }
                }
            }
        return json, 200

#user cards
class UserCardsResource(Resource):
    def post(self, id):
        card = Card(
            category=request.json['category'],
            front=request.json['frontSide']           
            )
        if request.json['backSide']:
            card.back = request.json['backSide']
        db.session.add(card)
        db.session.commit()

        json = {
            "data": {
                "id": str(card.id),
                "type": "flashCard",
                "attributes": {
                    "category": card.category,
                    "competenceRating": 0.0,
                    "frontSide": card.front,
                    "backSide": card.back,
                    "userId": str(card.user_id)
                }
            }
        }]


api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(LoginResource, '/api/v1/login')
api.add_resource(UserShowResource, '/api/v1/users/<id>')
api.add_resource(UserCardsResource, '/api/v1/users/<id>/cards')

if __name__ == '__main__':
    app.run()
