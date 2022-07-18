from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy, Model
from flask_restful import Api, Resource
from flask_migrate import Migrate
from sqlalchemy.orm import relationship
import requests
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
    cards = relationship("Card", lazy='select')

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def cards_by_category(self, cat):
        return Card.query.filter_by(user_id=self.id, category=cat).all()

    def average_card_rating_by_category(self, cat):
        sum = 0
        cards = self.cards_by_category(cat)

        if cards: 
            for card in cards: sum += card.rating 
            avg = sum / len(cards)
            return round(avg, 2)
        else:
            return "null"

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    rating = db.Column(db.Float(), default=0.0)
    front = db.Column(db.Text())
    back = db.Column(db.Text(), default='')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def as_json(self):
        json = {
            "id": str(self.id),
            "type": "flashCard",
            "attributes": {
                "category": self.category,
                "competenceRating": self.rating,
                "frontSide": self.front,
                "backSide": self.back,
                "userId": str(self.user_id)
            }
        }
        return json

    def __repr__(self):
        return '<id {}>'.format(self.id)

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

        json = {
                "data": {
                    "userId": str(user.id),
                    "type": "userDashboard",
                    "attributes": {
                        "username": user.username,
                        "preparednessRating": {
                            "technicalBE": user.average_card_rating_by_category('technicalBE'),
                            "technicalFE": user.average_card_rating_by_category('technicalFE'),
                            "behavioral": user.average_card_rating_by_category('behavioral')
                            },
                        "cwAttributes": {
                            "cwLeaderboardPosition": "null",
                            "totalCompleted": "null",
                            "languageRanks": {}
                            }
                        }
                    }
                }

        if user.codewars_username is None or user.codewars_username == '':
            return json, 200
        else:
            cw_response = requests.get(f'https://www.codewars.com/api/v1/users/{user.codewars_username}').json()
            if 'id' not in cw_response.keys():
                return json, 200

            user_cw_attributes = json['data']['attributes']['cwAttributes']
            user_cw_attributes['cwLeaderboardPosition'] = cw_response['leaderboardPosition']
            user_cw_attributes['totalCompleted'] = cw_response['codeChallenges']['totalCompleted']

            for key, value in cw_response['ranks']['languages'].items():
                user_cw_attributes['languageRanks'][key] = value['rank']

            return json, 200

# user show
class UserShowResource(Resource):
    def patch(self, id=None):
        user = User.query.get(id)
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
                            "technicalBE": user.average_card_rating_by_category('technicalBE'),
                            "technicalFE": user.average_card_rating_by_category('technicalFE'),
                            "behavioral": user.average_card_rating_by_category('behavioral')
                            },
                        "cwAttributes": {
                            "cwLeaderboardPosition": "null",
                            "totalCompleted": "null",
                            "languageRanks": {}
                            }
                        }
                    }
                }

        if user.codewars_username is None or user.codewars_username == '':
            return json, 200
        else:
            cw_response = requests.get(f'https://www.codewars.com/api/v1/users/{user.codewars_username}').json()
            if 'id' not in cw_response.keys():
                return { "error": "invalid codewars username" }, 404

            user_cw_attributes = json['data']['attributes']['cwAttributes']
            user_cw_attributes['cwLeaderboardPosition'] = cw_response['leaderboardPosition']
            user_cw_attributes['totalCompleted'] = cw_response['codeChallenges']['totalCompleted']

            for key, value in cw_response['ranks']['languages'].items():
                user_cw_attributes['languageRanks'][key] = value['rank']

            return json, 200

#user dashboard
class UserDashboardResource(Resource):
    def get(self):
        params = dict(request.args)
        if 'userId' not in params.keys():
            return { 'error': 'userId param is required' }, 404

        user = User.query.get(params['userId'])
        if user == None:
            return { 'error': 'invalid user id' }

        json = {
                "data": {
                    "userId": str(user.id),
                    "type": "userDashboard",
                    "attributes": {
                        "username": user.username,
                        "preparednessRating": {
                            "technicalBE": user.average_card_rating_by_category('technicalBE'),
                            "technicalFE": user.average_card_rating_by_category('technicalFE'),
                            "behavioral": user.average_card_rating_by_category('behavioral')
                            },
                        "cwAttributes": {
                            "cwLeaderboardPosition": "null",
                            "totalCompleted": "null",
                            "languageRanks": {}
                            }
                        }
                    }
                }

        if user.codewars_username is None or user.codewars_username == '':
            return json, 200
        else:
            cw_response = requests.get(f'https://www.codewars.com/api/v1/users/{user.codewars_username}').json()
            if 'id' not in cw_response.keys():
                return json, 200

            user_cw_attributes = json['data']['attributes']['cwAttributes']
            user_cw_attributes['cwLeaderboardPosition'] = cw_response['leaderboardPosition']
            user_cw_attributes['totalCompleted'] = cw_response['codeChallenges']['totalCompleted']

            for key, value in cw_response['ranks']['languages'].items():
                user_cw_attributes['languageRanks'][key] = value['rank']

            return json, 200

#user cards
class UserCardsResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user == None:
            return { "error": "invalid user id" }, 404
        
        json = {
            "data": {
                "BEtechnicalCards": [],
                "FEtechnicalCards": [],
                "behavioralCards": []
            }
        }

        for card in user.cards_by_category('technicalBE'):
            json['data']['BEtechnicalCards'].append(card.as_json())

        for card in user.cards_by_category('technicalFE'):
            json['data']['FEtechnicalCards'].append(card.as_json())

        for card in user.cards_by_category('behavioral'):
            json['data']['behavioralCards'].append(card.as_json())

        return json, 200

    def post(self, id):
        user = User.query.get(id)
        if user == None:
            return { "error": "invalid user id" }, 400

        if 'frontSide' not in request.json.keys():
            return { "error": "bad request" }, 400

        if 'category' not in request.json.keys():
            return { "error": "bad request" }, 400

        card = Card(
                category=request.json['category'],
                front=request.json['frontSide'],
                user_id=id           
                )
        if 'backSide' in request.json.keys():
            card.back = request.json['backSide']
        else:
            card.back = ""

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
                }
        return json, 201

# user card show

class UserCardShowResource(Resource):
    def patch(self, user_id, card_id):
        card = Card.query.get(card_id)
        if card == None:
            return { "error": "invalid card id" }, 400

        user = User.query.get(user_id)
        if user == None:
            return { "error": "invalid user id" }, 400

        for key, value in request.json.items():
            if "category" in key:
                card.category = value
            if "frontSide" in key:
                card.front = value
            if "backSide" in key:
                card.back = value
            if "competenceRating" in key:
                card.rating = value

        db.session.add(card)
        db.session.commit()

        json = {
                "data": {
                    "id": str(card.id),
                    "type": "flashCard",
                    "attributes": {
                        "category": card.category,
                        "competenceRating": card.rating,
                        "frontSide": card.front,
                        "backSide": card.back,
                        "userId": str(card.user_id)
                        }
                    }
                }
        return json, 200

    def delete(self, user_id, card_id):
        card = Card.query.get(card_id)
        if card == None:
            return { "error": "invalid card or user" }, 400

        db.session.delete(card)
        db.session.commit()

        return {}, 204

api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(LoginResource, '/api/v1/login')
api.add_resource(UserShowResource, '/api/v1/users/<id>')
api.add_resource(UserDashboardResource, '/api/v1/dashboard')
api.add_resource(UserCardsResource, '/api/v1/users/<id>/cards')
api.add_resource(UserCardShowResource, '/api/v1/users/<user_id>/cards/<card_id>')

if __name__ == '__main__':
    app.run()
