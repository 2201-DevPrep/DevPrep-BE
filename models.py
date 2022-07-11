from app import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    codewars_username = db.Column(db.String())

    def __init__(self, email, first_name, last_name, codewars_username):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.codewars_username = codewars_username

    def __repr__(self):
        return '<id {}>'.format(self.id)

class CardModel(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.Text())
    answer = db.Column(db.Text())
    star_rating = db.Column(db.Integer())

    def __init__(self, user_id, question, answer, star_rating):
        self.question = question
        self.answer = answer
        self.user_id = user_id
        self.star_rating = star_rating

    def __repr__(self):
        return '<id {}>'.format(self.id)