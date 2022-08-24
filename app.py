from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_caching import Cache
from flask_cors import CORS
import os

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
cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR': 'cache'})
db = SQLAlchemy(app)
api = Api(app)

from models.user import User
from models.card import Card

# creates the database only if DB_URL is set to 'sqlite:///test.db'
# if coding locally, must set DB_URL manually with this command: export DB_URL='sqlite:///test.db'
if os.environ['DB_URL'] == 'sqlite:///test.db':
    db.create_all()

from resources.users.list_resource import UserListResource
from resources.users.show_resource import UserShowResource
from resources.users.login_resource import LoginResource
from resources.users.dashboard_resource import DashboardResource
from resources.cards.list_resource import CardListResource
from resources.cards.show_resource import CardShowResource
from resources.quote_resource import QuoteResource

api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(UserShowResource, '/api/v1/users/<id>')
api.add_resource(LoginResource, '/api/v1/login')
api.add_resource(DashboardResource, '/api/v1/dashboard')
api.add_resource(CardListResource, '/api/v1/users/<id>/cards')
api.add_resource(CardShowResource, '/api/v1/users/<user_id>/cards/<card_id>')
api.add_resource(QuoteResource, '/api/v1/quote')

if __name__ == '__main__':
    app.run()
