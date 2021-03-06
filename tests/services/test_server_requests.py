import json
import sys
import unittest
import requests
from unittest.mock import Mock, patch

from osa.exceptions.invalid_response import InvalidResponse
from osa.exceptions.response_timeout import ResponseTimeout
from osa.services import server_requests


def load_test_json_response() -> json:
    with open('./data/small_trace_response.json') as f:
        return json.load(f)


class GetTraceTests(unittest.TestCase):
    def setUp(self):
        self.test_json_response = load_test_json_response()

    @patch('requests.get')
    def test_valid_response(self, mock_get):
        mock_get.return_value.json.return_value = self.test_json_response

        try:
            response = server_requests.get_trace()
        except:
            self.fail("Error thrown for valid request response.")

        self.assertGreater(len(response.data), 0)

    @patch('requests.get')
    def test_response_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        try:
            response = server_requests.get_trace()
        except ResponseTimeout as e:
            self.assertIsNotNone(str(e))
            return
        except Exception as e:
            self.fail(f"Wrong error thrown for trace request timeout: {e.__class__.__name__}")

        self.fail("No error thrown for trace request timeout")

    @patch('requests.get')
    def test_invalid_response(self, mock_get):
        mock_get.return_value = 'S8ehEak32JE3'

        try:
            response = server_requests.get_trace()
        except InvalidResponse as e:
            self.assertIsNotNone(str(e))
            return
        except Exception as e:
            self.fail(f"Wrong error thrown for invalid trace response: {e.__class__.__name__}")

        self.fail("No error thrown for invalid trace response")


class GetLimTests(unittest.TestCase):
    @patch('requests.get')
    def test_valid_response(self, mock_get):
        mock_get.return_value.text = "+READY>[1515, 1580]"

        try:
            response = server_requests.get_x_lims()
        except:
            self.fail("Error thrown for valid request response.")

        self.assertEqual(response, [1515, 1580])

    @patch('requests.get')
    def test_response_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        try:
            response = server_requests.get_x_lims()
        except ResponseTimeout as e:
            self.assertIsNotNone(str(e))
            return
        except Exception as e:
            self.fail(f"Wrong error thrown for lim request timeout: {e.__class__.__name__}")

        self.fail("No error thrown for lim request timeout")

    @patch('requests.get')
    def test_invalid_response(self, mock_get):
        mock_get.return_value = 'S8ehEak32JE3'

        try:
            response = server_requests.get_x_lims()
        except InvalidResponse as e:
            self.assertIsNotNone(str(e))
            return
        except Exception as e:
            self.fail(f"Wrong error thrown for invalid lim response: {e.__class__.__name__}")
            return

        self.fail("No error thrown for invalid lim response")


if __name__ == "__main__":
    unittest.main()
