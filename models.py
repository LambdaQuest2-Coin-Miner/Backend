from app import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Room(db.Model):

    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    coordinates = db.Column(db.String)
    exits = db.Column(db.String)
    cooldown = db.Column(db.Numeric(asdecimal=True))
    errors = db.Column(db.String)
    messages = db.Column(db.String)
    users = relationship("Player", backref="player")

    def __init__(self, title, description, coordinates, exits, cooldown, errors, messages):
        self.title = title
        self.description = description
        self.coordinates = coordinates
        self.exits = exits
        self.cooldown = cooldown
        self.errors = errors
        self.messages = messages

    def __repr__(self):
        return f"{self.title}"


class Player(db.Model):

    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    encumbrance = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    bodywear = db.Column(db.String)
    footwear = db.Column(db.String)
    inventory = db.Column(db.String)
    status = db.Column(db.String)
    current_room_id = db.Column(db.Integer, ForeignKey('rooms.id'))
    last_room_visited_id = db.Column(db.Integer, ForeignKey('rooms.id'))

    def __init__(self, name, encumberance, strength, speed, gold, bodywear, footwear, inventory, status, current_room_id, last_room, visited_id):
        self.name = name
        self.encumberance = encumberance
        self.strength = strength
        self.speed = speed
        self.gold = gold
        self.bodywear = bodywear
        self.footwear = footwear
        self.inventory = inventory
        self.status = status
        self.current_room_id = current_room_id
        self.last_room = last_room
        self.visited_id = visited_id


    def __repr__(self):
        return f"{self.name}"