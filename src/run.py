from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://selena:selena@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-data'

db = SQLAlchemy(app)

from src.users import models as users_models, resources as user_resources
from src.main import resources as main_resources


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

from src.main import cli

app.cli.add_command(cli.drop_db)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return users_models.RevokedTokenModel.is_jti_blacklisted(jti)


API_VERSION = '/api/v1'

api.add_resource(user_resources.UserSignUp, f'{API_VERSION}/signup')
api.add_resource(user_resources.UserSignIn, f'{API_VERSION}/signin')
api.add_resource(user_resources.UserLogoutAccess, f'{API_VERSION}/signout')
api.add_resource(user_resources.UserLogoutRefresh, f'{API_VERSION}/signout/refresh')
api.add_resource(user_resources.TokenRefresh, f'{API_VERSION}/token/refresh')
api.add_resource(user_resources.AllUsers, f'{API_VERSION}/users')
api.add_resource(main_resources.UploadCSVFile, f'{API_VERSION}/upload')

api.add_resource(main_resources.Index, '/')

if __name__ == '__main__':
    app.run()
