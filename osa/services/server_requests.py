import json
import math
from typing import Dict, Union

import requests

from osa.config import API_URL
from osa.exceptions.invalid_response import InvalidResponse
from osa.exceptions.response_timeout import ResponseTimeout


def get_trace() -> Dict[str, Union[float, str, list[float]]]:
    """
    Requests trace data from osa server.
    Converts x_increment to nanometers and returns x_units as nm
    """

    print("Requesting trace.")

    try:
        trace_res = requests.get(API_URL + 'TRACE', timeout=1).json()
    except requests.exceptions.Timeout:
        raise ResponseTimeout("TRACE request timed out.")
    except:
        raise InvalidResponse("Invalid response to TRACE request.")

    x_increment_nm = trace_res['xincrement'] * math.pow(10, 9)

    try:
        print("Returning trace.")
        return {'time': trace_res['timestamp'],
                'instrument': trace_res['instrument_object'],
                'x_label': trace_res['xlabel'],
                'x_increment': x_increment_nm,
                'x_units': 'nm',
                'y_label': 'dBm',
                'data': trace_res['ydata']}
    except KeyError:
        raise InvalidResponse("Missing data in response to TRACE request.")


def get_x_lims() -> list[int]:
    """
    Requests x limits from OSA server
    :return: List of two integers: [start, stop] x limits in nm
    """

    try:
        res = requests.get(API_URL + 'LIM', timeout=2)
    except requests.exceptions.Timeout:
        raise ResponseTimeout("LIM request timed out.")

    try:
        return __parse_lim__(res.text)
    except:
        raise (InvalidResponse("Invalid response to LIM request."))


def __parse_lim__(s: str) -> list[float]:
    return eval(__remove_console_prefix__(s))


def __remove_console_prefix__(s: str):
    return s.replace('+READY>', '', 1)
