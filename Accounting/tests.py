from rest_framework.test import APITestCase, APIClient


class ProposalTest(APITestCase):
    def setUp(self):
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
        
        data = {
            'contact':self.contact_id,
            'confidence':0.3
        }
        response = self.client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.lead_id=response.json()['data']['id']
        
        data={
            'contact':self.contact_id,
            'amount':9000,
        }
        response=self.client.post('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.proposal_id=response.json()['data']['id']

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
        
        data = {
            'contact':self.contact_id_diff,
            'confidence':0.6
        }
        response = client.post('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.lead_id_diff=response.json()['data']['id']
        
        data={
            'contact':self.contact_id_diff,
            'amount':9000,
        }
        response=client.post('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.proposal_id_diff=response.json()['data']['id']
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_proposal_with_login(self):
        response=self.client.get('/accounting/proposal')
        self.assertEqual(response.status_code, 200)

    def test_get_proposal_without_login(self):
        client=APIClient()
        response=client.get('/accounting/proposal')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    # ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_proposal_with_login(self):
        data={
            'contact':self.contact_id,
            'amount':9000,
        }
        response=self.client.post('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_proposal_without_login(self):
        client=APIClient()
        data={
            'contact':self.contact_id,
            'amount':9000,
        }
        response=client.post('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_proposal_with_invalid_lead(self):
        data={
            'contact':self.contact_id,
            'lead':self.lead_id_diff,
            'amount':9000,
        }
        response=self.client.post('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Lead does not belong to the user')
    
    def test_post_proposal_with_invalid_lead_id(self):
        data={
            'contact':self.contact_id,
            'lead':'Invalid',
            'amount':9000,
        }
        response=self.client.post('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Lead ID')
    
    def test_post_proposal_with_no_amount(self):
        data={
            'contact':self.contact_id,
        }
        response=self.client.post('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_proposal_without_login(self):
        client=APIClient()
        data = {
            'proposal':self.proposal_id,
            'amount':3000
        }
        response = client.put('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_put_proposal_invalid_proposal(self):
        data = {
            'proposal':self.proposal_id_diff,
            'amount':3000
        }
        response = self.client.put('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Proposal does not belong to the user')
    
    def test_put_proposal_invalid_proposal_id(self):
        data = {
            'proposal':"invalid",
            'amount':3000
        }
        response = self.client.put('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Proposal ID')
    
    def test_put_proposal_invalid_no_proposal(self):
        data = {
            'confidence':0.2
        }
        response = self.client.put('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Proposal ID provided')
    
    def test_put_proposal_valid(self):
        data = {
            'proposal':self.proposal_id,
            'amount':3000
        }
        response = self.client.put('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_check_null_after_lead_delete(self):
        data={
            'lead':self.lead_id
        }
        response = self.client.delete('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code,200)
        response=self.client.get('/accounting/proposal')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'][0]['lead'], None)
        
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_proposal_without_login(self):
        client=APIClient()
        response = client.delete('/accounting/proposal', {'proposal':self.proposal_id}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_delete_proposal_valid(self):
        data={
            'proposal':self.proposal_id
        }
        response = self.client.delete('/accounting/proposal', data, format='json')
        self.assertEqual(response.status_code, 200)


class TestInvoice(APITestCase):
    def setUp(self):
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
        
        data={
            'name':'Test Project',
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project_id=response.json()['data']['id']
        
        data={
            'contact':self.contact_id,
            'amount':9000,
            'project':self.project_id,
        }
        response=self.client.post('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.invoice_id=response.json()['data']['id']

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
        
        data={
            'name':'Test Project',
            'contact':self.contact_id_diff,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project_id_diff=response.json()['data']['id']
        
        data={
            'contact':self.contact_id_diff,
            'amount':9000,
            'project':self.project_id_diff,
        }
        response=client.post('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.invoice_id_diff=response.json()['data']['id']
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_invoice_without_login(self):
        client=APIClient()
        response = client.get('/accounting/invoice')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_get_invoice_with_login(self):
        response = self.client.get('/accounting/invoice')
        self.assertEqual(response.status_code, 200)
    
    # ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_invoice_without_login(self):
        client=APIClient()
        data={
            'contact':self.contact_id,
            'amount':9000,
            'project':self.project_id,
        }
        response = client.post('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_invoice_with_login(self):
        data={
            'contact':self.contact_id,
            'amount':9000,
            'project':self.project_id,
        }
        response=self.client.post('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_invoice_with_invalid_project(self):
        data={
            'contact':self.contact_id,
            'project':self.project_id_diff,
            'amount':9000,
        }
        response=self.client.post('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Project does not belong to the user')
    
    def test_post_invoice_with_invalid_project_id(self):
        data={
            'contact':self.contact_id,
            'project':'Invalid',
            'amount':9000,
        }
        response=self.client.post('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Project ID')
    
    def test_post_invoice_with_no_amount(self):
        data={
            'contact':self.contact_id,
        }
        response=self.client.post('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 400)
        
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_invoice_without_login(self):
        client=APIClient()
        data={
            'invoice':self.invoice_id,
            'amount':9000,
        }
        response = client.put('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_put_invoice_with_login(self):
        data={
            'invoice':self.invoice_id,
            'amount':9000,
        }
        response=self.client.put('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_put_invoice_with_invalid_invoice(self):
        data={
            'invoice':self.invoice_id_diff,
            'amount':9000,
        }
        response=self.client.put('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Invoice does not belong to the user')
    
    def test_put_invoice_no_invoice(self):
        data={
            'amount':9000,
        }
        response=self.client.put('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Invoice ID provided')
    
    def test_put_invoice_with_invalid_invoice_id(self):
        data={
            'invoice':'Invalid',
            'amount':9000,
        }
        response=self.client.put('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Invoice ID')
    
    def test_check_null_after_project_delete(self):
        data={
            'project':self.project_id,
        }
        response = self.client.delete('/projects/project', data, format='json')
        self.assertEqual(response.status_code,200)
        
        response=self.client.get('/accounting/invoice')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'][0]['project'], None)
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_invoice_without_login(self):
        client=APIClient()
        data={
            'invoice':self.invoice_id,
        }
        response = client.delete('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_delete_invoice_with_login(self):
        data={
            'invoice':self.invoice_id,
        }
        response=self.client.delete('/accounting/invoice', data, format='json')
        self.assertEqual(response.status_code, 200)
        

class PaymentTest(APITestCase):
    def setUp(self):
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
        
        data={
            'name':'Test Project',
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project_id=response.json()['data']['id']
        
        data={
            'contact':self.contact_id,
            'amount_received':9000,
            'project':self.project_id,
        }
        response=self.client.post('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.payment_id=response.json()['data']['id']

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
        
        data={
            'name':'Test Project',
            'contact':self.contact_id_diff,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project_id_diff=response.json()['data']['id']
        
        data={
            'contact':self.contact_id_diff,
            'amount_received':9000,
            'project':self.project_id_diff,
        }
        response=client.post('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.payment_id_diff=response.json()['data']['id']
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_payment_without_login(self):
        client=APIClient()
        response = client.get('/accounting/payment')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_get_payment_with_login(self):
        response=self.client.get('/accounting/payment')
        self.assertEqual(response.status_code, 200)
    
    #- ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_payment_without_login(self):
        client=APIClient()
        data={
            'contact':self.contact_id,
            'amount_received':9000,
            'project':self.project_id,
        }
        response = client.post('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
        
    def test_post_payment_with_login(self):
        data={
            'contact':self.contact_id,
            'amount_received':9000,
            'project':self.project_id,
        }
        response=self.client.post('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_payment_with_invalid_project(self):
        data={
            'contact':self.contact_id,
            'project':self.project_id_diff,
            'amount_received':9000,
        }
        response=self.client.post('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Project does not belong to the user')
    
    def test_post_payment_with_invalid_project_id(self):
        data={
            'contact':self.contact_id,
            'project':'Invalid',
            'amount_received':9000,
        }
        response=self.client.post('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Project ID')
    
    def test_post_payment_with_no_amount(self):
        data={
            'contact':self.contact_id,
        }
        response=self.client.post('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_payment_without_login(self):
        client=APIClient()
        data={
            'payment':self.payment_id,
            'amount_received':9000,
        }
        response = client.put('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_put_payment_with_login(self):
        data={
            'payment':self.payment_id,
            'amount_received':9000,
        }
        response=self.client.put('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_put_payment_with_invalid_payment(self):
        data={
            'payment':self.payment_id_diff,
            'amount_received':9000,
        }
        response=self.client.put('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Payment does not belong to the user')
    
    def test_put_payment_with_invalid_payment_id(self):
        data={
            'payment':'Invalid',
            'amount_received':9000,
        }
        response=self.client.put('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Payment ID')
    
    def test_put_payment_no_payment(self):
        data={
            'amount_received':9000,
        }
        response=self.client.put('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Payment ID provided')
    
    def test_check_null_after_project_delete(self):
        data={
            'project':self.project_id,
        }
        response = self.client.delete('/projects/project', data, format='json')
        self.assertEqual(response.status_code,200)
        
        response=self.client.get('/accounting/payment')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'][0]['project'], None)
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_payment_without_login(self):
        client=APIClient()
        data={
            'payment':self.payment_id,
        }
        response = client.delete('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_delete_payment_with_login(self):
        data={
            'payment':self.payment_id,
        }
        response=self.client.delete('/accounting/payment', data, format='json')
        self.assertEqual(response.status_code, 200)
    