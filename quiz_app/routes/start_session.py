import uuid
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime
from flask_jwt_extended import jwt_required
from quiz_app.repo.session import SessionRepo
from quiz_app.utils import session_collection

start_session_bp = Blueprint('start_session_bp', __name__)

@start_session_bp.route('/session', methods=['GET'])
@jwt_required()
def start_session():
    duration = request.args.get('duration')
    jwt_content = getattr(request, 'jwt_content')

    user_id = jwt_content['sub']

    if user_id is None:
        return jsonify({'message': 'Invalid user'}), 400

    active_session = SessionRepo.find_active_by_user_id(user_id)

    if active_session is not None:
            response = make_response('')
            response.headers['X-Session-Id'] = active_session['session_id']

            return response, 201

    session = SessionRepo.create_session(user_id, duration)

    response = make_response('')
    response.headers['X-Session-Id'] = session['session_id']

    return jsonify({
         "created_at": session['created_at'],
         "expires_at": session['expires_at'],
    }), 201
