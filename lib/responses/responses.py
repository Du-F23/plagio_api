from rest_framework import status
from rest_framework.response import Response


class BadResponse(Response):
    def __init__(self, data=None, **kwargs):
        kwargs.setdefault("status", status.HTTP_400_BAD_REQUEST)
        super().__init__(data=data or {"message": "Bad Request"}, **kwargs)

class InternalServerResponse(Response):
    def __init__(self, data=None, **kwargs):
        kwargs.setdefault("status", status.HTTP_500_INTERNAL_SERVER_ERROR)
        super().__init__(data=data or {"message": "Internal server error"}, **kwargs)

class NoContentResponse(Response):
    def __init__(self, data=None, **kwargs):
        kwargs.setdefault("status", status.HTTP_204_NO_CONTENT)
        super().__init__(data=data or {"message": "No content"}, **kwargs)