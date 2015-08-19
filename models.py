from app import db
from sqlalchemy.dialects.postgresql import JSON

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    stats = db.Column(JSON)
    
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
        
    def __repr__(self):
        return "<id {}>".format(self.id)