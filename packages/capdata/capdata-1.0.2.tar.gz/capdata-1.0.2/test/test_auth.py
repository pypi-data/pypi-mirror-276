import unittest
import data.token as auth


class TestAuthFunctions(unittest.TestCase):
    def test_get_token(self):
        token = auth.get_token("xxxx", "xxxx")
        print(token)
