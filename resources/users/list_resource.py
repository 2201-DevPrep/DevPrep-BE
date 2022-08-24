from app import db
from flask import request
from flask_restful import Resource
from models.user import User
from serializers import user_serializer

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
