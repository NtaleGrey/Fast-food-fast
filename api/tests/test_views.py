from app import app
import unittest
import json


class TestCase(unittest.TestCase):

    def setUp(self):
        self.orders = {
            "order": "1 chicken wing",
            "location": "Ntinda",
            "comment": "Just...Give me my money's worth",
            "price": 3000,
            "delivery_time": "20:45"

        }
        self.update = {
            "order": "3 chicken wings",
            "location": "Bukoto",
            "Comment": "Want it deep fried",
            "price": 8000,
            "delivery_time": "19:45"
        }
        self.incomplete = {
            "order": "pilawo",
            "location": "Nakawa",
            "price": 3000,
        }
        self.client = app.test_client(self)

    def tearDown(self):
        self.orders.clear()
        self.incomplete.clear()

    def test_index_route_response(self):
        '''Tests the index route's response data'''
        res = self.client.get('api/v1/', content_type='application/json')
        self.assertTrue(b'Welcome to Fast-food-fast' in res.data)
        self.assertEqual(res.status_code, 200)

    def test_post_method_response(self):
        '''This tests for the post method's response data'''
        res = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.orders),
            content_type='application/json')
        self.assertTrue(b'New order created' in res.data)
        self.assertEqual(res.status_code, 201)

    def test_post_method_invalid_content_type_response(self):
        '''This tests for the response when content type other than json is
         entered'''
        res = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.orders),
            content_type='text/plain')
        self.assertTrue(b'Invalid Content Type' in res.data)
        self.assertEqual(res.status_code, 406)

    def test_post_method_missing_fields(self):
        res = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.incomplete),
            content_type='application/json')
        self.assertTrue(b'Missing field/s' in res.data)
        self.assertEqual(res.status_code, 400)

    def test_get_all_method(self):
        '''This tests the get_all method'''

        res = self.client.get('/api/v1/orders')
        self.assertEqual(res.status_code, 200)

    def test_get_one_method_response(self):
        '''This tests the get_one method response status code '''
        res = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.orders),
            content_type='application/json')

        res = self.client.get('/api/v1/orders/1')
        self.assertEqual(res.status_code, 200)

    def test_get_one_method_index_error(self):
        res = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.orders),
            content_type='application/json')

        res = self.client.get('/api/v1/orders/23')
        self.assertTrue(b'Not found!'in res.data)
        self.assertEqual(res.status_code, 404)

    def test_put_method_response(self):
        '''This tests the put method's response status code'''
        res = self.client.post(
            '/api/v1/orders',
            data=json.dumps(
                self.orders),
            content_type='application/json')

        res = self.client.put(
            '/api/v1/orders/1',
            data=json.dumps(
                self.update),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(b'Order Updated' in res.data)


if __name__ == '__main__':
    unittest.main()
