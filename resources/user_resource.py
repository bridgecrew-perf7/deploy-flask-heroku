from flask_restful import Resource, reqparse

from models.user_model import UserModel


class UserRegistrationResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="'username' is a mandatory field to register a user."
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="'password' is a mandatory field to register a user."
    )

    def post(self):
        data = UserRegistrationResource.parser.parse_args()
        if UserModel.find_user_by_username(data['username']):
            return {"message": "User with that username {} already exists.".format(data['username'])}, 400

        try:
            UserModel(**data).save_to_db()
        except:
            return {"message": "Failed to register the user."}, 500

        return {"message": "Successfully registered the user."}, 200
