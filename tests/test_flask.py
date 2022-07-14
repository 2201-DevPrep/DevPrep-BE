from server import app
import json
from models import UserModel, CardModel

def test_register_user():
    response = app.test_client().post('api/v1/users', data={'username': 'bonnyjowman08', 'email': 'bonfjowman.hello@notreal.com', 'codewarsUsername': undefined}))
    json_data = json.loads(response.data)

    assert response.status_code == 201

    assert json_data['type'] == 'users'
    assert json_data['attributes']['email'] == 'bonfjowman.hello@notreal.com'
    assert json_data['attributes']['username'] == 'bonnyjowman08'

def test_login_user():
    response = app.test_client().post('api/v1/login', data={'username': 'bonnyjowman08', 'email': 'bonfjowman.hello@notreal.com'}))
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

def test_update_user():
    response = app.test_client().post('api/v1/users/1', data={'username': 'bonnyjowman08', 'codewarsUsername': 'SuperHacker3000'}))
    json_data = json.loads(response.data)

    assert response.status_code == 200

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
