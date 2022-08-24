from app import db, csv, relationship
from models.card import Card

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    username = db.Column(db.String())
    codewars_username = db.Column(db.String())
    cards = relationship("Card", lazy='select')

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def cards_by_category(self, cat):
        return Card.query.filter_by(user_id=self.id, category=cat).all()

    def average_card_rating_by_category(self, cat):
        from sqlalchemy.sql import func
        sql_result = db.session.query(func.avg(Card.rating)).filter(Card.user_id==self.id, Card.category==cat)
        if sql_result[0][0]:
            rounded = round(sql_result[0][0], 2)
            return float(rounded)
        else:
            return "null"

    def generate_default_cards(self):
        with open('data/interview_questions.csv', newline='') as f:
            fdicts = csv.DictReader(f.read().splitlines(), skipinitialspace=True)

            csv_dicts = [{k: v for k, v in row.items()} for row in fdicts]
            for dict in csv_dicts:
                card = Card(
                    category=dict['category'],
                    front=dict['question'],
                    user_id=self.id
                )
                db.session.add(card)
                db.session.commit()
