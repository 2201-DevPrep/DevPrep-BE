def show(user):
    json = { 
            "data": {
                "id": str(user.id),
                "type": "users",
                "attributes": {
                    "username": user.username
                    }
                }
            }
    return json

def dashboard(user):
    import requests
    json = {
            "data": {
                "userId": str(user.id),
                "type": "userDashboard",
                "attributes": {
                    "username": user.username,
                    "preparednessRating": {
                        "technicalBE": user.average_card_rating_by_category('technicalBE'),
                        "technicalFE": user.average_card_rating_by_category('technicalFE'),
                        "behavioral": user.average_card_rating_by_category('behavioral')
                        },
                    "cwAttributes": {
                        "cwUsername": "null",
                        "cwLeaderboardPosition": "null",
                        "totalCompleted": "null",
                        "languageRanks": {}
                        }
                    }
                }
            }

    if user.codewars_username is None or user.codewars_username == '':
        return json
    else:
        cw_response = requests.get(f'https://www.codewars.com/api/v1/users/{user.codewars_username}').json()
        if 'id' not in cw_response.keys():
            return { "error": "invalid codewars username" }, 400
        json['data']['attributes']['cwAttributes']['cwUsername'] = user.codewars_username
        user_cw_attributes = json['data']['attributes']['cwAttributes']
        user_cw_attributes['cwLeaderboardPosition'] = cw_response['leaderboardPosition']
        user_cw_attributes['totalCompleted'] = cw_response['codeChallenges']['totalCompleted']

        for key, value in cw_response['ranks']['languages'].items():
            user_cw_attributes['languageRanks'][key] = value['rank']

        return json
