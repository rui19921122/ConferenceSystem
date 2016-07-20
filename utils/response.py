from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


class ErrorResponse(Response):
    def __init__(self, error: str, status_code=HTTP_400_BAD_REQUEST):
        super(ErrorResponse, self).__init__(
            data={'error': error},status=status_code
        )
