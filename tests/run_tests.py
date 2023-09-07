import helpers
helpers.modify_system_path()

import unittest
from tests.test_authentication import TestAuthentication
from tests.test_yelp import TestYelp
from tests.test_spotify import TestSpotify


if __name__ == '__main__':
    unittest.main()

# Note: to run on command line: 
# $ python3 run_tests.py -v
# $ python3 run_tests.py TestAuthentication -v
# $ python3 run_tests.py TestYelp -v
# $ python3 run_tests.py TestSpotify -v
