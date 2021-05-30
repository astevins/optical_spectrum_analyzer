from osa.exceptions.osa_server_exception import OsaServerException


class ResponseTimeout(OsaServerException):
    """
    Raised when request to OSA server times out
    """
    pass
