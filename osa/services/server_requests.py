import json
from typing import Dict, Union

import requests

from osa.config import API_URL
from osa.exceptions.invalid_response import InvalidResponse
from osa.exceptions.response_timeout import ResponseTimeout


def get_trace() -> Dict[str, Union[int, str]]:
    """
    Requests trace data from osa server.
    """

    print("Requesting trace.")

    try:
        trace_res = requests.get(API_URL + 'TRACE', timeout=1).json()
    except requests.exceptions.Timeout:
        raise ResponseTimeout("TRACE request timed out.")
    except:
        raise InvalidResponse("Invalid response to TRACE request.")

    print(trace_res)
    try:
        print("Returning trace.")
        return {'time': trace_res['timestamp'],
                'instrument': trace_res['instrument_object'],
                'x_label': trace_res['xlabel'],
                'x_increment': trace_res['xincrement'],
                'x_units': trace_res['xunits'],
                'y_label': 'dBm',
                'data': trace_res['ydata']}
    except KeyError:
        raise InvalidResponse("Missing data in response to TRACE request.")
