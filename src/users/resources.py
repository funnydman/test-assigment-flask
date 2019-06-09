from logging import getLogger

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from flask_restful import Resource, reqparse

from src.users.models import User, RevokedTokenModel

logger = getLogger(__name__)


class UserSignUp(Resource):
    @property
    def parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('surname', required=True)
        parser.add_argument('email', required=True)
        return parser

    def post(self):
        data = self.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': f"User {data['username']} already exists"}, 409

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
                       'message': f"User {data['username']} was created",
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 201
        except Exception as e:
            logger.error(e)
            return {'message': 'Something went wrong'}, 500


class UserSignIn(Resource):
    @property
    def parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('password', required=True)
        return parser

    def post(self):
        data = self.parser.parse_args()
        current_user = None
        if data.get('username') and data.get('email'):
            return {'message': 'Use username or email not both at the same time to sign in'}, 400
        elif data.get('username'):
            current_user = User.find_by_username(data['username'])
        elif data.get('email'):
            current_user = User.find_by_email(data['email'])

        if current_user is None:
            return {'message': "User does not exist"}, 404

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=(data.get('username') or data.get('email')))
            refresh_token = create_refresh_token(identity=(data.get('username') or data.get('email')))
            return {
                       'message': f'Logged in as {current_user.username}',
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200, {'Set-Cookie': 'access_token_cookie=' + access_token}
        else:
            return {'message': 'Wrong credentials'}, 400


class UserLogoutAccess(Resource):
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except Exception as e:
            logger.error(e)
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except Exception as e:
            logger.error(e)
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
