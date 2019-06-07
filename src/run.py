from src.app import db, app, api, jwt
from src.main import resources as main_resources, cli
from src.users import models as users_models
from src.users import resources as user_resources

app.cli.add_command(cli.drop_db)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return users_models.RevokedTokenModel.is_jti_blacklisted(jti)


API_VERSION = '/api/v1'

API_URL = f"http://127.0.0.1:5000{API_VERSION}"

api.add_resource(main_resources.Index, '/')
api.add_resource(main_resources.UploadCSVFile, f'{API_VERSION}/upload')
api.add_resource(main_resources.ExternalAPI, f'{API_VERSION}/countries/population')
api.add_resource(main_resources.ExternalCSV, f'{API_VERSION}/countries/csv')
api.add_resource(main_resources.ExternalPDF, f'{API_VERSION}/countries/pdf')

api.add_resource(user_resources.UserSignUp, f'{API_VERSION}/signup')
api.add_resource(user_resources.UserSignIn, f'{API_VERSION}/signin')
api.add_resource(user_resources.UserLogoutAccess, f'{API_VERSION}/signout')
api.add_resource(user_resources.UserLogoutRefresh, f'{API_VERSION}/signout/refresh')
api.add_resource(user_resources.TokenRefresh, f'{API_VERSION}/token/refresh')
api.add_resource(user_resources.AllUsers, f'{API_VERSION}/users')
