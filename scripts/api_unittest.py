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

    ''' Retrieve the annotated webpage
    '''
    def test_1_annotations(self):
        r = requests.get(self.server_url+'api/annotations?link=Sagrada_Fam%C3%ADlia')
        self.assertEqual(r.status_code, 401)

    def test_2_annotations(self):
        r = requests.get(self.server_url+'api/annotations?link=Antoni_Gaud%C3%AD ')
        self.assertEqual(r.status_code, 401)

    def test_3_annotations(self):
        r = requests.get(self.server_url+'api/annotations?after=2014-02-04 15:57:58.046908&before=2014-04-06 10:08:16.213186')
        self.assertEqual(r.status_code, 401)


    def test_4_annotations(self):
        r = requests.get(self.server_url+'api/annotations/00000000-0000-0000-0000-000000000022 ')
        self.assertEqual(r.status_code, 400)


    def test_5_annotations(self):
        r = requests.get(self.server_url+'api/annotations/00000000-0000-0000-0000-000000000022/targets ')
        self.assertEqual(r.status_code, 400)

    def test_6_annotations(self):
        r = requests.get(self.server_url+'api/annotations/00000000-0000-0000-0000-000000000022/permissions')
        self.assertEqual(r.status_code, 401)


        
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


