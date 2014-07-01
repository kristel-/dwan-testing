'''
Usage: python api_unittest.py -v
'''
import unittest
import requests
from xml2json import Xml2Json
from requests.auth import HTTPBasicAuth

class DWANApiTests(unittest.TestCase):
    server_url = 'http://lux17.mpi.nl/ds/webannotator-basic/' # for non-shibboleth users
    user = 'unittest'
    pwd  = 'unittest4API2dwan'
    user_id = ''
    s = requests.Session()

    def setUp(self):
        pass

    ''' Tests for LOGIN
    '''

    def test_00_not_login_state(self):
        '''
        API should return 401 when user is not authenticated
        '''
        r = requests.get(self.server_url+'api/authentication/principal')
        self.assertEqual(r.status_code, 401)

    def test_01_do_nsh_login(self):
        r = self.s.get(self.server_url+'api/authentication/login')
        payload = {'username': self.user, 'password': self.pwd}
        r = self.s.post(self.server_url+'j_spring_security_check', data=payload)
        self.assertEqual(r.status_code, 200)

    def test_02_login_state(self):
        r = self.s.get(self.server_url+'api/authentication/principal')
        data = Xml2Json(r.text).result
        self.user_id = data['principal'][1]['xml:id']
        self.assertEqual(r.status_code, 200)

    ''' Place for the specific tests
    '''
        
    ''' Tests for LOGOUT
    '''

    def test_zy_do_logout(self):
        r = self.s.get(self.server_url+'api/authentication/logout')
        self.assertEqual(r.status_code, 200)

    def test_zz_not_login_state_after_logout(self):
        '''
        API should return 401 when user is not authenticated
        '''
        r = self.s.get(self.server_url+'api/authentication/principal')
        self.assertEqual(r.status_code, 401)
        self.user_id = ''

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
