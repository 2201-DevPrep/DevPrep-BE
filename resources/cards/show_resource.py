from app import db
from flask import request
from flask_restful import Resource
from models.user import User
from models.card import Card
from serializers import card_serializer

class CardShowResource(Resource):
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
