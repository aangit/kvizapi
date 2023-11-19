from flask import Blueprint, request
import requests
from quiz_app.repo.user import UserRepo

from quiz_app.services.google import exchange_tokens, get_user_info
from quiz_app.utils.jwt import generat_jwt

oauth_bp = Blueprint('oauth_bp', __name__)

@oauth_bp.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')

    access_token = exchange_tokens(code)

    user_info = get_user_info(access_token)

    UserRepo.upsert_user(user_info)

    return {
        "id": user_info['id'],
        "name": user_info['name'],
        "picture": user_info['picture'],
        "token": generat_jwt(user_info)
    }

