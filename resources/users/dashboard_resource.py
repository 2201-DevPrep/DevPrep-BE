from app import db
from flask import request
from flask_restful import Resource
from models.user import User
from serializers import user_serializer

class DashboardResource(Resource):
    def get(self):
        params = dict(request.args)
        if 'userId' not in params.keys():
            return { 'error': 'userId param is required' }, 404

        user = User.query.get(params['userId'])
        if user == None:
            return { 'error': 'invalid user id' }, 404

        return user_serializer.dashboard(user)
