from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask_restful import Resource, reqparse

from src.users.models import User

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500
