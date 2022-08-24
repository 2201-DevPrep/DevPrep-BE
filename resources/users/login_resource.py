from app import db
from flask import request
from flask_restful import Resource
from models.user import User
from serializers import user_serializer

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
