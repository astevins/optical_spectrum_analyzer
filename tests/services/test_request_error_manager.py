import unittest
from unittest.mock import Mock

from osa.exceptions.response_timeout import ResponseTimeout
from osa.services.request_error_manager import *


class RequestUntilSuccessTests(unittest.TestCase):
    def test_valid_response(self):
        return_value = 'some value'
        fn = Mock(return_value=return_value)

        try:
            response = request_until_success(fn, 5)
        except InvalidResponse:
            self.fail("Error raised for valid function response.")

        self.assertEqual(response, return_value)

    def test_valid_response_after_failures(self):
        return_value = 'some value'
        fn = Mock()
        fn.side_effect = [InvalidResponse('invalid'), ResponseTimeout('invalid'), return_value]

        try:
            response = request_until_success(fn, 5)
        except InvalidResponse:
            self.fail("Error raised for valid function response.")

        self.assertEqual(response, return_value)

    def test_always_invalid_response(self):
        fn = Mock(side_effect=ResponseTimeout('timeout'))
        try:
            request_until_success(fn, 5)
        except InvalidResponse as e:
            self.assertIsNotNone(str(e))
            return

        self.fail("No error thrown for function that continuously fails.")


if __name__ == "__main__":
    unittest.main()