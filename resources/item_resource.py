from flask_restful import Resource, reqparse
from models.item_model import ItemModels
from flask_jwt import jwt_required


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="The price field cannot be missing in the request."
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="The 'store_id' is a mandatory field for every item."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModels.find_item_by_name(name)
        if item:
            return item.json()
        return {"message": f"The product with {name} is not found."}, 404

    def post(self, name):
        item = ItemModels.find_item_by_name(name)
        if item:
            return {"message": f"A product with {name} already exists."}, 400

        data = ItemResource.parser.parse_args()
        new_item = ItemModels(name, **data)

        try:
            new_item.save_to_db()
        except:
            return {"message": f"Failed to add the request to database.."}, 500
        return new_item.json(), 201

    def delete(self, name):
        item = ItemModels.find_item_by_name(name)
        if item:
            try:
                item.delete()
                return {"message": f"Successfully deleted the product {name}."}
            except:
                return {"message": f"Failed to delete the item to database.."}, 500

        return {"message": f"A product with {name} does not exist."}, 400

    def put(self, name):
        data = ItemResource.parser.parse_args()
        item = ItemModels.find_item_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModels(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": f"Failed while adding the item {name}."}

        return item.json()


class ItemsResource(Resource):
    def get(self):
        items = list(map(lambda item: item.json(), ItemModels.find_all_items()))
        return {"items": items}

