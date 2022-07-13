# DevPrep-BE
The RESTful API for DevPrep



## Endpoints
<details>
  <summary><b/> Register User </b> </summary>
  
```shell
POST api/v1/users
Content-Type: application/json
Accept: application/json
body: {
  "username": "coolguy123",
  "email": "hello@example.com",
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
            "username": "coolguy123"
        }
    }
}
```
  
</details>


<details>
  <summary><b>Login User</b></summary>
  
```shell
POST api/v1/login
Content-Type: application/json
Accept: application/json
body: {
  "email": "hello@example.com",
  "username": "coolguy123"
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
             "username": "coolguy123",
             "codewars_username": "null"
            
        }
    }
}
```

</details>

<details>
  <summary><b>Update user with codewars username</b></summary>
  
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
  
</details>
<details>
  <summary><b> Create new Flash Card</b></summary>
 
```shell
POST /api/v1/cards
Content-Type: application/json
Accept: application/json
body: {
  "user_id": "1",
  "category": "technical-BE",     <-- (or "technical-FE", "behavioral")
  "front_side": "What is MVC?",
  "back_side": "stuff and things",     <-- (optional)
}
```
---
```
Status 201
{
  "data": {
    "id": "1",
    "type": "flash_card",
    "attributes": {
      "category": "technical-BE",
      "competence_rating": 0,
      "front_side": "what is MVC?",
      "back_side": "stuff and things",
      "user_id": "1"
    }
  }
}
```


If the `user_id` is not present, or not in the DB, i see this error with the status code 400:
```
{
  "error": "invalid user_id"
}
```

  </details>
  
<details>
  <summary><b> Find A Flash Card</b></summary>
  
```shell
GET /api/v1/users/:user_id/cards/:card_id
```
---
```
Status 200
{
  "data": {
    "id": "1",
    "type": "flash_card",
    "attributes": {
      "category": "technical-BE",
      "competence_rating": 4.5,
      "front_side": "what is MVC?",
      "back_side": "A design pattern commonly used to build web applications.",
      "user_id": "1"
    }
  }
}
```

If the `user_id` or `:flash_card_id` is not in the DB, i see this error with the status code 404:
```
{
  "error": "invalid user_id or flash_card_id"
}
```
  
</details>
<details>
  <summary><b>Update Flash Card</b></summary>

```shell
PATCH api/v1/users/:user_id/cards/:card_id
Content-Type: application/json
Accept: application/json
body: {
  "category": "technical",
  "competence_rating": 4.5,
  "front_side": "What is MVC?",
  "back_side": "stuff and things"
}
```
*note that you do need at least 1 attribute present to send this request*

Then I should see the following response with a status code of 200:
```
{
  "data": {
    "id": "1",
    "type": "flash_card",
    "attributes": {
      "category": "technical-FE",
      "competence_rating": 4.5,
      "front_side": "what is MVC?",
      "back_side": "stuff and things",
      "user_id": "1"
    }
  }
}
```

If the `user_id` is not in the database, I should see this error with a status code of 400:
```
{
  "error": "invalid user_id"
}
```
  
</details>

<details>
  <summary><b>Delete Flash Card</b></summary>

```shell
DELETE /api/v1/users/user_id/cards/card_id
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
  
</details>

<details>
  <summary><b>Return all Flash Cards for a User</b></summary>

```shell
GET /api/v1/users/:user_id/cards 
(potential extension: add query params to determine which deck)

```
---
```
Status 200
{
  "data": {
    "technical_cards": [
      {
        "id": "1",
        "type": "flash_card",
        "attributes": {
          "category": "technical",
          "competence_rating": 4.5,
          "front_side": "what is MVC?",
          "back_side": "A design pattern commonly used to build web applications.",
          "user_id": "1"
        }
      },
      {
        "id": "2",
        "type": "flash_card",
        "attributes": {
          "category": "technical",
          "competence_rating": 0,
          "front_side": "Explain your understanding of relational databases.",
          "back_side": "",
          "user_id": "1"
        }
      },
      {...}
    ],
    "behavioral_cards": [
      {
        "id": "3",
        "type": "flash_card",
        "attributes": {
          "category": "behavioral",
          "competence_rating": 0,
          "front_side": "What are you looking for in a role?",
          "back_side": "",
          "user_id": "1"
        }
      },
      {
        "id": "4",
        "type": "flash_card",
        "attributes": {
          "category": "technical",
          "competence_rating": 0,
          "front_side": "What are you proud of?",
          "back_side": "",
          "user_id": "1"
        }
      },
      {...}
    ]
  }
}
```

If the user_id is not in the DB, i see this error with a status of 404:
```
  "error": "no user found with the given id."
```
  
  </details>
