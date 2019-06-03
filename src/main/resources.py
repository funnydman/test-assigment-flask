import base64
import os

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
HELP_MESSAGE = 'This field cannot be blank'
parser.add_argument('file_content', help=HELP_MESSAGE, required=True)
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
FOLDER_TO_SAVE = os.path.join(BASE_DIR, 'csv')


class Index(Resource):
    def get(self):
        return "Hello World"


class UploadCSVFile(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            decoded = base64.b64decode(data['file_content'])
        except:
            return {"message": "Unable to decode content"}, 500
        filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".csv"
        with open(os.path.join(FOLDER_TO_SAVE, filename), "w") as f:
            f.write(decoded.decode())
        return {'message': 'File was decoded and saved'}
