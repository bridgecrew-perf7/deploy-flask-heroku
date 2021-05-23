from models.user_model import UserModel


def authenticate(username, password):
    user = UserModel.find_user_by_username(username)
    if user:
        if user.password == password:
            return user


def identity(payload):
    user_id = payload["identity"]
    if UserModel.find_user_by_id(user_id):
        return user_id
