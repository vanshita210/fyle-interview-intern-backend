from flask import Response, jsonify, make_response

class APIResponse(Response):
    def __init__(self, data=None, error=None):
        super().__init__()
        self.data = data
        self.error = error

    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))

