from osa.exceptions.invalid_response import InvalidResponse
from osa.exceptions.osa_server_exception import OsaServerException


def request_until_success(fn, max_attempts: int):
    """
    Makes requests by calling input function.
    On error, retries until valid response is received.
    :param fn: Request function to call
    :param max_attempts: Maximum number of times to attempt calling fn
    :return: Valid response from fn
    :raises:
        InvalidResponse - raised if no valid response is received from fn
        after maxAttempts
    """

    for i in range(0, max_attempts):
        try:
            return fn()
        except OsaServerException as e:
            print(str(e))
            print(f"Attempt {i + 1} to call {fn} failed.")

    raise InvalidResponse(f"Failed to get valid response from {fn} after "
                          f"{max_attempts} attempts.")
