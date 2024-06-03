import unittest

from pyctapi.auth import Auth


class TestAuth(unittest.TestCase):
    
    def test_generate_sign_code(self):
        auth = Auth(sk='a', ak='b')
        data = auth.generate_sign_headers(query_params={'a': 1})
        self.assertIn('eop-date', data)
        self.assertIn('ctyun-eop-request-id', data)
        self.assertIn('Eop-Authorization', data)
        data = auth.generate_sign_headers(body_params={'a': 1})
        self.assertIn('eop-date', data)
        self.assertIn('ctyun-eop-request-id', data)
        self.assertIn('Eop-Authorization', data)


if __name__ == '__main__':
    unittest.main()
