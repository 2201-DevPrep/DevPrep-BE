from app import db
from flask import request
from flask_restful import Resource
from models.user import User
from serializers import user_serializer

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
