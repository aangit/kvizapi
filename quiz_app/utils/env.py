import os


class EnvVar():
    @staticmethod
    def google_client_id():
        client_id = os.environ.get("GOOGLE_CLIENT_ID")

        if client_id is None:
            raise ValueError ("GOOGLE_CLIENT_ID is required")

    @staticmethod
    def google_client_secret():
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

        if client_secret is None:
            raise ValueError ("GOOGLE_CLIENT_SECRET is required")
