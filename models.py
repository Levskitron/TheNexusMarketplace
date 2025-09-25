from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    privilege = db.Column(db.Integer, nullable=False)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(150), db.ForeignKey('user.username'))
    is_sold = db.Column(db.Boolean, default=False)
    buyer_username = db.Column(db.String(150), db.ForeignKey('user.username'), nullable=True)