import helpers
helpers.modify_system_path()

import unittest
from unittest.mock import MagicMock
import time
from apis import yelp

class TestYelp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.valid_argument_list = [
            dict(location='Tallahassee, FL'),
            dict(location='Tallahassee, FL', limit=5),
            dict(location='Berkeley, CA', term='italian'),
            dict(limit=8, term='chinese'),
            dict(term='italian'),
            dict(term='italian', sort_by='best_match'),
            dict(term='italian', sort_by='rating'),
            dict(term='italian', sort_by='distance'),
            dict(term='italian', sort_by='review_count'),
            dict(term='pho', categories='vietnamese,thai'),
            dict(term='italian', price='3,4,1'),
            dict(term='italian', price=1),
            dict(term='italian', price=2),
            dict(term='italian', price=3),
            dict(term='italian', price=4),
            dict(term='italian', open_now=True)
        ]
        super(TestYelp, self).__init__(*args, **kwargs)


    def test_get_categories(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Berkeley%2C+CA&limit=10&categories=vietnamese,thai'
        url = yelp._generate_business_search_url(location='Berkeley, CA', categories='vietnamese,thai')
        self.assertEqual(url, goal_url)
    
    def test_get_categories_fail(self):
        with self.assertRaises(Exception) as cm:
            yelp._generate_business_search_url(location='Berkeley, CA', categories='vietnamese,thai,awesomepizza,pho')
        self.assertEqual(
            '"awesomepizza" is not a valid category because it isn\'t in the yelp.get_categories() list. Please make sure that the following categories are valid (with a comma separating each of them): vietnamese,thai,awesomepizza,pho',
            str(cm.exception)
        )

    def test_get_categories_abridged(self):
        self.assertEqual(type(yelp.get_categories_abridged()), list)
        self.assertEqual(len(yelp.get_categories_abridged()), 20)

    def test_yelp_generate_business_search_url_location(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Berkeley%2C+CA&limit=10'
        url = yelp._generate_business_search_url(location='Berkeley, CA')
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Tallahassee%2C+FL&limit=10'
        url = yelp._generate_business_search_url(location='Tallahassee, FL')
        self.assertEqual(url, goal_url)

    def test_yelp_generate_business_search_url_limit(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Berkeley%2C+CA&limit=5'
        url = yelp._generate_business_search_url(location='Berkeley, CA', limit=5)
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=8'
        url = yelp._generate_business_search_url(limit=8)
        self.assertEqual(url, goal_url)

    def test_yelp_generate_business_search_url_term(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Berkeley%2C+CA&limit=10&term=italian'
        url = yelp._generate_business_search_url(location='Berkeley, CA', term='italian')
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=8&term=chinese'
        url = yelp._generate_business_search_url(limit=8, term='chinese')
        self.assertEqual(url, goal_url)

    def test_yelp_generate_business_search_url_categories(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=8&term=chinese&categories=thai,vietnamese'
        url = yelp._generate_business_search_url(limit=8, term='chinese', categories='thai,vietnamese')
        self.assertEqual(url, goal_url)

    def test_yelp_generate_business_search_url_categories_error(self):
        with self.assertRaises(Exception) as cm:
            yelp._generate_business_search_url(categories='blah,italian')
        error_message = '"blah" is not a valid category because it isn\'t in the yelp.get_categories() list. Please make sure that the following categories are valid (with a comma separating each of them): blah,italian'
        self.assertEqual(error_message, str(cm.exception))

    def test_yelp_generate_business_search_url_sort_by(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian'
        url = yelp._generate_business_search_url(term='italian')
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&sort_by=best_match'
        url = yelp._generate_business_search_url(term='italian', sort_by='best_match')
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&sort_by=rating'
        url = yelp._generate_business_search_url(term='italian', sort_by='rating')
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&sort_by=distance'
        url = yelp._generate_business_search_url(term='italian', sort_by='distance')
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&sort_by=review_count'
        url = yelp._generate_business_search_url(term='italian', sort_by='review_count')
        self.assertEqual(url, goal_url)

        with self.assertRaises(Exception) as cm:
            url = yelp._generate_business_search_url(term='italian', sort_by='price')
        self.assertIn(
            "price not in ['best_match', 'rating', 'review_count', 'distance']", str(cm.exception)
        )

    def test_yelp_generate_business_search_url_price_fail(self):
        with self.assertRaises(Exception) as cm:
            yelp._generate_business_search_url(term='italian', price='$$')
        error_message = "The price parameter can be 1, 2, 3, 4, or some comma-separated combination (e.g. 1,2,3). You used: $$"
        self.assertEqual(error_message, str(cm.exception))

        with self.assertRaises(Exception) as cm:
            yelp._generate_business_search_url(term='italian', price='3,4,5')
        error_message = "The price parameter can be 1, 2, 3, 4, or some comma-separated combination (e.g. 1,2,3). You used: 3,4,5"
        self.assertEqual(error_message, str(cm.exception))

        with self.assertRaises(Exception) as cm:
            yelp._generate_business_search_url(term='italian', price='0')
        error_message = "The price parameter can be 1, 2, 3, 4, or some comma-separated combination (e.g. 1,2,3). You used: 0"
        self.assertEqual(error_message, str(cm.exception))

    def test_yelp_generate_business_search_url_price_success(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&price=1,2,3,4'
        url = yelp._generate_business_search_url(term='italian', price='3,2,4,1')
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&price=1'
        url = yelp._generate_business_search_url(term='italian', price=1)
        self.assertEqual(url, goal_url)
        
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&price=2'
        url = yelp._generate_business_search_url(term='italian', price=2)
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&price=3'
        url = yelp._generate_business_search_url(term='italian', price=3)
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&price=4'
        url = yelp._generate_business_search_url(term='italian', price=4)
        self.assertEqual(url, goal_url)

    def test_yelp_generate_business_search_url_open_now(self):
        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian&open_now=true'
        url = yelp._generate_business_search_url(term='italian', open_now=1)
        self.assertEqual(url, goal_url)

        url = yelp._generate_business_search_url(term='italian', open_now=True)
        self.assertEqual(url, goal_url)

        goal_url = 'https://api.yelp.com/v3/businesses/search?location=Evanston%2C+IL&limit=10&term=italian'
        url = yelp._generate_business_search_url(term='italian', open_now=False)
        self.assertEqual(url, goal_url)
    
        url = yelp._generate_business_search_url(term='italian', open_now=0)
        self.assertEqual(url, goal_url)

    def test_execute_business_queries_simplified(self):
        for kwargs in self.valid_argument_list:
            results = yelp.get_businesses(**kwargs)
            self.assertEqual(type(results), list)
            self.assertGreaterEqual(len(results), 1)
            self.assertEqual(type(results[0]), dict)
            keys = set(results[0].keys())
            if 'price' in keys:
                keys.remove('price')
            self.assertSetEqual(keys, set([
                 'id', 'name', 'rating', 'image_url', 'display_address',
                 'coordinates', 'review_count', 'share_url', 'categories'
            ]))
            time.sleep(1.0)

    def test_execute_business_queries_just_one_simplified(self):
        kwargs = self.valid_argument_list[0]
        results = yelp.get_businesses(**kwargs)
        self.assertEqual(type(results), list)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(type(results[0]), dict)
        keys = set(results[0].keys())
        if 'price' in keys:
            keys.remove('price')
        self.assertSetEqual(keys, set([
                'id', 'name', 'rating', 'image_url', 'display_address',
                'coordinates', 'review_count', 'share_url', 'categories'
        ]))
        time.sleep(1.0)

    def test_execute_business_queries(self):
        for kwargs in self.valid_argument_list:
            results = yelp.get_businesses(simplify=False, **kwargs)
            self.assertEqual(type(results), dict)
            self.assertEqual(list(results.keys()), ['businesses', 'total', 'region'])
            time.sleep(1.0)

    def test_execute_review_query_simplified(self):
        reviews = yelp.get_reviews('0b6AU869xq6KXdK3NtVJnw')
        self.assertEqual(type(reviews), list)
        self.assertEqual(
            list(reviews[0].keys()), 
            ['id', 'rating', 'text', 'time_created', 'url']
        )
        time.sleep(1.0)

    def test_execute_review_query_error(self):
        with self.assertRaises(Exception) as cm: 
            yelp.get_reviews('XXX', simplify=False)
        error_message = 'This URL is invalid: https://api.yelp.com/v3/businesses/XXX/reviews'
        self.assertIn(error_message, str(cm.exception))
        time.sleep(1.0)

    def test_execute_review_query(self):
        reviews = yelp.get_reviews('0b6AU869xq6KXdK3NtVJnw', simplify=False)
        self.assertEqual(type(reviews), dict)
        self.assertEqual(
            list(reviews['reviews'][0].keys()), 
            ['id', 'url', 'text', 'rating', 'time_created', 'user']
        )
        time.sleep(1.0)

    def test_get_formatted_business_table(self):
        business = yelp.get_businesses()[0]
        reviews = yelp.get_reviews(business['id'])
        table_text = yelp.get_formatted_business_table(business, reviews, to_html=False)
        table_html = yelp.get_formatted_business_table(business, reviews, to_html=True)
        # print(table_text)
        # print(table_html)
        self.assertIn('------------------------------------------------------------------------\nKABUL HOUSE', table_text)
        
        self.assertIn('<h1>KABUL HOUSE</h1><table style="border-collapse: collapse; border: solid 1px #CCC;width:700px;">', table_html)
        time.sleep(1.0)


if __name__ == '__main__':
    unittest.main()