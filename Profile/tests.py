from rest_framework.test import APITestCase, APIClient


class ProfileTest(APITestCase):
    def setUp(self):
        data = {
            'username': 'test',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'asfdas@sfas.com'
        }
        self.client.post('/auth/signup', data, format='json')
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_profile_with_login(self):
        response = self.client.get('/profile/profile')
        self.assertEqual(response.status_code, 200)
    
    def test_get_profile_without_login(self):
        client=APIClient()
        response = client.get('/profile/profile')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_profile_with_login(self):
        data={
            'legal_name': 'test',
            'entity': 'test',
            'country': 'test',
            'state': 'test',
            'currency': 'test',
            'timezone': 'Asia/Dubai',
            'address': 'test',
            'city': 'test',
            'pincode': 123456,
            'phone_no': '+919876543210'
        }
        response=self.client.put('/profile/profile', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_put_profile_invalid_phone_no(self):
        data={
            'legal_name': 'test',
            'entity': 'test',
            'country': 'test',
            'state': 'test',
            'currency': 'test',
            'timezone': 'Asia/Kolkata',
            'address': 'test',
            'city': 'test',
            'pincode': 123456,
            'phone_no': '9876543210'
        }
        response=self.client.put('/profile/profile', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_put_profile_invalid_timezone(self):
        data={
            'legal_name': 'test',
            'entity': 'test',
            'country': 'test',
            'state': 'test',
            'currency': 'test',
            'timezone': 'Asia/Dubai1',
            'address': 'test',
            'city': 'test',
            'pincode': 123456,
            'phone_no': '+919876543210'
        }
        response=self.client.put('/profile/profile', data, format='json')
        self.assertEqual(response.status_code, 400)


class AccountTest(APITestCase):
    def setUp(self):
        data = {
            'username': 'test',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'asfdas@sfas.com'
        }
        self.client.post('/auth/signup', data, format='json')
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_account_with_login(self):
        response = self.client.get('/profile/account')
        self.assertEqual(response.status_code, 200)
    
    def test_get_account_without_login(self):
        client=APIClient()
        response = client.get('/profile/account')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_account_with_username(self):
        data={
            'username':'test'
        }
        response = self.client.put('/profile/account', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Username cannot be changed more than once')
    
    def test_put_account_with_email(self):
        data={
            'email':'test@test.com'
        }
        response = self.client.put('/profile/account', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Email cannot be changed')
    
    def test_put_account_with_first_name(self):
        data={
            'first_name':'test'
        }
        response = self.client.put('/profile/account', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'First name cannot be changed more than once')
    
    def test_put_account_with_last_name(self):
        data={
            'last_name':'test'
        }
        response = self.client.put('/profile/account', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Last name cannot be changed more than once')
    
    def test_put_account_with_password(self):
        data={
            'password':'test'
        }
        response = self.client.put('/profile/account', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_without_login(self):
        client=APIClient()
        response=client.delete('/profile/account')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_delete_valid(self):
        response=self.client.delete('/profile/account')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Message'], 'Account deleted successfully')
        self.assertTrue(response.cookies['JWT_TOKEN'].value == '')