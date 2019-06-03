from flask_jwt_extended import jwt_required
from flask_restful import Resource


class Index(Resource):
    def get(self):
        return "Hello World"


class GetSecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
