from flask import Request as FlaskRequest


class Request(FlaskRequest):

    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)

        #: Store additionnal data about the request.
        self.metadata = {}


__all__ = ["Request"]
