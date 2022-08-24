from app import db
from flask import request
from flask_restful import Resource
from models.user import User
from models.card import Card
from serializers import card_serializer

class CardListResource(Resource):
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
