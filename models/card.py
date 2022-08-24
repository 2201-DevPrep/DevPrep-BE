from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    rating = db.Column(db.Float(), default=0.0)
    front = db.Column(db.Text())
    back = db.Column(db.Text(), default='')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return '<id {}>'.format(self.id)
