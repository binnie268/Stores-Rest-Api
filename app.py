from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# sql alchemy the main library has own tracking modification
#  so turn off the flask one.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

# JWT creates new endpoint /auth. when we call /auth, send username and
# password. jwt takes username, password, sends over to authenticate function.
# find correct username and password. if match, return user. user becomes
# identity.


jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

# silent=True return nothing
# force=True
# circular imports -> model is going to import db too.
# db will be in app and in resources.
