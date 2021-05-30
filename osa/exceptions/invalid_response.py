from osa.exceptions.osa_server_exception import OsaServerException


class InvalidResponse(OsaServerException):
    """
    Raised when request to OSA server results in invalid response
    """
    pass
