from app import db
from sqlalchemy.dialects.postgresql import JSON

pokemon_moves = db.Table('pokemon_moves',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
    db.Column('move_id', db.Integer, db.ForeignKey('moves.id'))
    )

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    stats = db.Column(JSON)
    moves = db.relationship('Move', secondary=pokemon_moves, backref=db.backref('Pokemon',lazy='dynamic'))

    def __init__(self, name, stats):
        self.name = name
        self.stats = stats

    def __repr__(self):
        return "<name {} id {}>".format(self.name,self.id)

    def serialize(self):
        return {
            'name': self.name,
            'stats': self.stats,
            'id': self.id
        }

    def get_moves(self):
        arr = []
        for move in self.moves:
            arr.append(move.name)
        arr.sort()
        return arr

class Nature(db.Model):
    __tablename__ = 'natures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    bonus = db.Column(db.String())
    penalty = db.Column(db.String())

    def __init__(self, name, bonus=None, penalty=None):
        self.name = name
        self.bonus = bonus
        self.penalty = penalty

    def __repr__(self):
        return "<name {} id {}>".format(self.name,self.id)

    def serialize(self):
        return {
            'name': self.name,
            'bonus': self.bonus,
            'penalty': self.penalty,
        }

    def reference(self):
        abbrev = {
            'attack':'Atk',
            'defense':'Def',
            'sp_attack':'SpAtk',
            'sp_defense':'SpDef',
            'speed':'Spd',
        }
        if(self.bonus and self.penalty):
            return "(+{}/-{})".format(abbrev[self.bonus],abbrev[self.penalty])
        else:
            return ''

class Move(db.Model):
    __tablename__ = 'moves'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    category = db.Column(db.String())
    power = db.Column(db.Integer)
    pp = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    effect = db.Column(db.String())

    def __init__(self, name, type=None, category=None, power=None, pp=0, accuracy=100, effect=''):
        self.name = name
        self.type = type
        self.category = category
        self.power = power
        self.pp = pp
        self.accuracy = accuracy
        self.effect = effect

    def __repr__(self):
        return "<name {} id {}>".format(self.name,self.id)

    def serialize(self):
        return {
            'name':self.name,
            'type':self.type,
            'category':self.category,
            'power':self.power,
            'pp':self.pp,
            'accuracy':self.accuracy,
            'effect':self.effect,
        }