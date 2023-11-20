import datetime
import os
from flask import jsonify
import jwt

jwt_secret = os.environ.get("JWT_SECRET")

if jwt_secret is None:
    raise ValueError ("jwt_secret is not available")


def generat_jwt(user_info):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=6)

    token = jwt.encode(
        {
            "email": user_info['email'],
            "id": user_info['id'],
            "exp": expiration_time
        },
        jwt_secret,
        algorithm='HS256'
    )

    return token
