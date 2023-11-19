from quiz_app.utils.env import EnvVar
from quiz_app.utils.request import safe_request

client_id = EnvVar.google_client_id()
client_secret = EnvVar.google_client_secret()


def exchange_tokens(code):
    token_url = 'https://accounts.google.com/o/oauth2/token'
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code'
    }

    response = safe_request('post', token_url, data=data)

    return response['access_token']

def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    return safe_request('get', 'https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)


