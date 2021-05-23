from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user_resource import UserRegistrationResource
from resources.item_resource import ItemsResource, ItemResource
from resources.store_resources import StoreResource, StoresResource
from security import authenticate, identity
from db import db

app = Flask(__name__)
app.secret_key = "Shirya2021"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
jwt = JWT(app, authenticate, identity)
db.init_app(app)


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(StoreResource, '/store/<string:name>')
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemsResource, '/items')
api.add_resource(StoresResource, '/stores')
api.add_resource(UserRegistrationResource, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
