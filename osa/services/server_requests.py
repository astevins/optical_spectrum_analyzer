import json
import math
from typing import Dict, Union

import requests

from osa.config import API_URL
from osa.exceptions.invalid_response import InvalidResponse
from osa.exceptions.response_timeout import ResponseTimeout


class TraceData:
    def __init__(self, data: list[float], time: str, instrument: str,
                 x_label: str, y_label: str,
                 x_units: str, x_increment: float):
        self.data = data
        self.time = time
        self.instrument = instrument
        self.x_label = x_label
        self.y_label = y_label
        self.x_units = x_units
        self.x_increment = x_increment


def get_trace() -> TraceData:
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
    time_formatted = __convert_to_iso_8601__(trace_res['timestamp'])

    try:
        return TraceData(data=trace_res['ydata'],
                         time=time_formatted,
                         instrument=trace_res['instrument_object'],
                         x_label=trace_res['xlabel'],
                         y_label='dBm',
                         x_increment=x_increment_nm,
                         x_units='nm')
    except KeyError:
        raise InvalidResponse("Missing data in response to TRACE request.")


def __convert_to_iso_8601__(date_and_time: str) -> str:
    """
    Converts date and time from OSA server to ISO 8601 format
    :param time: Date and time in format given by instrument
    :return: Date and time in ISO 8601 format
    """
    split = date_and_time.split(' ')
    date = split[0]
    time = split[1]

    date = '20' + date.replace('.', '-')
    time = time + 'Z'
    return date + 'T' + time

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
