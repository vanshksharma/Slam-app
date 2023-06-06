from rest_framework.test import APIClient, APITestCase


class ProjectTest(APITestCase):
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
            'name':'Test Project',
            'lead':self.lead_id,
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
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01'
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.task_id=response.json()['data']['id']

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
            'name':'Test Project',
            'lead':self.lead_id_diff,
            'contact':self.contact_id_diff,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project_id_diff=response.json()['data']['id']
    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_project_without_login(self):
        client=APIClient()
        response = client.get('/projects/project')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_get_project_with_login(self):
        response = self.client.get('/projects/project')
        self.assertEqual(response.status_code, 200)
    
    # ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_project_without_login(self):
        client=APIClient()
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_project_with_login(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_project_invalid_lead(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id_diff,
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Lead does not belong to the user')
    
    def test_post_project_invalid_lead_id(self):
        data={
            'name':'Test Project',
            'lead':'invalid_id',
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Lead ID')
    
    def test_post_project_invalid_priority(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'priority':'invalid_priority',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Priority Provided')
    
    def test_post_project_invalid_status(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'status':'invalid_status',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Status Provided')
    
    def test_post_project_invalid_dates_1(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2019-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Due date cannot be before Start date')
    
    def test_post_project_invalid_dates_2(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'invalid date',
            'due_date':'2019-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Start date or Due date provided')
    
    def test_post_project_invalid_dates_3(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'invalid date',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Start date or Due date provided')
    
    def test_post_project_no_dates(self):
        data={
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'description':'This is a test project',
            'status':'invalid_status',
            'value':9000
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_project_no_login(self):
        client=APIClient()
        data={
            'project':self.project_id,
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_put_project_invalid_project(self):
        data={
            'project':self.project_id_diff,
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The project does not belong to the user')
    
    def test_put_project_invalid_project_id(self):
        data={
            'project':'invalid_id',
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Project ID')
        
    def test_put_project_no_project(self):
        data={
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Project ID provided')
    
    def test_put_project_invalid_lead(self):
        data={
            'project':self.project_id,
            'lead':self.lead_id_diff,
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Lead does not belong to the user')
    
    def test_put_project_invalid_lead_id(self):
        data={
            'project':self.project_id,
            'lead':"invalid",
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Lead ID')
    
    def test_put_project_invalid_priority(self):
        data={
            'project':self.project_id,
            'priority':'inavlid',
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Priority Provided')
    
    def test_put_project_invalid_status(self):
        data={
            'project':self.project_id,
            'status':'invalid',
            'name':'Test Project',
            'description':'This is a test project'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Status Provided')
    
    def test_put_project_complete_before_tasks(self):
        data={
            'project':self.project_id,
            'status':'Complete'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Complete all the tasks before marking the project as Complete')
    
    def test_project_put_invalid_start_date_1(self):
        data={
            'project':self.project_id,
            'start_date':'2023-01-01'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Project Start date cannot be after Due Date')
    
    def test_project_put_invalid_start_date_2(self):
        data={
            'project':self.project_id,
            'start_date':'2020-05-01'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Project contains Tasks with start date before the start date of Project')

    def test_project_put_invalid_start_date_3(self):
        data={
            'project':self.project_id,
            'start_date':'invalid'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Start date provided')
    
    def test_project_put_invalid_due_date_1(self):
        data={
            'project':self.project_id,
            'due_date':'2019-01-01'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Project Due date cannot be before Start date')
    
    def test_project_put_invalid_due_date_2(self):
        data={
            'project':self.project_id,
            'due_date':'2020-11-01'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Project contains Tasks with Due date after the Due date of Project')
    
    def test_project_put_invalid_due_date_3(self):
        data={
            'project':self.project_id,
            'due_date':'invalid'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Due date provided')
    
    def test_project_put_invalid_dates_1(self):
        data={
            'project':self.project_id,
            'start_date':'2020-05-05',
            'due_date':'2020-11-11'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Project contains Tasks with Due date after the Due date of Project or with Start date before the Start date of Project')
        
    def test_project_put_invalid_dates_2(self):
        data={
            'project':self.project_id,
            'start_date':'2020-05-05',
            'due_date':'2020-01-11'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Due date cannot be before Start date')
    
    def test_project_put_invalid_dates_3(self):
        data={
            'project':self.project_id,
            'start_date':'invalid',
            'due_date':'2020-01-11'
        }
        response = self.client.put('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Start date or Due date provided')
    
    def check_null_after_lead_deletion(self):
        data={
            'lead':self.lead_id
        }
        response = self.client.delete('/pipeline/lead', data, format='json')
        self.assertEqual(response.status_code,200)
        
        response = self.client.get('/projects/project')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['lead'], None)
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_project_with_invalid_project_id(self):
        data={
            'project':self.project_id_diff,
        }
        response = self.client.delete('/projects/project', data, format='json')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.json()['Error'], 'The project does not belong to the user')
    
    def test_delete_project_valid(self):
        data={
            'project':self.project_id,
        }
        response = self.client.delete('/projects/project', data, format='json')
        self.assertEqual(response.status_code,200)


class TaskTest(APITestCase):
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
            'name':'Test Project',
            'lead':self.lead_id,
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
            'name':'Test Project',
            'lead':self.lead_id,
            'contact':self.contact_id,
            'status':'complete',
            'description':'This is a test project',
            'value':9000,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/project', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project_id_complete=response.json()['data']['id']
        
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01'
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.task_id=response.json()['data']['id']

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
            'name':'Test Project',
            'lead':self.lead_id_diff,
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
            'name':'test_task',
            'project':self.project_id_diff,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01'
        }
        response = client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.task_id_diff=response.json()['data']['id']

    
    # ------------------------------------------- GET Test Started -----------------------------------------------------
    def test_get_task_without_login(self):
        client=APIClient()
        response = client.get('/projects/task')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_get_task_with_login(self):
        response = self.client.get('/projects/task')
        self.assertEqual(response.status_code, 200)
    
    # ------------------------------------------- POST Test Started -----------------------------------------------------
    def test_post_task_without_login(self):
        client=APIClient()
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01'
        }
        response = client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_post_task_with_login(self):
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01'
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_task_invalid_status(self):
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
            'status':'INVALID'
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Status Provided')
    
    def test_post_task_invalid_priority(self):
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
            'priority':'INVALID'
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Priority Provided')
    
    def test_post_task_invalid_dates_1(self):
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2019-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Task Start date cannot be before Project Start date')
    
    def test_post_task_invalid_dates_2(self):
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2022-01-01',
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Task Due date cannot be after Project Due date')
    
    def test_post_task_invalid_dates_3(self):
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'2020-01-01',
            'due_date':'2019-01-01',
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Due date cannot be before Start date')
    
    def test_post_task_invalid_dates_4(self):
        data={
            'name':'test_task',
            'project':self.project_id,
            'start_date':'inavlid',
            'due_date':'2019-01-01',
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Start date or Due date provided')
    
    def test_post_task_no_dates(self):
        data={
            'name':'test_task',
            'project':self.project_id,
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_post_task_completed_project(self):
        data={
            'name':'test_task',
            'project':self.project_id_complete,
            'start_date':'2020-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.post('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Cannot add task to an already completed project')
    
    # ------------------------------------------- PUT Test Started -----------------------------------------------------
    def test_put_task_no_login(self):
        client=APIClient()
        data={
            'task':self.task_id,
            'name':'Test task',
            'description':'This is a test task'
        }
        response = client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
    
    def test_put_task_invalid_task(self):
        data={
            'task':self.task_id_diff,
            'name':'Test task',
            'description':'This is a test task'
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'The Task does not belong to the user')
    
    def test_put_task_invalid_task_id(self):
        data={
            'task':'invalid',
            'name':'Test task',
            'description':'This is a test task'
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Please Enter Valid Task ID')
    
    def test_put_task_no_task(self):
        data={
            'name':'Test task',
            'description':'This is a test task'
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'No Task ID provided')
    
    def test_put_task_invalid_status(self):
        data={
            'task':self.task_id,
            'status':'INVALID'
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Status Provided')
    
    def test_put_task_invalid_priority(self):
        data={
            'task':self.task_id,
            'priority':'INVALID'
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Priority Provided')
    
    def test_put_task_invalid_start_date_1(self):
        data={
            'task':self.task_id,
            'start_date':'2019-01-01',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Task Start date cannot be before Project Start date')
    
    def test_put_task_invalid_start_date_2(self):
        data={
            'task':self.task_id,
            'start_date':'2021-05-05',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Task Start date cannot be after Due date')
    
    def test_put_task_invalid_start_date_3(self):
        data={
            'task':self.task_id,
            'start_date':'invalid',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Start date provided')
    
    def test_put_task_invalid_due_date_1(self):
        data={
            'task':self.task_id,
            'due_date':'2022-01-01',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Task Due date cannot be after Project Due date')
    
    def test_put_task_invalid_due_date_2(self):
        data={
            'task':self.task_id,
            'due_date':'2019-01-01',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Task Due date cannot be before Start date')
    
    def test_put_task_invalid_due_date_3(self):
        data={
            'task':self.task_id,
            'due_date':'invalid',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Invalid Due date provided')
    
    def test_put_task_invalid_dates_1(self):
        data={
            'task':self.task_id,
            'start_date':'2019-01-01',
            'due_date':'2021-01-01',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'], 'Task Start date cannot be before Project Start date')
    
    def test_put_task_invalid_dates_2(self):
        data={
            'task':self.task_id,
            'start_date':'2020-01-01',
            'due_date':'2022-01-01',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'],'Task Due date cannot be after Project Due date')
    
    def test_put_task_invalid_dates_3(self):
        data={
            'task':self.task_id,
            'start_date':'2020-05-05',
            'due_date':'2019-01-01',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'],'Due date cannot be before Start date')
    
    def test_put_task_invalid_dates_4(self):
        data={
            'task':self.task_id,
            'start_date':'invalid',
            'due_date':'invalid',
        }
        response = self.client.put('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['Error'],'Invalid Start date or Due date provided')
    
    # ------------------------------------------- DELETE Test Started -----------------------------------------------------
    def test_delete_task(self):
        data={
            'task':self.task_id,
        }
        response = self.client.delete('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_task_without_login(self):
        client=APIClient()
        data={
            'task':self.task_id,
        }
        response = client.delete('/projects/task', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Error'], 'Forbidden')
