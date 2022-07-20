from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy, Model
from flask_restful import Api, Resource
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from serializers import user_serializer, card_serializer
from sqlalchemy.orm import relationship
import random
import os
import csv

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initializes a memory cache and sets the default timeout to 1 day
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 86400})
cache.init_app(app)
db = SQLAlchemy(app)
api = Api(app)

# creates the database only if DB_URL is set to 'sqlite:///test.db'
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
        from sqlalchemy.sql import func
        sql_result = db.session.query(func.avg(Card.rating)).filter(Card.user_id==self.id, Card.category==cat)
        if sql_result[0][0]:
            rounded = round(sql_result[0][0], 2)
            return float(rounded)
        else:
            return "null"

    def generate_default_cards(self):
        with open('interview_questions.csv', newline='') as f:
            fdicts = csv.DictReader(f.read().splitlines(), skipinitialspace=True)

            csv_dicts = [{k: v for k, v in row.items()} for row in fdicts]
            for dict in csv_dicts:
                card = Card(
                    category=dict['category'],
                    front=dict['question'],
                    user_id=self.id
                )
                db.session.add(card)
                db.session.commit()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    rating = db.Column(db.Float(), default=0.0)
    front = db.Column(db.Text())
    back = db.Column(db.Text(), default='')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return '<id {}>'.format(self.id)

# user create
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
        # grabs the most recently created user for serialization
        user = User.query.order_by(User.id.desc()).first()

        # this is where we create the default flash cards for a new user
        user.generate_default_cards()

        return user_serializer.show(user), 201

# User Login
class LoginResource(Resource):
    def post(self):
        user_check = [
                User.query.filter_by(email=request.json['email']).first(),
                User.query.filter_by(username=request.json['username']).first()
                ]

        if user_check[0] != user_check[1] or None in user_check:
            return { "error": "invalid login credentials" }, 400

        user = user_check[0]

        return user_serializer.dashboard(user), 200

# user update
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
        
        return user_serializer.dashboard(user)
#user dashboard
class UserDashboardResource(Resource):
    def get(self):
        params = dict(request.args)
        if 'userId' not in params.keys():
            return { 'error': 'userId param is required' }, 404

        user = User.query.get(params['userId'])
        if user == None:
            return { 'error': 'invalid user id' }, 404

        return user_serializer.dashboard(user)

#user cards
class UserCardsResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user == None:
            return { "error": "invalid user id" }, 404

        return card_serializer.cards_index(user)

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

        return {"data": card_serializer.show(card)}, 201

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

        return {"data": card_serializer.show(card)}, 200

    def delete(self, user_id, card_id):
        card = Card.query.get(card_id)
        if card == None:
            return { "error": "invalid card or user" }, 400

        db.session.delete(card)
        db.session.commit()

        return {}, 204

# quote of the day
class QuoteResource(Resource):
    def get(self):
        # checks if a current quote of the day exists
        cached_quote = cache.get('quote_of_the_day')
        if cached_quote:
            return cached_quote, 200
        else:
            # if not, reads the CSV and caches a random quote
            with open('quotes.csv', newline='') as f:
                fdicts = csv.DictReader(f.read().splitlines(), skipinitialspace=True)

                csv_dicts = [{k: v for k, v in row.items()} for row in fdicts]

            quote = random.choice(csv_dicts)
            cache.set('quote_of_the_day', quote, timeout=86400)
            return cache.get('quote_of_the_day'), 200

api.add_resource(QuoteResource, '/api/v1/quote')
api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(LoginResource, '/api/v1/login')
api.add_resource(UserShowResource, '/api/v1/users/<id>')
api.add_resource(UserDashboardResource, '/api/v1/dashboard')
api.add_resource(UserCardsResource, '/api/v1/users/<id>/cards')
api.add_resource(UserCardShowResource, '/api/v1/users/<user_id>/cards/<card_id>')

if __name__ == '__main__':
    app.run()
