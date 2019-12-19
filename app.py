import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, timedelta

from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rose'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login' # changing endpoint '/auth' to '/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) # extending token expiration time


jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

api.add_resource(UserRegister, '/signup')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5100, debug=True)
