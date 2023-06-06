from rest_framework.test import APITestCase, APIClient


class EventTest(APITestCase):
    def setUp(self) -> None:
        data = {
            'username': 'test',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'asfdas@sfas.com'
        }
        self.client.post('/auth/signup', data, format='json')
        
        #Adding a Contact
        data={
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'bsfa@DSF.com'
        }
        response=self.client.post('/pipeline/contact', data, format='json')
        self.contact_id=response.json()['data']['id']

        #Adding a Contact from different user
        client=APIClient()
        data = {
            'username': 'test12',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'as@sfas.com'
        }
        client.post('/auth/signup', data, format='json')
        data={
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'bssda@DSF.com'
        }
        response=client.post('/pipeline/contact', data, format='json')
        self.contact_id_diff=response.json()['data']['id']
    
    def test_get_event_without_login(self):
        client=APIClient()
        response = client.get('/calender/event')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_get_event_with_login(self):
        response = self.client.get('/calender/event')
        self.assertEqual(response.status_code, 200)
    
    def test_post_event_without_login(self):
        client=APIClient()
        response = client.post('/calender/event')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_event_with_login_without_contact(self):
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'date': '2021-01-01',
            'status': 'COMPLETE'
        }
        response = self.client.post('/calender/event', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Contact ID provided')
    
    def test_post_event_with_login_without_contact(self):
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'date': '2021-01-01',
            'status': 'COMPLETE'
        }
        response = self.client.post('/calender/event', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Contact ID provided')
    
    def test_post_event_with_login_with_wrong_contact(self):
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'contact':"helo",
            'date': '2021-01-01',
            'status': 'COMPLETE'
        }
        response = self.client.post('/calender/event', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Contact ID')
    
    
    
    def test_post_event_with_login_with_different_user_contact(self):
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'contact':self.contact_id_diff,
            'date': '2021-01-01',
            'status': 'COMPLETE'
        }
        response = self.client.post('/calender/event', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Contact does not belong to the user')
    
    def test_post_event_wrong_status(self):
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'contact':self.contact_id,
            'date': '2021-01-01',
            'status': 'COMPLETED'
        }
        response = self.client.post('/calender/event', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Status Provided')
    
    def test_post_event_valid(self):
        data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'contact':self.contact_id,
            'date': '2021-01-01',
            'status': 'COMPLETE'
        }
        response = self.client.post('/calender/event', data, format='json')
        self.assertEqual(response.status_code, 200)
