<center><h1>Slam API Documentation</h1></center>

# Auth API

## Login (POST)
``` https://api.slamapp.co/auth/login ```

Body:
- username: required
- password: required

Command:
```
curl --location 'https://api.slamapp.co/auth/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"vansh123",
    "password":"9ismine.."
}'

```
A cookie will be set with the name "JWT_TOKEN" and the value will be the JWT token for the user.

<hr>
<br>

## Signup (POST)
``` https://api.slamapp.co/auth/signup ```

Body:
- username: required
- email: required
- password: required
- first_name: required
- last_name: required

Command:
```
curl --location 'https://api.slamapp.co/auth/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"vns.vansh123@gmail.com",
    "username":"vansh123",
    "password":"9ismine..",
    "first_name":"Vansh",
    "last_name":"Sharma"
}'
```
A cookie will be set with the name "JWT_TOKEN" and the value will be the JWT token for the user.

<hr>
<br>

## Logout (POST)
``` https://api.slamapp.co/auth/logout ```

Command:
```
curl --location --request POST 'https://api.slamapp.co/auth/logout' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'
```
The cookie with the name "JWT_TOKEN" will be deleted.

<hr>
<br>

# Pipeline API

## Get Contact (GET)
``` https://api.slamapp.co/pipeline/contact ```

Command:
```
curl --location 'https://api.slamapp.co/pipeline/contact' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'
```

<hr>
<br>

## Post Contact (POST)
``` https://api.slamapp.co/pipeline/contact ```

Body:
- name: required
- email: required
- contact_type: required (must be one of the following: "individual", "company")

Command:
```
curl --location 'https://api.slamapp.co/pipeline/contact' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data-raw '{
    "contact_type":"individual",
    "name":"Test_2",
    "email":"abcd@xyz.com"
}'
```

<hr>
<br>

## Put Contact (PUT)
``` https://api.slamapp.co/pipeline/contact ```

Body:
- contact: required
- name: optional
- email: optional
- contact_type: optional (must be one of the following: "individual", "company")
  
Command:
```
curl --location --request PUT 'https://api.slamapp.co/pipeline/contact' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data-raw '{
    "contact": 2,
    "email": "vnsfghs@vns.com"
}'
```

<hr>
<br>

## Delete Contact (DELETE)
``` https://api.slamapp.co/pipeline/contact ```

Body:
- contact: required

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/pipeline/contact' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "contact":2
}'
```

<hr>
<br>

## Get Address (GET)
``` https://api.slamapp.co/pipeline/address ```

Command:
```
curl --location 'https://api.slamapp.co/pipeline/address' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'
```

<hr>
<br>

## Post Address (POST)
``` https://api.slamapp.co/pipeline/address ```

Body:
- contact: required
- street: required
- city: required
- state: required
- country: required
- pincode: required

Command:
```
curl --location 'https://api.slamapp.co/pipeline/address' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "contact":1,
    "street":"ABCDefsc",
    "city":"hudsnscs",
    "state":"HUddhvd",
    "country":"INsfad",
    "pincode":221005
}'
```

<hr>
<br>

## Put Address (PUT)
``` https://api.slamapp.co/pipeline/address ```

Body:
- address: required
- street: optional
- city: optional
- state: optional
- country: optional
  
Command:
```
curl --location --request PUT 'https://api.slamapp.co/pipeline/address' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "address":1,
    "state":"UP",
    "country":"India"
}'
```

<hr>
<br>

## Delete Address (DELETE)
``` https://api.slamapp.co/pipeline/address ```

Body:
- address: required
  
Command:
```
curl --location --request DELETE 'https://api.slamapp.co/pipeline/address' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "address":1
}'
```

<hr>
<br>

## Get Lead (GET)
``` https://api.slamapp.co/pipeline/lead ```

Command:
```
curl --location 'https://api.slamapp.co/pipeline/lead' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'
```

<hr>
<br>

## Post Lead (POST)
``` https://api.slamapp.co/pipeline/lead ```

Body:
- contact: required
- amount: required ("contacted", "negotiation", "closed_won")
- stage: required (must be one of the following: "opportunity", "contacted", "negotiation", "closed_won", "closed_lost")
- confidence: required (must be between 0 and 1 inclusive)
- closing_date: required ("closed_won") (must be in the format YYYY-MM-DD)
- description: optional
  
Command:
```
curl --location 'https://api.slamapp.co/pipeline/lead' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "contact":1,
    "stage":"negotiation",
    "description":"test",
    "confidence":0.8,
    "amount":8000
}'
```

<hr>
<br>

## Put Lead (PUT)
``` https://api.slamapp.co/pipeline/lead ```

Body:
- lead: required
- amount: optional (required for "contacted", "negotiation", "closed_won")
- stage: optional (must be one of the following: "opportunity", "contacted", "negotiation", "closed_won", "closed_lost")
- confidence: optional (must be between 0 and 1 inclusive)
- closing_date: optional (required for "closed_won") (must be in the format YYYY-MM-DD)
- description: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/pipeline/lead' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "lead":1,
    "stage":"closed_won",
    "amount":8000

}'
```

<hr>
<br>

## Delete Lead (DELETE)
``` https://api.slamapp.co/pipeline/lead ```

Body:
- lead: required

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/pipeline/lead' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "lead":1
}'
```

<hr>
<br>

# Projects API

## Get Project (GET)
``` https://api.slamapp.co/projects/project ```

Command:
```
curl --location 'https://api.slamapp.co/projects/project' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'
```

<hr>
<br>

## Post Project (POST)
``` https://api.slamapp.co/projects/project ```

Body:
- name: required
- value: required
- contact: required
- priority: required (must be one of the following: "low", "medium", "high")
- start_date: required (must be in the format YYYY-MM-DD)
- due_date: required (must be in the format YYYY-MM-DD)
- status: required (must be one of the following: "incomplete", "complete")
- lead: optional

Command:
```
curl --location 'https://api.slamapp.co/projects/project' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "name":"test_project",
    "contact":1,
    "value":1000,
    "priority":"high",
    "start_date":"2023-05-29",
    "due_date":"2024-05-05",
    "status":"Incomplete"
}'
```

<hr>
<br>

## Put Project (PUT)
``` https://api.slamapp.co/projects/project ```

Body:
- project: required
- name: optional
- value: optional
- priority: optional (must be one of the following: "low", "medium", "high")
- start_date: optional (must be in the format YYYY-MM-DD)
- due_date: optional (must be in the format YYYY-MM-DD)
- status: optional (must be one of the following: "incomplete", "complete")
- lead: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/projects/project' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "project":1,
    "due_date":"2024-04-04"
}'
```

<hr>
<br>

## Delete Project (DELETE)
``` https://api.slamapp.co/projects/project ```

Body:
- project: required

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/projects/project' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "project":1
}'
```

<hr>
<br>

## Get Task (GET)
``` https://api.slamapp.co/projects/task ```

Command:
```
curl --location 'https://api.slamapp.co/projects/task' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'
```

<hr>
<br>

## Post Task (POST)
``` https://api.slamapp.co/projects/task ```

Body:
- name: required
- priority: required (must be one of the following: "low", "medium", "high")
- project: required
- status: required (must be one of the following: "incomplete", "complete")
- start_date: required (must be in the format YYYY-MM-DD)
- due_date: required (must be in the format YYYY-MM-DD)

**Task Start date and Due date must be between Project Start date and Due date**

Command:
```
curl --location 'https://api.slamapp.co/projects/task' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "name":"test_task",
    "priority":"low",
    "project":2,
    "status":"incomplete",
    "start_date":"2023-07-06",
    "due_date":"2023-08-06"
}'
```

<hr>
<br>

## Put Task (PUT)
``` https://api.slamapp.co/projects/task ```

Body:
- task: required
- name: optional
- priority: optional (must be one of the following: "low", "medium", "high")
- status: optional (must be one of the following: "incomplete", "complete")
- start_date: optional (must be in the format YYYY-MM-DD)
- due_date: optional (must be in the format YYYY-MM-DD)

**Task Start date and Due date must be between Project Start date and Due date**

Command:
```
curl --location --request PUT 'https://api.slamapp.co/projects/task' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "task":2,
    "start_date":"2023-08-06",
    "due_date":"2024-02-05"
}'
```

<hr>
<br>

## Delete Task (DELETE)
``` https://api.slamapp.co/projects/task ```

Body:
- task: required

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/projects/task' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "task":2
}'
```

<hr>
<br>

# Accounting API

## Get Invoice (GET)
``` https://api.slamapp.co/accounting/invoice ```

Command:
```
curl --location 'https://api.slamapp.co/accounting/invoice' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'

```

<hr>
<br>

## Post Invoice (POST)
``` https://api.slamapp.co/accounting/invoice ```

Body:
- contact: required
- amount: required
- date: required (must be in the format YYYY-MM-DD)
- project: optional
  
Command:
```
curl --location 'https://api.slamapp.co/accounting/invoice' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "contact":1,
    "amount":8000,
    "date":"2023-05-05"
}'

```

<hr>
<br>

## Put Invoice (PUT)
``` https://api.slamapp.co/accounting/invoice ```

Body:
- invoice: required
- amount: optional
- date: optional (must be in the format YYYY-MM-DD)
- project: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/accounting/invoice' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "invoice":1,
    "amount":9000,
    "date":"2024-05-06"
}'
```

<hr>
<br>

## Delete Invoice (DELETE)
``` https://api.slamapp.co/accounting/invoice ```

Body:
- invoice: required
  
Command:
```
curl --location --request DELETE 'https://api.slamapp.co/accounting/invoice' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "invoice":1
}'
```

<hr>
<br>

## Get Payment (GET)
``` https://api.slamapp.co/accounting/payment ```

Command:
```
curl --location 'https://api.slamapp.co/accounting/payment' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'

```

<hr>
<br>

## Post Payment (POST)
``` https://api.slamapp.co/accounting/payment ```

Body:
- contact: required
- amount_received: required
- date: required (must be in the format YYYY-MM-DD)
- project: optional

Command:
```
curl --location 'https://api.slamapp.co/accounting/payment' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "contact":1,
    "amount_received":9000
}'
```

<hr>
<br>

## Put Payment (PUT)
``` https://api.slamapp.co/accounting/payment ```

Body:
- payment: required
- amount_received: optional
- date: optional (must be in the format YYYY-MM-DD)
- project: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/accounting/payment' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "payment":1,
    "amount_received":10000
}'
```

<hr>
<br>

## Delete Payment (DELETE)
``` https://api.slamapp.co/accounting/payment ```

Body:
- payment: required

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/accounting/payment' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "payment":1
}'
```

<hr>
<br>

## Get Proposal (GET)
``` https://api.slamapp.co/accounting/proposal ```

Command:
```
curl --location 'https://api.slamapp.co/accounting/proposal' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'

```

<hr>
<br>

## Post Proposal (POST)
``` https://api.slamapp.co/accounting/proposal ```

Body:
- contact: required
- amount: required
- date: required (must be in the format YYYY-MM-DD)
- lead: optional

Command:
```
curl --location 'https://api.slamapp.co/accounting/proposal' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "contact":1,
    "amount":90000,
    "date":"2023-06-06"
}'
```

<hr>
<br>

## Put Proposal (PUT)
``` https://api.slamapp.co/accounting/proposal ```

Body:
- proposal: required
- amount: optional
- date: optional (must be in the format YYYY-MM-DD)
- lead: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/accounting/proposal' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "proposal":1,
    "amount":100000
}'
```

<hr>
<br>

## Delete Proposal (DELETE)
``` https://api.slamapp.co/accounting/proposal ```

Body:
- proposal: required

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/accounting/proposal' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "proposal":1
}'
```

<hr>
<br>

# Calendar API

## Get Event (GET)
``` https://api.slamapp.co/calendar/event ```

Command:
```
curl --location 'https://api.slamapp.co/calender/event' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'

```

<hr>
<br>

## Post Event (POST)
``` https://api.slamapp.co/calendar/event ```

Body:
- title: required
- contact: required
- description: optional
- date: required (must be in the format YYYY-MM-DD)
- status: required (must be one of the following: "incomplete", "complete")
- link: optional

Command:
```
curl --location 'https://api.slamapp.co/calender/event' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "title":"Event_1",
    "contact":1,
    "description":"This is a test event",
    "date":"2023-06-06",
    "status":"incomplete"
}'
```

<hr>
<br>

## Put Event (PUT)
``` https://api.slamapp.co/calendar/event ```

Body:
- event: required
- title: optional
- description: optional
- date: optional (must be in the format YYYY-MM-DD)
- status: optional (must be one of the following: "incomplete", "complete")
- link: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/calender/event' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "event":1,
    "status":"complete"
}'
```

<hr>
<br>

## Delete Event (DELETE)
``` https://api.slamapp.co/calendar/event ```

Body:
- event: required

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/calender/event' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "event":1
}'
```

<hr>
<br>

# Profile API

## Get Profile (GET)
``` https://api.slamapp.co/profile/profile ```

Command:
```
curl --location 'https://api.slamapp.co/profile/profile' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'

```

<hr>
<br>

## Put Profile (PUT)
``` https://api.slamapp.co/profile/profile ```

Body:
- legal_name: optional
- entity: optional
- country: optional
- state: optional
- currency: optional
- timezone: optional
- address: optional
- city: optional
- pincode: optional
- phone_no: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/profile/profile' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "user":4,
    "phone_no":"+919473746140",
    "pincode":221005,
    "legal_name":"Vansh Kumar Sharma",
    "timezone":"Asia/Dubai"
}'
```

<hr>
<br>

## Get Account (GET)
``` https://api.slamapp.co/profile/account ```

Command:
```
curl --location 'https://api.slamapp.co/profile/account' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk'

```

<hr>
<br>

## Put Account (PUT)
``` https://api.slamapp.co/profile/account ```

Body:
- first_name: optional
- last_name: optional
- username: optional
- password: optional

Command:
```
curl --location --request PUT 'https://api.slamapp.co/profile/account' \
--header 'Content-Type: application/json' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.eYPJ9nK6fnbho1y1Oi1XZxbOB4kZh4jqpa2FJsqR_nk' \
--data '{
    "password":"helloisvello"
}'
```

<hr>
<br>

## Delete Account (DELETE)
``` https://api.slamapp.co/profile/account ```

Command:
```
curl --location --request DELETE 'https://api.slamapp.co/profile/account' \
--header 'Cookie: JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Nn0.zBdutOvncGUTYYWZkc9pit5ps90LO1kz1WFtLloSNxI'

```

<hr>
<br>