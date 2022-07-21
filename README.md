# DevPrep-BE
The RESTful API for DevPrep 

## Local Setup
Assuming you have a mac/unix machine with `sqlite 3.37.0`, `python 3.10.5` and `pip 22.0.4` installed:
- run `pip3 install virtualenv` then `python3 -m venv env` to create a local environment for the project
- run `source env/bin/activate` to connect to your local environment
- `pip3 install -r requirements.txt` to install the required packages
- `export DB_URL='sqlite:///test.db` sets the required environment variable 
- `flask run` to start up the server. By default it will run on `http://localhost:5000`
- You're all set to start making some requests! 

<details>
  <summary><b/> Database Schema </b></summary>
  <img width="349" alt="Screen Shot 2022-07-18 at 8 21 44 PM" src="https://user-images.githubusercontent.com/94757433/179650492-0d746cfb-9f9f-4ec9-9ca3-0d501bc0da57.png">
</details>

## Endpoints
<details>
  <summary><b/> Register User </b> </summary>
  
```shell
POST https://devprep-be.herokuapp.com/api/v1/users
Content-Type: application/json
Accept: application/json
body: {
  "username": "coolguy123",
  "email": "hello@example.com",
  "codewarsUsername": undefined
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
  <summary><b>User Dashboard</b></summary>
  
```shell
GET https://devprep-be.herokuapp.com/api/v1/dashboard?userId=1
(userId query param is required)
```
```
{
  "data": {
    "userId": "1",
    "type": "userDashboard",
    "attributes": {
      "username": "coolguy123",
      "preparednessRating": {
        "technicalBE": 4.34,
        "technicalFE": 3.54,
        "behavioral": 5.0
      },
      "cwAttributes": {
        "cwLeaderboardPosition": 236,
        "totalCompleted": 230,
        "languageRanks": {
          "java": 1234,
          "ruby": 1324,
          [...]
        }
      }
    }
  }
}
```

</details>

<details>
  <summary><b>Login User</b></summary>
  
```shell
POST https://devprep-be.herokuapp.com/api/v1/login
Content-Type: application/json
Accept: application/json
body: {
  "email": "hello@example.com",
  "username": "coolguy123"
  }
```
--- (should be a Dashboard response)
```
{
  "data": {
    "userId": "1",
    "type": "userDashboard",
    "attributes": {
      "username": "coolguy123",
      "preparednessRating": {
        "technicalBE": 4.34,
        "technicalFE": 3.54,
        "behavioral": 5.0
      },
      "cwAttributes": {
        "cwLeaderboardPosition": 236,
        "totalCompleted": 230,
        "languageRanks": {
          "java": 1234,
          "ruby": 1324,
          [...]
        }
      }
    }
  }
}
```

</details>

<details>
  <summary><b>Update user</b></summary>
  
```shell
PATCH https://devprep-be.herokuapp.com/api/v1/users/:user_id
Content-Type: application/json
Accept: application/json
body: {
  "codewarsUsername": "SuperHacker3000",
  "username": "goofyguy1342"
  [any/all attributes can be updated]
}
```
--- (should be a dashboard response)
```
{
  "data": {
    "userId": "1",
    "type": "userDashboard",
    "attributes": {
      "username": "coolguy123",
      "preparednessRating": {
        "technicalBE": 4.34,
        "technicalFE": 3.54,
        "behavioral": 5.0
      },
      "cwAttributes": {
        "cwLeaderboardPosition": 236,
        "totalCompleted": 230,
        "languageRanks": {
          "java": 1234,
          "ruby": 1324,
          [...]
        }
      }
    }
  }
}
```
  
</details>
<details>
  <summary><b> Create new Flash Card</b></summary>
 
```shell
POST https://devprep-be.herokuapp.com/api/v1/users/:user_id/cards
Content-Type: application/json
Accept: application/json
body: {
  "category": "technicalBE",     <-- (or "technicalFE", "behavioral")
  "frontSide": "What is MVC?",
  "backSide": "stuff and things",     <-- (optional)
}
```
---
```
Status 201
{
  "data": {
    "id": "1",
    "type": "flashCard",
    "attributes": {
      "category": "technicalBE",
      "competenceRating": 0,
      "frontSide": "what is MVC?",
      "backSide": "stuff and things",
      "userId": "1"
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
GET https://devprep-be.herokuapp.com/api/v1/users/:user_id/cards/:card_id
```
---
```
Status 200
{
  "data": {
    "id": "1",
    "type": "flashCard",
    "attributes": {
      "category": "technicalBE",
      "competenceRating": 4.5,
      "frontSide": "what is MVC?",
      "backSide": "A design pattern commonly used to build web applications.",
      "userId": "1"
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
PATCH https://devprep-be.herokuapp.com/api/v1/users/:user_id/cards/:card_id
Content-Type: application/json
Accept: application/json
body: {
  "category": "technical",
  "competenceRating": 4.5,
  "frontSide": "What is MVC?",
  "backSide": "stuff and things"
  [any/all attributes can be updated]
}
```
*note that you do need at least 1 attribute present to send this request*

Then I should see the following response with a status code of 200:
```
{
  "data": {
    "id": "1",
    "type": "flashCard",
    "attributes": {
      "category": "technicalFE",
      "competenceRating": 4.5,
      "frontSide": "what is MVC?",
      "backSide": "stuff and things",
      "userId": "1"
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
DELETE https://devprep-be.herokuapp.com/api/v1/users/:user_id/cards/:card_id
```
--- Response:
```
Status 204
```
  
</details>

<details>
  <summary><b>Return all Flash Cards for a User</b></summary>

```shell
GET https://devprep-be.herokuapp.com/api/v1/users/:user_id/cards 
(potential extension: add query params to determine which deck)

```
---
```
Status 200
{
  "data": {
    "BEtechnicalCards": [
      {
        "id": "1",
        "type": "flashCard",
        "attributes": {
          "category": "technicalBE",
          "competenceRating": 4.5,
          "frontSide": "what is MVC?",
          "backSide": "A design pattern commonly used to build web applications.",
          "userId": "1"
        }
      },
      {
        "id": "2",
        "type": "flashCard",
        "attributes": {
          "category": "technicalBE",
          "competenceRating": 0,
          "frontSide": "Explain your understanding of relational databases.",
          "backSide": "",
          "userId": "1"
        }
      },
      {...}
    ],
    "FEtechnicalCards": [
      {
        "id": "1",
        "type": "flashCard",
        "attributes": {
          "category": "technicalFE",
          "competenceRating": 4.5,
          "frontSide": "what is MVC?",
          "backSide": "A design pattern commonly used to build web applications.",
          "userId": "1"
        }
      },
      {
        "id": "2",
        "type": "flashCard",
        "attributes": {
          "category": "technicalFE",
          "competenceRating": 0,
          "frontSide": "Explain your understanding of relational databases.",
          "backSide": "",
          "userId": "1"
        }
      },
      {...}
    ],
    "behavioralCards": [
      {
        "id": "3",
        "type": "flashCard",
        "attributes": {
          "category": "behavioral",
          "competenceRating": 0,
          "frontSide": "What are you looking for in a role?",
          "backSide": "",
          "userId": "1"
        }
      },
      {
        "id": "4",
        "type": "flashCard",
        "attributes": {
          "category": "behavioral",
          "competenceRating": 0,
          "frontSide": "What are you proud of?",
          "backSide": "",
          "userId": "1"
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
 
<details>
  <summary><b>Quote of the Day</b></summary>
  
```shell
GET https://devprep-be.herokuapp.com/api/v1/quote
```
---
```shell
{
  "author": "quote"
}
```
  </details>
