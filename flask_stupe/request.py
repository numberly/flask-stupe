from flask import Request as FlaskRequest


class Request(FlaskRequest):

    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)

        #: Store additionnal data about the request.
        self.metadata = {}
        self.response_headers = {}


__all__ = ["Request"]
