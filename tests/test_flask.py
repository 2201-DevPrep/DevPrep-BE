from app import app, db, User
import json
# from models import UserModel, CardModel
db.create_all()

def test_register_user():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
        db.session.commit()

    body = {'username': 'bonnyjowman08', 'email': 'bonfjowman.hello@notreal.com'}

    response = app.test_client().post(
            'api/v1/users', 
            data=json.dumps(body),
            headers={"Content-Type": "application/json"}
        )
    json_data = json.loads(response.data)['data']

    assert response.status_code == 201

    assert json_data['type'] == 'users'
    assert json_data['attributes']['username'] == 'bonnyjowman08'

def xtest_login_user():
    response = app.test_client().post('api/v1/login', data={'username': 'bonnyjowman08', 'email': 'bonfjowman.hello@notreal.com'})
    json_data = json.loads(response.data)

    assert response.status_code == 201

    assert json_data['type'] == 'user_dashboard'
    assert type(json_data['userId']) is str
    assert json_data['attributes']['email'] == 'bonfjowman.hello@notreal.com'
    assert json_data['attributes']['username'] == 'bonnyjowman08'
    assert type(json_data['attributes']['preparednessRating']) is dict
    assert type(json_data['attributes']['preparednessRating']['technicalBE']) is float
    assert type(json_data['attributes']['preparednessRating']['technicalFE']) is float
    assert type(json_data['attributes']['preparednessRating']['behavioral']) is float
    assert type(json_data['attributes']['cwAttributes']) is dict
    assert type(json_data['attributes']['cwAttributes']['cwLeaderboardPosition']) is int
    assert type(json_data['attributes']['cwAttributes']['totalCompleted']) is int
    assert type(json_data['attributes']['cwAttributes']['languageRanks']) is dict
    assert type(json_data['attributes']['cwAttributes']['languageRanks']['java']) is int
    assert type(json_data['attributes']['cwAttributes']['languageRanks']['ruby']) is int

def xtest_update_user():
    response = app.test_client().post('api/v1/users/1', data={'username': 'bonnyjowman08', 'codewarsUsername': 'SuperHacker3000'})
    json_data = json.loads(response.data)

    assert response.status_code == 200

    assert json_data['type'] == 'userDashboard'
    assert type(json_data['userId']) is str
    assert json_data['attributes']['email'] == 'bonfjowman.hello@notreal.com'
    assert json_data['attributes']['username'] == 'bonnyjowman08'
    assert type(json_data['attributes']['preparednessRating']) is dict
    assert type(json_data['attributes']['preparednessRating']['technicalBE']) is float
    assert type(json_data['attributes']['preparednessRating']['technicalFE']) is float
    assert type(json_data['attributes']['preparednessRating']['behavioral']) is float
    assert type(json_data['attributes']['cwAttributes']) is dict
    assert type(json_data['attributes']['cwAttributes']['cwLeaderboardPosition']) is int
    assert type(json_data['attributes']['cwAttributes']['totalCompleted']) is int
    assert type(json_data['attributes']['cwAttributes']['languageRanks']) is dict
    assert type(json_data['attributes']['cwAttributes']['languageRanks']['java']) is int
    assert type(json_data['attributes']['cwAttributes']['languageRanks']['ruby']) is int

def xtest_card_create():
    response = app.test_client().post('api/v1/users/1/cards', data={'category': 'technicalBE', 'frontSide': 'What is MVC?', 'backSide': 'stuff and things'})
    json_data = json.loads(response.data)

    assert response.status_code == 201

    assert json_data['type'] == 'flashCard'
    assert json_data['attributes']['category'] == 'technicalBE'
    assert type(json_data['attributes']['competenceRating']) == float
    assert json_data['attributes']['frontSide'] == 'What is MVC?'
    assert json_data['attributes']['backSide'] == 'stuff and things'

def xtest_card_create_invalid_user_id():
    response = app.test_client().post('api/v1/users/1000/cards', data={'category': 'technicalBE', 'frontSide': 'What is MVC?', 'backSide': 'stuff and things'})
    json_data = json.loads(response.data)

    assert response.status_code == 400

    assert json_data['error'] == 'invalid user_id'

def xtest_card_get():
    # Needs refactoring to make sure user and card with id's '1' are created before this is run
    response = app.test_client().get('api/v1/users/1/cards/1')
    json_data = json.loads(response.data)

    assert response.status_code == 200

    assert json_data['type'] == 'flashCard'
    assert json_data['attributes']['category'] == 'technicalBE'
    assert type(json_data['attributes']['competenceRating']) == float
    assert json_data['attributes']['frontSide'] == 'What is MVC?'
    assert json_data['attributes']['backSide'] == 'stuff and things'

def xtest_card_update():
    response = app.test_client().patch('api/v1/users/1/cards/1', data={'backSide': 'updated stuff and things'})
    json_data = json.loads(response.data)

    assert response.status_code == 200

    assert json_data['type'] == 'flashCard'
    assert json_data['attributes']['category'] == 'technicalBE'
    assert type(json_data['attributes']['competenceRating']) == float
    assert json_data['attributes']['frontSide'] == 'What is MVC?'
    assert json_data['attributes']['backSide'] == 'updated stuff and things'

def xtest_card_update_invalid_user_id():
    response = app.test_client().patch('api/v1/users/1000/cards/1', data={'backSide': 'updated stuff and things'})
    json_data = json.loads(response.data)

    assert response.status_code == 400

    assert json_data['error'] == 'invalid user_id'

def xtest_card_delete():
    response = app.test_client().delete('api/v1/users/1000/cards/1')

    assert response.status_code == 204


def xtest_cards_get_list():
    # Needs refactoring to make sure user and card with id's '1' are created before this is run
    response = app.test_client().get('api/v1/users/1/cards')
    json_data = json.loads(response.data)

    assert response.status_code == 200

    assert type(json_data['technicalCards']) == list
    assert json_data['technicalCards'][0]['type'] == 'flashCard'
    assert json_data['technicalCards'][0]['attributes']['category'] == 'technicalBE'
    assert type(json_data['technicalCards'][0]['attributes']['competenceRating']) == float
    assert type(json_data['technicalCards'][0]['attributes']['frontSide']) == str
    assert type(json_data['technicalCards'][0]['attributes']['backSide']) == str

    assert type(json_data['behavioralCards']) == list
    assert json_data['behavioralCards'][0]['type'] == 'flashCard'
    assert json_data['behavioralCards'][0]['attributes']['category'] == 'technicalBE'
    assert type(json_data['behavioralCards'][0]['attributes']['competenceRating']) == float
    assert type(json_data['behavioralCards'][0]['attributes']['frontSide']) == str
    assert type(json_data['behavioralCards'][0]['attributes']['backSide']) == str

def xtest_card_update_invalid_user_id():
    response = app.test_client().get('api/v1/users/1/cards')
    json_data = json.loads(response.data)

    assert response.status_code == 400

    assert json_data['error'] == 'no user found with the given id.'
