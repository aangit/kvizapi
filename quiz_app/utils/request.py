from flask import jsonify
import requests


def safe_request(method, url, **kwargs):
    response = requests.request(method, url, **kwargs)

    response.raise_for_status()

    return response.json()

def handle_request_errors():
    try:
        pass

    except requests.HTTPError as http_err:
        if http_err.response.status_code == 404:
            error_response = jsonify({'error': 'Not found'})
            error_response.status_code = 404
        else:
            error_response = jsonify({'error': 'Internal Server Error'})
            error_response.status_code = 500
        return error_response
