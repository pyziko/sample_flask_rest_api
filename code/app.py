from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'pyziko'
api = Api(app)

# todo INFO: jwt creates an endpoint called /auth
# todo INFO: we send it a username an password, jwt takes the credentials and sends it to the authenticate fn
# todo INFO: to check if username exist, we then compare the password from the /auth as done in security/authenticate
# todo INFO: if credentials are valid, jwt then returns an jwt_token
# todo INFO: we can then send the token to the next request we need,
# todo INFO: jwt then calls the identity fn which inturn returns the user
# todo INFO: to access RESOURCE header >>> key =>Authorization,  value =>JWT access_token
jwt = JWT(app, authenticate, identity)

items = []


# no need for jsonify as flask_restful does the conversion for us
# todo INFO: next gives us the first item (can be called multiple times to gives the next and next ...)
# todo INFO: None included with next ensures that if no more items, it returns None
# todo INFO: request.get_json(force=True) ignores the header and formats body to json
# todo INFO: request.get_json(silent=True) returns None if not payload is wrong
# todo INFO: pip install Flask-JWT for authentication
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    data = parser.parse_args()

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item["name"] == name:
        #         return item
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with name '{name}' already exist"}, 400

        data = Item.parser.parse_args()

        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x["name"] == name, items), None)

        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)  # debug+True helps to debug
