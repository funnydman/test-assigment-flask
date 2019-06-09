import base64
import csv
import io
import os
from datetime import datetime

import flask
import pdfkit
import requests
from flask import render_template, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.constants import required_msg

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
    @property
    def parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file_content', help=required_msg, required=True)
        return parser

    def post(self):
        data = self.parser.parse_args()
        try:
            decoded = base64.b64decode(data['file_content'])
        except Exception as e:
            return {"message": "Unable to decode content"}, 500

        filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".csv"
        with open(os.path.join(FOLDER_TO_SAVE, filename), "w") as f:
            f.write(decoded.decode())
        return {'message': 'File was decoded and saved'}


class ExternalAPI(Resource):
    @jwt_required
    def get(self):
        data = requests.get('https://restcountries.eu/rest/v2/all')
        return {i['name']: i['population'] for i in data.json()}


class ExternalCSV(Resource):
    @jwt_required
    def get(self):
        buffer = io.StringIO()

        keys = ('name', 'capital', 'region', 'lat', 'long', 'population', 'alpha3Code')

        writer = csv.DictWriter(buffer, keys)
        writer.writeheader()

        data = requests.get('https://restcountries.eu/rest/v2/all')
        for line in data.json():
            latlng = line.get('latlng')
            if latlng:
                line['lat'] = line['latlng'][0]
                line['long'] = line['latlng'][1]
            writer.writerow({k: v for k, v in line.items() if k in keys})

        resp = flask.make_response(buffer.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=population.csv"
        resp.headers["Content-type"] = "text/csv"

        return resp


class ExternalPDF(Resource):
    @jwt_required
    def get(self):
        keys = ('name', 'capital', 'region', 'lat', 'long', 'population', 'alpha3Code')
        parsed = []
        buffer = io.StringIO()
        data = requests.get('https://restcountries.eu/rest/v2/all')
        for line in data.json():
            latlng = line.get('latlng')
            if latlng:
                line['lat'] = line['latlng'][0]
                line['long'] = line['latlng'][1]
            parsed.append({k: v for k, v in line.items() if k in keys})
        # TODO: beatify formatting
        res = render_template('to_pdf.html', parsed=parsed)
        pdf = pdfkit.from_string(res, buffer.getvalue())
        resp = Response(pdf)
        resp.headers["Content-Disposition"] = "attachment; filename=countries.pdf"
        resp.headers["Content-type"] = "application/pdf"

        return resp
