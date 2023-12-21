from datetime import datetime, timedelta
import os
from flask import request, jsonify
import jwt

jwt_secret = os.environ.get("JWT_SECRET")

if jwt_secret is None:
    raise ValueError ("jwt_secret is not available")


def generat_jwt(user_info):
    expiration_time = datetime.utcnow() + timedelta(hours=24)

    token = jwt.encode(
        {
            "email": user_info['email'],
            "sub": user_info['id'],
            "exp": expiration_time
        },
        jwt_secret,
        algorithm='HS256'
    )

    return token

def process_token():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):

        return jsonify({'message': 'Token is missing'}), 401

    token = token.split(' ')[1]
    try:
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])

        if 'exp' in decoded_token:
            token_exp = datetime.utcfromtimestamp(decoded_token['exp'])
            current_time = datetime.utcnow()
            if token_exp < current_time:
                return jsonify({'message': 'Token has expired'}), 401

        setattr(request, 'jwt_content', decoded_token)
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

    return None, None
