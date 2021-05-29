from typing import Dict, Union

import requests

from osa.config import API_URL

def get_trace() -> Dict[str, Union[int, str]]:
    '''
    Requests trace data from osa server.
    '''

    # TODO
    return {'time': '',
            'instrument': '',
            'x_label': '',
            'y_label': '',
            'x_increment': 0,
            'x_units': '',
            'data': []}
