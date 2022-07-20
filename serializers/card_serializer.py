def show(card):
    json = {
        "id": str(card.id),
        "type": "flashCard",
        "attributes": {
            "category": card.category,
            "competenceRating": card.rating,
            "frontSide": card.front,
            "backSide": card.back,
            "userId": str(card.user_id)
        }
    }
    return json

def cards_index(user):
    json = {
        "data": {
            "BEtechnicalCards": [],
            "FEtechnicalCards": [],
            "behavioralCards": []
        }
    }

    for card in user.cards_by_category('technicalBE'):
        json['data']['BEtechnicalCards'].append(show(card))

    for card in user.cards_by_category('technicalFE'):
        json['data']['FEtechnicalCards'].append(show(card))

    for card in user.cards_by_category('behavioral'):
        json['data']['behavioralCards'].append(show(card))

    return json, 200
