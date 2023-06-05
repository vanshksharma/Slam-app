from rest_framework.test import APIClient, APITestCase
from datetime import date

class ContactTest(APITestCase):
    def setUp(self):
        data = {
            'username': 'test',
            'password': 'test',
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

    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_contact_with_login(self):
        response = self.client.get('/pipeline/contact')
        self.assertEqual(response.status_code, 200)
    
    def test_get_contact_without_login(self):
        client=APIClient()
        response = client.get('/pipeline/contact')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    # ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_contact_with_login(self):
        data = {
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'bssdfa@DSF.com'
        }
        response = self.client.post('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_contact_without_login(self):
        client=APIClient()
        data = {
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'sad@sf.com'
        }
        response = client.post('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_contact_with_login_invalid_contact_type(self):
        data = {
            'contact_type':'INVALID',
            'name':'Test Contact',
            'email':'sad@sd.com'
        }
        response = self.client.post('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Contact Type Provided')
    
    def test_post_contact_with_login_invalid_email(self):
        data = {
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'sad'
        }
        response = self.client.post('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_post_contact_with_login_duplicate_email_different_user(self):
        data = {
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'bssda@DSF.com'
        }
        response = self.client.post('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_contact_with_login_duplicate_email_same_user(self):
        data = {
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'bsfa@DSF.com'
        }
        response = self.client.post('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Contact with this email already exists')
    
    def test_post_contact_with_login_invalid_name(self):
        data = {
            'contact_type':'INDIVIDUAL',
            'name':'',
            'email':'sd@eg.com'
        }
        response = self.client.post('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_contact_valid(self):
        data = {
            'contact':self.contact_id,
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact',
            'email':'sg5@hgu.com'
        }
        response = self.client.put('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_put_contact_invalid(self):
        data = {
            'contact':self.contact_id_diff,
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact'
        }
        response = self.client.put('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Contact does not belong to the user')
    
    def test_put_contact_invalid_contact_id(self):
        data = {
            'contact':"INVALID",
            'contact_type':'INDIVIDUAL',
            'name':'Test Contact'
        }
        response = self.client.put('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Contact ID')
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_contact_invalid(self):
        data = {
            'contact':self.contact_id_diff
        }
        response = self.client.delete('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Contact does not belong to the user')
    
    def test_delete_contact_valid(self):
        data = {
            'contact':self.contact_id
        }
        response = self.client.delete('/pipeline/contact', data, format='json')
        self.assertEqual(response.status_code, 200)


class AddressTest(APITestCase):
    def setUp(self):
        data = {
            'username': 'test',
            'password': 'test',
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
        
        data = {
            'contact':self.contact_id,
            'street':"regeg",
            'city':"edgwsg",
            'state':"fdhth",
            "country":"fhdhh",
            'pincode':221006
        }
        response = self.client.post('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.address_id=response.json()['data']['id']

        #Adding a Contact from different user
        client=APIClient()
        data = {
            'username': 'test12',
            'password': 'test',
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
        
        data = {
            'contact':self.contact_id_diff,
            'street':"regeg",
            'city':"edgwsg",
            'state':"fdhth",
            "country":"fhdhh",
            'pincode':221002
        }
        response = client.post('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.address_id_diff=response.json()['data']['id']
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_address_with_login(self):
        response = self.client.get('/pipeline/address')
        self.assertEqual(response.status_code, 200)
    
    def test_get_address_without_login(self):
        client=APIClient()
        response = client.get('/pipeline/address')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    # ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_address_with_login(self):
        data = {
            'contact':self.contact_id,
            'street':"regeg",
            'city':"edgwsg",
            'state':"fdhth",
            "country":"fhdhh",
            'pincode':221006
        }
        response = self.client.post('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.address_id=response.json()['data']['id']
    
    def test_post_address_without_login(self):
        client=APIClient()
        data = {
            'contact':self.contact_id,
            'street':"regeg",
            'city':"edgwsg",
            'state':"fdhth",
            "country":"fhdhh",
            'pincode':221006
        }
        response = client.post('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_address_with_login_invalid_contact(self):
        data = {
            'contact':self.contact_id_diff,
            'street':"regeg",
            'city':"edgwsg",
            'state':"fdhth",
            "country":"fhdhh",
            'pincode':221006
        }
        response = self.client.post('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Contact does not belong to the user')
    
    def test_post_address_with_login_invalid_contact_id(self):
        data = {
            'contact':"invalid",
            'street':"regeg",
            'city':"edgwsg",
            'state':"fdhth",
            "country":"fhdhh",
            'pincode':221006
        }
        response = self.client.post('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Contact ID')
    
    def test_post_address_with_login_invalid_data(self):
        data = {
            'contact':self.contact_id,
            'street':"regeg",
            'state':"fdhth",
            "country":"fhdhh",
            'pincode':221006
        }
        response = self.client.post('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_address_with_invalid_address(self):
        data={
            'address':self.address_id_diff,
            'state':"MPPPP"
        }
        response = self.client.put('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.json()['Error'], 'The Address does not belong to the user')
    
    def test_put_address_with_invalid_address_id(self):
        data={
            'address':"dsgws",
            'state':"MPPPP"
        }
        response = self.client.put('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Address ID')
    
    def test_put_address_with_no_address_id(self):
        data={
            'state':"MPPPP"
        }
        response = self.client.put('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['Error'], 'No Address ID provided')
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_address_with_invalid_address_id(self):
        data={
            'address':self.address_id_diff,
        }
        response = self.client.delete('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.json()['Error'], 'The Address does not belong to the user')
    
    def test_delete_address_valid(self):
        data={
            'address':self.address_id
        }
        response = self.client.delete('/pipeline/address', data, format='json')
        self.assertEqual(response.status_code,200)
    

class LeadTest(APITestCase):
    def setUp(self):
        data = {
            'username': 'test',
            'password': 'test',
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
        
        data = {
            'contact':self.contact_id,
            'confidence':0.3
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.lead_id=response.json()['data']['id']

        #Adding a Contact from different user
        client=APIClient()
        data = {
            'username': 'test12',
            'password': 'test',
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
        
        data = {
            'contact':self.contact_id_diff,
            'confidence':0.6
        }
        response = client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.lead_id_diff=response.json()['data']['id']
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_lead_without_login(self):
        client=APIClient()
        response = client.get('/pipeline/lead')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_get_lead_with_login(self):
        response = self.client.get('/pipeline/lead')
        self.assertEqual(response.status_code, 200)
    
    # ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_lead_without_login(self):
        client=APIClient()
        data = {
            'contact':self.contact_id,
            'confidence':0.3
        }
        response = client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_lead_with_login_invalid_data(self):
        data = {
            'contact':self.contact_id,
            'confidence':"invalid"
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Confidence Level Provided')
    
    def test_post_lead_with_login_invalid_confidence_level(self):
        data = {
            'contact':self.contact_id,
            'confidence':2
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Confidence must be between 0 and 1')
    
    def test_post_lead_invalid_stage(self):
        data = {
            'contact':self.contact_id,
            'confidence':0.3,
            'stage':"invalid"
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Stage Provided')
    
    def test_post_lead_with_login_with_closing_date(self):
        data = {
            'stage':"Opportunity",
            'contact':self.contact_id,
            'confidence':0.3,
            'closing_date':"2021-03-03"
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Only leads in Closed Won or Closed Lost stage can be provided a closing date')
    
    def test_post_lead_with_login_with_amount(self):
        data = {
            'stage':"Opportunity",
            'contact':self.contact_id,
            'confidence':0.3,
            'amount':7000
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be provided for a Lead in Opportunity stage')
    
    def test_post_lead_with_login_with_closing_date(self):
        data = {
            'stage':"Contacted",
            'contact':self.contact_id,
            'confidence':0.3,
            'closing_date':"2021-03-03"
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Only leads in Closed Won or Closed Lost stage can be provided a closing date')
    
    def test_post_lead_with_login_with_amount(self):
        data = {
            'stage':"Contacted",
            'contact':self.contact_id,
            'confidence':0.3
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be null for Contacted or Negotiation leads')
    
    def test_post_lead_with_login_with_no_amount(self):
        data = {
            'stage':"Closed_won",
            'contact':self.contact_id,
            'confidence':0.3
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be null for Closed Won leads')
    
    def test_post_lead_with_login_with_no_closing_date(self):
        data = {
            'stage':"Closed_won",
            'contact':self.contact_id,
            'confidence':0.3,
            'amount':7000
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['closing_date'], date.today().isoformat())
    
    def test_post_lead_with_login_with_closing_date(self):
        data = {
            'stage':"Closed_won",
            'contact':self.contact_id,
            'confidence':0.3,
            'amount':7000,
            'closing_date':'invalid'
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Enter Valid Closing Date')
    
    def test_post_lead_closing_date_without_stage(self):
        data = {
            'contact':self.contact_id,
            'confidence':0.3,
            'closing_date':"2021-03-03"
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Only leads in Closed Won or Closed Lost stage can be provided a closing date')
    
    def test_post_lead_amount_without_stage(self):
        data = {
            'contact':self.contact_id,
            'confidence':0.3,
            'amount':7000
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be provided for a Lead in Opportunity stage')
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_lead_without_login(self):
        client=APIClient()
        data = {
            'lead':self.lead_id,
            'confidence':0.3
        }
        response = client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_put_lead_invalid_lead(self):
        data = {
            'lead':self.lead_id_diff,
            'confidence':0.2
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Lead does not belong to the user')
    
    def test_put_lead_invalid_lead_id(self):
        data = {
            'lead':"invalid",
            'confidence':0.2
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Lead ID')
    
    def test_put_lead_invalid_no_lead(self):
        data = {
            'confidence':0.2
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Lead ID provided')
    
    def test_put_lead_invalid_stage(self):
        data = {
            'lead':self.lead_id,
            'confidence':0.3,
            'stage':"invalid"
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Stage Provided')
    
    def test_put_lead_valid(self):
        data = {
            'lead':self.lead_id,
            'stage':'opportunity'
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['amount'], None)
        self.assertEqual(response.json()['data']['closing_date'], None)
    
    def test_put_lead_with_amount(self):
        data = {
            'lead':self.lead_id,
            'stage':'opportunity',
            'amount':7000
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be provided for a Lead in Opportunity stage')
    
    def test_put_lead_with_closing_date(self):
        data = {
            'lead':self.lead_id,
            'stage':'opportunity',
            'closing_date':'2024-05-05'
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Only leads in Closed Won or Closed Lost stage can be provided a closing date')
    
    def test_put_lead_with_closing_date(self):
        data = {
            'lead':self.lead_id,
            'stage':'negotiation',
            'closing_date':'2024-05-05'
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Only leads in Closed Won or Closed Lost stage can be provided a closing date')
    
    def test_put_lead_with_no_amount(self):
        data = {
            'lead':self.lead_id,
            'stage':'negotiation'
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be null for Contacted or Negotiation leads')
    
    def test_put_lead_with_no_amount(self):
        data = {
            'lead':self.lead_id,
            'stage':'closed_won'
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be null for Closed Won leads')
    
    def test_put_lead_with_invalid_closing_date(self):
        data = {
            'lead':self.lead_id,
            'stage':'closed_won',
            'amount':7000,
            'closing_date':'invalid'
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Enter Valid Closing Date')
    
    def test_put_lead_valid(self):
        data = {
            'lead':self.lead_id,
            'stage':'closed_won',
            'amount':7000
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['closing_date'], date.today().isoformat())
    
    def test_put_lead_closing_date_no_stage(self):
        data = {
            'lead':self.lead_id,
            'closing_date':'2024-05-05'
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Only leads in Closed Won or Closed Lost stage can be provided a closing date')
    
    def test_put_lead_amount_no_stage(self):
        data = {
            'lead':self.lead_id,
            'amount':700000
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Amount cannot be provided for a Lead in Opportunity stage')
    
    def test_put_lead_invalid_confidence(self):
        data = {
            'lead':self.lead_id,
            'confidence':"invalid"
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Confidence Level Provided')
    
    def test_put_lead_invalid_confidence_level(self):
        data = {
            'lead':self.lead_id,
            'confidence':9
        }
        response = self.client.put('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Confidence must be between 0 and 1')
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_lead_with_invalid_lead_id(self):
        data={
            'lead':self.lead_id_diff,
        }
        response = self.client.delete('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.json()['Error'], 'The Lead does not belong to the user')
    
    def test_delete_lead_valid(self):
        data={
            'lead':self.lead_id
        }
        response = self.client.delete('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code,200)
    