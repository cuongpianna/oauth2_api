from flask import request
from werkzeug.security import safe_str_cmp
from flask_restful import Resource
from flask_jwt_extended import create_refresh_token, create_access_token, fresh_jwt_required, jwt_required

from app.user.models import UserModel
from app.user.schemas import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        print(user_json)
        # user = user_schema.load(user_json)
        user = user_schema.make_instance(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": "A user with that username already exists."}, 400
        user.save_to_db()
        return {"message": "Account created successfully."}, 201


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404

        return user_schema.dump(user).data, 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404

        user.delete_to_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        payload = request.get_json()
        user_data = user_schema.make_instance(payload)
        user = UserModel.find_by_username(user_schema.username)

        if user and user.password and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 401


class SetPassword(Resource):
    @classmethod
    @fresh_jwt_required
    def post(cls):
        payload = request.get_json()
        user_data = user_schema.make_instance(payload)
        user = UserModel.find_by_username(user_data.username)

        if not user:
            return {"message": "User not found."}, 400

        user.password = user_data.password
        user.save_to_db()

        return {"message": "User password updated successfully."}, 201

