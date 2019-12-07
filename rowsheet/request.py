import base64
import json
from termcolor import cprint

class RequestRoute:

    def __init__(self, djangoRequest):

        url = djangoRequest.path.strip("/")
        path  = url.split("/")
        if len(path) < 5:
            raise Exception("Invalid djangoRequest route.")

        self.version = path[1]
        self.user_group = path[2]
        self.module = path[3]
        self.command = path[4]
        self.method = djangoRequest.method

class RequestAuthorization:

    def __init__(self, djangoRequest):

        auth_header = djangoRequest.META.get('HTTP_AUTHORIZATION')
        cprint(auth_header, "blue")

        if auth_header is None:
            self.authorization = False
            self.username = None
            self.password = None
            return

        # Remove "Basic " to isolate credentials.
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')

        # Remove the square brackets around username.
        self.authorization: True
        self.username = decoded_credentials[0][1:-1]
        self.password = decoded_credentials[1]

class Request:

    #---------------------------------------------------------------------------
    # Request has 3 parts:
    #   1) Route
    #   2) Args
    #   3) Authorization
    #---------------------------------------------------------------------------

    def __init__(self, djangoRequest):

        try:
            self.args = self.parse_args(djangoRequest)
        except Exception as ex:
            msg = "Unparsable Args:"
            cprint(msg + str(ex), "red")
            raise Exception(msg)

        try:
            self.route = RequestRoute(djangoRequest)
        except Exception as ex:
            msg = "Unparsable Route: "
            cprint(msg + str(ex), "red")
            raise Exception(msg)

        try:
            self.auth = RequestAuthorization(djangoRequest)
        except Exception as ex:
            msg = "Unparsable Authorization:"
            cprint(msg + str(ex), "red")
            raise Exception(msg)

    #---------------------------------------------------------------------------
    # A less shitty way of parsing simple fucking arguments from common wasy:
    #
    #   1) JSON     encoded     POST
    #   2) FORM     encoded     POST
    #   3) URL      encoded     GET
    #
    # Thanks for the bullshit, Django!
    #---------------------------------------------------------------------------

    def parse_args(self, djangoRequest):
        args = {}
        if djangoRequest.content_type == "application/json":
            args = json.loads(djangoRequest.body.decode('utf-8'))
        if djangoRequest.content_type == "application/x-www-form-urlencoded":
            if djangoRequest.method == "POST":
                args = { key : val for key, val in djangoRequest.POST.items()}
        if djangoRequest.content_type == "text/plain":
            if djangoRequest.method == "GET":
                args = { key : val for key, val in djangoRequest.GET.items()}
        return args
