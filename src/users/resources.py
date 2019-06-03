from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from flask_restful import Resource, reqparse

from src.users.models import User, RevokedTokenModel

parser = reqparse.RequestParser()
HELP_MESSAGE = 'This field cannot be blank'
parser.add_argument('username', help=HELP_MESSAGE, required=True)
parser.add_argument('password', help=HELP_MESSAGE, required=True)
parser.add_argument('name', help=HELP_MESSAGE, required=True)
parser.add_argument('surname', help=HELP_MESSAGE, required=True)
parser.add_argument('email', help=HELP_MESSAGE, required=True)

sign_in_parser = reqparse.RequestParser()
sign_in_parser.add_argument('username', help=HELP_MESSAGE)
sign_in_parser.add_argument('email', help=HELP_MESSAGE)
sign_in_parser.add_argument('password', help=HELP_MESSAGE)


class UserSignUp(Resource):
    def post(self):
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password']),
            name=data['name'],
            surname=data['surname'],
            email=data['email']
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


class UserSignIn(Resource):
    def post(self):
        data = sign_in_parser.parse_args()
        if data.get('username') and data.get('email'):
            return {'message': 'use username or email not both at the same time to sign in'}
        elif data.get('username'):
            current_user = User.find_by_username(data['username'])
        elif data.get('email'):
            current_user = User.find_by_email(data['email'])
        else:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=(data.get('username') or data.get('email')))
            refresh_token = create_refresh_token(identity=(data.get('username') or data.get('email')))
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()
