import logging
from flask import make_response, jsonify
from app.db import db
from . import status


@status.route('', methods=['GET'])
def health():
    message = {
        'status': 'error',
        'message': {
            'Database': 'Down',
        }
    }
    status_code = 500

    try:
        db.engine.table_names()
        message['status'] = 'success'
        message['message']['Database'] = 'Up'
        status_code = 200
    except Exception as e:
        logging.exception(e)

    return make_response(jsonify(message), status_code)