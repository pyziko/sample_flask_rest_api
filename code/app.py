from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


# no need for jsonify as flask_restful does the conversion for us
# todo INFO: next gives us the first item (can be called multiple times to gives the next and next ...)
# todo INFO: None included with next ensures that if no more items, it returns None
# todo INFO: request.get_json(force=True) ignores the header and formats body to json
# todo INFO: request.get_json(silent=True) returns None if not payload is wrong
# todo INFO: pip install Flask-JWT for authentication
class Item(Resource):
    def get(self, name):
        # for item in items:
        #     if item["name"] == name:
        #         return item
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with name '{name}' already exist"}, 400

        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)  # debug+True helps to debug
