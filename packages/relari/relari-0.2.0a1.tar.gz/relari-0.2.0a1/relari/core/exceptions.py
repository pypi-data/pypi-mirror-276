class APIError(Exception):
    def __init__(self, message: str, response):
        body = response.json()
        msg = f"{message}: {body['detail']}" if "detail" in body else message
        super().__init__(msg)