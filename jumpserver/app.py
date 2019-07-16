from flask import Flask
from flask_restful import Api
# from flask_migrate import Migrate
# from flask_jwt import JWT

# from security import authenticate, identity
#from resources.user import UserRegister
# from resources.item import Item, ItemList
# from resources.store import Store, StoreList
# from resources.firebase import Firebase
# from resources.toybox import Toybox
# from resources.badge import AvailableBadge, AvailableBadgeList
# from resources.badge_instance import BadgeInstanceList, BadgeInstance
#from db import db


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sm_dev_user:q5SzKU48B9R3pDCNG73x@mysql.seamonkey.trysexualsmedia.com/seamonkey_dev'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
# app.secret_key = 'jose'

api = Api(app)
# migrate = Migrate(app, db)



@app.before_first_request
def create_tables():
    db.create_all()
    


# jwt = JWT(app, authenticate, identity)  # /auth

# api.add_resource(Store, '/store/<string:name>')
# api.add_resource(Toybox, '/toybox/<string:name>')
# api.add_resource(StoreList, '/stores')
# api.add_resource(Item, '/item/<string:name>')
# api.add_resource(ItemList, '/items')
# api.add_resource(UserRegister, '/register')
# api.add_resource(Firebase, '/googleauth')
# api.add_resource(AvailableBadge, '/available_badge')
# api.add_resource(AvailableBadgeList, '/available_badges')

# Badges
# api.add_resource(BadgeInstanceList, '/sash')
# api.add_resource(BadgeInstance, '/badge')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    from db import db
    
    db.init_app(app)
    app.run(port=5000, debug=True)

    # app.run(port=5000, debug=True,host='0.0.0.0')
