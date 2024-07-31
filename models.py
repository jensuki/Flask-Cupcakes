"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_img = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, default=default_img)

    def serialize(self):
        """Returns a 'dict' representation of a single cupcake -> into JSON"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image or ''
        }

    def __repr__(self):
        return f"<Cupcake id={self.id} flavor={self.flavor} size={self.size} rating={self.rating}>"


def connect_db(app):
    """Connect DB + Flask app"""
    db.app = app
    db.init_app(app)