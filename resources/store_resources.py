from flask_restful import Resource, reqparse
from models.store_model import StoreModel


class StoreResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Store name is a mandatory field."
    )

    def get(self, name):
        store = StoreModel.get_store_by_name(name)
        return store.json()

    def post(self, name):
        if StoreModel.get_store_by_name(name):
            return {"message": f"store with name {name} already exists"}, 400

        data = StoreResource.parser.parse_args()
        store = StoreModel(**data)
        try:
            store.save_to_db()
            return {"message": "Successfully saved the store."}
        except:
            return {"message": f"Failed to store information for the store {name}"}, 500

    def delete(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {"message": f"Failed while deleting the store {name} from db."}, 500

        return {"message": f"Successfully deleted the store {name} from db."}


class StoresResource(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}