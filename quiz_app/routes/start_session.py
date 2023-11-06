import uuid
from flask import Blueprint, make_response
from datetime import datetime
from quiz_app.utils import session_collection

start_session_bp = Blueprint('start_session_bp', __name__)

@start_session_bp.route('/session', methods=['GET'])
def start_session():

    session_id = str(uuid.uuid4())

    payload = {
        'session_id': session_id,
        'created_at': datetime.now().isoformat(),
        'is_active': True
    }

    session_collection.insert_one(payload)

    response = make_response('')
    response.headers['X-Session-Id'] = session_id

    return response, 201
