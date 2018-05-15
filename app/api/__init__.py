from flask import Blueprint

status = Blueprint('status', __name__)

# Load all API files after creating Blueprint
api_files = ['statuses']

for api_file in api_files:
    __import__('app.api.{}'.format(api_file))