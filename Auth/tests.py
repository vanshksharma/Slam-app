from rest_framework.test import APITestCase, APIClient


class SignupTest(APITestCase):
    def test_signup_without_email(self):
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post('/auth/signup', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_signup_without_username(self):
        data = {
            'password': 'test',
            'email': 'ssa@zv.com'
        }
        response = self.client.post('/auth/signup', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid form data')
    
    def test_signup_without_password(self):
        data = {
            'username': 'test',
            'email': 'cascs@sda.com'
        }
        response = self.client.post('/auth/signup', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid form data')
    
    def test_signup_without_first_name(self):
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'saf78a@ds.com'
        }
        response = self.client.post('/auth/signup', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid form data')
    
    def test_signup_without_last_name(self):
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'dfh65@fhj.com'
        }
        response = self.client.post('/auth/signup', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid form data')
    
    def test_signup_with_valid_data(self):
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'dfadf@dfad.com',
            'first_name': 'test',
            'last_name': 'test'
        }
        response = self.client.post('/auth/signup', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Message'], 'Signup Successful')
        self.assertTrue(response.cookies.get('JWT_TOKEN', None).value is not None)


class LoginTest(APITestCase):
    # First create a user
    def setUp(self) -> None:
        data = {
            'username': 'test',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'dfadf@dfad.com'
        }
        self.client.post('/auth/signup', data, format='json')
        
    def test_login_without_username(self):
        data = {
            'password': 'test'
        }
        response = self.client.post('/auth/login', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid Username/Password')
    
    def test_login_without_password(self):
        data = {
            'username': 'test'
        }
        response = self.client.post('/auth/login', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid Username/Password')
    
    def test_login_with_invalid_username(self):
        data = {
            'username': 'test123',
            'password': 'test'
        }
        response = self.client.post('/auth/login', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid Username/Password')
    
    def test_login_with_invalid_password(self):
        data = {
            'username': 'test',
            'password': 'test123'
        }
        response = self.client.post('/auth/login', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid Username/Password')
    
    def test_login_with_invalid_password_and_username(self):
        data = {
            'username': 'test123',
            'password': 'test123'
        }
        response = self.client.post('/auth/login', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid Username/Password')
    
    def test_login_with_valid_data(self):
        data = {
            'username': 'test',
            'password': 'test'
        }
        client=APIClient()
        response = client.post('/auth/login', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Message'], 'Login Successful')
        self.assertTrue(response.cookies.get('JWT_TOKEN', None).value is not None)
    
    def test_add_contact_valid_token_no_user(self):
        client=APIClient()
        client.cookies['JWT_TOKEN'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Nn0.zBdutOvncGUTYYWZkc9pit5ps90LO1kz1WFtLloSNxI'
        data = {
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'bssda@DSF.com'
        }
        response=client.post('/pipeline/contact',data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['Error'], 'User Does not Exist')
    

class LogoutTest(APITestCase):
    def setUp(self) -> None:
        data = {
            'username': 'test',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'dfadf@dfad.com'
        }
        self.client.post('/auth/signup', data, format='json')
    
    def test_logout_without_login(self):
        client=APIClient()
        response=client.post('/auth/logout')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_logout_invalid_token(self):
        client=APIClient()
        client.cookies['JWT_TOKEN'] = "abcd"
        response=client.post('/auth/logout')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Invalid Token')
    
    def test_logout_valid(self):
        response=self.client.post('/auth/logout')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Message'], 'Logout Successful')
        self.assertTrue(response.cookies['JWT_TOKEN'].value == '')