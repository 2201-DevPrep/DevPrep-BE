# DevPrep-BE
The RESTful API for DevPrep



## Endpoints

- Register User
```shell
POST api/v1/users
Content-Type: application/json
Accept: application/json
body: {
  "email": "hello@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "codewars_username": undefined
}
```
---
```
{
    "data": {
        "id": "1",
        "type": "users",
        "attributes": {
            "email": "hello@example.com",
            "first_name": "Jane",
            "last_name": "Doe"
        }
    }
}
```

- Login User
```shell
POST api/v1/login
Content-Type: application/json
Accept: application/json
body: {
  "email": "hello@example.com"
  }
```
---
```
{
    "data": {
        "id": "1",
        "type": "user",
        "attributes": {
             "email": "hello@example.com",
             "first_name": "Jane",
             "last_name": "Doe",
             "codewars_username": "null"
            
        }
    }
}
```

- Update user with codewars username
```shell
PATCH /api/v1/users
Content-Type: application/json
Accept: application/json
body: {
  "email": "hello@example.com",
  "codewars_username": "SuperHacker3000"
}
```
---
```
{
    "data": {
        "id": "1",
        "type": "user",
        "attributes": {
            "email": "hello@example.com",
            "codewars_username": "SuperHacker3000"
            }
        }
    }
}
```

- Create new Flash Card
```shell
Create /api/v1/cards
Content-Type: application/json
Accept: application/json
body: {
  "email": "hello@example.com",
  "type": 0,
  "question": "A question",
  "answer": "The answer to the question"
}
```
---
```
Status 201
{
    "data": {
        "id": "1",
        "type": "card",
        "attributes": {
            "user_id": 1,
            "type": 0,
            "question": "A question",
            "answer": "The answer to the question"
            "rating": 0
            }
        }
    }
}
```
- Update Flash Card
```shell
Patch /api/v1/cards
Content-Type: application/json
Accept: application/json
body: { 
  "email": "hello@example.com",
  "card_id": 34
  "rating": 4
  "answer": "A new answer to the question"
}
```
---
```
Status 200
{
    "data": {
        "id": nil,
        "type": "card",
        "attributes": {
            "text": "Card 34 has been updated sucessfully"
            }
        }
    }
}
```
- Delete Flash Card
```shell
DELETE /api/v1/cards
Content-Type: application/json
Accept: application/json
body: {
  "email": "hello@example.com",
  "card_id": 34
  }

```
---
```
Status 200
{
    "data": {
        "id": nil,
        "type": "card",
        "attributes": {
            "text": "Card 34 has been deleted sucessfully"
            }
        }
    }
}
```
