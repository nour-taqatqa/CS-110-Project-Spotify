import helpers
helpers.modify_system_path()

import unittest
from apis import authentication
import time
# from unittest.mock import MagicMock

class TestAuthentication(unittest.TestCase):

    def test_token(self):
        self.assertEqual(authentication.API_TUTOR_TOKEN, 'API.fda8c628-f8f0-448d-aad8-42c2fcd067ec')

    def test_get_key(self):
        yelp_key = authentication.get_token('https://www.apitutor.org/yelp/key')
        self.assertEqual(len(yelp_key), 128)
        time.sleep(1.0)
        spotify_key = authentication.get_token('https://www.apitutor.org/spotify/key')
        self.assertEqual(len(spotify_key), 144)
        time.sleep(1.0)

    # def test_malformed_query_yields_errors(self):
    #     with self.assertRaises(Exception) as cm:
    #         authentication.get_token('https://www.apitutor.org/yelp/ke')
    #     self.assertIn(
    #         'This URL is invalid: https://www.apitutor.org/yelp/ke', str(cm.exception)
    #     )
    #     time.sleep(1.0)
    #     with self.assertRaises(Exception) as cm:
    #         authentication.get_token('https://www.apitutor.org/spotify/ke')
    #     self.assertIn(
    #         'This URL is invalid: https://www.apitutor.org/spotify/ke', str(cm.exception)
    #     )

if __name__ == '__main__':
    unittest.main()